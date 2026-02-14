"""
Unit tests for memory span creation.

These tests validate that spans are created with the correct attributes
following the GenAI Memory semantic conventions.

Note: `store_memory` is removed from the spec; `update_memory` is now an upsert
operation used for both creating and updating memories.
"""

import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.trace import SpanKind, StatusCode

from genai_memory_otel import (
    MemorySpanBuilder,
    MemoryOperationName,
    MemoryType,
    MemoryScope,
    MemoryUpdateStrategy,
    MemoryProviderName,
    MemoryAttributes,
    GenAIAttributes,
    ErrorAttributes,
)


@pytest.fixture(autouse=True)
def reset_tracer_provider():
    """Reset the tracer provider before each test."""
    # Store original provider
    original_provider = trace.get_tracer_provider()
    yield
    # Note: We can't easily reset the global provider, but we handle it per-test


@pytest.fixture
def tracer_with_exporter():
    """Create tracer with in-memory exporter for testing."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    # Get tracer directly from this provider instead of global
    tracer = provider.get_tracer(__name__)
    yield tracer, exporter
    exporter.clear()


class TestUpdateMemorySpan:
    """Tests for update_memory span creation (upsert - create or update)."""

    def test_required_attributes_present(self, tracer_with_exporter):
        """Verify required attributes are set on update_memory span."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
        ):
            pass

        spans = exporter.get_finished_spans()
        assert len(spans) == 1

        span = spans[0]
        attrs = dict(span.attributes)

        # Required attributes per semantic conventions
        assert attrs[GenAIAttributes.OPERATION_NAME] == MemoryOperationName.UPDATE_MEMORY
        assert attrs[GenAIAttributes.PROVIDER_NAME] == MemoryProviderName.PINECONE
        assert attrs[MemoryAttributes.STORE_ID] == "test_store"

    def test_span_name_format(self, tracer_with_exporter):
        """Verify span name follows convention: {operation} {store_id}."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="my_index",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.name == "update_memory my_index"

    def test_span_name_uses_store_name_when_provided(self, tracer_with_exporter):
        """Verify span name uses store_name when provided."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="idx_123",
            store_name="User Preferences",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.name == "update_memory User Preferences"

    def test_span_kind_is_client(self, tracer_with_exporter):
        """Verify span kind is CLIENT for remote operations."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.kind == SpanKind.CLIENT

    def test_content_not_captured_by_default(self, tracer_with_exporter):
        """Verify content attribute is NOT captured by default (privacy)."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer, capture_content=False)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            content="sensitive user data",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert MemoryAttributes.MEMORY_CONTENT not in span.attributes

    def test_content_captured_when_enabled(self, tracer_with_exporter):
        """Verify content attribute IS captured when opt-in enabled."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer, capture_content=True)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            content="sensitive user data",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.attributes[MemoryAttributes.MEMORY_CONTENT] == "sensitive user data"

    def test_optional_attributes(self, tracer_with_exporter):
        """Verify optional attributes are set when provided."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            memory_id="mem_001",
            memory_type=MemoryType.SEMANTIC,
            scope=MemoryScope.USER,
            update_strategy=MemoryUpdateStrategy.MERGE,
            namespace="user_12345",
            importance=0.85,
            expiration_date="2026-12-31",
            agent_id="agent_001",
            conversation_id="conv_456",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        attrs = dict(span.attributes)

        assert attrs[MemoryAttributes.MEMORY_ID] == "mem_001"
        assert attrs[MemoryAttributes.MEMORY_TYPE] == MemoryType.SEMANTIC
        assert attrs[MemoryAttributes.MEMORY_SCOPE] == MemoryScope.USER
        assert attrs[MemoryAttributes.UPDATE_STRATEGY] == MemoryUpdateStrategy.MERGE
        assert attrs[MemoryAttributes.MEMORY_NAMESPACE] == "user_12345"
        assert attrs[MemoryAttributes.IMPORTANCE] == 0.85
        assert attrs[MemoryAttributes.EXPIRATION_DATE] == "2026-12-31"
        assert attrs[GenAIAttributes.AGENT_ID] == "agent_001"
        assert attrs[GenAIAttributes.CONVERSATION_ID] == "conv_456"

    def test_error_handling(self, tracer_with_exporter):
        """Verify error attributes set on exception."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with pytest.raises(ValueError):
            with span_builder.update_memory_span(
                provider_name=MemoryProviderName.PINECONE,
                store_id="test_store",
            ):
                raise ValueError("Upsert failed")

        span = exporter.get_finished_spans()[0]
        assert span.status.status_code == StatusCode.ERROR
        assert span.attributes[ErrorAttributes.ERROR_TYPE] == "ValueError"

    def test_extra_attributes(self, tracer_with_exporter):
        """Verify extra attributes can be added."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            extra_attributes={
                "db.system": "pinecone",
                "custom.tag": "value",
            },
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.attributes["db.system"] == "pinecone"
        assert span.attributes["custom.tag"] == "value"

    def test_memory_id_can_be_set_after_upsert(self, tracer_with_exporter):
        """Verify memory_id can be set after upsert when generated."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.update_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
        ) as span:
            # Simulate memory ID being generated
            span.set_attribute(MemoryAttributes.MEMORY_ID, "mem_generated_123")

        finished_span = exporter.get_finished_spans()[0]
        assert finished_span.attributes[MemoryAttributes.MEMORY_ID] == "mem_generated_123"


class TestSearchMemorySpan:
    """Tests for search_memory span creation."""

    def test_required_attributes(self, tracer_with_exporter):
        """Verify required attributes for search_memory span."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.search_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        attrs = dict(span.attributes)

        assert attrs[GenAIAttributes.OPERATION_NAME] == MemoryOperationName.SEARCH_MEMORY
        assert attrs[GenAIAttributes.PROVIDER_NAME] == MemoryProviderName.PINECONE
        assert attrs[MemoryAttributes.STORE_ID] == "test_store"

    def test_result_count_can_be_set(self, tracer_with_exporter):
        """Verify result_count can be set after search completes."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.search_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
        ) as span:
            # Simulate search results
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 5)

        finished_span = exporter.get_finished_spans()[0]
        assert finished_span.attributes[MemoryAttributes.SEARCH_RESULT_COUNT] == 5

    def test_similarity_threshold(self, tracer_with_exporter):
        """Verify similarity threshold is captured."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.search_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            similarity_threshold=0.75,
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.attributes[MemoryAttributes.SEARCH_SIMILARITY_THRESHOLD] == 0.75

    def test_query_not_captured_by_default(self, tracer_with_exporter):
        """Verify query is NOT captured by default (privacy)."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer, capture_content=False)

        with span_builder.search_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            query="user private search query",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert MemoryAttributes.MEMORY_QUERY not in span.attributes

    def test_query_captured_when_enabled(self, tracer_with_exporter):
        """Verify query IS captured when opt-in enabled."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer, capture_content=True)

        with span_builder.search_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            query="user search query",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.attributes[MemoryAttributes.MEMORY_QUERY] == "user search query"


class TestDeleteMemorySpan:
    """Tests for delete_memory span creation."""

    def test_required_attributes(self, tracer_with_exporter):
        """Verify required attributes for delete_memory span (scope is REQUIRED)."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.delete_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            scope=MemoryScope.USER,
            memory_id="mem_001",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        attrs = dict(span.attributes)

        assert attrs[GenAIAttributes.OPERATION_NAME] == MemoryOperationName.DELETE_MEMORY
        assert attrs[GenAIAttributes.PROVIDER_NAME] == MemoryProviderName.PINECONE
        assert attrs[MemoryAttributes.STORE_ID] == "test_store"
        assert attrs[MemoryAttributes.MEMORY_SCOPE] == MemoryScope.USER
        assert attrs[MemoryAttributes.MEMORY_ID] == "mem_001"

    def test_delete_by_namespace(self, tracer_with_exporter):
        """Verify delete can be done by namespace without memory_id."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.delete_memory_span(
            provider_name=MemoryProviderName.PINECONE,
            store_id="test_store",
            scope=MemoryScope.USER,
            namespace="user_12345",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        attrs = dict(span.attributes)

        assert attrs[MemoryAttributes.MEMORY_SCOPE] == MemoryScope.USER
        assert attrs[MemoryAttributes.MEMORY_NAMESPACE] == "user_12345"
        assert MemoryAttributes.MEMORY_ID not in attrs


class TestCreateMemoryStoreSpan:
    """Tests for create_memory_store span creation."""

    def test_required_attributes(self, tracer_with_exporter):
        """Verify required attributes for create_memory_store span (scope is REQUIRED)."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.create_memory_store_span(
            provider_name=MemoryProviderName.PINECONE,
            store_name="user-preferences",
            scope=MemoryScope.USER,
        ):
            pass

        span = exporter.get_finished_spans()[0]
        attrs = dict(span.attributes)

        assert attrs[GenAIAttributes.OPERATION_NAME] == MemoryOperationName.CREATE_MEMORY_STORE
        assert attrs[GenAIAttributes.PROVIDER_NAME] == MemoryProviderName.PINECONE
        assert attrs[MemoryAttributes.STORE_NAME] == "user-preferences"
        assert attrs[MemoryAttributes.MEMORY_SCOPE] == MemoryScope.USER

    def test_span_name_format(self, tracer_with_exporter):
        """Verify span name format for create_memory_store."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.create_memory_store_span(
            provider_name=MemoryProviderName.PINECONE,
            store_name="User Preferences",
            scope=MemoryScope.USER,
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.name == "create_memory_store User Preferences"

    def test_store_id_can_be_set_after_creation(self, tracer_with_exporter):
        """Verify store_id can be set after store is created."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.create_memory_store_span(
            provider_name=MemoryProviderName.PINECONE,
            store_name="user-preferences",
            scope=MemoryScope.USER,
        ) as span:
            # Simulate store ID being returned from creation
            span.set_attribute(MemoryAttributes.STORE_ID, "idx_abc123")

        finished_span = exporter.get_finished_spans()[0]
        assert finished_span.attributes[MemoryAttributes.STORE_ID] == "idx_abc123"


class TestDeleteMemoryStoreSpan:
    """Tests for delete_memory_store span creation."""

    def test_required_attributes(self, tracer_with_exporter):
        """Verify required attributes for delete_memory_store span."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.delete_memory_store_span(
            provider_name=MemoryProviderName.PINECONE,
            store_name="user-preferences",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        attrs = dict(span.attributes)

        assert attrs[GenAIAttributes.OPERATION_NAME] == MemoryOperationName.DELETE_MEMORY_STORE
        assert attrs[GenAIAttributes.PROVIDER_NAME] == MemoryProviderName.PINECONE
        assert attrs[MemoryAttributes.STORE_NAME] == "user-preferences"

    def test_span_name_format(self, tracer_with_exporter):
        """Verify span name format for delete_memory_store."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.delete_memory_store_span(
            provider_name=MemoryProviderName.PINECONE,
            store_name="User Preferences",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.name == "delete_memory_store User Preferences"

    def test_store_id_optional(self, tracer_with_exporter):
        """Verify store_id is optional."""
        tracer, exporter = tracer_with_exporter
        span_builder = MemorySpanBuilder(tracer)

        with span_builder.delete_memory_store_span(
            provider_name=MemoryProviderName.PINECONE,
            store_name="user-preferences",
            store_id="idx_abc123",
        ):
            pass

        span = exporter.get_finished_spans()[0]
        assert span.attributes[MemoryAttributes.STORE_ID] == "idx_abc123"


class TestMemoryTypeValues:
    """Tests for memory type values."""

    def test_all_memory_types(self):
        """Verify all memory type values are correct."""
        assert MemoryType.SHORT_TERM == "short_term"
        assert MemoryType.LONG_TERM == "long_term"
        assert MemoryType.SEMANTIC == "semantic"
        assert MemoryType.EPISODIC == "episodic"
        assert MemoryType.PROCEDURAL == "procedural"
        assert MemoryType.ENTITY == "entity"


class TestMemoryScopeValues:
    """Tests for memory scope values."""

    def test_all_memory_scopes(self):
        """Verify all memory scope values are correct."""
        assert MemoryScope.USER == "user"
        assert MemoryScope.SESSION == "session"
        assert MemoryScope.AGENT == "agent"
        assert MemoryScope.TEAM == "team"
        assert MemoryScope.GLOBAL == "global"


class TestMemoryUpdateStrategyValues:
    """Tests for update strategy values."""

    def test_all_update_strategies(self):
        """Verify all update strategy values are correct."""
        assert MemoryUpdateStrategy.OVERWRITE == "overwrite"
        assert MemoryUpdateStrategy.MERGE == "merge"
        assert MemoryUpdateStrategy.APPEND == "append"


class TestOperationNameValues:
    """Tests for operation name values."""

    def test_all_operation_names(self):
        """Verify all operation name values are correct."""
        assert MemoryOperationName.SEARCH_MEMORY == "search_memory"
        assert MemoryOperationName.UPDATE_MEMORY == "update_memory"
        assert MemoryOperationName.DELETE_MEMORY == "delete_memory"
        assert MemoryOperationName.CREATE_MEMORY_STORE == "create_memory_store"
        assert MemoryOperationName.DELETE_MEMORY_STORE == "delete_memory_store"

    def test_store_memory_removed(self):
        """Verify store_memory is NOT in operation names (removed from spec)."""
        assert not hasattr(MemoryOperationName, 'STORE_MEMORY')
