#!/usr/bin/env python3
"""
Story 2: Personal Shopping Assistant

This scenario demonstrates a shopping assistant that learns user preferences:
0. Creates a user-scoped memory store for preferences
1. Stores initial preferences with high importance
2. Merges new preferences using update.strategy="merge"
3. Searches preferences with similarity threshold for recommendations
4. Handles GDPR deletion requests (delete all user data)

Key Attributes Demonstrated:
- gen_ai.memory.scope: user (on create_memory_store, delete_memory)
- gen_ai.memory.type: long_term
- gen_ai.memory.importance: 0.9, 0.75, etc.
- gen_ai.memory.update.strategy: merge
- gen_ai.memory.content: (opt-in) preference data

Memory Spans Used:
- create_memory_store: Provision preferences store
- update_memory: Store/merge preferences
- search_memory: Retrieve preferences for recommendations
- delete_memory: GDPR data deletion

Run with:
    python main.py

To export to OTLP:
    GENAI_MEMORY_USE_OTLP=true python main.py
"""

import os
import json
import sys
import uuid

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core', 'python'))

from opentelemetry import trace
from opentelemetry.trace import SpanKind

from genai_memory_otel import (
    setup_tracing,
    MemorySpanBuilder,
    MemoryType,
    MemoryScope,
    MemoryUpdateStrategy,
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


def generate_recommendation(tracer, *, conversation_id: str, query: str, preferences_summary: str) -> str:
    """Call a real LLM when configured (falls back to mock)."""
    llm = LLMClient()
    system_prompt = "You are a personal shopping assistant. Recommend concise options and explain briefly."
    user_content = f"User query: {query}\n\nKnown preferences:\n{preferences_summary}"
    result = llm.chat(
        tracer,
        messages=[{"role": "user", "content": user_content}],
        system_prompt=system_prompt,
        conversation_id=conversation_id,
        max_tokens=200,
        temperature=0.4,
        emit_events=True,
    )
    return result.content


def run_shopping_assistant_scenario():
    """
    Run the personal shopping assistant scenario.

    Story: Mike uses ShopSmart, an AI shopping assistant that learns
    his preferences over time and provides personalized recommendations.
    """
    print_section("Story 2: Personal Shopping Assistant")
    print("""
Scenario: Mike is a ShopSmart user. Over several weeks, the assistant
learns his preferences:

1. Onboarding: Mike mentions he prefers sustainable products (explicit, high importance)
2. Learning: Browsing reveals he likes minimalist designs (inferred, medium importance)
3. Shopping: Mike asks for laptop recommendations - assistant uses preferences
4. Update: Mike says "I no longer care about sustainability" - preferences updated
5. GDPR: Mike requests deletion of all his preference data
""")

    # Setup tracing
    use_otlp = os.getenv("GENAI_MEMORY_USE_OTLP", "false").lower() == "true"
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="shopping-assistant",
        use_console=use_console,
        use_otlp=use_otlp,
        capture_content=capture_content,
    )
    span_builder = MemorySpanBuilder(tracer, capture_content=capture_content)

    # User parameters
    user_id = "user_mike_456"
    preferences_store_id = f"store_{user_id}_prefs"
    agent_id = "shopping_agent_001"
    conversation_id = f"conv_shop_{uuid.uuid4().hex[:8]}"

    print(f"\nUser Info:")
    print(f"  User ID: {user_id}")
    print(f"  Preferences Store: {preferences_store_id}")
    print(f"  Content Capture: {capture_content}")
    print(f"  Conversation ID: {conversation_id}")

    # Start the agent invocation
    llm = LLMClient()
    agent_provider = llm.provider_name()

    with tracer.start_as_current_span(
        f"story_2.shopping_assistant.{conversation_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            "story.id": 2,
            "story.title": "Personal Shopping Assistant",
            "scenario.name": "preferences_learning_and_gdpr",
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ):
        with tracer.start_as_current_span(
            "invoke_agent ShopSmartAssistant",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "invoke_agent",
                GenAIAttributes.PROVIDER_NAME: agent_provider,
                GenAIAttributes.REQUEST_MODEL: llm.model,
                "server.address": "api.openai.com",
                GenAIAttributes.AGENT_NAME: "ShopSmartAssistant",
                GenAIAttributes.AGENT_ID: agent_id,
                GenAIAttributes.CONVERSATION_ID: conversation_id,
            },
        ) as agent_span:

            # 1. Create user-scoped preferences store
            print_section("Step 1: Create Preferences Memory Store")

            with span_builder.create_memory_store_span(
                provider_name="pinecone",
                store_name="user-preferences",
                scope=MemoryScope.USER,
                memory_type=MemoryType.LONG_TERM,
            ) as span:
                span.set_attribute(MemoryAttributes.STORE_ID, preferences_store_id)
                print_span_info("create_memory_store (user preferences)", {
                    "gen_ai.operation.name": "create_memory_store",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.name": "user-preferences",
                    "gen_ai.memory.store.id": preferences_store_id,
                    "gen_ai.memory.scope": MemoryScope.USER,
                    "gen_ai.memory.type": MemoryType.LONG_TERM,
                })

            # 2. Store initial preference (high importance - explicit)
            print_section("Step 2: Store Initial Preference (Explicit)")
            print("\n  Mike: 'I prefer to buy sustainable products'")

            pref_id_1 = f"pref_{uuid.uuid4().hex[:12]}"
            content_1 = '{"preference": "sustainable_products", "source": "explicit"}'

            with span_builder.update_memory_span(
                provider_name="pinecone",
                store_id=preferences_store_id,
                store_name="user-preferences",
                memory_id=pref_id_1,
                memory_type=MemoryType.LONG_TERM,
                importance=0.9,
                content=content_1 if capture_content else None,
            ) as span:
                print_span_info("update_memory (explicit preference)", {
                    "gen_ai.operation.name": "update_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": preferences_store_id,
                    "gen_ai.memory.id": pref_id_1,
                    "gen_ai.memory.type": MemoryType.LONG_TERM,
                    "gen_ai.memory.importance": 0.9,
                    "gen_ai.memory.content": content_1 if capture_content else "(opt-in disabled)",
                })

            # 3. Learn and merge new preference (medium importance - inferred)
            print_section("Step 3: Learn Preference from Behavior")
            print("\n  [Analyzing browsing behavior...]")
            print("  Inferred: Mike prefers minimalist designs")

            pref_id_2 = f"pref_{uuid.uuid4().hex[:12]}"
            content_2 = '{"preference": "minimalist_design", "source": "behavior"}'

            with span_builder.update_memory_span(
                provider_name="pinecone",
                store_id=preferences_store_id,
                store_name="user-preferences",
                memory_id=pref_id_2,
                memory_type=MemoryType.LONG_TERM,
                update_strategy=MemoryUpdateStrategy.MERGE,
                importance=0.75,
                content=content_2 if capture_content else None,
            ) as span:
                print_span_info("update_memory (merge inferred preference)", {
                    "gen_ai.operation.name": "update_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": preferences_store_id,
                    "gen_ai.memory.id": pref_id_2,
                    "gen_ai.memory.type": MemoryType.LONG_TERM,
                    "gen_ai.memory.update.strategy": MemoryUpdateStrategy.MERGE,
                    "gen_ai.memory.importance": 0.75,
                })

            # 4. Search preferences for recommendations
            print_section("Step 4: Get Recommendations Using Preferences")
            print("\n  Mike: 'Can you recommend a laptop?'")

            with span_builder.search_memory_span(
                provider_name="pinecone",
                store_id=preferences_store_id,
                store_name="user-preferences",
                query="laptop recommendations criteria",
                memory_type=MemoryType.LONG_TERM,
                similarity_threshold=0.6,
            ) as span:
                span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 5)
                print_span_info("search_memory (get preferences)", {
                    "gen_ai.operation.name": "search_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": preferences_store_id,
                    "gen_ai.memory.query": "laptop recommendations criteria" if capture_content else "(opt-in disabled)",
                    "gen_ai.memory.type": MemoryType.LONG_TERM,
                    "gen_ai.memory.search.similarity.threshold": 0.6,
                    "gen_ai.memory.search.result.count": 5,
                })

            print("\n  Found preferences:")
            print("    - sustainable_products (importance: 0.9)")
            print("    - minimalist_design (importance: 0.75)")

            # Generate recommendation
            preferences_summary = "- sustainable_products (importance: 0.9)\n- minimalist_design (importance: 0.75)"
            recommendation_query = "Can you recommend a laptop?"
            response = generate_recommendation(
                tracer,
                conversation_id=conversation_id,
                query=recommendation_query,
                preferences_summary=preferences_summary,
            )
            print(f"\n  Assistant: {response}")

            if capture_content:
                agent_span.set_attribute(
                    "gen_ai.input.messages",
                    json.dumps(
                        [{"role": "user", "parts": [{"type": "text", "content": recommendation_query}]}],
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

            # 5. Update preference (user explicitly changes mind)
            print_section("Step 5: Update Preference (User Changes Mind)")
            print("\n  Mike: 'Actually, I no longer care about sustainability'")

            with span_builder.update_memory_span(
                provider_name="pinecone",
                store_id=preferences_store_id,
                memory_id=pref_id_1,
                memory_type=MemoryType.LONG_TERM,
                update_strategy=MemoryUpdateStrategy.MERGE,
                importance=0.1,  # Dramatically reduced importance
                content='{"preference": "sustainable_products", "active": false}' if capture_content else None,
            ) as span:
                print_span_info("update_memory (reduce importance)", {
                    "gen_ai.operation.name": "update_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": preferences_store_id,
                    "gen_ai.memory.id": pref_id_1,
                    "gen_ai.memory.update.strategy": MemoryUpdateStrategy.MERGE,
                    "gen_ai.memory.importance": 0.1,
                })

            print("\n  Preference 'sustainable_products' importance reduced: 0.9 -> 0.1")

            # 6. GDPR Deletion Request
            print_section("Step 6: GDPR Data Deletion Request")
            print("\n  Mike: 'Please delete all my preference data'")

            with span_builder.delete_memory_span(
                provider_name="pinecone",
                store_id=preferences_store_id,
                store_name="user-preferences",
                scope=MemoryScope.USER,
            ) as span:
                print_span_info("delete_memory (GDPR deletion)", {
                    "gen_ai.operation.name": "delete_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": preferences_store_id,
                    "gen_ai.memory.store.name": "user-preferences",
                    "gen_ai.memory.scope": MemoryScope.USER,
                })

            print("\n  All user preferences deleted for GDPR compliance")

            # Set final agent span attributes
            agent_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 400)
            agent_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 150)

    # Summary
    print_section("Scenario Complete!")
    print("""
Trace Summary:
  - 1x create_memory_store (user preferences store)
  - 3x update_memory (initial preference, merge behavior, update importance)
  - 1x search_memory (retrieve for recommendations)
  - 1x delete_memory (GDPR deletion)
  - 1x chat (LLM recommendation)

Key Observability Insights:
  - Explicit preferences have higher importance (0.9) than inferred (0.75)
  - Merge strategy combines new data with existing preferences
  - GDPR deletion traced with user scope for audit compliance
  - Content capture is opt-in to protect user privacy
""")

    if use_otlp:
        print("Traces exported to OTLP collector.")
    else:
        print("Tip: Set GENAI_MEMORY_USE_OTLP=true to export to a collector.")
        print("     Set GENAI_MEMORY_CAPTURE_CONTENT=true to include preference content.")


if __name__ == "__main__":
    run_shopping_assistant_scenario()
