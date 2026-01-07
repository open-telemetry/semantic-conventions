#!/usr/bin/env python3
"""
Story 5: Multi-Tenant SaaS Platform — Tenant Isolation & SLA Monitoring

This story demonstrates how the apply_guardrail span supports multi-tenant
AI platforms with per-tenant security policies.

Key Features:
- tenant.id resource attribute for trace segmentation
- Per-tenant policy configuration
- SLA metrics tracking (coverage, blocks, modifications)
- Tenant isolation proof via separate traces

Trace Structure:
    chat shared_model (CLIENT span)
    ├── Resource: tenant.id=acme_corp
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
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
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
        max_token_limit=4096,
    ),
    "globalbank": TenantConfig(
        tenant_id="globalbank",
        tenant_name="GlobalBank Financial",
        input_policy_id="globalbank_compliance_v2",
        output_policy_id="globalbank_pii_v4",
        pii_sensitivity="high",
        content_filter_level="strict",
        max_token_limit=2048,
    ),
    "techstartup": TenantConfig(
        tenant_id="techstartup",
        tenant_name="TechStartup Inc",
        input_policy_id="techstartup_default",
        output_policy_id="techstartup_pii_v1",
        pii_sensitivity="medium",
        content_filter_level="permissive",
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

            if findings:
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
                "name_pattern": r"\b(Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b",
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
    """

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self._guards: Dict[str, tuple] = {}

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

        with tracer.start_as_current_span(
            "chat shared_model",
            kind=SpanKind.CLIENT
        ) as chat_span:
            # Set tenant context
            chat_span.set_attribute("tenant.id", tenant_id)
            chat_span.set_attribute("tenant.name", tenant_config.tenant_name)
            chat_span.set_attribute("gen_ai.operation.name", "chat")
            chat_span.set_attribute("gen_ai.request.model", "gpt-4o")
            chat_span.set_attribute("gen_ai.conversation.id", conversation_id)

            # === Input Guard ===
            input_result = input_guard.evaluate(user_input, conversation_id)

            if input_result.decision_type == DecisionType.DENY:
                chat_span.set_status(Status(StatusCode.OK))
                return {
                    "tenant_id": tenant_id,
                    "status": "blocked",
                    "reason": input_result.decision_reason,
                    "policy_id": input_result.policy_id,
                }

            # === Simulated LLM Response ===
            # In a real system, this would call the actual LLM
            mock_response = self._generate_mock_response(tenant_id, user_input)

            # === Output Guard ===
            output_result = output_guard.evaluate(mock_response, conversation_id)

            if output_result.decision_type == DecisionType.MODIFY:
                final_response = output_result.modified_content
            else:
                final_response = mock_response

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
                }
            }

    def _generate_mock_response(self, tenant_id: str, user_input: str) -> str:
        """Generate mock LLM response with potential PII for testing."""
        if "contact" in user_input.lower() or "email" in user_input.lower():
            return "You can reach our support team at support@example.com or call 555-123-4567."
        elif "account" in user_input.lower():
            return "Your account manager is Mr. John Smith. His direct line is 555-987-6543."
        else:
            return f"Hello! I'm the {TENANT_CONFIGS[tenant_id].tenant_name} assistant. How can I help you today?"


# ============================================================================
# Scenario Runner
# ============================================================================

def run_multi_tenant_scenario():
    """
    Run the multi-tenant SaaS story scenario.

    Demonstrates:
    1. Tenant isolation via tenant.id resource attribute
    2. Per-tenant policy application
    3. Different PII sensitivity levels
    4. SLA metrics (all requests are traced)
    """
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║         Story 5: Multi-Tenant SaaS Platform                          ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║  Demonstrates:                                                        ║
    ║  - tenant.id resource attribute for trace segmentation               ║
    ║  - Per-tenant security policies                                       ║
    ║  - Different PII sensitivity levels                                   ║
    ║  - SLA metrics tracking                                               ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    tracer = GuardianTracer(service_name="multi-tenant-demo")
    service = MultiTenantAIService(tracer)

    # === Tenant 1: Acme Corp (High Sensitivity) ===
    print("\n" + "=" * 70)
    print("Tenant: Acme Corp (High PII Sensitivity, Strict Filter)")
    print("=" * 70)

    # Request 1: Normal request
    print("\nRequest 1: Normal query")
    result = service.process_request(
        "acme_corp",
        "What are your business hours?",
        "acme_sess_001"
    )
    print(f"  Status: {result['status']}")
    print(f"  Input Decision: {result.get('input_decision', 'N/A')}")
    print(f"  Output Decision: {result.get('output_decision', 'N/A')}")

    # Request 2: PII in response
    print("\nRequest 2: Request that triggers PII redaction")
    result = service.process_request(
        "acme_corp",
        "What's the contact email for support?",
        "acme_sess_002"
    )
    print(f"  Status: {result['status']}")
    print(f"  Redacted: {result.get('redacted', False)}")
    print(f"  Output Policy: {result.get('policy_ids', {}).get('output', 'N/A')}")
    if result.get('response'):
        print(f"  Response (redacted): {result['response'][:80]}...")

    # Request 3: Sensitive topic (strict filter)
    print("\nRequest 3: Sensitive topic query (strict filter)")
    result = service.process_request(
        "acme_corp",
        "Tell me about the salary data for executives",
        "acme_sess_003"
    )
    print(f"  Status: {result['status']}")
    print(f"  Input Decision: {result.get('input_decision', 'N/A')}")

    # === Tenant 2: GlobalBank (High Sensitivity) ===
    print("\n" + "=" * 70)
    print("Tenant: GlobalBank Financial (High PII Sensitivity)")
    print("=" * 70)

    # Request with account manager info
    print("\nRequest 1: Request that triggers name + phone redaction")
    result = service.process_request(
        "globalbank",
        "Who is my account manager?",
        "globalbank_sess_001"
    )
    print(f"  Status: {result['status']}")
    print(f"  Redacted: {result.get('redacted', False)}")
    if result.get('response'):
        print(f"  Response (redacted): {result['response']}")

    # === Tenant 3: TechStartup (Medium Sensitivity, Permissive) ===
    print("\n" + "=" * 70)
    print("Tenant: TechStartup Inc (Medium Sensitivity, Permissive Filter)")
    print("=" * 70)

    # Normal request - permissive filter
    print("\nRequest 1: Sensitive topic (permissive filter - allowed)")
    result = service.process_request(
        "techstartup",
        "What's the internal project roadmap?",
        "techstartup_sess_001"
    )
    print(f"  Status: {result['status']}")
    print(f"  Input Decision: {result.get('input_decision', 'N/A')}")

    # PII request - medium sensitivity
    print("\nRequest 2: Contact info (medium sensitivity)")
    result = service.process_request(
        "techstartup",
        "What's the support email?",
        "techstartup_sess_002"
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
