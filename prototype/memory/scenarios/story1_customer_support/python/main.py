#!/usr/bin/env python3
"""
Story 1: Customer Support Agent with Memory

This scenario demonstrates a customer support agent that:
1. Creates a session-scoped memory store for conversation context
2. Searches user's past interactions (long_term, user-history store)
3. Stores conversation turns with 24h expiration (short_term, session scope)
4. Cleans up session memory on end

Key Attributes Demonstrated:
- gen_ai.memory.scope: session
- gen_ai.memory.type: short_term, long_term
- gen_ai.memory.expiration_date: 24h from now
- gen_ai.memory.search.similarity.threshold: 0.7
- gen_ai.conversation.id: links all operations

Memory Spans Used:
- create_memory_store: Session store initialization
- search_memory: User history retrieval
- update_memory: Store conversation turns
- delete_memory: Session cleanup

Run with:
    python main.py

To export to OTLP:
    GENAI_MEMORY_USE_OTLP=true python main.py
"""

import os
import json
import sys
import uuid
from datetime import datetime, timedelta, timezone

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core', 'python'))

from opentelemetry import trace
from opentelemetry.trace import SpanKind

from genai_memory_otel import (
    setup_tracing,
    MemorySpanBuilder,
    MemoryType,
    MemoryScope,
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


def generate_llm_response(tracer, *, conversation_id: str, prompt: str, context: str) -> str:
    """Call a real LLM when configured (falls back to mock)."""
    llm = LLMClient()
    system_prompt = (
        "You are a helpful customer support agent. Use any provided context. "
        "Be concise and actionable."
    )
    user_content = f"Context:\n{context}\n\nUser:\n{prompt}"
    result = llm.chat(
        tracer,
        messages=[{"role": "user", "content": user_content}],
        system_prompt=system_prompt,
        conversation_id=conversation_id,
        max_tokens=180,
        temperature=0.2,
        emit_events=True,
    )
    return result.content


def run_customer_support_scenario():
    """
    Run the customer support agent scenario.

    Story: Sarah contacts TechCorp support about a billing issue.
    The agent maintains session context and retrieves relevant history.
    """
    print_section("Story 1: Customer Support Agent")
    print("""
Scenario: Sarah contacts TechCorp support about a billing issue.
She was charged twice for her monthly subscription.

The support agent:
1. Creates a session memory store
2. Retrieves Sarah's past interactions
3. Stores each conversation turn with 24h expiration
4. Cleans up session memory when done
""")

    # Setup tracing
    use_otlp = os.getenv("GENAI_MEMORY_USE_OTLP", "false").lower() == "true"
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="customer-support-agent",
        use_console=use_console,
        use_otlp=use_otlp,
        capture_content=capture_content,
    )
    span_builder = MemorySpanBuilder(tracer, capture_content=capture_content)

    # Session parameters
    user_id = "user_sarah_123"
    session_short_id = uuid.uuid4().hex[:8]
    session_id = f"session_{session_short_id}"
    conversation_id = f"conv_{session_id}"
    agent_id = "support_agent_001"
    session_store_name = f"customer-session-{session_short_id}"

    print(f"\nSession Info:")
    print(f"  User ID: {user_id}")
    print(f"  Session ID: {session_id}")
    print(f"  Conversation ID: {conversation_id}")
    print(f"  Agent ID: {agent_id}")

    # Start the agent invocation
    llm = LLMClient()
    agent_provider = llm.provider_name()

    with tracer.start_as_current_span(
        f"story_1.customer_support.{conversation_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            "story.id": 1,
            "story.title": "Customer Support Agent with Memory",
            "scenario.name": "billing_duplicate_charge",
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ):
        with tracer.start_as_current_span(
            "invoke_agent CustomerSupportBot",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "invoke_agent",
                GenAIAttributes.PROVIDER_NAME: agent_provider,
                GenAIAttributes.REQUEST_MODEL: llm.model,
                "server.address": "api.openai.com",
                GenAIAttributes.AGENT_NAME: "CustomerSupportBot",
                GenAIAttributes.AGENT_ID: agent_id,
                GenAIAttributes.CONVERSATION_ID: conversation_id,
            },
        ) as agent_span:

            # 1. Create session-scoped memory store
            print_section("Step 1: Create Session Memory Store")
            session_store_id = f"store_{session_id}"

            with span_builder.create_memory_store_span(
                provider_name="chroma",
                store_name=session_store_name,
                scope=MemoryScope.SESSION,
                memory_type=MemoryType.SHORT_TERM,
            ) as span:
                span.set_attribute(MemoryAttributes.STORE_ID, session_store_id)
                span.set_attribute(GenAIAttributes.CONVERSATION_ID, conversation_id)
                print_span_info("create_memory_store", {
                    "gen_ai.operation.name": "create_memory_store",
                    "gen_ai.provider.name": "chroma",
                    "gen_ai.memory.store.name": session_store_name,
                    "gen_ai.memory.store.id": session_store_id,
                    "gen_ai.memory.scope": MemoryScope.SESSION,
                    "gen_ai.memory.type": MemoryType.SHORT_TERM,
                    "gen_ai.conversation.id": conversation_id,
                })

            # 2. Search user's past interactions (long-term user history)
            print_section("Step 2: Search User History")
            user_history_store_id = f"store_{user_id}_history"

            with span_builder.search_memory_span(
                provider_name="pinecone",
                store_id=user_history_store_id,
                store_name="user-history",
                query="billing issue duplicate charge",
                memory_type=MemoryType.LONG_TERM,
                similarity_threshold=0.7,
                agent_id=agent_id,
                conversation_id=conversation_id,
            ) as span:
                # Simulate finding 3 relevant past interactions
                span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 3)
                print_span_info("search_memory (user history)", {
                    "gen_ai.operation.name": "search_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": user_history_store_id,
                    "gen_ai.memory.store.name": "user-history",
                    "gen_ai.memory.query": "billing issue duplicate charge" if capture_content else "(opt-in disabled)",
                    "gen_ai.memory.type": MemoryType.LONG_TERM,
                    "gen_ai.memory.search.similarity.threshold": 0.7,
                    "gen_ai.memory.search.result.count": 3,
                    "gen_ai.agent.id": agent_id,
                    "gen_ai.conversation.id": conversation_id,
                })

            print("\n  Found: 3 relevant past interactions")
            print("    - Previous billing issue (3 months ago, refund issued)")
            print("    - Account upgrade request (6 months ago)")
            print("    - General inquiry (1 year ago)")

            # 3. Call LLM with context
            print_section("Step 3: Generate Response")
            user_message = "I was charged twice for my subscription this month"
            response = generate_llm_response(
                tracer,
                conversation_id=conversation_id,
                prompt=user_message,
                context="billing history context",
            )
            print(f"\n  User: {user_message}")
            print(f"  Agent: {response}")

            if capture_content:
                agent_span.set_attribute(
                    "gen_ai.input.messages",
                    json.dumps(
                        [{"role": "user", "parts": [{"type": "text", "content": user_message}]}],
                        ensure_ascii=False,
                    ),
                )
                agent_span.set_attribute(
                    "gen_ai.output.messages",
                    json.dumps(
                        [{"role": "assistant", "parts": [{"type": "text", "content": response}]}],
                        ensure_ascii=False,
                    ),
                )

            # 4. Store conversation turn with expiration
            print_section("Step 4: Store Conversation Turn")
            turn_memory_id = f"turn_{conversation_id}_001"
            expiration = (
                (datetime.now(timezone.utc) + timedelta(hours=24))
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z")
            )

            with span_builder.update_memory_span(
                provider_name="chroma",
                store_id=session_store_id,
                store_name=session_store_name,
                memory_id=turn_memory_id,
                memory_type=MemoryType.SHORT_TERM,
                expiration_date=expiration,
                agent_id=agent_id,
                conversation_id=conversation_id,
            ) as span:
                print_span_info("update_memory (store turn)", {
                    "gen_ai.operation.name": "update_memory",
                    "gen_ai.provider.name": "chroma",
                    "gen_ai.memory.store.id": session_store_id,
                    "gen_ai.memory.id": turn_memory_id,
                    "gen_ai.memory.type": MemoryType.SHORT_TERM,
                    "gen_ai.memory.expiration_date": expiration,
                    "gen_ai.agent.id": agent_id,
                    "gen_ai.conversation.id": conversation_id,
                })

            # 5. Simulate second turn
            print_section("Step 5: Second Conversation Turn")
            user_message_2 = "Can you check my payment history?"

            # Search session context
            with span_builder.search_memory_span(
                provider_name="chroma",
                store_id=session_store_id,
                store_name=session_store_name,
                query=user_message_2,
                memory_type=MemoryType.SHORT_TERM,
                conversation_id=conversation_id,
            ) as span:
                span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 1)
                print_span_info("search_memory (session context)", {
                    "gen_ai.operation.name": "search_memory",
                    "gen_ai.provider.name": "chroma",
                    "gen_ai.memory.store.id": session_store_id,
                    "gen_ai.memory.type": MemoryType.SHORT_TERM,
                    "gen_ai.memory.search.result.count": 1,
                    "gen_ai.conversation.id": conversation_id,
                })

            response_2 = "Yes, I can see the duplicate charge. I'll process a refund immediately."
            print(f"\n  User: {user_message_2}")
            print(f"  Agent: {response_2}")

            # Store second turn
            turn_memory_id_2 = f"turn_{conversation_id}_002"
            with span_builder.update_memory_span(
                provider_name="chroma",
                store_id=session_store_id,
                store_name=session_store_name,
                memory_id=turn_memory_id_2,
                memory_type=MemoryType.SHORT_TERM,
                expiration_date=expiration,
                conversation_id=conversation_id,
            ):
                pass  # Span attributes set by builder

            # 6. Session cleanup (after resolution)
            print_section("Step 6: Session Cleanup")

            with span_builder.delete_memory_span(
                provider_name="chroma",
                store_id=session_store_id,
                store_name=session_store_name,
                scope=MemoryScope.SESSION,
                conversation_id=conversation_id,
            ) as span:
                print_span_info("delete_memory (session cleanup)", {
                    "gen_ai.operation.name": "delete_memory",
                    "gen_ai.provider.name": "chroma",
                    "gen_ai.memory.store.id": session_store_id,
                    "gen_ai.memory.scope": MemoryScope.SESSION,
                    "gen_ai.conversation.id": conversation_id,
                })

            # Set final agent span attributes
            agent_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 300)
            agent_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 100)

    # Summary
    print_section("Scenario Complete!")
    print("""
Trace Summary:
  - 1x create_memory_store (session store)
  - 2x search_memory (user history + session context)
  - 2x update_memory (conversation turns with expiration)
  - 1x delete_memory (session cleanup)
  - 1x chat (LLM call)

Key Observability Insights:
  - Session memory has 24h expiration for automatic cleanup
  - User history search shows past billing issue (similarity: 0.7+)
  - All operations linked by conversation_id for debugging
""")

    if use_otlp:
        print("Traces exported to OTLP collector.")
    else:
        print("Tip: Set GENAI_MEMORY_USE_OTLP=true to export to a collector.")


if __name__ == "__main__":
    run_customer_support_scenario()
