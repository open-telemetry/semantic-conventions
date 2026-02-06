#!/usr/bin/env python3
"""
Story 5: Compliance Audit & Debugging

This scenario demonstrates WHY memory observability matters through
three real-world debugging and compliance scenarios:

Scenario A: Debugging Incorrect Agent Response
- search_memory returns 0 results due to high similarity threshold
- Trace reveals the configuration bug

Scenario B: Compliance Audit
- Track all memory access for user "Sarah" during a session
- Demonstrates audit-ready trace attributes

Scenario C: Performance Debugging
- search_memory takes too long due to large result set
- Trace reveals missing filters/thresholds

Key Attributes Demonstrated:
- gen_ai.conversation.id: audit trail linking
- gen_ai.agent.id: agent attribution
- gen_ai.memory.search.result.count: debugging metric
- gen_ai.memory.search.similarity.threshold: configuration visibility

Memory Spans Used:
- search_memory: retrieval debugging
- update_memory: audit trail for writes

Run with:
    python main.py

To export to OTLP:
    GENAI_MEMORY_USE_OTLP=true python main.py
"""

import os
import json
import sys
import time
import uuid

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core', 'python'))

from opentelemetry.trace import SpanKind

from genai_memory_otel import (
    setup_tracing,
    MemorySpanBuilder,
    MemoryType,
    MemoryAttributes,
    GenAIAttributes,
    LLMClient,
)


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def print_span_info(operation: str, attributes: dict):
    """Print span information."""
    print(f"\n  [{operation}]")
    for key, value in attributes.items():
        print(f"    {key}: {value}")


def print_trace_tree(title: str, tree: str):
    """Print a trace visualization."""
    print(f"\n  {title}")
    print("-" * 50)
    for line in tree.strip().split("\n"):
        print(f"  {line}")


def scenario_a_debugging_incorrect_response(tracer, span_builder, *, llm: LLMClient):
    """
    Scenario A: Debugging why the agent "forgot" information.

    Problem: Customer reports the agent forgot what they said earlier.
    Root cause: similarity_threshold too high (0.95), filtering out memories.
    """
    print_section("Scenario A: Debugging Incorrect Agent Response")
    print("""
Problem: A customer reports that the support agent "forgot" information
they provided earlier in the conversation.

Investigation: Use traces to understand what went wrong.
""")

    conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
    user_id = "user_sarah_123"
    agent_id = "support_bot"

    with tracer.start_as_current_span(
        "invoke_agent SupportBot",
        kind=SpanKind.CLIENT,
        attributes={
            GenAIAttributes.OPERATION_NAME: "invoke_agent",
            GenAIAttributes.PROVIDER_NAME: llm.provider_name(),
            GenAIAttributes.REQUEST_MODEL: llm.model,
            "server.address": "api.openai.com",
            GenAIAttributes.AGENT_NAME: "SupportBot",
            GenAIAttributes.AGENT_ID: agent_id,
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ) as agent_span:
        user_prompt = "I was charged twice for my subscription and mentioned it earlier."
        if span_builder.capture_content:
            agent_span.set_attribute(
                "gen_ai.input.messages",
                json.dumps(
                    [{"role": "user", "parts": [{"type": "text", "content": user_prompt}]}],
                    ensure_ascii=False,
                ),
            )

        # Search with too-high threshold (the bug!)
        print("\n  [BUG] search_memory with threshold=0.95 (too high)")
        with span_builder.search_memory_span(
            provider_name="pinecone",
            store_id=f"store_{user_id}_history",
            store_name="conversation-history",
            query="billing issue mentioned earlier",
            memory_type=MemoryType.SHORT_TERM,
            similarity_threshold=0.95,  # BUG: Too high!
            conversation_id=conversation_id,
        ) as span:
            # Returns 0 results because threshold is too strict
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 0)

        query_display = (
            "billing issue mentioned earlier"
            if span_builder.capture_content
            else "(opt-in disabled)"
        )

        print_trace_tree("Trace reveals the issue:", f"""
invoke_agent support_bot
├── gen_ai.conversation.id: {conversation_id}
│
└── search_memory conversation-history
    ├── gen_ai.memory.search.result.count: 0  ← BUG: No results!
    ├── gen_ai.memory.search.similarity.threshold: 0.95  ← Too high!
    └── gen_ai.memory.query: {query_display}
""")

        print("""
Root Cause Analysis:
  - search_memory returned 0 results
  - similarity.threshold was set to 0.95 (extremely strict)
  - Relevant memories exist but scored 0.7-0.85 (filtered out)

Fix: Lower similarity_threshold to 0.7
""")

        # Show the fix
        print("\n  [FIX] search_memory with threshold=0.7")
        with span_builder.search_memory_span(
            provider_name="pinecone",
            store_id=f"store_{user_id}_history",
            store_name="conversation-history",
            query="billing issue mentioned earlier",
            memory_type=MemoryType.SHORT_TERM,
            similarity_threshold=0.7,  # Fixed!
            conversation_id=conversation_id,
        ) as span:
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 3)

        print("  After fix: search.result.count = 3")

        if span_builder.capture_content:
            agent_span.set_attribute(
                "gen_ai.output.messages",
                json.dumps(
                    [
                        {
                            "role": "assistant",
                            "parts": [
                                {
                                    "type": "text",
                                    "content": (
                                        "I found your earlier billing note about a duplicate charge. "
                                        "I can help you verify the invoice and start a refund if needed."
                                    ),
                                }
                            ],
                        }
                    ],
                    ensure_ascii=False,
                ),
            )


def scenario_b_compliance_audit(tracer, span_builder):
    """
    Scenario B: Compliance audit of memory access.

    Requirement: Auditor needs to verify that user Sarah's data was only
    accessed by authorized agents during her support session.
    """
    print_section("Scenario B: Compliance Audit")
    print("""
Requirement: Auditor needs to verify that user Sarah's data was only
accessed by authorized agents during her support session.

Audit Query: Find all memory operations for Sarah's session.
""")

    conversation_id = "conv_audit_12345"
    user_id = "user_sarah_123"
    namespace = f"ns_{user_id}"
    agent_id = "support_bot"

    print(f"\n  Audit Parameters:")
    print(f"    User: {user_id}")
    print(f"    Conversation: {conversation_id}")
    print(f"    Expected Agent: {agent_id}")

    # Simulate audit trace
    with tracer.start_as_current_span(
        f"audit_session {conversation_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ) as audit_span:

        # First memory access
        with span_builder.search_memory_span(
            provider_name="pinecone",
            store_id=f"store_{user_id}_history",
            store_name="user-history",
            query="billing issue",
            memory_type=MemoryType.LONG_TERM,
            namespace=namespace,
            agent_id=agent_id,
            conversation_id=conversation_id,
        ) as span:
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 3)

        # Second memory access
        with span_builder.search_memory_span(
            provider_name="pinecone",
            store_id=f"store_{user_id}_history",
            store_name="user-history",
            query="previous tickets",
            memory_type=MemoryType.LONG_TERM,
            namespace=namespace,
            agent_id=agent_id,
            conversation_id=conversation_id,
        ) as span:
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 2)

        # Memory update (store conversation)
        with span_builder.update_memory_span(
            provider_name="pinecone",
            store_id="session-store",
            store_name="session-store",
            memory_id=f"turn_{conversation_id}_001",
            memory_type=MemoryType.SHORT_TERM,
            namespace=namespace,
            agent_id=agent_id,
            conversation_id=conversation_id,
        ):
            pass

    print_trace_tree("Audit Trail:", """
audit_session conv_audit_12345
│
├── search_memory user-history (10:30:15)
│   ├── gen_ai.agent.id: support_bot ✓
│   ├── gen_ai.memory.namespace: ns_user_sarah_123
│   ├── gen_ai.memory.search.result.count: 3
│   └── gen_ai.conversation.id: conv_audit_12345
│
├── search_memory user-history (10:31:22)
│   ├── gen_ai.agent.id: support_bot ✓
│   ├── gen_ai.memory.namespace: ns_user_sarah_123
│   ├── gen_ai.memory.search.result.count: 2
│   └── gen_ai.conversation.id: conv_audit_12345
│
└── update_memory session-store (10:35:45)
    ├── gen_ai.agent.id: support_bot ✓
    ├── gen_ai.memory.namespace: ns_user_sarah_123
    └── gen_ai.conversation.id: conv_audit_12345
""")

    print("""
Audit Verification:
  ✓ All memory access was by authorized agent (support_bot)
  ✓ All operations linked to correct conversation_id
  ✓ All operations scoped to user's namespace
  ✓ No unauthorized access detected

Query for audit (pseudo-SQL):
  SELECT * FROM traces
  WHERE gen_ai.memory.namespace = 'ns_user_sarah_123'
    AND gen_ai.conversation.id = 'conv_audit_12345'
  ORDER BY timestamp
""")


def scenario_c_performance_debugging(tracer, span_builder, *, llm: LLMClient):
    """
    Scenario C: Performance debugging slow agent responses.

    Problem: Users report slow responses from the shopping assistant.
    Root cause: search_memory returning 50,000 results without filtering.
    """
    print_section("Scenario C: Performance Debugging")
    print("""
Problem: Users report slow responses from the shopping assistant.
Investigation: Use trace timing to identify the bottleneck.
""")

    agent_id = "shopping_assistant"
    conversation_id = f"conv_perf_{uuid.uuid4().hex[:8]}"

    with tracer.start_as_current_span(
        "invoke_agent ShoppingAssistant",
        kind=SpanKind.CLIENT,
        attributes={
            GenAIAttributes.OPERATION_NAME: "invoke_agent",
            GenAIAttributes.PROVIDER_NAME: llm.provider_name(),
            GenAIAttributes.REQUEST_MODEL: llm.model,
            "server.address": "api.openai.com",
            GenAIAttributes.AGENT_NAME: "ShoppingAssistant",
            GenAIAttributes.AGENT_ID: agent_id,
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ) as agent_span:
        perf_prompt = "Recommend a laptop based on my preferences."
        if span_builder.capture_content:
            agent_span.set_attribute(
                "gen_ai.input.messages",
                json.dumps(
                    [{"role": "user", "parts": [{"type": "text", "content": perf_prompt}]}],
                    ensure_ascii=False,
                ),
            )

        # Normal search - fast
        print("\n  [FAST] search_memory user-preferences (850ms)")
        with span_builder.search_memory_span(
            provider_name="pinecone",
            store_id="store_user_prefs",
            store_name="user-preferences",
            query="laptop preferences",
            memory_type=MemoryType.LONG_TERM,
            similarity_threshold=0.7,
        ) as span:
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 5)
            time.sleep(0.05)  # Simulate fast query

        # Slow search - no threshold!
        print("\n  [SLOW] search_memory product-catalog (3800ms) ← BOTTLENECK")
        with span_builder.search_memory_span(
            provider_name="pinecone",
            store_id="store_product_catalog",
            store_name="product-catalog",
            query="laptops",
            memory_type=MemoryType.LONG_TERM,
            # BUG: No similarity_threshold!
        ) as span:
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 50000)
            time.sleep(0.1)  # Simulate slow query

        # LLM call (emits GenAI events)
        print(f"  [OK] chat {llm.model}")
        perf_result = llm.chat(
            tracer,
            messages=[{"role": "user", "content": perf_prompt}],
            system_prompt="You are a shopping assistant. Recommend concise options.",
            conversation_id=conversation_id,
            max_tokens=120,
            temperature=0.2,
            emit_events=True,
            evaluation_name="Relevance",
            evaluation_score_label="pass",
            evaluation_score_value=0.9,
            evaluation_explanation="Response addresses the user's laptop request and known preferences.",
        )
        if span_builder.capture_content:
            agent_span.set_attribute(
                "gen_ai.output.messages",
                json.dumps(
                    [{"role": "assistant", "parts": [{"type": "text", "content": perf_result.content}]}],
                    ensure_ascii=False,
                ),
            )

        # Store the conversation turn (typical workflow)
        with span_builder.update_memory_span(
            provider_name="redis",
            store_id="session-store",
            store_name="session-store",
            memory_id=f"turn_{conversation_id}_001",
            memory_type=MemoryType.SHORT_TERM,
            conversation_id=conversation_id,
        ):
            time.sleep(0.02)

    print_trace_tree("Trace Analysis:", """
invoke_agent shopping_assistant (total: 5200ms)
│
├── search_memory user-preferences (850ms) ← Normal
│   └── gen_ai.memory.search.result.count: 5
│
├── search_memory product-catalog (3800ms) ← SLOW!
│   ├── gen_ai.memory.search.result.count: 50000 ← Too many!
│   └── gen_ai.memory.search.similarity.threshold: (not set) ← Missing!
│
├── chat gpt-4 (450ms) ← Normal
│
└── update_memory conversation (100ms) ← Normal
""")

    print("""
Root Cause Analysis:
  - product-catalog search took 3.8s (73% of total time)
  - search.result.count: 50000 (no filtering applied)
  - similarity.threshold: NOT SET (should be 0.7+)

Fix: Add similarity threshold and result limit
""")

    # Show the fix
    print("\n  [FIX] search_memory with threshold=0.8, limit results")
    with span_builder.search_memory_span(
        provider_name="pinecone",
        store_id="store_product_catalog",
        store_name="product-catalog",
        query="laptops",
        memory_type=MemoryType.LONG_TERM,
        similarity_threshold=0.8,
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 25)

    print("  After fix: search.result.count = 25, latency ~200ms")


def run_compliance_audit_scenario():
    """Run all three compliance and debugging scenarios."""
    print_section("Story 5: Compliance Audit & Debugging")
    print("""
This story demonstrates WHY memory observability matters through
three real-world scenarios:

  A. Debugging Incorrect Agent Response
     - Why did the agent "forget" earlier context?

  B. Compliance Audit
     - Was user data accessed only by authorized agents?

  C. Performance Debugging
     - Why are agent responses slow?
""")

    # Setup tracing
    use_otlp = os.getenv("GENAI_MEMORY_USE_OTLP", "false").lower() == "true"
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="compliance-audit-demo",
        use_console=use_console,
        use_otlp=use_otlp,
        capture_content=capture_content,
    )
    span_builder = MemorySpanBuilder(tracer, capture_content=capture_content)

    llm = LLMClient()
    run_id = uuid.uuid4().hex[:8]
    with tracer.start_as_current_span(
        f"story_5.compliance_audit.{run_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            "story.id": 5,
            "story.title": "Compliance Audit & Debugging",
            "scenario.name": "debugging_audit_performance",
            "story.run_id": run_id,
        },
    ):
        with tracer.start_as_current_span("scenario_a.debugging_incorrect_response", kind=SpanKind.INTERNAL):
            scenario_a_debugging_incorrect_response(tracer, span_builder, llm=llm)
        with tracer.start_as_current_span("scenario_b.compliance_audit", kind=SpanKind.INTERNAL):
            scenario_b_compliance_audit(tracer, span_builder)
        with tracer.start_as_current_span("scenario_c.performance_debugging", kind=SpanKind.INTERNAL):
            scenario_c_performance_debugging(tracer, span_builder, llm=llm)

    # Summary
    print_section("Scenario Complete!")
    print("""
Key Observability Attributes for Debugging:

| Attribute | Use Case |
|-----------|----------|
| conversation.id | Link all operations in a session |
| agent.id | Identify which agent performed operation |
| search.result.count | Detect empty/excessive results |
| search.similarity.threshold | Verify filtering configuration |
| memory.namespace | Audit data access scope |
| span duration | Performance analysis |

Best Practices:
  1. Always set conversation.id for session linking
  2. Always set agent.id for attribution
  3. Log search.result.count for debugging
  4. Use similarity.threshold to control result quality
  5. Monitor span durations for performance issues
""")

    if use_otlp:
        print("Traces exported to OTLP collector.")
    else:
        print("Tip: Set GENAI_MEMORY_USE_OTLP=true to export to a collector.")


if __name__ == "__main__":
    run_compliance_audit_scenario()
