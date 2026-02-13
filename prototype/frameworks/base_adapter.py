"""
Base Guardian Adapter

Shared functionality for all framework-specific guardian adapters.
This module provides the common interface and utilities that all adapters use.

Author: OpenTelemetry GenAI SIG
"""

import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
# Base Configuration
# ============================================================================

@dataclass
class GuardianPolicy:
    """Defines a security policy for the guardian adapter."""
    id: str
    name: str
    version: str = "1.0.0"
    description: Optional[str] = None
    enabled: bool = True

    # Thresholds
    warn_threshold: float = 0.5
    deny_threshold: float = 0.85

    # Patterns to check (framework-specific interpretation)
    blocked_patterns: Optional[List[str]] = None
    audit_patterns: Optional[List[str]] = None


@dataclass
class AdapterConfig:
    """Configuration for the guardian adapter."""
    guardian_id: str
    guardian_name: str
    guardian_version: str = "1.0.0"
    provider_name: str = "custom"

    # Feature flags
    capture_content: bool = False

    # Policies
    policies: Optional[List[GuardianPolicy]] = None

    def __post_init__(self):
        # Check environment for content capture override
        if os.environ.get("OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT", "").lower() == "true":
            self.capture_content = True


# ============================================================================
# Base Adapter Interface
# ============================================================================

T = TypeVar('T')  # Framework-specific context type


class BaseGuardianAdapter(ABC, Generic[T]):
    """
    Abstract base class for framework-specific guardian adapters.

    Each adapter implements the hook points specific to its framework
    while using the shared guardian utilities for telemetry emission.
    """

    def __init__(self, config: AdapterConfig, tracer: Optional[GuardianTracer] = None):
        """
        Initialize the guardian adapter.

        Args:
            config: Adapter configuration
            tracer: Optional existing GuardianTracer; creates one if not provided
        """
        self.config = config
        self.tracer = tracer or GuardianTracer(
            service_name=config.guardian_name,
            enable_console_export=False  # Let the framework/story configure export
        )

        self._guardian_config = GuardianConfig(
            id=config.guardian_id,
            name=config.guardian_name,
            version=config.guardian_version,
            provider_name=config.provider_name,
        )

    @property
    def guardian_config(self) -> GuardianConfig:
        """Get the guardian configuration."""
        return self._guardian_config

    # =========================================================================
    # Abstract Methods (Framework-specific implementations)
    # =========================================================================

    @abstractmethod
    def extract_agent_id(self, context: T) -> Optional[str]:
        """
        Extract the agent ID from the framework context.

        Maps to: gen_ai.agent.id
        """
        pass

    @abstractmethod
    def extract_conversation_id(self, context: T) -> Optional[str]:
        """
        Extract the conversation/session ID from the framework context.

        Maps to: gen_ai.conversation.id
        """
        pass

    # =========================================================================
    # Common Guard Methods
    # =========================================================================

    def guard_llm_input(
        self,
        content: str,
        context: T,
        target_id: Optional[str] = None,
    ) -> GuardianResult:
        """
        Guard LLM input content.

        Target type: llm_input
        """
        return self._evaluate_guard(
            content=content,
            context=context,
            target_type=TargetType.LLM_INPUT,
            target_id=target_id,
        )

    def guard_llm_output(
        self,
        content: str,
        context: T,
        target_id: Optional[str] = None,
    ) -> GuardianResult:
        """
        Guard LLM output content.

        Target type: llm_output
        """
        return self._evaluate_guard(
            content=content,
            context=context,
            target_type=TargetType.LLM_OUTPUT,
            target_id=target_id,
        )

    def guard_tool_call(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        context: T,
        target_id: Optional[str] = None,
    ) -> GuardianResult:
        """
        Guard a tool call.

        Target type: tool_call
        """
        import json
        content = json.dumps({"tool_name": tool_name, "args": tool_args}, sort_keys=True)
        return self._evaluate_guard(
            content=content,
            context=context,
            target_type=TargetType.TOOL_CALL,
            target_id=target_id or f"call_{tool_name}",
        )

    def guard_tool_definition(
        self,
        tool_definition: Dict[str, Any],
        context: T,
        target_id: Optional[str] = None,
    ) -> GuardianResult:
        """
        Validate a tool definition at registration time.

        Target type: tool_definition
        """
        import json
        content = json.dumps(tool_definition, sort_keys=True)
        tool_name = tool_definition.get("name", "unknown")
        return self._evaluate_guard(
            content=content,
            context=context,
            target_type=TargetType.TOOL_DEFINITION,
            target_id=target_id or f"tool_{tool_name}",
        )

    def guard_message(
        self,
        message_content: str,
        source_agent_id: str,
        target_agent_id: str,
        context: T,
    ) -> GuardianResult:
        """
        Guard inter-agent messages.

        Target type: message
        """
        return self._evaluate_guard(
            content=message_content,
            context=context,
            target_type=TargetType.MESSAGE,
            target_id=f"msg_{source_agent_id}_to_{target_agent_id}",
        )

    def guard_memory_store(
        self,
        key: str,
        value: str,
        context: T,
    ) -> GuardianResult:
        """
        Guard memory store operations.

        Target type: memory_store
        """
        return self._evaluate_guard(
            content=value,
            context=context,
            target_type=TargetType.MEMORY_STORE,
            target_id=key,
        )

    def guard_memory_retrieve(
        self,
        key: str,
        context: T,
    ) -> GuardianResult:
        """
        Guard memory retrieve operations.

        Target type: memory_retrieve
        """
        return self._evaluate_guard(
            content=key,
            context=context,
            target_type=TargetType.MEMORY_RETRIEVE,
            target_id=key,
        )

    def guard_knowledge_query(
        self,
        query: str,
        context: T,
        data_source_id: Optional[str] = None,
    ) -> GuardianResult:
        """
        Guard knowledge/RAG queries.

        Target type: knowledge_query
        """
        return self._evaluate_guard(
            content=query,
            context=context,
            target_type=TargetType.KNOWLEDGE_QUERY,
            target_id=data_source_id,
        )

    def guard_knowledge_result(
        self,
        result_content: str,
        context: T,
        query_fingerprint: Optional[str] = None,
    ) -> GuardianResult:
        """
        Guard knowledge/RAG results.

        Target type: knowledge_result
        """
        return self._evaluate_guard(
            content=result_content,
            context=context,
            target_type=TargetType.KNOWLEDGE_RESULT,
            target_id=f"kb_results:{query_fingerprint}" if query_fingerprint else None,
        )

    # =========================================================================
    # Internal Methods
    # =========================================================================

    def _evaluate_guard(
        self,
        content: str,
        context: T,
        target_type: str,
        target_id: Optional[str] = None,
    ) -> GuardianResult:
        """
        Core guard evaluation logic.

        This method:
        1. Creates the apply_guardrail span
        2. Records content (hash always, value if opt-in)
        3. Runs policy checks
        4. Records findings and decision
        """
        agent_id = self.extract_agent_id(context)
        conversation_id = self.extract_conversation_id(context)

        with self.tracer.create_guardian_span(
            self._guardian_config,
            target_type,
            target_id=target_id,
            agent_id=agent_id,
            conversation_id=conversation_id,
        ) as ctx:
            # Always record content hash for forensic correlation
            ctx.record_content_hash(content)

            # Opt-in: record actual content
            ctx.record_content_input(content)

            # Run policy evaluation
            result = self._run_policy_checks(content, target_type)

            # Record output if modified
            if result.decision_type == DecisionType.MODIFY and result.modified_content:
                ctx.record_content_output(result.modified_content)

            # Record the result
            ctx.record_result(result)

            return result

    def _run_policy_checks(self, content: str, target_type: str) -> GuardianResult:
        """
        Run policy checks against content.

        Override this method in subclasses for framework-specific logic.
        Default implementation provides basic pattern matching.
        """
        if not self.config.policies:
            return GuardianResult(decision_type=DecisionType.ALLOW)

        findings: List[SecurityFinding] = []
        max_score = 0.0
        triggered_policy: Optional[GuardianPolicy] = None

        lowered = content.lower()

        for policy in self.config.policies:
            if not policy.enabled:
                continue

            # Check blocked patterns
            if policy.blocked_patterns:
                for pattern in policy.blocked_patterns:
                    if pattern.lower() in lowered:
                        findings.append(SecurityFinding(
                            risk_category=RiskCategory.EXCESSIVE_AGENCY,
                            risk_severity=RiskSeverity.HIGH,
                            risk_score=0.9,
                            policy_id=policy.id,
                            policy_name=policy.name,
                            metadata=[f"pattern:{pattern[:20]}...", f"target:{target_type}"],
                        ))
                        max_score = max(max_score, 0.9)
                        triggered_policy = policy

            # Check audit patterns
            if policy.audit_patterns:
                for pattern in policy.audit_patterns:
                    if pattern.lower() in lowered:
                        findings.append(SecurityFinding(
                            risk_category=RiskCategory.EXCESSIVE_AGENCY,
                            risk_severity=RiskSeverity.LOW,
                            risk_score=0.3,
                            policy_id=policy.id,
                            policy_name=policy.name,
                            metadata=[f"audit_pattern:{pattern[:20]}...", f"target:{target_type}"],
                        ))
                        max_score = max(max_score, 0.3)
                        if not triggered_policy:
                            triggered_policy = policy

        # Determine decision based on score
        if max_score >= (triggered_policy.deny_threshold if triggered_policy else 0.85):
            decision = DecisionType.DENY
            reason = "Content blocked by security policy"
        elif max_score >= (triggered_policy.warn_threshold if triggered_policy else 0.5):
            decision = DecisionType.WARN
            reason = "Content flagged for review"
        elif findings:
            decision = DecisionType.AUDIT
            reason = "Content logged for audit"
        else:
            decision = DecisionType.ALLOW
            reason = None

        return GuardianResult(
            decision_type=decision,
            decision_reason=reason,
            decision_code=403 if decision == DecisionType.DENY else None,
            findings=findings if findings else None,
            policy_id=triggered_policy.id if triggered_policy else None,
            policy_name=triggered_policy.name if triggered_policy else None,
        )


# ============================================================================
# Utility Functions
# ============================================================================

def create_default_policies() -> List[GuardianPolicy]:
    """Create a set of default security policies."""
    return [
        GuardianPolicy(
            id="policy_injection_prevention_v1",
            name="Injection Prevention Policy",
            blocked_patterns=[
                "ignore previous instructions",
                "ignore all instructions",
                "new system prompt",
                "act as administrator",
                "sudo",
                "rm -rf",
            ],
            audit_patterns=[
                "pretend",
                "roleplay",
                "imagine you are",
            ],
        ),
        GuardianPolicy(
            id="policy_pii_protection_v1",
            name="PII Protection Policy",
            audit_patterns=[
                "password",
                "credit card",
                "social security",
                "api key",
                "secret",
            ],
        ),
        GuardianPolicy(
            id="policy_tool_safety_v1",
            name="Tool Safety Policy",
            blocked_patterns=[
                "shell",
                "system_command",
                "file_delete",
                "admin_access",
            ],
            audit_patterns=[
                "execute",
                "sandbox",
                "network",
                "external",
            ],
        ),
    ]
