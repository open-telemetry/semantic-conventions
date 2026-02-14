"""
GenAI Memory OTEL - OpenTelemetry Semantic Conventions for GenAI Memory Operations

This package provides utilities for instrumenting GenAI memory operations
following the proposed OpenTelemetry semantic conventions.

Note: `store_memory` is removed; use `update_memory` for both create and update (upsert).

Quick Start:
    from genai_memory_otel import (
        setup_tracing,
        MemorySpanBuilder,
        MemoryType,
        MemoryScope,
        MemoryProviderName,
    )

    # Initialize tracing
    tracer = setup_tracing(service_name="my-agent")
    span_builder = MemorySpanBuilder(tracer)

    # Create memory operation spans (update_memory is an upsert)
    with span_builder.update_memory_span(
        provider_name=MemoryProviderName.PINECONE,
        store_id="user-preferences",
        memory_type=MemoryType.LONG_TERM,
        scope=MemoryScope.USER,
        update_strategy="merge",
    ) as span:
        # Perform memory upsert operation
        result = memory_provider.upsert(...)
        span.set_attribute("gen_ai.memory.id", result.id)

Reference:
    https://github.com/open-telemetry/semantic-conventions/issues/2664
"""

__version__ = "0.1.0"

# Attributes
from .attributes import (
    # Operation Names
    MemoryOperationName,
    # Memory Classifications
    MemoryType,
    MemoryScope,
    MemoryUpdateStrategy,
    # Provider Names
    MemoryProviderName,
    # Attribute Keys
    MemoryAttributes,
    GenAIAttributes,
    ErrorAttributes,
    DatabaseAttributes,
)

# Span Builders
from .spans import (
    MemorySpanBuilder,
    InternalMemorySpanBuilder,
    # Convenience functions
    set_search_result_count,
    set_memory_id,
    set_store_id,
)

# Exporters
from .exporters import (
    setup_tracing,
    should_capture_content,
    get_tracer,
    shutdown_tracing,
    TracingConfig,
)

# LLM + tool helpers (demo utilities)
from .llm_client import LLMClient, ChatResult, add_inference_details_event, add_evaluation_result_event
from .tool_spans import execute_tool_span

__all__ = [
    # Version
    "__version__",
    # Operation Names
    "MemoryOperationName",
    # Memory Classifications
    "MemoryType",
    "MemoryScope",
    "MemoryUpdateStrategy",
    # Provider Names
    "MemoryProviderName",
    # Attribute Keys
    "MemoryAttributes",
    "GenAIAttributes",
    "ErrorAttributes",
    "DatabaseAttributes",
    # Span Builders
    "MemorySpanBuilder",
    "InternalMemorySpanBuilder",
    # Convenience functions
    "set_search_result_count",
    "set_memory_id",
    "set_store_id",
    # Exporters
    "setup_tracing",
    "should_capture_content",
    "get_tracer",
    "shutdown_tracing",
    "TracingConfig",
    # Demo utilities
    "LLMClient",
    "ChatResult",
    "add_inference_details_event",
    "add_evaluation_result_event",
    "execute_tool_span",
]
