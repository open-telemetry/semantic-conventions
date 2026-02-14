"""
GenAI Memory Semantic Conventions - Span Creation Utilities

This module provides utilities for creating OpenTelemetry spans that follow
the proposed semantic conventions for GenAI Memory Operations.

Note: `store_memory` is removed; use `update_memory` for both create and update (upsert).

Example usage:
    from opentelemetry import trace
    from genai_memory_otel import MemorySpanBuilder, MemoryType, MemoryScope

    tracer = trace.get_tracer(__name__)
    span_builder = MemorySpanBuilder(tracer)

    # update_memory is an upsert: use it for both create + update
    with span_builder.update_memory_span(
        provider_name="pinecone",
        store_id="user-preferences",
        update_strategy="merge",
        memory_type="long_term",
        namespace="user_12345",
    ) as span:
        result = memory_provider.upsert(...)
        span.set_attribute("gen_ai.memory.id", result.id)
"""

from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

from opentelemetry import trace
from opentelemetry.trace import Span, SpanKind, Status, StatusCode

from .attributes import (
    MemoryAttributes,
    MemoryOperationName,
    GenAIAttributes,
    ErrorAttributes,
)


class MemorySpanBuilder:
    """
    Builder for creating memory operation spans following semantic conventions.

    This class provides context managers for each memory operation type,
    ensuring consistent attribute assignment and error handling.

    Attributes:
        tracer: OpenTelemetry Tracer instance
        capture_content: Whether to capture sensitive content (default: False)
    """

    def __init__(
        self,
        tracer: trace.Tracer,
        capture_content: bool = False,
    ):
        """
        Initialize the MemorySpanBuilder.

        Args:
            tracer: OpenTelemetry Tracer instance for creating spans
            capture_content: Whether to capture sensitive memory content.
                            Should only be enabled when explicitly requested
                            due to privacy concerns.
        """
        self.tracer = tracer
        self.capture_content = capture_content

    def _should_capture_content(self, content: Optional[str]) -> Optional[str]:
        """Return content only if capture is enabled."""
        return content if self.capture_content and content else None

    # NOTE: store_memory_span is REMOVED per spec.
    # Use update_memory_span for both create and update (upsert) operations.

    @contextmanager
    def search_memory_span(
        self,
        provider_name: str,
        store_id: str,
        *,
        store_name: Optional[str] = None,
        query: Optional[str] = None,
        memory_type: Optional[str] = None,
        similarity_threshold: Optional[float] = None,
        namespace: Optional[str] = None,
        agent_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[Span, None, None]:
        """
        Create a span for search_memory operation.

        Span name: search_memory {gen_ai.memory.store.name}
        Span kind: CLIENT

        This span represents a memory search/retrieval operation - querying
        the memory store for relevant memories.

        Memory search is critical for agent performance - the latency and
        quality of retrieved memories directly impact response quality.

        Args:
            provider_name: Memory provider (e.g., 'pinecone', 'chroma')
            store_id: Unique identifier of the memory store
            store_name: Human-readable store name (optional)
            query: Search query (opt-in, sensitive)
            memory_type: Filter by memory type (recommended)
            similarity_threshold: Minimum similarity score (optional)
            namespace: Namespace for memory isolation (optional)
            agent_id: Agent ID for agent-scoped search (optional)
            conversation_id: Conversation ID for session-scoped search (optional)
            extra_attributes: Additional attributes to set (optional)

        Yields:
            Span: The created span for the search_memory operation

        Note:
            After the search completes, set the result_count attribute:
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, len(results))

        Example:
            with span_builder.search_memory_span(
                provider_name="pinecone",
                store_id="user-prefs",
                similarity_threshold=0.7,
            ) as span:
                results = memory_provider.search(query_embedding)
                span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, len(results))
        """
        display_name = store_name or store_id
        span_name = f"{MemoryOperationName.SEARCH_MEMORY} {display_name}"

        attributes: Dict[str, Any] = {
            GenAIAttributes.OPERATION_NAME: MemoryOperationName.SEARCH_MEMORY,
            GenAIAttributes.PROVIDER_NAME: provider_name,
            MemoryAttributes.STORE_ID: store_id,
        }

        if store_name:
            attributes[MemoryAttributes.STORE_NAME] = store_name
        if self._should_capture_content(query):
            attributes[MemoryAttributes.MEMORY_QUERY] = query
        if memory_type:
            attributes[MemoryAttributes.MEMORY_TYPE] = memory_type
        if similarity_threshold is not None:
            attributes[MemoryAttributes.SEARCH_SIMILARITY_THRESHOLD] = similarity_threshold
        if namespace:
            attributes[MemoryAttributes.MEMORY_NAMESPACE] = namespace
        if agent_id:
            attributes[GenAIAttributes.AGENT_ID] = agent_id
        if conversation_id:
            attributes[GenAIAttributes.CONVERSATION_ID] = conversation_id
        if extra_attributes:
            attributes.update(extra_attributes)

        with self.tracer.start_as_current_span(
            span_name,
            kind=SpanKind.CLIENT,
            attributes=attributes,
        ) as span:
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.set_attribute(ErrorAttributes.ERROR_TYPE, type(e).__name__)
                raise

    @contextmanager
    def update_memory_span(
        self,
        provider_name: str,
        store_id: str,
        *,
        memory_id: Optional[str] = None,
        update_strategy: Optional[str] = None,
        store_name: Optional[str] = None,
        memory_type: Optional[str] = None,
        scope: Optional[str] = None,
        namespace: Optional[str] = None,
        content: Optional[str] = None,
        importance: Optional[float] = None,
        expiration_date: Optional[str] = None,
        agent_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[Span, None, None]:
        """
        Create a span for update_memory operation (upsert).

        Span name: update_memory {gen_ai.memory.store.name}
        Span kind: CLIENT

        This span represents a memory upsert operation - creating a new memory
        item or updating an existing one. Use this for both create and update.

        NOTE: This replaces the removed store_memory operation. Use update_memory
        for both creating new memories and updating existing ones.

        Args:
            provider_name: Memory provider (e.g., 'pinecone', 'chroma')
            store_id: Unique identifier of the memory store
            memory_id: Unique identifier of the memory (optional, may be generated)
            update_strategy: How to update (overwrite, merge, append) - recommended
            store_name: Human-readable store name (optional)
            memory_type: Type of memory (e.g., 'short_term', 'long_term') - recommended
            scope: Memory scope (user, session, agent, team, global) - recommended
            namespace: Namespace for memory isolation (optional)
            content: Memory content (opt-in, sensitive)
            importance: Importance score 0.0-1.0 (optional)
            expiration_date: ISO 8601 expiration date (optional)
            agent_id: Agent ID for agent-scoped memory (optional)
            conversation_id: Conversation ID for session-scoped memory (optional)
            extra_attributes: Additional attributes to set (optional)

        Yields:
            Span: The created span for the update_memory operation

        Note:
            If the memory_id is generated during the operation, set it on the span:
            span.set_attribute(MemoryAttributes.MEMORY_ID, generated_id)

        Example:
            # Upsert (create or update) a memory
            with span_builder.update_memory_span(
                provider_name="pinecone",
                store_id="user-prefs",
                memory_type="long_term",
                scope="user",
                update_strategy="merge",
                namespace="user_12345",
            ) as span:
                result = memory_provider.upsert(content, metadata)
                span.set_attribute(MemoryAttributes.MEMORY_ID, result.id)
        """
        display_name = store_name or store_id
        span_name = f"{MemoryOperationName.UPDATE_MEMORY} {display_name}"

        attributes: Dict[str, Any] = {
            GenAIAttributes.OPERATION_NAME: MemoryOperationName.UPDATE_MEMORY,
            GenAIAttributes.PROVIDER_NAME: provider_name,
            MemoryAttributes.STORE_ID: store_id,
        }

        if memory_id:
            attributes[MemoryAttributes.MEMORY_ID] = memory_id
        if update_strategy:
            attributes[MemoryAttributes.UPDATE_STRATEGY] = update_strategy
        if store_name:
            attributes[MemoryAttributes.STORE_NAME] = store_name
        if memory_type:
            attributes[MemoryAttributes.MEMORY_TYPE] = memory_type
        if scope:
            attributes[MemoryAttributes.MEMORY_SCOPE] = scope
        if namespace:
            attributes[MemoryAttributes.MEMORY_NAMESPACE] = namespace
        if self._should_capture_content(content):
            attributes[MemoryAttributes.MEMORY_CONTENT] = content
        if importance is not None:
            attributes[MemoryAttributes.IMPORTANCE] = importance
        if expiration_date:
            attributes[MemoryAttributes.EXPIRATION_DATE] = expiration_date
        if agent_id:
            attributes[GenAIAttributes.AGENT_ID] = agent_id
        if conversation_id:
            attributes[GenAIAttributes.CONVERSATION_ID] = conversation_id
        if extra_attributes:
            attributes.update(extra_attributes)

        with self.tracer.start_as_current_span(
            span_name,
            kind=SpanKind.CLIENT,
            attributes=attributes,
        ) as span:
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.set_attribute(ErrorAttributes.ERROR_TYPE, type(e).__name__)
                raise

    @contextmanager
    def delete_memory_span(
        self,
        provider_name: str,
        store_id: str,
        scope: str,
        *,
        memory_id: Optional[str] = None,
        store_name: Optional[str] = None,
        memory_type: Optional[str] = None,
        namespace: Optional[str] = None,
        agent_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[Span, None, None]:
        """
        Create a span for delete_memory operation.

        Span name: delete_memory {gen_ai.memory.store.name}
        Span kind: CLIENT

        This span represents a memory deletion operation - removing memory
        item(s) from the store. Can delete by ID or by scope+namespace.

        Args:
            provider_name: Memory provider (e.g., 'pinecone', 'chroma')
            store_id: Unique identifier of the memory store
            scope: Memory scope (user, session, agent, team, global) - REQUIRED
            memory_id: Unique identifier of the memory to delete (optional)
            store_name: Human-readable store name (optional)
            memory_type: Type of memory being deleted (optional)
            namespace: Namespace for memory isolation (optional)
            agent_id: Agent ID for agent-scoped delete (optional)
            conversation_id: Conversation ID for session-scoped delete (optional)
            extra_attributes: Additional attributes to set (optional)

        Yields:
            Span: The created span for the delete_memory operation

        Example:
            # Delete specific memory by ID
            with span_builder.delete_memory_span(
                provider_name="pinecone",
                store_id="user-prefs",
                scope=MemoryScope.USER,
                memory_id="mem_123",
            ) as span:
                memory_provider.delete(memory_id)

            # Delete all memories in a namespace
            with span_builder.delete_memory_span(
                provider_name="pinecone",
                store_id="user-prefs",
                scope=MemoryScope.USER,
                namespace="user_12345",
            ) as span:
                memory_provider.delete_by_namespace(namespace)
        """
        display_name = store_name or store_id
        span_name = f"{MemoryOperationName.DELETE_MEMORY} {display_name}"

        attributes: Dict[str, Any] = {
            GenAIAttributes.OPERATION_NAME: MemoryOperationName.DELETE_MEMORY,
            GenAIAttributes.PROVIDER_NAME: provider_name,
            MemoryAttributes.STORE_ID: store_id,
            MemoryAttributes.MEMORY_SCOPE: scope,
        }

        if memory_id:
            attributes[MemoryAttributes.MEMORY_ID] = memory_id
        if store_name:
            attributes[MemoryAttributes.STORE_NAME] = store_name
        if memory_type:
            attributes[MemoryAttributes.MEMORY_TYPE] = memory_type
        if namespace:
            attributes[MemoryAttributes.MEMORY_NAMESPACE] = namespace
        if agent_id:
            attributes[GenAIAttributes.AGENT_ID] = agent_id
        if conversation_id:
            attributes[GenAIAttributes.CONVERSATION_ID] = conversation_id
        if extra_attributes:
            attributes.update(extra_attributes)

        with self.tracer.start_as_current_span(
            span_name,
            kind=SpanKind.CLIENT,
            attributes=attributes,
        ) as span:
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.set_attribute(ErrorAttributes.ERROR_TYPE, type(e).__name__)
                raise

    @contextmanager
    def create_memory_store_span(
        self,
        provider_name: str,
        store_name: str,
        scope: str,
        *,
        store_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        namespace: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[Span, None, None]:
        """
        Create a span for create_memory_store operation.

        Span name: create_memory_store {gen_ai.memory.store.name}
        Span kind: CLIENT

        This span represents creating/initializing a memory store (e.g.,
        creating a Pinecone index or Chroma collection).

        Args:
            provider_name: Memory provider (e.g., 'pinecone', 'chroma')
            store_name: Human-readable name for the store
            scope: Memory scope (user, session, agent, team, global) - REQUIRED
            store_id: Unique identifier (if known at creation time)
            memory_type: Type of memory if store is type-dedicated (optional)
            namespace: Namespace for memory isolation (optional)
            extra_attributes: Additional attributes to set (optional)

        Yields:
            Span: The created span for the create_memory_store operation

        Note:
            If the store_id is generated during creation, set it on the span:
            span.set_attribute(MemoryAttributes.STORE_ID, new_store_id)

        Example:
            with span_builder.create_memory_store_span(
                provider_name="pinecone",
                store_name="user-preferences",
                scope=MemoryScope.USER,
            ) as span:
                index = pinecone.create_index(name="user-preferences", ...)
                span.set_attribute(MemoryAttributes.STORE_ID, index.name)
        """
        span_name = f"{MemoryOperationName.CREATE_MEMORY_STORE} {store_name}"

        attributes: Dict[str, Any] = {
            GenAIAttributes.OPERATION_NAME: MemoryOperationName.CREATE_MEMORY_STORE,
            GenAIAttributes.PROVIDER_NAME: provider_name,
            MemoryAttributes.STORE_NAME: store_name,
            MemoryAttributes.MEMORY_SCOPE: scope,
        }

        if store_id:
            attributes[MemoryAttributes.STORE_ID] = store_id
        if memory_type:
            attributes[MemoryAttributes.MEMORY_TYPE] = memory_type
        if namespace:
            attributes[MemoryAttributes.MEMORY_NAMESPACE] = namespace
        if extra_attributes:
            attributes.update(extra_attributes)

        with self.tracer.start_as_current_span(
            span_name,
            kind=SpanKind.CLIENT,
            attributes=attributes,
        ) as span:
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.set_attribute(ErrorAttributes.ERROR_TYPE, type(e).__name__)
                raise

    @contextmanager
    def delete_memory_store_span(
        self,
        provider_name: str,
        store_name: str,
        *,
        store_id: Optional[str] = None,
        namespace: Optional[str] = None,
        extra_attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[Span, None, None]:
        """
        Create a span for delete_memory_store operation.

        Span name: delete_memory_store {gen_ai.memory.store.name}
        Span kind: CLIENT

        This span represents deleting/deprovisioning a memory store (e.g.,
        deleting a Pinecone index or Chroma collection).

        Args:
            provider_name: Memory provider (e.g., 'pinecone', 'chroma')
            store_name: Human-readable name of the store
            store_id: Unique identifier of the store (optional)
            namespace: Namespace for memory isolation (optional)
            extra_attributes: Additional attributes to set (optional)

        Yields:
            Span: The created span for the delete_memory_store operation

        Example:
            with span_builder.delete_memory_store_span(
                provider_name="pinecone",
                store_name="user-preferences",
                store_id="idx_abc123",
            ) as span:
                pinecone.delete_index(name="user-preferences")
        """
        span_name = f"{MemoryOperationName.DELETE_MEMORY_STORE} {store_name}"

        attributes: Dict[str, Any] = {
            GenAIAttributes.OPERATION_NAME: MemoryOperationName.DELETE_MEMORY_STORE,
            GenAIAttributes.PROVIDER_NAME: provider_name,
            MemoryAttributes.STORE_NAME: store_name,
        }

        if store_id:
            attributes[MemoryAttributes.STORE_ID] = store_id
        if namespace:
            attributes[MemoryAttributes.MEMORY_NAMESPACE] = namespace
        if extra_attributes:
            attributes.update(extra_attributes)

        with self.tracer.start_as_current_span(
            span_name,
            kind=SpanKind.CLIENT,
            attributes=attributes,
        ) as span:
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.set_attribute(ErrorAttributes.ERROR_TYPE, type(e).__name__)
                raise


class InternalMemorySpanBuilder(MemorySpanBuilder):
    """
    Span builder for in-process memory operations.

    Use this for memory implementations that run in the same process
    (e.g., LangChain in-memory, local Chroma). Creates INTERNAL spans
    instead of CLIENT spans.

    NOTE: store_memory_span is removed per spec.
    Use update_memory_span for both create and update (upsert) operations.
    """

    def _create_internal_span(
        self,
        span_name: str,
        attributes: Dict[str, Any],
    ) -> Generator[Span, None, None]:
        """Create an INTERNAL span for in-process operations."""
        with self.tracer.start_as_current_span(
            span_name,
            kind=SpanKind.INTERNAL,
            attributes=attributes,
        ) as span:
            try:
                yield span
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.set_attribute(ErrorAttributes.ERROR_TYPE, type(e).__name__)
                raise


def set_search_result_count(span: Span, count: int) -> None:
    """
    Convenience function to set search result count on a span.

    Args:
        span: The current span
        count: Number of results returned
    """
    span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, count)


def set_memory_id(span: Span, memory_id: str) -> None:
    """
    Convenience function to set memory ID on a span.

    Useful when the memory ID is generated during the operation.

    Args:
        span: The current span
        memory_id: The generated memory ID
    """
    span.set_attribute(MemoryAttributes.MEMORY_ID, memory_id)


def set_store_id(span: Span, store_id: str) -> None:
    """
    Convenience function to set store ID on a span.

    Useful when the store ID is generated during creation.

    Args:
        span: The current span
        store_id: The generated store ID
    """
    span.set_attribute(MemoryAttributes.STORE_ID, store_id)
