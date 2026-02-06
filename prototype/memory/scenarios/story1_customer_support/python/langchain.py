#!/usr/bin/env python3
"""
Story 1: Customer Support Agent with Memory (LangChain Implementation)

This shows how the same scenario from main.py maps to LangChain memory classes
and how our proposed semantic conventions would instrument them.

LangChain Memory Classes Used:
- ConversationBufferMemory: Maps to session-scoped, short_term memory
- VectorStoreRetrieverMemory: Maps to long_term memory with similarity search

Key Mappings:
| LangChain Class           | gen_ai.operation.name | gen_ai.memory.scope | gen_ai.memory.type |
|---------------------------|----------------------|---------------------|---------------------|
| ConversationBufferMemory  | update_memory        | session             | short_term          |
| ConversationBufferMemory  | search_memory        | session             | short_term          |
| VectorStoreRetrieverMemory| search_memory        | user                | long_term           |
| memory.clear()            | delete_memory        | session             | short_term          |

Run with:
    pip install langchain langchain-openai chromadb opentelemetry-api
    python langchain.py

Note: This example shows the INSTRUMENTATION pattern, not the full LangChain
integration. A production opentelemetry-instrumentation-langchain package would
automatically instrument these calls.
"""

import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core', 'python'))

from opentelemetry import trace
from opentelemetry.trace import SpanKind

# Import our OTel utilities
from genai_memory_otel import (
    setup_tracing,
    MemoryType,
    MemoryScope,
    MemoryAttributes,
    GenAIAttributes,
)

# LangChain imports (optional - we show the pattern even without langchain installed)
try:
    from langchain.memory import ConversationBufferMemory
    from langchain_community.vectorstores import Chroma
    from langchain.memory import VectorStoreRetrieverMemory
    from langchain_openai import OpenAIEmbeddings
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Note: LangChain not installed. Showing instrumentation pattern with mocks.")


class InstrumentedConversationBufferMemory:
    """
    Wrapper around LangChain's ConversationBufferMemory showing how
    OTel instrumentation would capture memory operations.

    Maps to:
    - save_context() -> update_memory span
    - load_memory_variables() -> search_memory span
    - clear() -> delete_memory span
    """

    def __init__(
        self,
        tracer: trace.Tracer,
        *,
        store_name: str,
        session_id: str,
        conversation_id: str,
        capture_content: bool = False,
    ):
        self.tracer = tracer
        self.store_name = store_name
        self.store_id = f"store_{session_id}"
        self.conversation_id = conversation_id
        self.capture_content = capture_content
        self._buffer: List[Dict[str, str]] = []

        # Real LangChain memory (if available)
        if LANGCHAIN_AVAILABLE:
            self._memory = ConversationBufferMemory(return_messages=True)
        else:
            self._memory = None

    def save_context(self, inputs: Dict[str, str], outputs: Dict[str, str]) -> None:
        """
        Save conversation turn to memory.

        LangChain: memory.save_context({"input": "..."}, {"output": "..."})
        OTel Span: update_memory with session scope, short_term type
        """
        memory_id = f"turn_{self.conversation_id}_{len(self._buffer):03d}"
        expiration = (
            (datetime.now(timezone.utc) + timedelta(hours=24))
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

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
                MemoryAttributes.EXPIRATION_DATE: expiration,
                GenAIAttributes.CONVERSATION_ID: self.conversation_id,
            },
        ) as span:
            # Add content if opt-in
            if self.capture_content:
                span.set_attribute(
                    MemoryAttributes.CONTENT,
                    f"input: {inputs.get('input', '')}, output: {outputs.get('output', '')}",
                )

            # Call real LangChain memory
            if self._memory:
                self._memory.save_context(inputs, outputs)

            # Store in buffer for mock
            self._buffer.append({"input": inputs, "output": outputs})

    def load_memory_variables(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Load conversation history from memory.

        LangChain: memory.load_memory_variables({})
        OTel Span: search_memory with session scope, short_term type
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
                GenAIAttributes.CONVERSATION_ID: self.conversation_id,
            },
        ) as span:
            # Get results
            if self._memory:
                result = self._memory.load_memory_variables(inputs or {})
                result_count = len(result.get("history", []))
            else:
                result = {"history": self._buffer}
                result_count = len(self._buffer)

            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, result_count)
            return result

    def clear(self) -> None:
        """
        Clear all memory (session cleanup).

        LangChain: memory.clear()
        OTel Span: delete_memory with session scope
        """
        with self.tracer.start_as_current_span(
            f"delete_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "delete_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.SCOPE: MemoryScope.SESSION,
                GenAIAttributes.CONVERSATION_ID: self.conversation_id,
            },
        ):
            if self._memory:
                self._memory.clear()
            self._buffer.clear()


class InstrumentedVectorStoreRetrieverMemory:
    """
    Wrapper around LangChain's VectorStoreRetrieverMemory showing how
    OTel instrumentation would capture memory operations.

    Maps to:
    - load_memory_variables() -> search_memory span with similarity threshold
    - save_context() -> update_memory span (when adding to vector store)

    This is typically used for long-term, user-scoped memory.
    """

    def __init__(
        self,
        tracer: trace.Tracer,
        *,
        store_name: str,
        user_id: str,
        similarity_threshold: float = 0.7,
        capture_content: bool = False,
    ):
        self.tracer = tracer
        self.store_name = store_name
        self.store_id = f"store_{user_id}_history"
        self.user_id = user_id
        self.similarity_threshold = similarity_threshold
        self.capture_content = capture_content
        self._mock_memories: List[Dict[str, Any]] = [
            {"content": "Previous billing issue - refund issued", "score": 0.85},
            {"content": "Account upgrade request", "score": 0.72},
            {"content": "General inquiry", "score": 0.65},
        ]

    def load_memory_variables(
        self,
        inputs: Dict[str, Any],
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search vector store for relevant memories.

        LangChain: memory.load_memory_variables({"prompt": "billing issue"})
        OTel Span: search_memory with similarity threshold
        """
        query = inputs.get("prompt", inputs.get("input", ""))

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
                MemoryAttributes.SEARCH_SIMILARITY_THRESHOLD: self.similarity_threshold,
            },
        ) as span:
            # Add query if opt-in
            if self.capture_content and query:
                span.set_attribute(MemoryAttributes.QUERY, query)

            # Filter by similarity threshold
            results = [
                m for m in self._mock_memories
                if m["score"] >= self.similarity_threshold
            ]

            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, len(results))

            return {"history": results}


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def run_customer_support_scenario():
    """
    Run the customer support scenario using LangChain-style memory.

    This demonstrates how our semantic conventions map to LangChain's
    memory abstractions.
    """
    print_section("Story 1: Customer Support Agent (LangChain Style)")
    print("""
This example shows how LangChain memory classes map to our semantic conventions:

- ConversationBufferMemory -> session scope, short_term type
- VectorStoreRetrieverMemory -> user scope, long_term type

The instrumentation pattern would be applied automatically by
opentelemetry-instrumentation-langchain.
""")

    # Setup tracing
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="customer-support-langchain",
        use_console=use_console,
        capture_content=capture_content,
    )

    # Session parameters
    user_id = "user_sarah_123"
    session_short_id = uuid.uuid4().hex[:8]
    session_id = f"session_{session_short_id}"
    conversation_id = f"conv_{session_id}"

    print(f"\nSession Info:")
    print(f"  User ID: {user_id}")
    print(f"  Session ID: {session_id}")
    print(f"  Conversation ID: {conversation_id}")

    # Initialize memories (LangChain style)
    session_memory = InstrumentedConversationBufferMemory(
        tracer,
        store_name="session-context",
        session_id=session_id,
        conversation_id=conversation_id,
        capture_content=capture_content,
    )

    user_history = InstrumentedVectorStoreRetrieverMemory(
        tracer,
        store_name="user-history",
        user_id=user_id,
        similarity_threshold=0.7,
        capture_content=capture_content,
    )

    # Start agent invocation
    with tracer.start_as_current_span(
        "invoke_agent CustomerSupportBot",
        kind=SpanKind.CLIENT,
        attributes={
            GenAIAttributes.OPERATION_NAME: "invoke_agent",
            GenAIAttributes.PROVIDER_NAME: "langchain",
            GenAIAttributes.AGENT_NAME: "CustomerSupportBot",
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ):
        # Step 1: Search user's long-term history
        print_section("Step 1: Search User History (VectorStoreRetrieverMemory)")
        user_context = user_history.load_memory_variables(
            {"prompt": "billing issue duplicate charge"}
        )
        print(f"  Found {len(user_context['history'])} relevant memories")
        for mem in user_context["history"]:
            print(f"    - {mem['content']} (score: {mem['score']})")

        # Step 2: First conversation turn
        print_section("Step 2: First Turn (ConversationBufferMemory.save_context)")
        user_message = "I was charged twice for my subscription"
        agent_response = "I can see the duplicate charge. Let me process a refund."

        session_memory.save_context(
            {"input": user_message},
            {"output": agent_response},
        )
        print(f"  User: {user_message}")
        print(f"  Agent: {agent_response}")

        # Step 3: Load session context for second turn
        print_section("Step 3: Load Session Context (ConversationBufferMemory.load_memory_variables)")
        context = session_memory.load_memory_variables({})
        print(f"  Loaded {len(context['history'])} previous turns")

        # Step 4: Second conversation turn
        print_section("Step 4: Second Turn")
        user_message_2 = "Can you confirm the refund amount?"
        agent_response_2 = "Your refund of $29.99 has been processed."

        session_memory.save_context(
            {"input": user_message_2},
            {"output": agent_response_2},
        )
        print(f"  User: {user_message_2}")
        print(f"  Agent: {agent_response_2}")

        # Step 5: Session cleanup
        print_section("Step 5: Session Cleanup (ConversationBufferMemory.clear)")
        session_memory.clear()
        print("  Session memory cleared")

    # Summary
    print_section("LangChain Memory Mapping Summary")
    print("""
| LangChain Method                              | OTel Operation   | Attributes                       |
|-----------------------------------------------|------------------|----------------------------------|
| ConversationBufferMemory.save_context()       | update_memory    | scope: session, type: short_term |
| ConversationBufferMemory.load_memory_variables()| search_memory  | scope: session, type: short_term |
| ConversationBufferMemory.clear()              | delete_memory    | scope: session                   |
| VectorStoreRetrieverMemory.load_memory_variables()| search_memory | scope: user, type: long_term,    |
|                                               |                  | similarity_threshold: 0.7        |

Key Insight: LangChain's memory abstractions map cleanly to our semantic
conventions because both model the same underlying concepts:
- Conversation context (session-scoped, short-term)
- User knowledge (user-scoped, long-term, similarity-based)
""")


if __name__ == "__main__":
    run_customer_support_scenario()
