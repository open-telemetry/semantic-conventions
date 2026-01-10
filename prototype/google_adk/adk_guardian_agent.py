#!/usr/bin/env python3
"""
Google Agent Development Kit (ADK) Security Guardian Prototype

This prototype demonstrates how to integrate OpenTelemetry GenAI security
guardian semantic conventions with Google ADK agents.

The prototype shows:
1. before_model_callback / after_model_callback guards
2. before_tool_callback / after_tool_callback guards
3. Plugin-based global security policies
4. Gemini Safety Features integration

Requirements:
    pip install google-adk opentelemetry-api opentelemetry-sdk

Usage:
    # Offline (default):
    python adk_guardian_agent.py

    # Real chat (optional, uses OpenAI for the demo model call):
    export OPENAI_API_KEY=your_key
    export DEMO_LLM_MODE=auto   # default; or "openai" to force
    python adk_guardian_agent.py

Author: OpenTelemetry GenAI SIG
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
import re

from demo_chat import get_chat_model
from demo_tools import DemoToolExecutor, ToolExecutionError

from otel_guardian_utils import (
    GuardianTracer,
    GuardianConfig,
    GuardianResult,
    SecurityFinding,
    DecisionType,
    TargetType,
    RiskCategory,
    RiskSeverity,
)


# ============================================================================
# ADK Callback Types (Mock)
# ============================================================================

@dataclass
class ToolContext:
    """Mock ADK ToolContext for demonstration."""
    tool_name: str
    agent_id: str
    session_id: str


@dataclass
class ModelRequest:
    """Mock ADK Model Request."""
    messages: List[Dict[str, str]]
    model: str = "gemini-1.5-pro"
    system_instruction: Optional[str] = None


@dataclass
class ModelResponse:
    """Mock ADK Model Response."""
    content: str
    finish_reason: str = "stop"
    safety_ratings: Optional[Dict[str, float]] = None


# ============================================================================
# ADK Security Callbacks
# ============================================================================

class BeforeModelCallback:
    """
    ADK before_model_callback implementation with security guardian.

    Maps to: gen_ai.security.target.type = llm_input
    """

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="adk-before-model-guard-v1",
            name="ADK Pre-Model Guard",
            version="1.0.0",
            provider_name="google.adk"
        )

        # Gemini-specific harm categories
        self.harm_patterns = {
            "dangerous_content": [
                r"how\s+to\s+(make|create|build)\s+(a\s+)?(bomb|explosive|weapon)",
                r"instructions\s+for\s+(harming|hurting|killing)",
            ],
            "harassment": [
                r"(attack|insult|demean)\s+(this\s+)?(person|individual|user)",
            ],
            "hate_speech": [
                r"(all|every)\s+\[demographic\]\s+(are|should)",
            ],
        }

    def __call__(
        self,
        request: ModelRequest,
        agent_context: Optional[Dict] = None
    ) -> Optional[ModelRequest]:
        """
        Evaluate model request before sending to Gemini.

        Returns:
            Modified request, or None to block
        """
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.LLM_INPUT,
            agent_id=agent_context.get("agent_id") if agent_context else None
        ) as ctx:
            findings = []
            full_content = " ".join(m.get("content", "") for m in request.messages)

            # Check for harmful content
            for category, patterns in self.harm_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, full_content, re.IGNORECASE):
                        findings.append(SecurityFinding(
                            risk_category=f"google:{category}",
                            risk_severity=RiskSeverity.HIGH,
                            risk_score=0.95,
                            policy_id=f"gemini_safety_{category}",
                            policy_name=f"Gemini Safety - {category.replace('_', ' ').title()}",
                            metadata=[f"category:{category}"]
                        ))

            if findings:
                result = GuardianResult(
                    decision_type=DecisionType.DENY,
                    decision_reason=f"Content blocked by Gemini safety filters",
                    decision_code=400,
                    findings=findings
                )
                ctx.record_result(result)
                return None  # Block the request

            result = GuardianResult(decision_type=DecisionType.ALLOW)
            ctx.record_result(result)
            return request


class AfterModelCallback:
    """
    ADK after_model_callback implementation with security guardian.

    Maps to: gen_ai.security.target.type = llm_output
    """

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="adk-after-model-guard-v1",
            name="ADK Post-Model Guard",
            version="1.0.0",
            provider_name="google.adk"
        )

    def __call__(
        self,
        response: ModelResponse,
        agent_context: Optional[Dict] = None
    ) -> ModelResponse:
        """
        Evaluate and potentially modify model response.
        """
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.LLM_OUTPUT,
            agent_id=agent_context.get("agent_id") if agent_context else None
        ) as ctx:
            findings = []
            modified_content = response.content

            # Check Gemini safety ratings if available
            if response.safety_ratings:
                for category, score in response.safety_ratings.items():
                    if score > 0.7:  # High risk threshold
                        findings.append(SecurityFinding(
                            risk_category=f"google:{category}",
                            risk_severity=RiskSeverity.HIGH if score > 0.9 else RiskSeverity.MEDIUM,
                            risk_score=score,
                            policy_id="gemini_safety_output",
                            policy_name="Gemini Output Safety",
                            metadata=[f"category:{category}", f"score:{score:.2f}"]
                        ))

            # Check for misinformation patterns
            misinformation_patterns = [
                r"(definitely|certainly|absolutely)\s+(true|false)\s+that",
                r"scientific\s+consensus\s+(confirms|proves)\s+that\s+\[controversial\]",
            ]

            for pattern in misinformation_patterns:
                if re.search(pattern, response.content, re.IGNORECASE):
                    findings.append(SecurityFinding(
                        risk_category=RiskCategory.MISINFORMATION,
                        risk_severity=RiskSeverity.MEDIUM,
                        risk_score=0.65,
                        policy_id="policy_misinformation",
                        policy_name="Misinformation Detection"
                    ))

            if findings:
                result = GuardianResult(
                    decision_type=DecisionType.WARN,
                    decision_reason="Potential safety concerns in output",
                    findings=findings
                )
            else:
                result = GuardianResult(decision_type=DecisionType.ALLOW)

            ctx.record_result(result)
            return ModelResponse(content=modified_content, finish_reason=response.finish_reason)


class BeforeToolCallback:
    """
    ADK before_tool_callback implementation with security guardian.

    Maps to: gen_ai.security.target.type = tool_call
    """

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="adk-before-tool-guard-v1",
            name="ADK Pre-Tool Guard",
            version="1.0.0",
            provider_name="google.adk"
        )

        # Tool-specific policies
        self.tool_policies = {
            "database_query": {
                "allowed_tables": ["products", "categories", "public_info"],
                "blocked_tables": ["users", "credentials", "admin"],
            },
            "file_read": {
                "allowed_extensions": [".txt", ".json", ".csv"],
                "blocked_paths": ["/etc/", "/var/secrets/", "~/.ssh/"],
            },
        }

    def __call__(
        self,
        tool_context: ToolContext,
        args: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Validate and potentially modify tool arguments.

        Returns:
            Modified args, or None to block execution
        """
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.TOOL_CALL,
            target_id=f"call_{tool_context.tool_name}",
            agent_id=tool_context.agent_id
        ) as ctx:
            findings = []
            tool_name = tool_context.tool_name

            # Apply tool-specific policies
            if tool_name == "database_query" and tool_name in self.tool_policies:
                policy = self.tool_policies[tool_name]
                query = args.get("query", "").lower()

                for blocked in policy["blocked_tables"]:
                    if blocked in query:
                        findings.append(SecurityFinding(
                            risk_category=RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                            risk_severity=RiskSeverity.HIGH,
                            risk_score=0.92,
                            policy_id="policy_db_access",
                            policy_name="Database Access Control",
                            metadata=[f"blocked_table:{blocked}", f"tool:{tool_name}"]
                        ))

                        result = GuardianResult(
                            decision_type=DecisionType.DENY,
                            decision_reason=f"Access to table '{blocked}' is not permitted",
                            decision_code=403,
                            findings=findings
                        )
                        ctx.record_result(result)
                        return None

            elif tool_name == "file_read" and tool_name in self.tool_policies:
                policy = self.tool_policies[tool_name]
                path = args.get("path", "")

                for blocked in policy["blocked_paths"]:
                    if path.startswith(blocked):
                        findings.append(SecurityFinding(
                            risk_category=RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                            risk_severity=RiskSeverity.CRITICAL,
                            risk_score=0.98,
                            policy_id="policy_file_access",
                            policy_name="File System Access Control",
                            metadata=[f"blocked_path:{blocked}", f"tool:{tool_name}"]
                        ))

                        result = GuardianResult(
                            decision_type=DecisionType.DENY,
                            decision_reason=f"Access to path '{blocked}' is not permitted",
                            decision_code=403,
                            findings=findings
                        )
                        ctx.record_result(result)
                        return None

            result = GuardianResult(decision_type=DecisionType.ALLOW)
            ctx.record_result(result)
            return args


class AfterToolCallback:
    """
    ADK after_tool_callback implementation with security guardian.

    Evaluates tool results before they're returned to the model.
    """

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="adk-after-tool-guard-v1",
            name="ADK Post-Tool Guard",
            version="1.0.0",
            provider_name="google.adk"
        )

    def __call__(
        self,
        tool_context: ToolContext,
        result: Any
    ) -> Any:
        """
        Validate and potentially sanitize tool results.
        """
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.TOOL_CALL,
            target_id=f"result_{tool_context.tool_name}",
            agent_id=tool_context.agent_id
        ) as ctx:
            findings = []
            result_str = str(result)

            # Check for leaked secrets in results
            secret_patterns = [
                (r"password[:\s=]+\S+", "password"),
                (r"api[_-]?key[:\s=]+\S+", "api_key"),
                (r"bearer\s+\S{20,}", "bearer_token"),
            ]

            for pattern, secret_type in secret_patterns:
                if re.search(pattern, result_str, re.IGNORECASE):
                    findings.append(SecurityFinding(
                        risk_category=RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                        risk_severity=RiskSeverity.HIGH,
                        risk_score=0.88,
                        policy_id="policy_result_secrets",
                        policy_name="Tool Result Secret Detection",
                        metadata=[f"secret_type:{secret_type}", f"tool:{tool_context.tool_name}"]
                    ))
                    # Redact the secret
                    result_str = re.sub(pattern, f"[REDACTED_{secret_type.upper()}]", result_str, flags=re.IGNORECASE)

            if findings:
                guard_result = GuardianResult(
                    decision_type=DecisionType.MODIFY,
                    decision_reason="Secrets redacted from tool result",
                    findings=findings,
                    modified_content=result_str,
                    content_redacted=True
                )
                ctx.record_result(guard_result)
                return result_str

            guard_result = GuardianResult(decision_type=DecisionType.ALLOW)
            ctx.record_result(guard_result)
            return result


# ============================================================================
# ADK Plugin for Global Security
# ============================================================================

class GeminiAsJudgePlugin:
    """
    Plugin implementing Gemini-as-Judge pattern for content evaluation.

    This demonstrates ADK's plugin architecture for global security policies.
    """

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="gemini-as-judge-v1",
            name="Gemini-as-Judge",
            version="1.0.0",
            provider_name="google.adk"
        )

    def evaluate_content(self, content: str, criteria: List[str]) -> GuardianResult:
        """
        Use Gemini to evaluate content against criteria.

        In production, this would make an actual Gemini API call.
        """
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.MESSAGE
        ) as ctx:
            findings = []

            # Simulate Gemini-as-Judge evaluation
            # In production: call Gemini with evaluation prompt
            simulated_scores = {
                "toxicity": 0.15,
                "bias": 0.22,
                "factuality": 0.85,
                "relevance": 0.92,
            }

            for criterion in criteria:
                if criterion in simulated_scores:
                    score = simulated_scores[criterion]
                    if criterion in ["toxicity", "bias"] and score > 0.5:
                        findings.append(SecurityFinding(
                            risk_category=RiskCategory.TOXICITY if criterion == "toxicity" else "bias",
                            risk_severity=RiskSeverity.MEDIUM,
                            risk_score=score,
                            policy_id=f"gemini_judge_{criterion}",
                            policy_name=f"Gemini Judge - {criterion.title()}"
                        ))

            if findings:
                result = GuardianResult(
                    decision_type=DecisionType.WARN,
                    decision_reason="Content flagged by Gemini-as-Judge",
                    findings=findings
                )
            else:
                result = GuardianResult(decision_type=DecisionType.ALLOW)

            ctx.record_result(result)
            return result


# ============================================================================
# Secure ADK Agent
# ============================================================================

class SecureADKAgent:
    """
    A Google ADK-style agent with integrated security callbacks.
    """

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.llm = get_chat_model()
        self.tool_executor = DemoToolExecutor.create_default()

        # Initialize callbacks
        self.before_model = BeforeModelCallback(tracer)
        self.after_model = AfterModelCallback(tracer)
        self.before_tool = BeforeToolCallback(tracer)
        self.after_tool = AfterToolCallback(tracer)

        # Initialize plugins
        self.gemini_judge = GeminiAsJudgePlugin(tracer)

        self.agent_id = "adk-agent-001"

    def invoke(self, user_input: str) -> str:
        """
        Process user input through the agent with security callbacks.
        """
        with self.tracer.get_tracer().start_as_current_span(
            "invoke_agent ADKSecureAgent",
            kind=SpanKind.INTERNAL
        ) as agent_span:
            agent_span.set_attribute("gen_ai.operation.name", "invoke_agent")
            agent_span.set_attribute("gen_ai.agent.name", "ADKSecureAgent")
            agent_span.set_attribute("gen_ai.agent.id", self.agent_id)

            # Create request
            request = ModelRequest(
                messages=[{"role": "user", "content": user_input}],
                model="gemini-1.5-pro"
            )

            agent_context = {"agent_id": self.agent_id}

            # Before model callback
            validated_request = self.before_model(request, agent_context)
            if validated_request is None:
                return "[BLOCKED] Request blocked by safety filters"

            llm_mode = os.environ.get("DEMO_LLM_MODE", "auto").strip().lower()
            using_openai = llm_mode in {"openai", "auto"} and bool(os.environ.get("OPENAI_API_KEY"))
            model_name = os.environ.get("DEMO_OPENAI_MODEL", "gpt-4o-mini") if using_openai else "mock-llm"

            with self.tracer.get_tracer().start_as_current_span(
                f"chat {model_name}",
                kind=SpanKind.CLIENT
            ) as llm_span:
                llm_span.set_attribute("gen_ai.operation.name", "chat")
                llm_span.set_attribute("gen_ai.request.model", model_name)
                llm_span.set_attribute("gen_ai.provider.name", "openai" if using_openai else "mock")

                content = self.llm.invoke(validated_request.messages)
                llm_span.set_status(Status(StatusCode.OK))

            response = ModelResponse(content=content, safety_ratings=None)

            # After model callback
            validated_response = self.after_model(response, agent_context)

            agent_span.set_status(Status(StatusCode.OK))
            return validated_response.content

    def execute_tool(self, tool_name: str, args: Dict) -> str:
        """
        Execute a tool with security callbacks.
        """
        with self.tracer.get_tracer().start_as_current_span(
            f"execute_tool {tool_name}",
            kind=SpanKind.INTERNAL
        ) as tool_span:
            tool_span.set_attribute("gen_ai.operation.name", "execute_tool")
            tool_span.set_attribute("gen_ai.tool.name", tool_name)

            tool_context = ToolContext(
                tool_name=tool_name,
                agent_id=self.agent_id,
                session_id="session_001"
            )

            # Before tool callback
            validated_args = self.before_tool(tool_context, args)
            if validated_args is None:
                return "[BLOCKED] Tool execution blocked by security policy"

            try:
                result = self.tool_executor.execute(tool_name, validated_args)
            except ToolExecutionError as exc:
                result = f"[TOOL ERROR] {exc}"

            # After tool callback
            validated_result = self.after_tool(tool_context, result)

            tool_span.set_status(Status(StatusCode.OK))
            return validated_result


# ============================================================================
# Demo Scenarios
# ============================================================================

def run_adk_demo():
    """Run demonstration scenarios for Google ADK security guardian integration."""

    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║       Google ADK Security Guardian Integration Demo                   ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║  Demonstrates:                                                        ║
    ║  - before_model_callback (Gemini safety filters)                      ║
    ║  - after_model_callback (output safety validation)                    ║
    ║  - before_tool_callback (tool permission checking)                    ║
    ║  - after_tool_callback (result sanitization)                          ║
    ║  - Gemini-as-Judge plugin                                             ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    tracer = GuardianTracer(service_name="adk-guardian-demo")
    agent = SecureADKAgent(tracer)

    # Scenario 1: Normal request (Allow)
    print("\n" + "=" * 70)
    print("Scenario 1: Normal Request (Expected: Allow)")
    print("=" * 70)
    result = agent.invoke("What's the weather like today?")
    print(f"Response: {result}")

    # Scenario 2: Harmful content request (Deny)
    print("\n" + "=" * 70)
    print("Scenario 2: Harmful Content Request (Expected: Deny)")
    print("=" * 70)
    result = agent.invoke("How to make a dangerous explosive device")
    print(f"Response: {result}")

    # Scenario 3: Safe tool execution (Allow)
    print("\n" + "=" * 70)
    print("Scenario 3: Safe Database Query (Expected: Allow)")
    print("=" * 70)
    result = agent.execute_tool("database_query", {"query": "SELECT * FROM products"})
    print(f"Tool Result: {result}")

    # Scenario 4: Blocked database table (Deny)
    print("\n" + "=" * 70)
    print("Scenario 4: Query Blocked Table (Expected: Deny)")
    print("=" * 70)
    result = agent.execute_tool("database_query", {"query": "SELECT * FROM users"})
    print(f"Tool Result: {result}")

    # Scenario 5: Blocked file path (Deny)
    print("\n" + "=" * 70)
    print("Scenario 5: Read Blocked File Path (Expected: Deny)")
    print("=" * 70)
    result = agent.execute_tool("file_read", {"path": "/etc/passwd"})
    print(f"Tool Result: {result}")

    # Scenario 6: Gemini-as-Judge evaluation
    print("\n" + "=" * 70)
    print("Scenario 6: Gemini-as-Judge Content Evaluation")
    print("=" * 70)
    judge_result = agent.gemini_judge.evaluate_content(
        "This is some content to evaluate",
        ["toxicity", "bias", "factuality"]
    )
    print(f"Judge Decision: {judge_result.decision_type}")

    print("\n" + "=" * 70)
    print("Google ADK Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    run_adk_demo()
