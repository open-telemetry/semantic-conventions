#!/usr/bin/env python3
"""
OpenTelemetry GenAI Security Guardian Utilities

Shared utilities for emitting security guardian telemetry across different
agent frameworks. These utilities implement the semantic conventions for:
- apply_guardrail span (operation name)
- gen_ai.security.finding event

Usage:
    from otel_guardian_utils import GuardianTracer, DecisionType, TargetType, RiskCategory

Author: OpenTelemetry GenAI SIG
Version: 0.2.0 (Development)
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.trace import SpanKind, Status, StatusCode
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import hashlib
import time


# ============================================================================
# Semantic Convention Constants
# ============================================================================

# Operation name
GEN_AI_OPERATION_NAME = "gen_ai.operation.name"

# Guardian attributes
GEN_AI_GUARDIAN_ID = "gen_ai.guardian.id"
GEN_AI_GUARDIAN_NAME = "gen_ai.guardian.name"
GEN_AI_GUARDIAN_VERSION = "gen_ai.guardian.version"
GEN_AI_GUARDIAN_PROVIDER_NAME = "gen_ai.guardian.provider.name"

# Security decision attributes
GEN_AI_SECURITY_DECISION_TYPE = "gen_ai.security.decision.type"
GEN_AI_SECURITY_DECISION_REASON = "gen_ai.security.decision.reason"
GEN_AI_SECURITY_DECISION_CODE = "gen_ai.security.decision.code"

# Security target attributes
GEN_AI_SECURITY_TARGET_TYPE = "gen_ai.security.target.type"
GEN_AI_SECURITY_TARGET_ID = "gen_ai.security.target.id"

# Security risk attributes (for events)
GEN_AI_SECURITY_RISK_CATEGORY = "gen_ai.security.risk.category"
GEN_AI_SECURITY_RISK_SEVERITY = "gen_ai.security.risk.severity"
GEN_AI_SECURITY_RISK_SCORE = "gen_ai.security.risk.score"
GEN_AI_SECURITY_RISK_METADATA = "gen_ai.security.risk.metadata"

# Policy attributes
GEN_AI_SECURITY_POLICY_ID = "gen_ai.security.policy.id"
GEN_AI_SECURITY_POLICY_NAME = "gen_ai.security.policy.name"
GEN_AI_SECURITY_POLICY_VERSION = "gen_ai.security.policy.version"

# Content attributes (opt-in only)
GEN_AI_SECURITY_CONTENT_INPUT_VALUE = "gen_ai.security.content.input.value"
GEN_AI_SECURITY_CONTENT_OUTPUT_VALUE = "gen_ai.security.content.output.value"
GEN_AI_SECURITY_CONTENT_INPUT_HASH = "gen_ai.security.content.input.hash"
GEN_AI_SECURITY_CONTENT_REDACTED = "gen_ai.security.content.redacted"

# Event name
GEN_AI_SECURITY_FINDING_EVENT = "gen_ai.security.finding"

# Agent/conversation context
GEN_AI_AGENT_ID = "gen_ai.agent.id"
GEN_AI_CONVERSATION_ID = "gen_ai.conversation.id"


# ============================================================================
# Enum Classes
# ============================================================================

class DecisionType:
    """Security decision types as per semantic conventions."""
    ALLOW = "allow"
    DENY = "deny"
    MODIFY = "modify"
    WARN = "warn"
    AUDIT = "audit"


class TargetType:
    """Target types that guardrails can be applied to."""
    LLM_INPUT = "llm_input"
    LLM_OUTPUT = "llm_output"
    TOOL_CALL = "tool_call"
    TOOL_DEFINITION = "tool_definition"
    MEMORY_STORE = "memory_store"
    MEMORY_RETRIEVE = "memory_retrieve"
    KNOWLEDGE_QUERY = "knowledge_query"
    KNOWLEDGE_RESULT = "knowledge_result"
    MESSAGE = "message"


class RiskSeverity:
    """Risk severity levels."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory:
    """OWASP LLM Top 10 2025 aligned risk categories."""
    PROMPT_INJECTION = "prompt_injection"
    SENSITIVE_INFO_DISCLOSURE = "sensitive_info_disclosure"
    SUPPLY_CHAIN = "supply_chain"
    DATA_AND_MODEL_POISONING = "data_and_model_poisoning"
    IMPROPER_OUTPUT_HANDLING = "improper_output_handling"
    EXCESSIVE_AGENCY = "excessive_agency"
    SYSTEM_PROMPT_LEAKAGE = "system_prompt_leakage"
    VECTOR_AND_EMBEDDING_WEAKNESSES = "vector_and_embedding_weaknesses"
    MISINFORMATION = "misinformation"
    UNBOUNDED_CONSUMPTION = "unbounded_consumption"
    JAILBREAK = "jailbreak"
    TOXICITY = "toxicity"
    PII = "pii"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class SecurityFinding:
    """Represents a security finding to be recorded as an event."""
    risk_category: str
    risk_severity: str
    risk_score: float
    policy_id: Optional[str] = None
    policy_name: Optional[str] = None
    policy_version: Optional[str] = None
    metadata: Optional[List[str]] = None


@dataclass
class GuardianConfig:
    """Configuration for a guardian/guardrail."""
    id: str
    name: str
    version: str = "1.0.0"
    provider_name: str = "custom"


@dataclass
class GuardianResult:
    """Result of a guardian evaluation."""
    decision_type: str
    decision_reason: Optional[str] = None
    decision_code: Optional[int] = None
    findings: Optional[List[SecurityFinding]] = None
    modified_content: Optional[str] = None
    content_redacted: bool = False
    # Span-level policy attributes (when a single policy drove the decision)
    policy_id: Optional[str] = None
    policy_name: Optional[str] = None
    policy_version: Optional[str] = None


# ============================================================================
# Guardian Tracer Class
# ============================================================================

class GuardianTracer:
    """
    Utility class for creating guardian spans and events following
    OpenTelemetry GenAI semantic conventions.
    """

    def __init__(
        self,
        service_name: str = "genai-security-guardian",
        service_version: str = "0.1.0",
        enable_console_export: bool = True
    ):
        """Initialize the guardian tracer."""
        self.provider = TracerProvider()

        if enable_console_export:
            self.provider.add_span_processor(
                SimpleSpanProcessor(ConsoleSpanExporter())
            )

        trace.set_tracer_provider(self.provider)

        self.tracer = trace.get_tracer(
            service_name,
            service_version,
            schema_url="https://opentelemetry.io/schemas/1.28.0"
        )

    def get_tracer(self) -> trace.Tracer:
        """Get the underlying tracer."""
        return self.tracer

    def add_processor(self, processor):
        """Add a span processor to the tracer provider."""
        self.provider.add_span_processor(processor)

    @staticmethod
    def hash_content(content: str, algorithm: str = "sha256") -> str:
        """
        Hash content for forensic correlation without storing raw content.

        Args:
            content: The content to hash
            algorithm: Hash algorithm to use (default: sha256)

        Returns:
            Hash string in format "algorithm:hash_value"
        """
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(content.encode('utf-8'))
        return f"{algorithm}:{hash_obj.hexdigest()[:16]}..."

    def create_guardian_span(
        self,
        guardian_config: GuardianConfig,
        target_type: str,
        target_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        conversation_id: Optional[str] = None
    ):
        """
        Create an apply_guardrail span as a context manager.

        Usage:
            with tracer.create_guardian_span(config, TargetType.LLM_INPUT) as span:
                # Perform evaluation
                span.record_result(result)
        """
        span_name = f"apply_guardrail {guardian_config.name}"

        return _GuardianSpanContext(
            self.tracer,
            span_name,
            guardian_config,
            target_type,
            target_id,
            agent_id,
            conversation_id
        )

    def add_security_finding(
        self,
        span: trace.Span,
        finding: SecurityFinding
    ) -> None:
        """Add a gen_ai.security.finding event to the span."""
        attributes: Dict[str, Any] = {
            GEN_AI_SECURITY_RISK_CATEGORY: finding.risk_category,
            GEN_AI_SECURITY_RISK_SEVERITY: finding.risk_severity,
            GEN_AI_SECURITY_RISK_SCORE: finding.risk_score,
        }

        if finding.policy_id:
            attributes[GEN_AI_SECURITY_POLICY_ID] = finding.policy_id
        if finding.policy_name:
            attributes[GEN_AI_SECURITY_POLICY_NAME] = finding.policy_name
        if finding.policy_version:
            attributes[GEN_AI_SECURITY_POLICY_VERSION] = finding.policy_version
        if finding.metadata:
            attributes[GEN_AI_SECURITY_RISK_METADATA] = finding.metadata

        span.add_event(GEN_AI_SECURITY_FINDING_EVENT, attributes=attributes)


class _GuardianSpanContext:
    """Context manager for guardian spans."""

    def __init__(
        self,
        tracer: trace.Tracer,
        span_name: str,
        guardian_config: GuardianConfig,
        target_type: str,
        target_id: Optional[str],
        agent_id: Optional[str],
        conversation_id: Optional[str]
    ):
        self.tracer = tracer
        self.span_name = span_name
        self.guardian_config = guardian_config
        self.target_type = target_type
        self.target_id = target_id
        self.agent_id = agent_id
        self.conversation_id = conversation_id
        self.span: Optional[trace.Span] = None

    def __enter__(self):
        self.span = self.tracer.start_span(
            self.span_name,
            kind=SpanKind.INTERNAL
        )
        self.span.__enter__()

        # Set required attributes
        self.span.set_attribute(GEN_AI_OPERATION_NAME, "apply_guardrail")
        self.span.set_attribute(GEN_AI_GUARDIAN_ID, self.guardian_config.id)
        self.span.set_attribute(GEN_AI_GUARDIAN_NAME, self.guardian_config.name)
        self.span.set_attribute(GEN_AI_GUARDIAN_VERSION, self.guardian_config.version)
        self.span.set_attribute(GEN_AI_GUARDIAN_PROVIDER_NAME, self.guardian_config.provider_name)
        self.span.set_attribute(GEN_AI_SECURITY_TARGET_TYPE, self.target_type)

        if self.target_id:
            self.span.set_attribute(GEN_AI_SECURITY_TARGET_ID, self.target_id)
        if self.agent_id:
            self.span.set_attribute(GEN_AI_AGENT_ID, self.agent_id)
        if self.conversation_id:
            self.span.set_attribute(GEN_AI_CONVERSATION_ID, self.conversation_id)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            if exc_type is not None:
                # Set error.type attribute as per spec (conditionally required on error)
                error_type = exc_type.__name__ if exc_type else "unknown_error"
                self.span.set_attribute("error.type", error_type)
                self.span.set_status(Status(StatusCode.ERROR, str(exc_val)))
            else:
                self.span.set_status(Status(StatusCode.OK))
            self.span.__exit__(exc_type, exc_val, exc_tb)

    def record_result(self, result: GuardianResult) -> None:
        """Record the guardian evaluation result."""
        if not self.span:
            return

        self.span.set_attribute(GEN_AI_SECURITY_DECISION_TYPE, result.decision_type)

        if result.decision_reason:
            self.span.set_attribute(GEN_AI_SECURITY_DECISION_REASON, result.decision_reason)
        if result.decision_code is not None:
            self.span.set_attribute(GEN_AI_SECURITY_DECISION_CODE, result.decision_code)
        if result.content_redacted:
            self.span.set_attribute(GEN_AI_SECURITY_CONTENT_REDACTED, True)

        # Span-level policy attributes (conditionally required: if a policy triggered the decision)
        if result.policy_id:
            self.span.set_attribute(GEN_AI_SECURITY_POLICY_ID, result.policy_id)
        if result.policy_name:
            self.span.set_attribute(GEN_AI_SECURITY_POLICY_NAME, result.policy_name)
        if result.policy_version:
            self.span.set_attribute(GEN_AI_SECURITY_POLICY_VERSION, result.policy_version)

        # Add finding events
        if result.findings:
            for finding in result.findings:
                self._add_finding(finding)

    def _add_finding(self, finding: SecurityFinding) -> None:
        """Add a security finding event."""
        if not self.span:
            return

        attributes: Dict[str, Any] = {
            GEN_AI_SECURITY_RISK_CATEGORY: finding.risk_category,
            GEN_AI_SECURITY_RISK_SEVERITY: finding.risk_severity,
            GEN_AI_SECURITY_RISK_SCORE: finding.risk_score,
        }

        if finding.policy_id:
            attributes[GEN_AI_SECURITY_POLICY_ID] = finding.policy_id
        if finding.policy_name:
            attributes[GEN_AI_SECURITY_POLICY_NAME] = finding.policy_name
        if finding.policy_version:
            attributes[GEN_AI_SECURITY_POLICY_VERSION] = finding.policy_version
        if finding.metadata:
            attributes[GEN_AI_SECURITY_RISK_METADATA] = finding.metadata

        self.span.add_event(GEN_AI_SECURITY_FINDING_EVENT, attributes=attributes)

    def record_content_hash(self, content: str) -> None:
        """Record a hash of the input content for correlation."""
        if self.span:
            content_hash = GuardianTracer.hash_content(content)
            self.span.set_attribute(GEN_AI_SECURITY_CONTENT_INPUT_HASH, content_hash)

    def record_error(self, error_type: str, error_message: str) -> None:
        """
        Record a guardian operation error without raising an exception.

        This sets error.type attribute and ERROR status on the span,
        useful for demonstrating error scenarios without noisy tracebacks.

        Args:
            error_type: The type of error (e.g., "GuardianTimeoutError")
            error_message: Human-readable error description
        """
        if self.span:
            self.span.set_attribute("error.type", error_type)
            self.span.set_status(Status(StatusCode.ERROR, error_message))

    def record_content_input(self, content: str) -> None:
        """
        Record the input content (OPT-IN ONLY).

        WARNING: This attribute may contain sensitive information including PII.
        Only enable via OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT=true environment variable.
        """
        import os
        if os.environ.get("OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT", "").lower() == "true":
            if self.span:
                self.span.set_attribute(GEN_AI_SECURITY_CONTENT_INPUT_VALUE, content)

    def record_content_output(self, content: str) -> None:
        """
        Record the output content after guardian processing (OPT-IN ONLY).

        WARNING: This attribute may contain sensitive information.
        Only enable via OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT=true environment variable.
        For 'modify' decisions, this should contain the sanitized/redacted result.
        """
        import os
        if os.environ.get("OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT", "").lower() == "true":
            if self.span:
                self.span.set_attribute(GEN_AI_SECURITY_CONTENT_OUTPUT_VALUE, content)


# ============================================================================
# Guardrail Decorator
# ============================================================================

def guardrail(
    guardian_config: GuardianConfig,
    target_type: str = TargetType.LLM_INPUT,
    tracer: Optional[GuardianTracer] = None
):
    """
    Decorator to wrap functions with guardian telemetry.

    The decorated function should return a GuardianResult.

    Usage:
        @guardrail(GuardianConfig("pii-guard", "PII Guard"), TargetType.LLM_OUTPUT)
        def check_pii(content: str) -> GuardianResult:
            # Check for PII
            return GuardianResult(decision_type=DecisionType.ALLOW)
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            nonlocal tracer
            if tracer is None:
                tracer = GuardianTracer()

            with tracer.create_guardian_span(guardian_config, target_type) as ctx:
                result = func(*args, **kwargs)
                if isinstance(result, GuardianResult):
                    ctx.record_result(result)
                return result

        return wrapper
    return decorator


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("GuardianTracer utilities loaded successfully!")
    print("\nAvailable classes:")
    print("  - GuardianTracer: Main tracer class for creating guardian spans")
    print("  - GuardianConfig: Configuration for a guardian/guardrail")
    print("  - GuardianResult: Result of a guardian evaluation")
    print("  - SecurityFinding: Individual security finding")
    print("\nAvailable enums:")
    print("  - DecisionType: allow, deny, modify, warn, audit")
    print("  - TargetType: llm_input, llm_output, tool_call, etc.")
    print("  - RiskSeverity: none, low, medium, high, critical")
    print("  - RiskCategory: OWASP LLM Top 10 categories")
