#!/usr/bin/env python3
"""
Story 2: Personal Shopping Assistant (LangChain Implementation)

This shows how the shopping assistant scenario maps to LangChain memory patterns
with emphasis on:
- EntityMemory: Maps to user-scoped, long_term memory with importance scoring
- ConversationSummaryMemory: Maps to merge update strategy

LangChain Memory Classes Used:
- EntityMemory: Long-term user preferences with entity extraction
- ConversationSummaryMemory: Summarized context with merge strategy

Key Mappings:
| LangChain Class            | gen_ai.operation.name | Key Attributes                    |
|----------------------------|----------------------|-----------------------------------|
| EntityMemory.save_context  | update_memory        | scope: user, importance: 0.9      |
| EntityMemory.load_memory   | search_memory        | type: long_term, similarity: 0.75 |
| ConversationSummaryMemory  | update_memory        | strategy: merge                   |

Run with:
    pip install langchain langchain-openai opentelemetry-api
    python langchain.py
"""

import os
import sys
import uuid
from typing import Dict, Any, List

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core', 'python'))

from opentelemetry import trace
from opentelemetry.trace import SpanKind

from genai_memory_otel import (
    setup_tracing,
    MemoryType,
    MemoryScope,
    MemoryUpdateStrategy,
    MemoryAttributes,
    GenAIAttributes,
)


class InstrumentedEntityMemory:
    """
    Wrapper around LangChain's EntityMemory showing how OTel instrumentation
    would capture memory operations for user preferences.

    EntityMemory extracts and stores information about entities (users, products, etc.)
    from conversations. This maps well to user-scoped, long-term memory.

    Maps to:
    - save_context() -> update_memory with importance scoring
    - load_memory_variables() -> search_memory with entity lookup
    """

    def __init__(
        self,
        tracer: trace.Tracer,
        *,
        store_name: str,
        user_id: str,
        capture_content: bool = False,
    ):
        self.tracer = tracer
        self.store_name = store_name
        self.store_id = f"store_{user_id}_preferences"
        self.user_id = user_id
        self.capture_content = capture_content
        self._entities: Dict[str, Dict[str, Any]] = {}
        self._memory_counter = 0

    def save_context(
        self,
        inputs: Dict[str, str],
        outputs: Dict[str, str],
        *,
        entities: List[str],
        importance: float = 0.8,
    ) -> None:
        """
        Save entity information extracted from conversation.

        LangChain: memory.save_context(inputs, outputs)
        OTel Span: update_memory with user scope, long_term type, importance

        The importance score indicates how critical this preference is:
        - 0.9+: Core preferences (allergies, dietary restrictions)
        - 0.7-0.9: Strong preferences (favorite brands, styles)
        - 0.5-0.7: Casual mentions (one-time interests)
        """
        self._memory_counter += 1
        memory_id = f"entity_{self.user_id}_{self._memory_counter:03d}"

        with self.tracer.start_as_current_span(
            f"update_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "update_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.MEMORY_ID: memory_id,
                MemoryAttributes.SCOPE: MemoryScope.USER,
                MemoryAttributes.TYPE: MemoryType.LONG_TERM,
                MemoryAttributes.NAMESPACE: self.user_id,
                MemoryAttributes.IMPORTANCE: importance,
            },
        ) as span:
            # Store entities
            for entity in entities:
                if entity not in self._entities:
                    self._entities[entity] = {
                        "mentions": [],
                        "importance": importance,
                    }
                self._entities[entity]["mentions"].append({
                    "input": inputs.get("input", ""),
                    "output": outputs.get("output", ""),
                })
                # Update importance to max seen
                self._entities[entity]["importance"] = max(
                    self._entities[entity]["importance"],
                    importance,
                )

            if self.capture_content:
                span.set_attribute(
                    MemoryAttributes.CONTENT,
                    f"entities: {entities}",
                )

    def load_memory_variables(
        self,
        inputs: Dict[str, Any],
        *,
        similarity_threshold: float = 0.75,
    ) -> Dict[str, Any]:
        """
        Load relevant entity information for the current context.

        LangChain: memory.load_memory_variables({"input": "..."})
        OTel Span: search_memory with similarity threshold
        """
        query = inputs.get("input", inputs.get("prompt", ""))

        with self.tracer.start_as_current_span(
            f"search_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "search_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.SCOPE: MemoryScope.USER,
                MemoryAttributes.TYPE: MemoryType.LONG_TERM,
                MemoryAttributes.NAMESPACE: self.user_id,
                MemoryAttributes.SEARCH_SIMILARITY_THRESHOLD: similarity_threshold,
            },
        ) as span:
            if self.capture_content and query:
                span.set_attribute(MemoryAttributes.QUERY, query)

            # Return all entities (in real implementation, would filter by relevance)
            results = [
                {"entity": k, "importance": v["importance"]}
                for k, v in self._entities.items()
            ]
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, len(results))

            return {"entities": results, "entity_store": self._entities}

    def delete_user_data(self) -> None:
        """
        Delete all user data (GDPR compliance).

        LangChain: memory.clear() or custom deletion
        OTel Span: delete_memory with user scope
        """
        with self.tracer.start_as_current_span(
            f"delete_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "delete_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.SCOPE: MemoryScope.USER,
                MemoryAttributes.NAMESPACE: self.user_id,
            },
        ):
            self._entities.clear()


class InstrumentedConversationSummaryMemory:
    """
    Wrapper around LangChain's ConversationSummaryMemory showing how
    OTel instrumentation captures the merge update strategy.

    ConversationSummaryMemory summarizes conversations rather than storing
    verbatim. This maps to update_memory with strategy="merge".

    Maps to:
    - save_context() -> update_memory with merge strategy
    - load_memory_variables() -> search_memory
    """

    def __init__(
        self,
        tracer: trace.Tracer,
        *,
        store_name: str,
        session_id: str,
        capture_content: bool = False,
    ):
        self.tracer = tracer
        self.store_name = store_name
        self.store_id = f"store_{session_id}_summary"
        self.session_id = session_id
        self.capture_content = capture_content
        self._summary = ""
        self._memory_counter = 0

    def save_context(
        self,
        inputs: Dict[str, str],
        outputs: Dict[str, str],
    ) -> None:
        """
        Save context by merging with existing summary.

        LangChain: memory.save_context(inputs, outputs)
        OTel Span: update_memory with merge strategy

        The merge strategy indicates that new information is combined with
        existing memory rather than replacing it.
        """
        self._memory_counter += 1
        memory_id = f"summary_{self.session_id}_{self._memory_counter:03d}"

        with self.tracer.start_as_current_span(
            f"update_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "update_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.MEMORY_ID: memory_id,
                MemoryAttributes.SCOPE: MemoryScope.SESSION,
                MemoryAttributes.TYPE: MemoryType.SHORT_TERM,
                MemoryAttributes.UPDATE_STRATEGY: MemoryUpdateStrategy.MERGE,
            },
        ) as span:
            # Merge new turn into summary
            new_content = f"User: {inputs.get('input', '')} -> Assistant: {outputs.get('output', '')}"
            if self._summary:
                self._summary = f"{self._summary} | {new_content}"
            else:
                self._summary = new_content

            if self.capture_content:
                span.set_attribute(MemoryAttributes.CONTENT, self._summary[:500])

    def load_memory_variables(self, inputs: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Load the current summary.

        OTel Span: search_memory
        """
        with self.tracer.start_as_current_span(
            f"search_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "search_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.SCOPE: MemoryScope.SESSION,
                MemoryAttributes.TYPE: MemoryType.SHORT_TERM,
            },
        ) as span:
            result_count = 1 if self._summary else 0
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, result_count)
            return {"summary": self._summary}


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def run_shopping_assistant_scenario():
    """
    Run the shopping assistant scenario using LangChain-style memory.
    """
    print_section("Story 2: Personal Shopping Assistant (LangChain Style)")
    print("""
This example shows how LangChain memory classes map to our semantic conventions
with emphasis on:
- EntityMemory -> importance scoring for user preferences
- ConversationSummaryMemory -> merge update strategy

Key insight: LangChain's EntityMemory perfectly demonstrates why we need
gen_ai.memory.importance - some preferences are critical (allergies: 0.95)
while others are casual mentions (color preference: 0.6).
""")

    # Setup tracing
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="shopping-assistant-langchain",
        use_console=use_console,
        capture_content=capture_content,
    )

    # Session parameters
    user_id = "user_alex_456"
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    conversation_id = f"conv_{session_id}"

    print(f"\nSession Info:")
    print(f"  User ID: {user_id}")
    print(f"  Session ID: {session_id}")

    # Initialize memories
    entity_memory = InstrumentedEntityMemory(
        tracer,
        store_name="user-preferences",
        user_id=user_id,
        capture_content=capture_content,
    )

    summary_memory = InstrumentedConversationSummaryMemory(
        tracer,
        store_name="conversation-summary",
        session_id=session_id,
        capture_content=capture_content,
    )

    # Start agent invocation
    with tracer.start_as_current_span(
        "invoke_agent ShoppingAssistant",
        kind=SpanKind.CLIENT,
        attributes={
            GenAIAttributes.OPERATION_NAME: "invoke_agent",
            GenAIAttributes.PROVIDER_NAME: "langchain",
            GenAIAttributes.AGENT_NAME: "ShoppingAssistant",
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ):
        # Step 1: User mentions dietary restriction (high importance)
        print_section("Step 1: Store Dietary Restriction (EntityMemory, importance=0.95)")
        entity_memory.save_context(
            {"input": "I'm allergic to nuts"},
            {"output": "I've noted your nut allergy. I'll exclude all products with nuts."},
            entities=["nut_allergy", "dietary_restrictions"],
            importance=0.95,  # Critical - safety concern
        )
        print("  User: I'm allergic to nuts")
        print("  Stored with importance=0.95 (critical safety preference)")

        # Step 2: User mentions brand preference (medium importance)
        print_section("Step 2: Store Brand Preference (EntityMemory, importance=0.75)")
        entity_memory.save_context(
            {"input": "I prefer organic products"},
            {"output": "Great! I'll prioritize organic options for you."},
            entities=["organic_preference", "brand_preferences"],
            importance=0.75,  # Strong preference
        )
        print("  User: I prefer organic products")
        print("  Stored with importance=0.75 (strong preference)")

        # Step 3: Conversation summary with merge
        print_section("Step 3: Summary Update (ConversationSummaryMemory, strategy=merge)")
        summary_memory.save_context(
            {"input": "Show me healthy snack options"},
            {"output": "Here are organic, nut-free snack options..."},
        )
        print("  First turn merged into summary")

        summary_memory.save_context(
            {"input": "What about protein bars?"},
            {"output": "I found several nut-free protein bars..."},
        )
        print("  Second turn merged into existing summary")

        # Step 4: Search preferences for recommendation
        print_section("Step 4: Search User Preferences (EntityMemory.load_memory_variables)")
        prefs = entity_memory.load_memory_variables(
            {"input": "recommend a snack"},
            similarity_threshold=0.75,
        )
        print(f"  Found {len(prefs['entities'])} relevant preferences:")
        for pref in prefs["entities"]:
            print(f"    - {pref['entity']} (importance: {pref['importance']})")

        # Step 5: Load conversation summary
        print_section("Step 5: Load Conversation Summary")
        summary = summary_memory.load_memory_variables({})
        print(f"  Summary: {summary['summary'][:100]}...")

        # Step 6: GDPR deletion
        print_section("Step 6: GDPR Deletion Request")
        entity_memory.delete_user_data()
        print("  All user preference data deleted")

    # Summary
    print_section("LangChain Memory Mapping Summary")
    print("""
| LangChain Pattern                | OTel Mapping                                    |
|----------------------------------|------------------------------------------------|
| EntityMemory.save_context()      | update_memory with gen_ai.memory.importance    |
| - Safety preferences             | importance: 0.95 (allergies, restrictions)     |
| - Strong preferences             | importance: 0.75 (brands, categories)          |
| - Casual mentions                | importance: 0.5 (one-time interests)           |
| ConversationSummaryMemory        | update_memory with strategy: merge             |
| Entity/preference deletion       | delete_memory with scope: user                 |

Key Insight: The gen_ai.memory.importance attribute is essential for observability
because it helps debug why certain preferences are prioritized (safety-critical
vs casual). This is unique to AI memory - databases don't track semantic importance.
""")


if __name__ == "__main__":
    run_shopping_assistant_scenario()
