#!/usr/bin/env python3
"""
Customer Support Agent with Memory - End-to-End Trace Example

This scenario demonstrates a complete agent workflow with memory operations,
producing OpenTelemetry traces that follow the GenAI Memory semantic conventions.

Note: `store_memory` is removed from the spec; `update_memory` is now an upsert
operation used for both creating and updating memories.

The scenario simulates:
1. Creating a memory store for user history
2. Loading user history (search_memory)
3. Making an LLM call with memory context
4. Storing the conversation turn (update_memory - upsert)
5. Updating user preferences (update_memory - upsert)

Expected trace hierarchy:
    invoke_agent CustomerSupportBot
    ├── search_memory user_history_store
    ├── chat gpt-4 (simulated)
    ├── update_memory user_history_store (upsert)
    └── update_memory user_preferences (upsert)

Run with:
    python main.py

To use OTLP exporter (requires collector):
    GENAI_MEMORY_USE_OTLP=true python main.py
"""

import os
import sys
import uuid
from datetime import datetime

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core', 'python'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'providers', 'chroma', 'python'))

from opentelemetry import trace
from opentelemetry.trace import SpanKind

from genai_memory_otel import (
    setup_tracing,
    MemorySpanBuilder,
    MemoryType,
    MemoryScope,
    MemoryUpdateStrategy,
    GenAIAttributes,
    LLMClient,
)

# Use mock provider for demonstration (no dependencies)
from chroma_mock import MockChromaMemoryProvider


def generate_llm_response(tracer, *, conversation_id: str, prompt: str, memory_context: str) -> str:
    """Call a real LLM when configured (falls back to mock)."""
    llm = LLMClient()
    user_content = f"User request:\n{prompt}\n\nRelevant memory context:\n{memory_context}"
    result = llm.chat(
        tracer,
        messages=[{"role": "user", "content": user_content}],
        system_prompt="You are a helpful customer support agent. Be concise and actionable.",
        conversation_id=conversation_id,
        max_tokens=160,
        temperature=0.2,
        emit_events=True,
    )
    return result.content


def generate_embedding(text: str) -> list:
    """
    Generate a mock embedding for text.

    In a real implementation, this would call an embedding model.
    """
    # Simple hash-based mock embedding
    import hashlib
    hash_bytes = hashlib.sha256(text.encode()).digest()
    return [float(b) / 255.0 for b in hash_bytes] * 48  # 1536 dimensions


def run_customer_support_scenario():
    """
    Run a complete customer support agent scenario.

    This demonstrates the full memory operation flow with proper
    OpenTelemetry instrumentation.
    """
    print("=" * 70)
    print("Customer Support Agent with Memory - OpenTelemetry Demo")
    print("=" * 70)

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

    # Simulation parameters
    user_id = "user_12345"
    conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
    agent_id = "agent_support_001"

    print(f"\nUser ID: {user_id}")
    print(f"Conversation ID: {conversation_id}")
    print(f"Agent ID: {agent_id}")
    print(f"Capture Content: {capture_content}")

    llm = LLMClient()
    agent_provider = llm.provider_name()

    with tracer.start_as_current_span(
        f"demo_customer_support_agent.{conversation_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            "demo.id": "customer_support_agent",
            "demo.title": "Customer Support Agent with Memory - End-to-End Trace Example",
            GenAIAttributes.CONVERSATION_ID: conversation_id,
            "user.id": user_id,
        },
    ):
        # Create memory providers
        print("\n--- Initializing Memory Stores ---")

        user_history_store = MockChromaMemoryProvider(
            span_builder=span_builder,
            collection_name="user_history",
        )

        user_preferences_store = MockChromaMemoryProvider(
            span_builder=span_builder,
            collection_name="user_preferences",
        )

        # Pre-populate some user history
        print("\n--- Pre-populating User History ---")

        user_history_store.store_memory(
            memory_id="mem_hist_001",
            embedding=generate_embedding("previous support ticket about billing"),
            metadata={
                "user_id": user_id,
                "topic": "billing",
                "resolution": "refund_issued",
                "date": "2025-12-01",
            },
            memory_type=MemoryType.EPISODIC,
            scope=MemoryScope.USER,
            namespace=user_id,
            content="User had a billing issue, refund was issued" if capture_content else None,
        )

        user_preferences_store.store_memory(
            memory_id="mem_pref_001",
            embedding=generate_embedding("user prefers email communication"),
            metadata={
                "user_id": user_id,
                "preference_key": "communication_channel",
                "preference_value": "email",
            },
            memory_type=MemoryType.SEMANTIC,
            scope=MemoryScope.USER,
            namespace=user_id,
            content="User prefers email communication" if capture_content else None,
            importance=0.9,
        )

        # Start the agent invocation
        print("\n--- Starting Agent Invocation ---")
        print("User message: 'I need help with my recent order'")

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
            user_message = "I need help with my recent order"

            # Step 1: Search for user history
            print("\n  1. Searching user history...")
            history_results = user_history_store.search_memory(
                query_embedding=generate_embedding(user_message),
                top_k=5,
                similarity_threshold=0.3,
                namespace=user_id,
                query_text=user_message,
                memory_type=MemoryType.EPISODIC,
                agent_id=agent_id,
                conversation_id=conversation_id,
            )
            print(f"     Found {len(history_results)} relevant history items")

            # Step 2: Search for user preferences
            print("\n  2. Loading user preferences...")
            pref_results = user_preferences_store.search_memory(
                query_embedding=generate_embedding("user preferences"),
                top_k=3,
                namespace=user_id,
                memory_type=MemoryType.SEMANTIC,
            )
            print(f"     Found {len(pref_results)} user preferences")

            # Build context from memories
            memory_context = ""
            for mem in history_results:
                memory_context += f"Previous: {mem['metadata'].get('topic', 'interaction')}\n"
            for pref in pref_results:
                memory_context += (
                    f"Preference: {pref['metadata'].get('preference_key', '')}: "
                    f"{pref['metadata'].get('preference_value', '')}\n"
                )

            # Step 3: Call LLM with memory context
            print("\n  3. Calling LLM with memory context...")
            response = generate_llm_response(
                tracer,
                conversation_id=conversation_id,
                prompt=user_message,
                memory_context=memory_context,
            )
            print(f"     Response: {response[:50]}...")

            # Step 4: Store this conversation turn
            print("\n  4. Storing conversation turn...")
            turn_memory_id = f"mem_turn_{conversation_id}_1"
            user_history_store.store_memory(
                memory_id=turn_memory_id,
                embedding=generate_embedding(f"{user_message} {response}"),
                metadata={
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                    "turn": 1,
                    "user_message": user_message,
                    "agent_response": response[:100],
                    "timestamp": datetime.utcnow().isoformat(),
                },
                memory_type=MemoryType.EPISODIC,
                scope=MemoryScope.SESSION,
                namespace=user_id,
                content=f"User: {user_message}\nAgent: {response}" if capture_content else None,
                agent_id=agent_id,
                conversation_id=conversation_id,
            )
            print(f"     Stored as: {turn_memory_id}")

            # Step 5: Update user preferences (simulating learned preference)
            print("\n  5. Updating user preferences...")
            user_preferences_store.update_memory(
                memory_id="mem_pref_001",
                metadata={
                    "last_interaction": datetime.utcnow().isoformat(),
                    "interaction_count": 2,
                },
                update_strategy=MemoryUpdateStrategy.MERGE,
                namespace=user_id,
            )
            print("     Updated last interaction timestamp")

            # Set final agent span attributes
            agent_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 150)
            agent_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 50)

    print("\n" + "=" * 70)
    print("Scenario Complete!")
    print("=" * 70)
    print("\nTrace Summary:")
    print("  - 1x invoke_agent span (parent)")
    print("  - 3x search_memory spans (history + preferences)")
    print("  - 1x chat span (LLM call)")
    print("  - 3x update_memory spans (pre-populate + conversation + preference update)")
    print("    (Note: update_memory is now an upsert for both create and update)")
    print("\nCheck the console output above for detailed span attributes.")

    if use_otlp:
        print("\nSpans also exported to OTLP collector.")
    else:
        print("\nTip: Set GENAI_MEMORY_USE_OTLP=true to export to a collector.")


if __name__ == "__main__":
    run_customer_support_scenario()
