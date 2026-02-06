#!/usr/bin/env python3
"""
Comprehensive GenAI Memory Spans Demo - All Operations & Frameworks Showcase

This script demonstrates ALL 5 memory span types defined in the OpenTelemetry
GenAI Memory semantic conventions:

1. create_memory_store - Create/initialize a memory store
2. search_memory - Query/retrieve memories
3. update_memory - Create or update (upsert) memory items
4. delete_memory - Delete memory items
5. delete_memory_store - Delete/deprovision a memory store

Additionally demonstrates framework-specific memory integrations for:
- LangChain (ConversationBufferMemory, VectorStoreMemory)
- LangGraph (Checkpointer, MemorySaver)
- LlamaIndex (ChatMemoryBuffer, SimpleChatStore)
- AutoGen (ConversableAgent message history)
- CrewAI (Long-term memory, Short-term memory)
- Google ADK (Session memory)
- Microsoft Azure AI Agent (Thread messages)

Each operation is demonstrated with various attribute combinations to showcase
the full range of the semantic conventions.

Run with:
    python main.py

To use OTLP exporter (requires collector):
    GENAI_MEMORY_USE_OTLP=true python main.py

To capture sensitive content:
    GENAI_MEMORY_CAPTURE_CONTENT=true python main.py
"""

import os
import sys
import uuid
from datetime import datetime, timedelta

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
    MemoryOperationName,
    GenAIAttributes,
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


def demo_create_memory_store(span_builder: MemorySpanBuilder):
    """
    Demonstrate create_memory_store spans with various configurations.

    Shows:
    - User-scoped store
    - Session-scoped store
    - Agent-scoped store with namespace
    """
    print_section("1. CREATE_MEMORY_STORE Spans")

    # 1a. Create user-scoped memory store
    print("\n  1a. Creating user-scoped memory store...")
    with span_builder.create_memory_store_span(
        provider_name="chroma",
        store_name="user-preferences",
        scope=MemoryScope.USER,
        memory_type=MemoryType.SEMANTIC,
    ) as span:
        store_id = f"store_{uuid.uuid4().hex[:8]}"
        span.set_attribute(MemoryAttributes.STORE_ID, store_id)
        print_span_info("create_memory_store", {
            "gen_ai.operation.name": MemoryOperationName.CREATE_MEMORY_STORE,
            "gen_ai.provider.name": "chroma",
            "gen_ai.memory.store.name": "user-preferences",
            "gen_ai.memory.scope": MemoryScope.USER,
            "gen_ai.memory.type": MemoryType.SEMANTIC,
            "gen_ai.memory.store.id": store_id,
        })

    # 1b. Create session-scoped memory store
    print("\n  1b. Creating session-scoped memory store...")
    with span_builder.create_memory_store_span(
        provider_name="redis",
        store_name="conversation-history",
        scope=MemoryScope.SESSION,
        memory_type=MemoryType.EPISODIC,
    ) as span:
        store_id = f"session_{uuid.uuid4().hex[:8]}"
        span.set_attribute(MemoryAttributes.STORE_ID, store_id)
        print_span_info("create_memory_store", {
            "gen_ai.operation.name": MemoryOperationName.CREATE_MEMORY_STORE,
            "gen_ai.provider.name": "redis",
            "gen_ai.memory.store.name": "conversation-history",
            "gen_ai.memory.scope": MemoryScope.SESSION,
            "gen_ai.memory.type": MemoryType.EPISODIC,
            "gen_ai.memory.store.id": store_id,
        })

    # 1c. Create agent-scoped memory store with namespace
    print("\n  1c. Creating agent-scoped memory store with namespace...")
    with span_builder.create_memory_store_span(
        provider_name="pinecone",
        store_name="agent-knowledge-base",
        scope=MemoryScope.AGENT,
        memory_type=MemoryType.PROCEDURAL,
        namespace="org_acme",
    ) as span:
        store_id = f"kb_{uuid.uuid4().hex[:8]}"
        span.set_attribute(MemoryAttributes.STORE_ID, store_id)
        print_span_info("create_memory_store", {
            "gen_ai.operation.name": MemoryOperationName.CREATE_MEMORY_STORE,
            "gen_ai.provider.name": "pinecone",
            "gen_ai.memory.store.name": "agent-knowledge-base",
            "gen_ai.memory.scope": MemoryScope.AGENT,
            "gen_ai.memory.type": MemoryType.PROCEDURAL,
            "gen_ai.memory.namespace": "org_acme",
            "gen_ai.memory.store.id": store_id,
        })

    return store_id


def demo_update_memory(span_builder: MemorySpanBuilder, store_id: str):
    """
    Demonstrate update_memory spans (upsert) with various configurations.

    Shows:
    - Creating new memory (upsert)
    - Updating with merge strategy
    - Updating with overwrite strategy
    - Memory with expiration and importance
    """
    print_section("2. UPDATE_MEMORY Spans (Upsert)")

    memory_ids = []

    # 2a. Create new memory (upsert - no existing)
    print("\n  2a. Creating new memory via upsert...")
    mem_id_1 = f"mem_{uuid.uuid4().hex[:12]}"
    memory_ids.append(mem_id_1)
    with span_builder.update_memory_span(
        provider_name="pinecone",
        store_id=store_id,
        memory_id=mem_id_1,
        memory_type=MemoryType.SEMANTIC,
        scope=MemoryScope.USER,
        namespace="user_12345",
        content="User prefers dark mode and email notifications",
        importance=0.85,
        agent_id="support_agent_001",
    ):
        print_span_info("update_memory", {
            "gen_ai.operation.name": MemoryOperationName.UPDATE_MEMORY,
            "gen_ai.provider.name": "pinecone",
            "gen_ai.memory.store.id": store_id,
            "gen_ai.memory.id": mem_id_1,
            "gen_ai.memory.type": MemoryType.SEMANTIC,
            "gen_ai.memory.scope": MemoryScope.USER,
            "gen_ai.memory.namespace": "user_12345",
            "gen_ai.memory.importance": 0.85,
            "gen_ai.agent.id": "support_agent_001",
        })

    # 2b. Update with merge strategy
    print("\n  2b. Updating memory with MERGE strategy...")
    with span_builder.update_memory_span(
        provider_name="pinecone",
        store_id=store_id,
        memory_id=mem_id_1,
        update_strategy=MemoryUpdateStrategy.MERGE,
        content="Added: prefers Spanish language",
    ):
        print_span_info("update_memory", {
            "gen_ai.operation.name": MemoryOperationName.UPDATE_MEMORY,
            "gen_ai.provider.name": "pinecone",
            "gen_ai.memory.store.id": store_id,
            "gen_ai.memory.id": mem_id_1,
            "gen_ai.memory.update.strategy": MemoryUpdateStrategy.MERGE,
        })

    # 2c. Create memory with expiration
    print("\n  2c. Creating session memory with expiration...")
    mem_id_2 = f"mem_{uuid.uuid4().hex[:12]}"
    memory_ids.append(mem_id_2)
    expiration = (datetime.utcnow() + timedelta(hours=24)).isoformat()
    with span_builder.update_memory_span(
        provider_name="redis",
        store_id="session-store",
        memory_id=mem_id_2,
        memory_type=MemoryType.SHORT_TERM,
        scope=MemoryScope.SESSION,
        expiration_date=expiration,
        conversation_id="conv_abc123",
    ):
        print_span_info("update_memory", {
            "gen_ai.operation.name": MemoryOperationName.UPDATE_MEMORY,
            "gen_ai.provider.name": "redis",
            "gen_ai.memory.store.id": "session-store",
            "gen_ai.memory.id": mem_id_2,
            "gen_ai.memory.type": MemoryType.SHORT_TERM,
            "gen_ai.memory.scope": MemoryScope.SESSION,
            "gen_ai.memory.expiration_date": expiration,
            "gen_ai.conversation.id": "conv_abc123",
        })

    # 2d. Update with overwrite strategy
    print("\n  2d. Updating memory with OVERWRITE strategy...")
    with span_builder.update_memory_span(
        provider_name="pinecone",
        store_id=store_id,
        memory_id=mem_id_1,
        update_strategy=MemoryUpdateStrategy.OVERWRITE,
        memory_type=MemoryType.SEMANTIC,
        scope=MemoryScope.USER,
        content="Complete replacement of user preferences",
        importance=0.95,
    ):
        print_span_info("update_memory", {
            "gen_ai.operation.name": MemoryOperationName.UPDATE_MEMORY,
            "gen_ai.provider.name": "pinecone",
            "gen_ai.memory.store.id": store_id,
            "gen_ai.memory.id": mem_id_1,
            "gen_ai.memory.update.strategy": MemoryUpdateStrategy.OVERWRITE,
            "gen_ai.memory.type": MemoryType.SEMANTIC,
            "gen_ai.memory.scope": MemoryScope.USER,
            "gen_ai.memory.importance": 0.95,
        })

    # 2e. Team-scoped memory for multi-agent collaboration
    print("\n  2e. Creating team-scoped memory for multi-agent collaboration...")
    mem_id_3 = f"mem_{uuid.uuid4().hex[:12]}"
    memory_ids.append(mem_id_3)
    with span_builder.update_memory_span(
        provider_name="milvus",
        store_id="team-knowledge",
        memory_id=mem_id_3,
        memory_type=MemoryType.PROCEDURAL,
        scope=MemoryScope.TEAM,
        namespace="research_team",
        content="Shared research findings about customer behavior",
        agent_id="researcher_agent",
    ):
        print_span_info("update_memory", {
            "gen_ai.operation.name": MemoryOperationName.UPDATE_MEMORY,
            "gen_ai.provider.name": "milvus",
            "gen_ai.memory.store.id": "team-knowledge",
            "gen_ai.memory.id": mem_id_3,
            "gen_ai.memory.type": MemoryType.PROCEDURAL,
            "gen_ai.memory.scope": MemoryScope.TEAM,
            "gen_ai.memory.namespace": "research_team",
            "gen_ai.agent.id": "researcher_agent",
        })

    return memory_ids


def demo_search_memory(span_builder: MemorySpanBuilder, store_id: str):
    """
    Demonstrate search_memory spans with various configurations.

    Shows:
    - Basic search with query
    - Search with similarity threshold
    - Search with namespace filter
    - Search with agent/conversation context
    """
    print_section("3. SEARCH_MEMORY Spans")

    # 3a. Basic search with query
    print("\n  3a. Basic memory search...")
    with span_builder.search_memory_span(
        provider_name="pinecone",
        store_id=store_id,
        query="user preferences for notifications",
        memory_type=MemoryType.SEMANTIC,
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 5)
        print_span_info("search_memory", {
            "gen_ai.operation.name": MemoryOperationName.SEARCH_MEMORY,
            "gen_ai.provider.name": "pinecone",
            "gen_ai.memory.store.id": store_id,
            "gen_ai.memory.query": "user preferences for notifications",
            "gen_ai.memory.type": MemoryType.SEMANTIC,
            "gen_ai.memory.search.result.count": 5,
        })

    # 3b. Search with similarity threshold
    print("\n  3b. Search with similarity threshold...")
    with span_builder.search_memory_span(
        provider_name="chroma",
        store_id="user-history",
        query="previous support interactions",
        memory_type=MemoryType.EPISODIC,
        similarity_threshold=0.75,
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 3)
        print_span_info("search_memory", {
            "gen_ai.operation.name": MemoryOperationName.SEARCH_MEMORY,
            "gen_ai.provider.name": "chroma",
            "gen_ai.memory.store.id": "user-history",
            "gen_ai.memory.query": "previous support interactions",
            "gen_ai.memory.type": MemoryType.EPISODIC,
            "gen_ai.memory.search.similarity.threshold": 0.75,
            "gen_ai.memory.search.result.count": 3,
        })

    # 3c. Search with namespace filter
    print("\n  3c. Search with namespace filter...")
    with span_builder.search_memory_span(
        provider_name="weaviate",
        store_id="global-knowledge",
        query="product information",
        namespace="org_acme",
        similarity_threshold=0.8,
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 10)
        print_span_info("search_memory", {
            "gen_ai.operation.name": MemoryOperationName.SEARCH_MEMORY,
            "gen_ai.provider.name": "weaviate",
            "gen_ai.memory.store.id": "global-knowledge",
            "gen_ai.memory.query": "product information",
            "gen_ai.memory.namespace": "org_acme",
            "gen_ai.memory.search.similarity.threshold": 0.8,
            "gen_ai.memory.search.result.count": 10,
        })

    # 3d. Search with agent context
    print("\n  3d. Search with agent context...")
    with span_builder.search_memory_span(
        provider_name="mem0",
        store_id="agent-memories",
        query="how to handle refund requests",
        memory_type=MemoryType.PROCEDURAL,
        agent_id="support_agent_001",
        conversation_id="conv_xyz789",
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 2)
        print_span_info("search_memory", {
            "gen_ai.operation.name": MemoryOperationName.SEARCH_MEMORY,
            "gen_ai.provider.name": "mem0",
            "gen_ai.memory.store.id": "agent-memories",
            "gen_ai.memory.query": "how to handle refund requests",
            "gen_ai.memory.type": MemoryType.PROCEDURAL,
            "gen_ai.agent.id": "support_agent_001",
            "gen_ai.conversation.id": "conv_xyz789",
            "gen_ai.memory.search.result.count": 2,
        })

    # 3e. Search returning no results
    print("\n  3e. Search with no results...")
    with span_builder.search_memory_span(
        provider_name="pinecone",
        store_id=store_id,
        query="nonexistent topic xyz",
        similarity_threshold=0.9,
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 0)
        print_span_info("search_memory", {
            "gen_ai.operation.name": MemoryOperationName.SEARCH_MEMORY,
            "gen_ai.provider.name": "pinecone",
            "gen_ai.memory.store.id": store_id,
            "gen_ai.memory.query": "nonexistent topic xyz",
            "gen_ai.memory.search.similarity.threshold": 0.9,
            "gen_ai.memory.search.result.count": 0,
        })


def demo_delete_memory(span_builder: MemorySpanBuilder, store_id: str, memory_ids: list):
    """
    Demonstrate delete_memory spans with various configurations.

    Shows:
    - Delete specific memory by ID
    - Delete by scope (bulk delete)
    - Delete by namespace
    """
    print_section("4. DELETE_MEMORY Spans")

    # 4a. Delete specific memory by ID
    if memory_ids:
        print("\n  4a. Deleting specific memory by ID...")
        mem_id = memory_ids[0]
        with span_builder.delete_memory_span(
            provider_name="pinecone",
            store_id=store_id,
            scope=MemoryScope.USER,
            memory_id=mem_id,
            memory_type=MemoryType.SEMANTIC,
        ):
            print_span_info("delete_memory", {
                "gen_ai.operation.name": MemoryOperationName.DELETE_MEMORY,
                "gen_ai.provider.name": "pinecone",
                "gen_ai.memory.store.id": store_id,
                "gen_ai.memory.scope": MemoryScope.USER,
                "gen_ai.memory.id": mem_id,
                "gen_ai.memory.type": MemoryType.SEMANTIC,
            })

    # 4b. Delete all memories in a scope (bulk)
    print("\n  4b. Bulk delete all session-scoped memories...")
    with span_builder.delete_memory_span(
        provider_name="redis",
        store_id="session-store",
        scope=MemoryScope.SESSION,
        conversation_id="conv_abc123",
    ):
        print_span_info("delete_memory", {
            "gen_ai.operation.name": MemoryOperationName.DELETE_MEMORY,
            "gen_ai.provider.name": "redis",
            "gen_ai.memory.store.id": "session-store",
            "gen_ai.memory.scope": MemoryScope.SESSION,
            "gen_ai.conversation.id": "conv_abc123",
        })

    # 4c. Delete by namespace
    print("\n  4c. Deleting memories by namespace...")
    with span_builder.delete_memory_span(
        provider_name="milvus",
        store_id="team-knowledge",
        scope=MemoryScope.TEAM,
        namespace="research_team",
        agent_id="researcher_agent",
    ):
        print_span_info("delete_memory", {
            "gen_ai.operation.name": MemoryOperationName.DELETE_MEMORY,
            "gen_ai.provider.name": "milvus",
            "gen_ai.memory.store.id": "team-knowledge",
            "gen_ai.memory.scope": MemoryScope.TEAM,
            "gen_ai.memory.namespace": "research_team",
            "gen_ai.agent.id": "researcher_agent",
        })

    # 4d. Delete agent-scoped memory
    print("\n  4d. Deleting agent-scoped memory...")
    with span_builder.delete_memory_span(
        provider_name="mem0",
        store_id="agent-memories",
        scope=MemoryScope.AGENT,
        memory_type=MemoryType.PROCEDURAL,
        agent_id="support_agent_001",
    ):
        print_span_info("delete_memory", {
            "gen_ai.operation.name": MemoryOperationName.DELETE_MEMORY,
            "gen_ai.provider.name": "mem0",
            "gen_ai.memory.store.id": "agent-memories",
            "gen_ai.memory.scope": MemoryScope.AGENT,
            "gen_ai.memory.type": MemoryType.PROCEDURAL,
            "gen_ai.agent.id": "support_agent_001",
        })


def demo_delete_memory_store(span_builder: MemorySpanBuilder, store_id: str):
    """
    Demonstrate delete_memory_store spans.

    Shows:
    - Delete memory store by name
    - Delete memory store with namespace
    """
    print_section("5. DELETE_MEMORY_STORE Spans")

    # 5a. Delete memory store
    print("\n  5a. Deleting memory store...")
    with span_builder.delete_memory_store_span(
        provider_name="pinecone",
        store_name="agent-knowledge-base",
        store_id=store_id,
    ):
        print_span_info("delete_memory_store", {
            "gen_ai.operation.name": MemoryOperationName.DELETE_MEMORY_STORE,
            "gen_ai.provider.name": "pinecone",
            "gen_ai.memory.store.name": "agent-knowledge-base",
            "gen_ai.memory.store.id": store_id,
        })

    # 5b. Delete memory store with namespace
    print("\n  5b. Deleting namespaced memory store...")
    with span_builder.delete_memory_store_span(
        provider_name="weaviate",
        store_name="tenant-data",
        namespace="org_acme",
    ):
        print_span_info("delete_memory_store", {
            "gen_ai.operation.name": MemoryOperationName.DELETE_MEMORY_STORE,
            "gen_ai.provider.name": "weaviate",
            "gen_ai.memory.store.name": "tenant-data",
            "gen_ai.memory.namespace": "org_acme",
        })


def demo_framework_integrations(span_builder: MemorySpanBuilder):
    """
    Demonstrate framework-specific memory integrations.

    Shows how memory operations look when using popular frameworks:
    - LangChain (ConversationBufferMemory pattern)
    - LangGraph (Checkpointer pattern)
    - LlamaIndex (ChatMemoryBuffer pattern)
    - AutoGen (Message history pattern)
    - CrewAI (Crew memory pattern)
    """
    print_section("6. FRAMEWORK INTEGRATIONS")

    # 6a. LangChain ConversationBufferMemory pattern
    print("\n  6a. LangChain Memory Pattern (save_context / load_memory_variables)")
    print("      Simulating ConversationBufferMemory operations...")

    # Save context (store)
    mem_id = f"langchain_{uuid.uuid4().hex[:8]}"
    with span_builder.update_memory_span(
        provider_name="langchain",
        store_id="conversation-buffer",
        memory_id=mem_id,
        memory_type=MemoryType.EPISODIC,
        scope=MemoryScope.SESSION,
        content="User: Hello! Assistant: Hi there!",
        conversation_id="langchain_conv_001",
        extra_attributes={
            "gen_ai.framework": "langchain",
            "langchain.memory_type": "ConversationBufferMemory",
            "langchain.operation": "save_context",
        },
    ):
        print_span_info("update_memory (LangChain save_context)", {
            "gen_ai.provider.name": "langchain",
            "gen_ai.memory.store.id": "conversation-buffer",
            "gen_ai.memory.type": MemoryType.EPISODIC,
            "langchain.memory_type": "ConversationBufferMemory",
            "langchain.operation": "save_context",
        })

    # Load memory variables (search)
    with span_builder.search_memory_span(
        provider_name="langchain",
        store_id="conversation-buffer",
        memory_type=MemoryType.EPISODIC,
        conversation_id="langchain_conv_001",
        extra_attributes={
            "gen_ai.framework": "langchain",
            "langchain.memory_type": "ConversationBufferMemory",
            "langchain.operation": "load_memory_variables",
        },
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 5)
        print_span_info("search_memory (LangChain load_memory_variables)", {
            "gen_ai.provider.name": "langchain",
            "gen_ai.memory.store.id": "conversation-buffer",
            "gen_ai.memory.type": MemoryType.EPISODIC,
            "langchain.operation": "load_memory_variables",
            "gen_ai.memory.search.result.count": 5,
        })

    # 6b. LangGraph Checkpointer pattern
    print("\n  6b. LangGraph Checkpointer Pattern (checkpoint persistence)")
    print("      Simulating StateGraph checkpoint operations...")

    thread_id = "langgraph_thread_001"

    # Put checkpoint
    checkpoint_id = f"ckpt_{uuid.uuid4().hex[:12]}"
    with span_builder.update_memory_span(
        provider_name="langchain",  # LangGraph is part of LangChain
        store_id="langgraph-checkpointer",
        memory_id=checkpoint_id,
        memory_type=MemoryType.EPISODIC,
        scope=MemoryScope.SESSION,
        namespace=thread_id,
        conversation_id=thread_id,
        extra_attributes={
            "gen_ai.framework": "langgraph",
            "langgraph.operation": "put",
            "langgraph.thread_id": thread_id,
            "langgraph.checkpoint_id": checkpoint_id,
        },
    ):
        print_span_info("update_memory (LangGraph put)", {
            "gen_ai.provider.name": "langchain",
            "gen_ai.memory.store.id": "langgraph-checkpointer",
            "langgraph.operation": "put",
            "langgraph.thread_id": thread_id,
            "langgraph.checkpoint_id": checkpoint_id,
        })

    # Get checkpoint
    with span_builder.search_memory_span(
        provider_name="langchain",
        store_id="langgraph-checkpointer",
        memory_type=MemoryType.EPISODIC,
        namespace=thread_id,
        conversation_id=thread_id,
        extra_attributes={
            "gen_ai.framework": "langgraph",
            "langgraph.operation": "get",
            "langgraph.thread_id": thread_id,
        },
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 1)
        print_span_info("search_memory (LangGraph get)", {
            "gen_ai.provider.name": "langchain",
            "gen_ai.memory.store.id": "langgraph-checkpointer",
            "langgraph.operation": "get",
            "langgraph.thread_id": thread_id,
            "gen_ai.memory.search.result.count": 1,
        })

    # List checkpoints
    with span_builder.search_memory_span(
        provider_name="langchain",
        store_id="langgraph-checkpointer",
        memory_type=MemoryType.EPISODIC,
        namespace=thread_id,
        extra_attributes={
            "gen_ai.framework": "langgraph",
            "langgraph.operation": "list",
            "langgraph.thread_id": thread_id,
        },
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 3)
        print_span_info("search_memory (LangGraph list)", {
            "gen_ai.provider.name": "langchain",
            "langgraph.operation": "list",
            "gen_ai.memory.search.result.count": 3,
        })

    # 6c. LlamaIndex ChatMemoryBuffer pattern
    print("\n  6c. LlamaIndex Memory Pattern (put / get)")
    print("      Simulating ChatMemoryBuffer operations...")

    # Put message
    llama_mem_id = f"llama_{uuid.uuid4().hex[:8]}"
    with span_builder.update_memory_span(
        provider_name="llamaindex",
        store_id="chat-memory-buffer",
        memory_id=llama_mem_id,
        memory_type=MemoryType.EPISODIC,
        scope=MemoryScope.SESSION,
        conversation_id="llama_conv_001",
        extra_attributes={
            "gen_ai.framework": "llamaindex",
            "llamaindex.memory_type": "ChatMemoryBuffer",
            "llamaindex.operation": "put",
            "llamaindex.message_role": "user",
        },
    ):
        print_span_info("update_memory (LlamaIndex put)", {
            "gen_ai.provider.name": "llamaindex",
            "gen_ai.memory.store.id": "chat-memory-buffer",
            "llamaindex.memory_type": "ChatMemoryBuffer",
            "llamaindex.operation": "put",
        })

    # Get history
    with span_builder.search_memory_span(
        provider_name="llamaindex",
        store_id="chat-memory-buffer",
        memory_type=MemoryType.EPISODIC,
        conversation_id="llama_conv_001",
        extra_attributes={
            "gen_ai.framework": "llamaindex",
            "llamaindex.memory_type": "ChatMemoryBuffer",
            "llamaindex.operation": "get_all",
        },
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 10)
        print_span_info("search_memory (LlamaIndex get_all)", {
            "gen_ai.provider.name": "llamaindex",
            "gen_ai.memory.store.id": "chat-memory-buffer",
            "llamaindex.operation": "get_all",
            "gen_ai.memory.search.result.count": 10,
        })

    # 6d. AutoGen Memory pattern
    print("\n  6d. AutoGen Memory Pattern (message history)")
    print("      Simulating ConversableAgent message storage...")

    autogen_conv_id = f"autogen_conv_{uuid.uuid4().hex[:8]}"
    autogen_mem_id = f"autogen_{uuid.uuid4().hex[:8]}"

    with span_builder.update_memory_span(
        provider_name="autogen",
        store_id="autogen-memory",
        memory_id=autogen_mem_id,
        memory_type=MemoryType.EPISODIC,
        scope=MemoryScope.SESSION,
        agent_id="assistant_agent",
        conversation_id=autogen_conv_id,
        extra_attributes={
            "gen_ai.framework": "autogen",
            "autogen.operation": "add_message",
            "autogen.message_role": "assistant",
            "autogen.sender": "assistant_agent",
        },
    ):
        print_span_info("update_memory (AutoGen add_message)", {
            "gen_ai.provider.name": "autogen",
            "gen_ai.memory.store.id": "autogen-memory",
            "autogen.operation": "add_message",
            "gen_ai.agent.id": "assistant_agent",
        })

    # Search messages
    with span_builder.search_memory_span(
        provider_name="autogen",
        store_id="autogen-memory",
        query="previous responses about code",
        memory_type=MemoryType.EPISODIC,
        agent_id="assistant_agent",
        conversation_id=autogen_conv_id,
        extra_attributes={
            "gen_ai.framework": "autogen",
            "autogen.operation": "search",
            "autogen.top_k": 5,
        },
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 3)
        print_span_info("search_memory (AutoGen search)", {
            "gen_ai.provider.name": "autogen",
            "autogen.operation": "search",
            "gen_ai.memory.search.result.count": 3,
        })

    # 6e. CrewAI Memory pattern
    print("\n  6e. CrewAI Memory Pattern (crew shared memory)")
    print("      Simulating Crew long-term memory operations...")

    crew_mem_id = f"crew_{uuid.uuid4().hex[:8]}"
    with span_builder.update_memory_span(
        provider_name="crewai",
        store_id="crew-long-term-memory",
        memory_id=crew_mem_id,
        memory_type=MemoryType.LONG_TERM,
        scope=MemoryScope.TEAM,
        namespace="research_crew",
        agent_id="researcher",
        content="Key finding: Market analysis shows 20% growth potential",
        importance=0.9,
        extra_attributes={
            "gen_ai.framework": "crewai",
            "crewai.operation": "save",
            "crewai.memory_type": "long_term",
            "crewai.crew_name": "research_crew",
        },
    ):
        print_span_info("update_memory (CrewAI save)", {
            "gen_ai.provider.name": "crewai",
            "gen_ai.memory.store.id": "crew-long-term-memory",
            "gen_ai.memory.type": MemoryType.LONG_TERM,
            "gen_ai.memory.scope": MemoryScope.TEAM,
            "crewai.operation": "save",
        })

    # Search crew memory
    with span_builder.search_memory_span(
        provider_name="crewai",
        store_id="crew-long-term-memory",
        query="market analysis findings",
        memory_type=MemoryType.LONG_TERM,
        namespace="research_crew",
        similarity_threshold=0.7,
        extra_attributes={
            "gen_ai.framework": "crewai",
            "crewai.operation": "search",
            "crewai.memory_type": "long_term",
        },
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 5)
        print_span_info("search_memory (CrewAI search)", {
            "gen_ai.provider.name": "crewai",
            "crewai.operation": "search",
            "gen_ai.memory.search.result.count": 5,
        })

    # 6f. Google ADK Memory pattern
    print("\n  6f. Google ADK Memory Pattern")
    print("      Simulating Agent Development Kit memory operations...")

    adk_session_id = f"adk_session_{uuid.uuid4().hex[:8]}"
    adk_mem_id = f"adk_{uuid.uuid4().hex[:8]}"

    with span_builder.update_memory_span(
        provider_name="google_adk",
        store_id="adk-memory",
        memory_id=adk_mem_id,
        memory_type=MemoryType.SEMANTIC,
        scope=MemoryScope.SESSION,
        agent_id="research_agent",
        extra_attributes={
            "gen_ai.framework": "google_adk",
            "adk.operation": "store",
            "adk.session_id": adk_session_id,
        },
    ):
        print_span_info("update_memory (Google ADK store)", {
            "gen_ai.provider.name": "google_adk",
            "gen_ai.memory.store.id": "adk-memory",
            "adk.operation": "store",
        })

    # 6g. Microsoft Azure AI Agent pattern
    print("\n  6g. Microsoft Azure AI Agent Pattern")
    print("      Simulating Azure AI Agent Service thread operations...")

    azure_thread_id = f"thread_{uuid.uuid4().hex[:24]}"
    azure_msg_id = f"msg_{uuid.uuid4().hex[:24]}"

    with span_builder.update_memory_span(
        provider_name="azure_ai",
        store_id="azure-agent-memory",
        memory_id=azure_msg_id,
        memory_type=MemoryType.EPISODIC,
        scope=MemoryScope.SESSION,
        agent_id="azure_agent_001",
        conversation_id=azure_thread_id,
        extra_attributes={
            "gen_ai.framework": "azure_ai_agent",
            "azure.operation": "add_message",
            "azure.thread_id": azure_thread_id,
            "azure.message_role": "user",
        },
    ):
        print_span_info("update_memory (Azure add_message)", {
            "gen_ai.provider.name": "azure_ai",
            "azure.operation": "add_message",
            "azure.thread_id": azure_thread_id,
        })

    # List messages
    with span_builder.search_memory_span(
        provider_name="azure_ai",
        store_id="azure-agent-memory",
        memory_type=MemoryType.EPISODIC,
        agent_id="azure_agent_001",
        conversation_id=azure_thread_id,
        extra_attributes={
            "gen_ai.framework": "azure_ai_agent",
            "azure.operation": "list_messages",
            "azure.thread_id": azure_thread_id,
        },
    ) as span:
        span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 15)
        print_span_info("search_memory (Azure list_messages)", {
            "gen_ai.provider.name": "azure_ai",
            "azure.operation": "list_messages",
            "gen_ai.memory.search.result.count": 15,
        })


def demo_nested_agent_workflow(tracer, span_builder: MemorySpanBuilder):
    """
    Demonstrate a complete nested agent workflow with memory operations.

    This shows how memory spans appear nested under an agent invocation.
    """
    print_section("7. NESTED AGENT WORKFLOW")
    print("\n  Simulating a complete agent workflow with memory operations...")

    with tracer.start_as_current_span(
        "invoke_agent CustomerSupportBot",
        kind=SpanKind.CLIENT,
        attributes={
            GenAIAttributes.OPERATION_NAME: "invoke_agent",
            GenAIAttributes.PROVIDER_NAME: "openai",
            GenAIAttributes.REQUEST_MODEL: "gpt-4",
            "server.address": "api.openai.com",
            GenAIAttributes.AGENT_NAME: "CustomerSupportBot",
            GenAIAttributes.AGENT_ID: "agent_001",
            GenAIAttributes.CONVERSATION_ID: "conv_demo_123",
        },
    ) as agent_span:
        print("\n  [invoke_agent CustomerSupportBot]")

        # Search for context
        print("    ├── search_memory (user history)")
        with span_builder.search_memory_span(
            provider_name="chroma",
            store_id="user-history",
            query="user's previous interactions",
            memory_type=MemoryType.EPISODIC,
            agent_id="agent_001",
            conversation_id="conv_demo_123",
        ) as span:
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 3)

        # Simulate LLM call
        print("    ├── chat gpt-4 (simulated)")
        with tracer.start_as_current_span(
            "chat gpt-4",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "chat",
                GenAIAttributes.PROVIDER_NAME: "openai",
                GenAIAttributes.REQUEST_MODEL: "gpt-4",
            },
        ) as llm_span:
            llm_span.set_attribute(GenAIAttributes.RESPONSE_MODEL, "gpt-4-0613")
            llm_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 150)
            llm_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 50)

        # Store the conversation
        print("    └── update_memory (store conversation)")
        with span_builder.update_memory_span(
            provider_name="chroma",
            store_id="user-history",
            memory_id=f"turn_{uuid.uuid4().hex[:8]}",
            memory_type=MemoryType.EPISODIC,
            scope=MemoryScope.SESSION,
            agent_id="agent_001",
            conversation_id="conv_demo_123",
        ):
            pass

        agent_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 200)
        agent_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 75)


def main():
    """Run the comprehensive memory spans demo."""
    print("\n" + "=" * 70)
    print("  GenAI Memory Semantic Conventions - All Spans Demo")
    print("=" * 70)
    print("""
This demo showcases all 5 memory operation spans defined in the
OpenTelemetry GenAI Memory semantic conventions:

  1. create_memory_store - Create/initialize a memory store
  2. search_memory      - Query/retrieve memories
  3. update_memory      - Create or update (upsert) memory items
  4. delete_memory      - Delete memory items
  5. delete_memory_store - Delete/deprovision a memory store
""")

    # Setup tracing
    use_otlp = os.getenv("GENAI_MEMORY_USE_OTLP", "false").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="genai-memory-spans-demo",
        use_console=True,
        use_otlp=use_otlp,
        capture_content=capture_content,
    )
    span_builder = MemorySpanBuilder(tracer, capture_content=capture_content)

    print(f"Configuration:")
    print(f"  - OTLP Export: {use_otlp}")
    print(f"  - Capture Content: {capture_content}")

    run_id = uuid.uuid4().hex[:8]
    with tracer.start_as_current_span(
        f"demo_all_memory_spans.{run_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            "demo.id": "all_memory_spans_demo",
            "demo.title": "Comprehensive GenAI Memory Spans Demo",
            "demo.run_id": run_id,
        },
    ):
        # Run all demos (nested under one trace for the viewer)
        store_id = demo_create_memory_store(span_builder)
        memory_ids = demo_update_memory(span_builder, store_id)
        demo_search_memory(span_builder, store_id)
        demo_delete_memory(span_builder, store_id, memory_ids)
        demo_delete_memory_store(span_builder, store_id)
        demo_framework_integrations(span_builder)
        demo_nested_agent_workflow(tracer, span_builder)

    # Summary
    print_section("DEMO COMPLETE")
    print("""
Summary of spans generated:

Core Memory Operations (5 operation types):
  - 3x create_memory_store spans (user, session, agent scopes)
  - 5x update_memory spans (create, merge, overwrite, expiration, team)
  - 5x search_memory spans (basic, threshold, namespace, agent, no results)
  - 4x delete_memory spans (by ID, by scope, by namespace, agent-scoped)
  - 2x delete_memory_store spans (basic, with namespace)

Framework Integrations (7 frameworks):
  - LangChain: save_context, load_memory_variables
  - LangGraph: put, get, list (checkpointer pattern)
  - LlamaIndex: put, get_all (ChatMemoryBuffer pattern)
  - AutoGen: add_message, search (ConversableAgent pattern)
  - CrewAI: save, search (long-term memory pattern)
  - Google ADK: store (session memory pattern)
  - Azure AI Agent: add_message, list_messages (thread pattern)

Nested Workflow:
  - 1x invoke_agent span with nested memory + LLM operations

Total: 35+ spans demonstrating ALL memory semantic conventions!
""")

    if use_otlp:
        print("Spans exported to OTLP collector.")
    else:
        print("Tip: Set GENAI_MEMORY_USE_OTLP=true to export to a collector.")
        print("     Set GENAI_MEMORY_CAPTURE_CONTENT=true to include content.")


if __name__ == "__main__":
    main()
