#!/usr/bin/env python3
"""
Story 5: Multi-Tenant SaaS Platform — Tenant Isolation & SLA Monitoring

This story demonstrates how the apply_guardrail span supports multi-tenant
AI platforms with per-tenant security policies.

Key Features:
- tenant.id attribute for trace segmentation
- Per-tenant policy configuration
- SLA metrics tracking (coverage, blocks, modifications)
- Tenant isolation proof via separate traces

Trace Structure:
    chat gpt-4o (CLIENT span)
    ├── tenant.id=acme_corp
    ├── apply_guardrail Acme Input Policy (INTERNAL span)
    │   ├── gen_ai.security.policy.id: acme_custom_policy_001
    │   └── gen_ai.security.decision.type: allow
    └── apply_guardrail Acme Output Policy (INTERNAL span)
        ├── gen_ai.security.policy.id: acme_pii_policy_v3
        ├── gen_ai.security.decision.type: modify
        └── gen_ai.security.finding: pii detected

Author: OpenTelemetry GenAI SIG
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from typing import Dict, Optional
from dataclasses import dataclass
import re

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

from stories.chat_span_utils import (
    GEN_AI_OPERATION_NAME,
    GEN_AI_PROVIDER_NAME,
    GEN_AI_REQUEST_MODEL,
    GEN_AI_RESPONSE_MODEL,
    GEN_AI_CONVERSATION_ID,
    GEN_AI_USAGE_INPUT_TOKENS,
    GEN_AI_USAGE_OUTPUT_TOKENS,
    GEN_AI_RESPONSE_FINISH_REASONS,
    GEN_AI_RESPONSE_ID,
    GEN_AI_INPUT_MESSAGES,
    GEN_AI_OUTPUT_MESSAGES,
)

from stories.demo_llm import DemoLLM, estimate_message_tokens, estimate_tokens


# ============================================================================
# Tenant Configuration
# ============================================================================

@dataclass
class TenantConfig:
    """Per-tenant security configuration."""
    tenant_id: str
    tenant_name: str
    input_policy_id: str
    output_policy_id: str
    pii_sensitivity: str  # low, medium, high
    content_filter_level: str  # permissive, standard, strict
    sensitive_topic_action: str  # allow, warn, deny
    max_token_limit: int


# Sample tenant configurations
TENANT_CONFIGS = {
    "acme_corp": TenantConfig(
        tenant_id="acme_corp",
        tenant_name="Acme Corporation",
        input_policy_id="acme_custom_policy_001",
        output_policy_id="acme_pii_policy_v3",
        pii_sensitivity="high",
        content_filter_level="strict",
        sensitive_topic_action="warn",
        max_token_limit=4096,
    ),
    "globalbank": TenantConfig(
        tenant_id="globalbank",
        tenant_name="GlobalBank Financial",
        input_policy_id="globalbank_compliance_v2",
        output_policy_id="globalbank_pii_v4",
        pii_sensitivity="high",
        content_filter_level="strict",
        sensitive_topic_action="deny",
        max_token_limit=2048,
    ),
    "techstartup": TenantConfig(
        tenant_id="techstartup",
        tenant_name="TechStartup Inc",
        input_policy_id="techstartup_default",
        output_policy_id="techstartup_pii_v1",
        pii_sensitivity="medium",
        content_filter_level="permissive",
        sensitive_topic_action="allow",
        max_token_limit=8192,
    ),
}


# ============================================================================
# Multi-Tenant Guards
# ============================================================================

class TenantInputGuard:
    """
    Tenant-specific input guard with configurable policies.
    """

    def __init__(self, tracer: GuardianTracer, tenant_config: TenantConfig):
        self.tracer = tracer
        self.tenant = tenant_config
        self.config = GuardianConfig(
            id=f"{tenant_config.tenant_id}_input_guard_v2",
            name=f"{tenant_config.tenant_name} Input Policy",
            version="2.0.0",
            provider_name="azure.ai.content_safety"
        )

    def evaluate(self, input_text: str, conversation_id: str) -> GuardianResult:
        """Evaluate input against tenant-specific policies."""
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.LLM_INPUT,
            conversation_id=conversation_id
        ) as ctx:
            findings = []
            sensitive_topic_triggered = False

            ctx.record_content_input(input_text)
            # Tenant-specific content filtering
            if self.tenant.content_filter_level == "strict":
                # Strict mode: check for any potentially sensitive topics
                sensitive_topics = [
                    r"(salary|compensation|bonus)\s+(data|information)",
                    r"(merger|acquisition)\s+(plan|deal)",
                    r"(internal|confidential)\s+project",
                ]
                for pattern in sensitive_topics:
                    if re.search(pattern, input_text, re.IGNORECASE):
                        sensitive_topic_triggered = True
                        findings.append(SecurityFinding(
                            risk_category=RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                            risk_severity=RiskSeverity.MEDIUM,
                            risk_score=0.65,
                            policy_id=self.tenant.input_policy_id,
                            policy_name=f"{self.tenant.tenant_name} Content Filter",
                            metadata=[f"pattern:{pattern[:20]}...", f"filter_level:{self.tenant.content_filter_level}"]
                        ))

            # Check token limit
            estimated_tokens = len(input_text.split()) * 1.3  # Rough estimate
            if estimated_tokens > self.tenant.max_token_limit:
                findings.append(SecurityFinding(
                    risk_category=RiskCategory.UNBOUNDED_CONSUMPTION,
                    risk_severity=RiskSeverity.LOW,
                    risk_score=0.45,
                    policy_id=self.tenant.input_policy_id,
                    metadata=[f"estimated_tokens:{int(estimated_tokens)}", f"limit:{self.tenant.max_token_limit}"]
                ))

            if sensitive_topic_triggered and self.tenant.sensitive_topic_action == "deny":
                result = GuardianResult(
                    decision_type=DecisionType.DENY,
                    decision_reason="Tenant policy blocked sensitive request",
                    decision_code=403,
                    findings=findings,
                    policy_id=self.tenant.input_policy_id,
                    policy_name=f"{self.tenant.tenant_name} Input Policy"
                )
            elif findings:
                result = GuardianResult(
                    decision_type=DecisionType.WARN,
                    decision_reason="Tenant policy flagged content for review",
                    findings=findings,
                    policy_id=self.tenant.input_policy_id,
                    policy_name=f"{self.tenant.tenant_name} Input Policy"
                )
            else:
                result = GuardianResult(
                    decision_type=DecisionType.ALLOW,
                    policy_id=self.tenant.input_policy_id
                )

            ctx.record_content_hash(input_text)
            ctx.record_result(result)
            return result


class TenantOutputGuard:
    """
    Tenant-specific output guard with PII detection.
    """

    def __init__(self, tracer: GuardianTracer, tenant_config: TenantConfig):
        self.tracer = tracer
        self.tenant = tenant_config
        self.config = GuardianConfig(
            id=f"{tenant_config.tenant_id}_output_guard_v2",
            name=f"{tenant_config.tenant_name} Output Policy",
            version="2.0.0",
            provider_name="azure.ai.content_safety"
        )

        # PII patterns based on sensitivity
        self.pii_patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        }

        # Additional patterns for high sensitivity
        if tenant_config.pii_sensitivity == "high":
            self.pii_patterns.update({
                "ssn": r"\b\d{3}[-]?\d{2}[-]?\d{4}\b",
                "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
                "name_pattern": r"(?<=Account manager: )[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?",
            })

    def evaluate(self, output_text: str, conversation_id: str) -> GuardianResult:
        """Evaluate output against tenant-specific PII policies."""
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.LLM_OUTPUT,
            conversation_id=conversation_id
        ) as ctx:
            findings = []
            modified_content = output_text
            has_pii = False

            ctx.record_content_input(output_text)
            ctx.record_content_hash(output_text)

            for pii_type, pattern in self.pii_patterns.items():
                matches = re.findall(pattern, output_text)
                if matches:
                    has_pii = True
                    findings.append(SecurityFinding(
                        risk_category=RiskCategory.PII if pii_type in ["ssn", "name_pattern"] else RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                        risk_severity=RiskSeverity.HIGH if pii_type in ["ssn", "credit_card"] else RiskSeverity.MEDIUM,
                        risk_score=0.90 if pii_type in ["ssn", "credit_card"] else 0.75,
                        policy_id=self.tenant.output_policy_id,
                        policy_name=f"{self.tenant.tenant_name} PII Policy",
                        metadata=[
                            f"pii_type:{pii_type}",
                            f"count:{len(matches)}",
                            f"sensitivity:{self.tenant.pii_sensitivity}"
                        ]
                    ))
                    # Redact PII
                    modified_content = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", modified_content)

            if has_pii:
                result = GuardianResult(
                    decision_type=DecisionType.MODIFY,
                    decision_reason="PII detected and redacted per tenant policy",
                    findings=findings,
                    modified_content=modified_content,
                    content_redacted=True,
                    policy_id=self.tenant.output_policy_id,
                    policy_name=f"{self.tenant.tenant_name} PII Policy"
                )
                ctx.record_content_output(modified_content)
            else:
                result = GuardianResult(
                    decision_type=DecisionType.ALLOW,
                    policy_id=self.tenant.output_policy_id
                )

            ctx.record_result(result)
            return result


# ============================================================================
# Multi-Tenant AI Service
# ============================================================================

class MultiTenantAIService:
    """
    Shared AI infrastructure with per-tenant security isolation.

    Creates properly instrumented chat spans following GenAI semantic conventions.
    """

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self._guards: Dict[str, tuple] = {}
        self._response_counter = 0
        self._llm = DemoLLM()
        self._model_name = self._llm.runtime.model_name
        self._provider_name = self._llm.runtime.provider_name
        self._server_address = self._llm.runtime.server_address

        # Check if content capture is enabled
        self._capture_content = os.environ.get(
            "OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT", "false"
        ).lower() == "true"

    def _get_guards(self, tenant_id: str):
        """Get or create guards for a tenant."""
        if tenant_id not in self._guards:
            config = TENANT_CONFIGS.get(tenant_id)
            if not config:
                raise ValueError(f"Unknown tenant: {tenant_id}")
            self._guards[tenant_id] = (
                TenantInputGuard(self.tracer, config),
                TenantOutputGuard(self.tracer, config)
            )
        return self._guards[tenant_id]

    def process_request(
        self,
        tenant_id: str,
        user_input: str,
        conversation_id: str
    ) -> Dict:
        """
        Process a request through the multi-tenant AI service.

        Each tenant's requests are traced with tenant.id for segmentation.
        """
        tenant_config = TENANT_CONFIGS.get(tenant_id)
        if not tenant_config:
            return {"error": f"Unknown tenant: {tenant_id}"}

        input_guard, output_guard = self._get_guards(tenant_id)

        # Create trace with tenant resource attribute
        tracer = trace.get_tracer(
            "multi_tenant_ai_service",
            "1.0.0",
            schema_url="https://opentelemetry.io/schemas/1.28.0"
        )

        # Span name follows convention: "chat {model}"
        with tracer.start_as_current_span(
            f"chat {self._model_name}",
            kind=SpanKind.CLIENT
        ) as chat_span:
            # === Required Attributes (gen-ai-spans.md) ===
            chat_span.set_attribute(GEN_AI_OPERATION_NAME, "chat")
            chat_span.set_attribute(GEN_AI_PROVIDER_NAME, self._provider_name)

            # === Conditionally Required ===
            chat_span.set_attribute(GEN_AI_REQUEST_MODEL, self._model_name)
            chat_span.set_attribute(GEN_AI_CONVERSATION_ID, conversation_id)
            if self._server_address:
                chat_span.set_attribute("server.address", self._server_address)

            # === Tenant-specific context ===
            chat_span.set_attribute("tenant.id", tenant_id)
            chat_span.set_attribute("tenant.name", tenant_config.tenant_name)

            # === Opt-in: Capture input messages ===
            if self._capture_content:
                system_prompt = self._system_prompt(tenant_config)
                system_instructions = [{"type": "text", "content": system_prompt}]
                chat_span.set_attribute("gen_ai.system_instructions", json.dumps(system_instructions))
                input_messages = [{
                    "role": "user",
                    "parts": [{"type": "text", "content": user_input}]
                }]
                chat_span.set_attribute(GEN_AI_INPUT_MESSAGES, json.dumps(input_messages))

            # === Input Guard ===
            input_result = input_guard.evaluate(user_input, conversation_id)

            if input_result.decision_type == DecisionType.DENY:
                # Still set response attributes even on deny
                chat_span.set_attribute(GEN_AI_RESPONSE_FINISH_REASONS, ["content_filter"])
                if self._capture_content:
                    output_messages = [{
                        "role": "assistant",
                        "parts": [{"type": "text", "content": f"Blocked by tenant policy: {input_result.decision_reason}"}],
                        "finish_reason": "content_filter"
                    }]
                    chat_span.set_attribute(GEN_AI_OUTPUT_MESSAGES, json.dumps(output_messages))
                chat_span.set_status(Status(StatusCode.OK))
                return {
                    "tenant_id": tenant_id,
                    "status": "blocked",
                    "reason": input_result.decision_reason,
                    "policy_id": input_result.policy_id,
                }

            # === LLM Call (real if configured; offline fallback otherwise) ===
            llm_response = self._call_llm(tenant_config, user_input)

            # === Recommended Response Attributes ===
            self._response_counter += 1
            chat_span.set_attribute(GEN_AI_RESPONSE_MODEL, self._model_name)
            chat_span.set_attribute(GEN_AI_RESPONSE_ID, f"chatcmpl-{tenant_id[:8]}-{self._response_counter}")
            chat_span.set_attribute(GEN_AI_RESPONSE_FINISH_REASONS, ["stop"])
            chat_span.set_attribute(GEN_AI_USAGE_INPUT_TOKENS, llm_response["input_tokens"])
            chat_span.set_attribute(GEN_AI_USAGE_OUTPUT_TOKENS, llm_response["output_tokens"])

            # === Output Guard ===
            output_result = output_guard.evaluate(llm_response["content"], conversation_id)

            if output_result.decision_type == DecisionType.MODIFY:
                final_response = output_result.modified_content
            else:
                final_response = llm_response["content"]

            # === Opt-in: Capture output messages ===
            if self._capture_content:
                output_messages = [{
                    "role": "assistant",
                    "parts": [{"type": "text", "content": final_response}],
                    "finish_reason": "stop"
                }]
                chat_span.set_attribute(GEN_AI_OUTPUT_MESSAGES, json.dumps(output_messages))

            chat_span.set_status(Status(StatusCode.OK))

            return {
                "tenant_id": tenant_id,
                "status": "success",
                "response": final_response,
                "input_decision": input_result.decision_type,
                "output_decision": output_result.decision_type,
                "redacted": output_result.content_redacted,
                "policy_ids": {
                    "input": input_result.policy_id,
                    "output": output_result.policy_id,
                },
                "usage": {
                    "input_tokens": llm_response["input_tokens"],
                    "output_tokens": llm_response["output_tokens"],
                }
            }

    def _system_prompt(self, tenant_config: TenantConfig) -> str:
        return (
            "You are a helpful assistant for a multi-tenant SaaS platform.\n"
            f"- Tenant: {tenant_config.tenant_name}\n"
            "- Keep answers short (1-2 sentences).\n"
            "- If asked for support contact email/phone, include: support@example.com and 555-123-4567.\n"
            "- If asked about account manager/contact, include: Account manager: Alex. Direct line: 555-987-6543.\n"
            "- Do not use pronouns when referring to the account manager.\n"
            "- Do not mention the account manager unless asked.\n"
            "- Do not invent real personal data; only use the placeholders above.\n"
        )

    def _call_llm(self, tenant_config: TenantConfig, user_input: str) -> Dict:
        """
        Call the LLM (real if configured) and return response with token counts.

        Returns a dict with content, input_tokens, output_tokens.
        """
        system_prompt = self._system_prompt(tenant_config)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

        try:
            content = self._llm.invoke(messages).strip()
        except Exception:
            content = self._generate_response_content(tenant_config.tenant_id, user_input)

        # Ensure the demo reliably triggers the output guard for key scenarios.
        lowered = user_input.lower()
        if ("contact" in lowered or "email" in lowered) and "support@example.com" not in content:
            content = "You can reach our support team at support@example.com or call 555-123-4567."
        if "account" in lowered and "Account manager:" not in content:
            content = "Account manager: Alex. Direct line: 555-987-6543."

        input_tokens = estimate_message_tokens(messages)
        output_tokens = estimate_tokens(content)

        return {
            "content": content,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }

    def _generate_response_content(self, tenant_id: str, user_input: str) -> str:
        """Generate mock LLM response with potential PII for testing."""
        if "contact" in user_input.lower() or "email" in user_input.lower():
            return "You can reach our support team at support@example.com or call 555-123-4567."
        elif "account" in user_input.lower():
            return "Account manager: Alex. Direct line: 555-987-6543."
        else:
            return f"Hello! I'm the {TENANT_CONFIGS[tenant_id].tenant_name} assistant. How can I help you today?"


# ============================================================================
# Scenario Runner
# ============================================================================

def run_multi_tenant_scenario():
    """
    Run the multi-tenant SaaS story scenario.

    Demonstrates:
    1. Tenant isolation via tenant.id attribute
    2. Per-tenant policy application
    3. Different PII sensitivity levels
    4. SLA metrics (all requests are traced)
    """
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║         Story 5: Multi-Tenant SaaS Platform                          ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║  Demonstrates:                                                        ║
    ║  - tenant.id attribute for trace segmentation                         ║
    ║  - Per-tenant security policies                                       ║
    ║  - Different PII sensitivity levels                                   ║
    ║  - SLA metrics tracking                                               ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    story_title = "Multi-Tenant SaaS Platform — Tenant Isolation & SLA Monitoring"

    tracer = GuardianTracer(service_name="multi-tenant-demo")
    service = MultiTenantAIService(tracer)
    story_tracer = trace.get_tracer("story_5_multi_tenant")
    root_context = trace.set_span_in_context(trace.INVALID_SPAN)

    def run_request_trace(*, tenant_id: str, scenario_name: str, user_input: str, conversation_id: str) -> Dict:
        with story_tracer.start_as_current_span(
            f"story_5.{tenant_id}.{scenario_name}",
            context=root_context,
        ) as root_span:
            root_span.set_attribute("story.id", 5)
            root_span.set_attribute("story.title", story_title)
            root_span.set_attribute("tenant.id", tenant_id)
            root_span.set_attribute("gen_ai.conversation.id", conversation_id)
            root_span.set_attribute("scenario.name", scenario_name)
            return service.process_request(tenant_id, user_input, conversation_id)

    # === Tenant 1: Acme Corp (High Sensitivity) ===
    print("\n" + "=" * 70)
    print("Tenant: Acme Corp (High PII Sensitivity, Strict Filter)")
    print("=" * 70)

    # Request 1: Normal request
    print("\nRequest 1: Normal query")
    result = run_request_trace(
        tenant_id="acme_corp",
        scenario_name="normal_query",
        user_input="What are your business hours?",
        conversation_id="acme_sess_001",
    )
    print(f"  Status: {result['status']}")
    print(f"  Input Decision: {result.get('input_decision', 'N/A')}")
    print(f"  Output Decision: {result.get('output_decision', 'N/A')}")

    # Request 2: PII in response
    print("\nRequest 2: Request that triggers PII redaction")
    result = run_request_trace(
        tenant_id="acme_corp",
        scenario_name="pii_redaction_email_phone",
        user_input="What's the contact email for support?",
        conversation_id="acme_sess_002",
    )
    print(f"  Status: {result['status']}")
    print(f"  Redacted: {result.get('redacted', False)}")
    print(f"  Output Policy: {result.get('policy_ids', {}).get('output', 'N/A')}")
    if result.get('response'):
        print(f"  Response (redacted): {result['response'][:80]}...")

    # Request 3: Sensitive topic (strict filter)
    print("\nRequest 3: Sensitive topic query (strict filter)")
    result = run_request_trace(
        tenant_id="acme_corp",
        scenario_name="sensitive_topic_warn",
        user_input="Tell me about the salary data for executives",
        conversation_id="acme_sess_003",
    )
    print(f"  Status: {result['status']}")
    print(f"  Input Decision: {result.get('input_decision', 'N/A')}")

    # === Tenant 2: GlobalBank (High Sensitivity) ===
    print("\n" + "=" * 70)
    print("Tenant: GlobalBank Financial (High PII Sensitivity)")
    print("=" * 70)

    # Request with account manager info
    print("\nRequest 1: Request that triggers name + phone redaction")
    result = run_request_trace(
        tenant_id="globalbank",
        scenario_name="pii_redaction_name_phone",
        user_input="Who is my account manager?",
        conversation_id="globalbank_sess_001",
    )
    print(f"  Status: {result['status']}")
    print(f"  Redacted: {result.get('redacted', False)}")
    if result.get('response'):
        print(f"  Response (redacted): {result['response']}")

    # Request 2: Sensitive topic (strict filter - blocked)
    print("\nRequest 2: Sensitive topic query (strict filter - blocked)")
    result = run_request_trace(
        tenant_id="globalbank",
        scenario_name="sensitive_topic_deny",
        user_input="Tell me about the merger plan details for Q4",
        conversation_id="globalbank_sess_002",
    )
    print(f"  Status: {result['status']}")
    print(f"  Input Decision: {result.get('input_decision', 'N/A')}")
    print(f"  Reason: {result.get('reason', 'N/A')}")

    # === Tenant 3: TechStartup (Medium Sensitivity, Permissive) ===
    print("\n" + "=" * 70)
    print("Tenant: TechStartup Inc (Medium Sensitivity, Permissive Filter)")
    print("=" * 70)

    # Normal request - permissive filter
    print("\nRequest 1: Sensitive topic (permissive filter - allowed)")
    result = run_request_trace(
        tenant_id="techstartup",
        scenario_name="sensitive_topic_allowed",
        user_input="What's the internal project roadmap?",
        conversation_id="techstartup_sess_001",
    )
    print(f"  Status: {result['status']}")
    print(f"  Input Decision: {result.get('input_decision', 'N/A')}")

    # PII request - medium sensitivity
    print("\nRequest 2: Contact info (medium sensitivity)")
    result = run_request_trace(
        tenant_id="techstartup",
        scenario_name="pii_redaction_email_phone",
        user_input="What's the support email?",
        conversation_id="techstartup_sess_002",
    )
    print(f"  Status: {result['status']}")
    print(f"  Redacted: {result.get('redacted', False)}")
    if result.get('response'):
        print(f"  Response: {result['response'][:80]}...")

    # === Summary ===
    print("\n" + "=" * 70)
    print("Multi-Tenant Scenario Summary")
    print("=" * 70)
    print("""
    ┌──────────────────────────────────────────────────────────────────┐
    │  Tenant          │ Filter Level │ PII Level │ Sample Policy ID   │
    │  ────────────────────────────────────────────────────────────────│
    │  acme_corp       │ strict       │ high      │ acme_pii_policy_v3 │
    │  globalbank      │ strict       │ high      │ globalbank_pii_v4  │
    │  techstartup     │ permissive   │ medium    │ techstartup_pii_v1 │
    └──────────────────────────────────────────────────────────────────┘

    Query Examples:
    - Filter spans by tenant: tenant.id="acme_corp"
    - Count blocked requests: gen_ai.security.decision.type="deny" | stats count by tenant.id
    - SLA coverage: count(apply_guardrail) / count(chat) GROUP BY tenant.id
    """)


if __name__ == "__main__":
    run_multi_tenant_scenario()
