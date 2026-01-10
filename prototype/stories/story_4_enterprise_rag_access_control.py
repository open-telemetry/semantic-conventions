#!/usr/bin/env python3
"""
Story 4: Enterprise RAG Access Control — Knowledge + Memory Guardrails

Demonstrates applying `apply_guardrail` spans to:
- knowledge queries (`gen_ai.security.target.type=knowledge_query`)
- knowledge results (`gen_ai.security.target.type=knowledge_result`)
- memory writes (`gen_ai.security.target.type=memory_store`)
- memory reads (`gen_ai.security.target.type=memory_retrieve`)

The goal is to showcase how a RAG system can:
- Block restricted knowledge queries
- Filter/redact restricted results before they reach the model or user
- Prevent secrets from being persisted to memory
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode

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


# =============================================================================
# Mock Knowledge + Memory Stores
# =============================================================================

@dataclass(frozen=True)
class KnowledgeDoc:
    doc_id: str
    title: str
    classification: str  # public | confidential | restricted
    content: str


KNOWLEDGE_BASE_ID = "kb_enterprise_wiki_v1"
KNOWLEDGE_BASE: List[KnowledgeDoc] = [
    KnowledgeDoc(
        doc_id="doc_pto_001",
        title="PTO Policy (Public Summary)",
        classification="public",
        content="Employees accrue PTO monthly. For details, see the HR portal.",
    ),
    KnowledgeDoc(
        doc_id="doc_hr_042",
        title="HR Handbook (Confidential)",
        classification="confidential",
        content="Internal HR procedures and manager-only guidance.",
    ),
    KnowledgeDoc(
        doc_id="doc_exec_900",
        title="Executive Compensation Bands (Restricted)",
        classification="restricted",
        content="Executive salary bands and bonus targets (restricted).",
    ),
]


def _is_role_allowed_for(doc: KnowledgeDoc, user_role: str) -> bool:
    if doc.classification == "public":
        return True
    if doc.classification == "confidential":
        return user_role in {"employee", "hr", "admin"}
    if doc.classification == "restricted":
        return user_role in {"hr", "admin"}
    return False


# =============================================================================
# Guards
# =============================================================================

class KnowledgeQueryGuard:
    """Guardrails for outbound knowledge queries."""

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="rag-query-guard-v1",
            name="RAG Query Access Guard",
            version="1.0.0",
            provider_name="custom.rag_access",
        )

        self._restricted_terms = [
            "executive salary",
            "compensation bands",
            "bonus targets",
            "merger plan",
        ]

    def evaluate(self, *, query: str, conversation_id: str, user_role: str) -> GuardianResult:
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.KNOWLEDGE_QUERY,
            target_id=KNOWLEDGE_BASE_ID,
            conversation_id=conversation_id,
        ) as ctx:
            ctx.record_content_hash(query)

            lowered = query.lower()
            if any(term in lowered for term in self._restricted_terms) and user_role not in {"hr", "admin"}:
                finding = SecurityFinding(
                    risk_category=RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                    risk_severity=RiskSeverity.HIGH,
                    risk_score=0.9,
                    policy_id="policy_rag_query_acl_v1",
                    policy_name="RAG Query ACL Policy",
                    metadata=[f"role:{user_role}", "action:blocked", f"kb:{KNOWLEDGE_BASE_ID}"],
                )
                result = GuardianResult(
                    decision_type=DecisionType.DENY,
                    decision_reason="User role not permitted to query restricted knowledge",
                    decision_code=403,
                    findings=[finding],
                    policy_id="policy_rag_query_acl_v1",
                    policy_name="RAG Query ACL Policy",
                )
            else:
                result = GuardianResult(
                    decision_type=DecisionType.ALLOW,
                    policy_id="policy_rag_query_acl_v1",
                    policy_name="RAG Query ACL Policy",
                )

            ctx.record_result(result)
            return result


class KnowledgeResultGuard:
    """Filters knowledge results before they are used by the model."""

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="rag-result-guard-v1",
            name="RAG Result Filter",
            version="1.0.0",
            provider_name="custom.rag_access",
        )

    def evaluate(
        self,
        *,
        docs: List[KnowledgeDoc],
        conversation_id: str,
        user_role: str,
        query_fingerprint: str,
    ) -> Tuple[GuardianResult, List[KnowledgeDoc]]:
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.KNOWLEDGE_RESULT,
            target_id=f"kb_results:{query_fingerprint}",
            conversation_id=conversation_id,
        ) as ctx:
            ctx.record_content_hash("|".join(d.doc_id for d in docs))

            allowed_docs = [d for d in docs if _is_role_allowed_for(d, user_role)]
            removed = [d for d in docs if d not in allowed_docs]

            if removed:
                finding = SecurityFinding(
                    risk_category=RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                    risk_severity=RiskSeverity.MEDIUM,
                    risk_score=0.7,
                    policy_id="policy_rag_result_filter_v1",
                    policy_name="RAG Result Filter Policy",
                    metadata=[
                        f"role:{user_role}",
                        f"removed:{len(removed)}",
                        "action:filtered",
                        f"kb:{KNOWLEDGE_BASE_ID}",
                    ],
                )
                result = GuardianResult(
                    decision_type=DecisionType.MODIFY,
                    decision_reason="Restricted knowledge removed from results",
                    findings=[finding],
                    content_redacted=True,
                    policy_id="policy_rag_result_filter_v1",
                    policy_name="RAG Result Filter Policy",
                )
                # Opt-in only (safe summary): titles only.
                ctx.record_content_output(json.dumps([d.title for d in allowed_docs]))
            else:
                result = GuardianResult(
                    decision_type=DecisionType.ALLOW,
                    policy_id="policy_rag_result_filter_v1",
                    policy_name="RAG Result Filter Policy",
                )

            ctx.record_result(result)
            return result, allowed_docs


class MemoryStoreGuard:
    """Prevents sensitive data from being persisted."""

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="memory-store-guard-v1",
            name="Memory Store Guard",
            version="1.0.0",
            provider_name="custom.memory",
        )

    def evaluate(self, *, key: str, value: str, conversation_id: str) -> GuardianResult:
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.MEMORY_STORE,
            target_id=key,
            conversation_id=conversation_id,
        ) as ctx:
            ctx.record_content_hash(value)

            lowered = value.lower()
            looks_like_secret = any(token in lowered for token in ["api_key", "apikey", "token=", "bearer "])
            if looks_like_secret:
                finding = SecurityFinding(
                    risk_category=RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                    risk_severity=RiskSeverity.HIGH,
                    risk_score=0.95,
                    policy_id="policy_memory_store_secrets_v1",
                    policy_name="Memory Secret Prevention",
                    metadata=["pattern:secret", "action:blocked"],
                )
                result = GuardianResult(
                    decision_type=DecisionType.DENY,
                    decision_reason="Potential secret detected; memory write blocked",
                    decision_code=403,
                    findings=[finding],
                    policy_id="policy_memory_store_secrets_v1",
                    policy_name="Memory Secret Prevention",
                )
            else:
                result = GuardianResult(
                    decision_type=DecisionType.ALLOW,
                    policy_id="policy_memory_store_secrets_v1",
                    policy_name="Memory Secret Prevention",
                )

            ctx.record_result(result)
            return result


class MemoryRetrieveGuard:
    """Guards reads from memory to prevent unsafe retrieval patterns."""

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.config = GuardianConfig(
            id="memory-retrieve-guard-v1",
            name="Memory Retrieve Guard",
            version="1.0.0",
            provider_name="custom.memory",
        )

    def evaluate(self, *, key: str, conversation_id: str) -> GuardianResult:
        with self.tracer.create_guardian_span(
            self.config,
            TargetType.MEMORY_RETRIEVE,
            target_id=key,
            conversation_id=conversation_id,
        ) as ctx:
            ctx.record_content_hash(key)
            result = GuardianResult(
                decision_type=DecisionType.ALLOW,
                policy_id="policy_memory_retrieve_v1",
                policy_name="Memory Retrieval Policy",
            )
            ctx.record_result(result)
            return result


# =============================================================================
# RAG Service (mock)
# =============================================================================

class EnterpriseRAGService:
    MODEL_NAME = "gpt-4o"
    PROVIDER_NAME = "mock"

    def __init__(self, tracer: GuardianTracer):
        self.tracer = tracer
        self.query_guard = KnowledgeQueryGuard(tracer)
        self.result_guard = KnowledgeResultGuard(tracer)
        self.mem_store_guard = MemoryStoreGuard(tracer)
        self.mem_retrieve_guard = MemoryRetrieveGuard(tracer)
        self._memory: Dict[str, str] = {}

    def _search(self, query: str) -> List[KnowledgeDoc]:
        q = query.lower()
        if "pto" in q or "time off" in q:
            return [KNOWLEDGE_BASE[0], KNOWLEDGE_BASE[1]]
        if "salary" in q or "compensation" in q or "bonus" in q:
            return [KNOWLEDGE_BASE[2], KNOWLEDGE_BASE[1]]
        return [KNOWLEDGE_BASE[0]]

    def process_question(self, *, query: str, conversation_id: str, user_role: str) -> Dict:
        otel_tracer = trace.get_tracer("enterprise_rag_service")
        capture_content = os.environ.get("OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT", "false").lower() == "true"

        with otel_tracer.start_as_current_span(f"chat {self.MODEL_NAME}", kind=SpanKind.CLIENT) as chat_span:
            chat_span.set_attribute("gen_ai.operation.name", "chat")
            chat_span.set_attribute("gen_ai.provider.name", self.PROVIDER_NAME)
            chat_span.set_attribute("gen_ai.request.model", self.MODEL_NAME)
            chat_span.set_attribute("gen_ai.conversation.id", conversation_id)
            chat_span.set_attribute("enduser.role", user_role)
            chat_span.set_attribute("gen_ai.data_source.id", KNOWLEDGE_BASE_ID)
            if capture_content:
                input_messages = [{
                    "role": "user",
                    "parts": [{"type": "text", "content": query}],
                }]
                chat_span.set_attribute("gen_ai.input.messages", json.dumps(input_messages))

            # 1) Guard the knowledge query.
            query_result = self.query_guard.evaluate(
                query=query,
                conversation_id=conversation_id,
                user_role=user_role,
            )
            if query_result.decision_type == DecisionType.DENY:
                chat_span.set_attribute("gen_ai.response.finish_reasons", ["content_filter"])
                chat_span.set_attribute("gen_ai.response.model", self.MODEL_NAME)
                chat_span.set_attribute("gen_ai.usage.input_tokens", int(len(query.split()) * 1.3))
                chat_span.set_attribute("gen_ai.usage.output_tokens", 0)
                if capture_content:
                    output_messages = [{
                        "role": "assistant",
                        "parts": [{"type": "text", "content": f"Blocked by policy: {query_result.decision_reason}"}],
                        "finish_reason": "content_filter",
                    }]
                    chat_span.set_attribute("gen_ai.output.messages", json.dumps(output_messages))
                chat_span.set_status(Status(StatusCode.OK))
                return {
                    "status": "blocked",
                    "reason": query_result.decision_reason,
                }

            # 2) Retrieve knowledge.
            docs = self._search(query)
            fingerprint = f"{conversation_id}:{abs(hash(query)) % 10000}"

            # 3) Guard the results (filter restricted docs).
            result_decision, allowed_docs = self.result_guard.evaluate(
                docs=docs,
                conversation_id=conversation_id,
                user_role=user_role,
                query_fingerprint=fingerprint,
            )

            # 4) Store a safe summary in memory.
            mem_key = f"rag:{conversation_id}:last_docs"
            mem_value = ",".join(d.doc_id for d in allowed_docs)
            store_decision = self.mem_store_guard.evaluate(
                key=mem_key,
                value=mem_value,
                conversation_id=conversation_id,
            )
            if store_decision.decision_type == DecisionType.ALLOW:
                self._memory[mem_key] = mem_value

            # 5) Retrieve the stored memory (for demonstration).
            _ = self.mem_retrieve_guard.evaluate(key=mem_key, conversation_id=conversation_id)
            remembered = self._memory.get(mem_key, "")

            # Mock response attributes (recommended)
            chat_span.set_attribute("gen_ai.response.model", self.MODEL_NAME)
            chat_span.set_attribute("gen_ai.response.id", f"chatcmpl-{fingerprint}")
            chat_span.set_attribute("gen_ai.response.finish_reasons", ["stop"])
            chat_span.set_attribute("gen_ai.usage.input_tokens", int(len(query.split()) * 1.3))
            chat_span.set_attribute("gen_ai.usage.output_tokens", int(80))
            if capture_content:
                assistant_reply = (
                    f"Found {len(allowed_docs)} document(s): "
                    + ", ".join(d.title for d in allowed_docs)
                    + (f". Remembered: {remembered}" if remembered else ".")
                )
                output_messages = [{
                    "role": "assistant",
                    "parts": [{"type": "text", "content": assistant_reply}],
                    "finish_reason": "stop",
                }]
                chat_span.set_attribute("gen_ai.output.messages", json.dumps(output_messages))

            chat_span.set_status(Status(StatusCode.OK))

            return {
                "status": "ok",
                "query_decision": query_result.decision_type,
                "result_decision": result_decision.decision_type,
                "doc_count": len(allowed_docs),
                "docs": [d.title for d in allowed_docs],
                "memory": remembered,
            }

    def attempt_store_secret(self, *, conversation_id: str, secret_value: str) -> Dict:
        otel_tracer = trace.get_tracer("enterprise_rag_service")
        capture_content = os.environ.get("OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT", "false").lower() == "true"
        with otel_tracer.start_as_current_span(f"chat {self.MODEL_NAME}", kind=SpanKind.CLIENT) as chat_span:
            chat_span.set_attribute("gen_ai.operation.name", "chat")
            chat_span.set_attribute("gen_ai.provider.name", self.PROVIDER_NAME)
            chat_span.set_attribute("gen_ai.request.model", self.MODEL_NAME)
            chat_span.set_attribute("gen_ai.conversation.id", conversation_id)
            if capture_content:
                input_messages = [{
                    "role": "user",
                    "parts": [{"type": "text", "content": f"Remember this for later: {secret_value}"}],
                }]
                chat_span.set_attribute("gen_ai.input.messages", json.dumps(input_messages))

            mem_key = f"rag:{conversation_id}:secret"
            store_decision = self.mem_store_guard.evaluate(
                key=mem_key,
                value=secret_value,
                conversation_id=conversation_id,
            )
            if store_decision.decision_type == DecisionType.ALLOW:
                self._memory[mem_key] = secret_value

            chat_span.set_attribute("gen_ai.response.model", self.MODEL_NAME)
            chat_span.set_attribute("gen_ai.response.finish_reasons", ["stop"])
            chat_span.set_attribute("gen_ai.usage.input_tokens", int(len(secret_value.split()) * 1.3))
            chat_span.set_attribute("gen_ai.usage.output_tokens", 0)
            if capture_content:
                output_text = (
                    "Stored in memory."
                    if store_decision.decision_type == DecisionType.ALLOW
                    else f"Blocked: {store_decision.decision_reason}"
                )
                output_messages = [{
                    "role": "assistant",
                    "parts": [{"type": "text", "content": output_text}],
                    "finish_reason": "stop",
                }]
                chat_span.set_attribute("gen_ai.output.messages", json.dumps(output_messages))
            chat_span.set_status(Status(StatusCode.OK))

            return {
                "status": "ok",
                "memory_store_decision": store_decision.decision_type,
                "stored": store_decision.decision_type == DecisionType.ALLOW,
            }


# =============================================================================
# Runner
# =============================================================================

def run_enterprise_rag_scenario():
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║         Story 4: Enterprise RAG Access Control                        ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║  Demonstrates:                                                        ║
    ║  - knowledge_query + knowledge_result guardrails                       ║
    ║  - memory_store + memory_retrieve guardrails                           ║
    ║  - modify (filter) and deny decisions                                  ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)

    story_title = "Enterprise RAG Access Control — Knowledge + Memory Guardrails"

    tracer = GuardianTracer(service_name="enterprise-rag-demo")
    service = EnterpriseRAGService(tracer)
    story_tracer = trace.get_tracer("story_4_enterprise_rag")
    root_context = trace.set_span_in_context(trace.INVALID_SPAN)

    def run_story_trace(scenario_name: str, fn):
        with story_tracer.start_as_current_span(
            f"story_4.{scenario_name}",
            context=root_context,
        ) as root_span:
            root_span.set_attribute("story.id", 4)
            root_span.set_attribute("story.title", story_title)
            root_span.set_attribute("scenario.name", scenario_name)
            return fn()

    print("\nScenario 1: Query allowed; results filtered (contractor); memory stored/retrieved")
    result = run_story_trace(
        "rag_query_allow_result_filter",
        lambda: service.process_question(
            query="What's the PTO policy for employees?",
            conversation_id="conv_rag_001",
            user_role="contractor",
        ),
    )
    print(f"  Status: {result['status']}")
    print(f"  Query Decision: {result.get('query_decision')}")
    print(f"  Result Decision: {result.get('result_decision')}")
    print(f"  Docs Returned: {result.get('doc_count')} -> {result.get('docs')}")

    print("\nScenario 2: Restricted query blocked at knowledge_query")
    result = run_story_trace(
        "rag_query_blocked",
        lambda: service.process_question(
            query="Show me executive salary and compensation bands",
            conversation_id="conv_rag_002",
            user_role="employee",
        ),
    )
    print(f"  Status: {result['status']}")
    print(f"  Reason: {result.get('reason')}")

    print("\nScenario 3: Secret blocked at memory_store")
    result = run_story_trace(
        "memory_store_secret_blocked",
        lambda: service.attempt_store_secret(
            conversation_id="conv_rag_003",
            secret_value="token=sk-super-secret-value",
        ),
    )
    print(f"  Memory Store Decision: {result['memory_store_decision']}")
    print(f"  Stored: {result['stored']}")


if __name__ == "__main__":
    run_enterprise_rag_scenario()
