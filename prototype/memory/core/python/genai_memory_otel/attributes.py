"""
GenAI Memory Semantic Conventions - Attribute Constants

This module defines attribute constants following the proposed OpenTelemetry
semantic conventions for GenAI Memory Operations.

Reference: https://github.com/open-telemetry/semantic-conventions/issues/2664
"""

from enum import Enum
from typing import Final


# =============================================================================
# Operation Names (extending gen_ai.operation.name)
# =============================================================================

class MemoryOperationName:
    """Memory operation names for gen_ai.operation.name attribute.

    Note: `store_memory` is removed; use `update_memory` for both create and update (upsert).
    """

    SEARCH_MEMORY: Final[str] = "search_memory"
    """Search/query memories."""

    UPDATE_MEMORY: Final[str] = "update_memory"
    """Create or update (upsert) memory items. Use for both create and update operations."""

    DELETE_MEMORY: Final[str] = "delete_memory"
    """Delete memory items (by id, or by scope+namespace)."""

    CREATE_MEMORY_STORE: Final[str] = "create_memory_store"
    """Create/initialize a memory store."""

    DELETE_MEMORY_STORE: Final[str] = "delete_memory_store"
    """Delete/deprovision a memory store."""


# =============================================================================
# Memory Types (gen_ai.memory.type)
# =============================================================================

class MemoryType:
    """
    Memory type/tier classification.

    This is intentionally modeled as a free-form string to accommodate framework differences.
    Instrumentations SHOULD use low-cardinality values and document any custom values they emit.

    Common examples:
    - short_term: Current session context
    - long_term: Persistent across sessions

    Additional examples (framework-specific):
    - semantic: Facts, concepts, and knowledge
    - episodic: Past interactions and experiences
    - procedural: Rules and procedures
    - entity: Information about specific entities
    """

    SHORT_TERM: Final[str] = "short_term"
    """Current session context. Example: Recent conversation history"""

    LONG_TERM: Final[str] = "long_term"
    """Persistent across sessions. Example: User preferences, learned behaviors"""

    # Additional types (for framework compatibility)
    SEMANTIC: Final[str] = "semantic"
    """Facts, concepts, and knowledge. Example: 'User prefers dark mode'"""

    EPISODIC: Final[str] = "episodic"
    """Past interactions and experiences. Example: Previous conversation patterns"""

    PROCEDURAL: Final[str] = "procedural"
    """Rules and procedures. Example: 'Always greet in Spanish for this user'"""

    ENTITY: Final[str] = "entity"
    """Information about specific entities. Example: Customer profiles"""


# =============================================================================
# Memory Scope (gen_ai.memory.scope)
# =============================================================================

class MemoryScope:
    """
    Memory scope defines the isolation and sharing boundaries.

    Scopes determine who can access the memory:
    - user: Persists across all conversations with a user
    - session: Context within a single conversation
    - agent: Specific to an AI agent instance
    - team: Shared across multiple agents
    - global: Globally accessible

    Requirement Level:
    - Required for `create_memory_store` and `delete_memory` operations
    - Recommended for other operations
    """

    USER: Final[str] = "user"
    """Scoped to a specific user. Use for personalization."""

    SESSION: Final[str] = "session"
    """Scoped to a session/thread. Use for conversation continuity."""

    AGENT: Final[str] = "agent"
    """Scoped to a specific agent. Use for agent-specific knowledge."""

    TEAM: Final[str] = "team"
    """Shared across a team of agents. Use for multi-agent collaboration."""

    GLOBAL: Final[str] = "global"
    """Globally accessible. Use for shared knowledge bases."""


# =============================================================================
# Update Strategy (gen_ai.memory.update.strategy)
# =============================================================================

class MemoryUpdateStrategy:
    """
    Strategy used when updating memory.

    Determines how existing memory content is modified:
    - overwrite: Replace existing memory entirely
    - merge: Merge with existing memory
    - append: Append to existing memory
    """

    OVERWRITE: Final[str] = "overwrite"
    """Replace existing memory entirely."""

    MERGE: Final[str] = "merge"
    """Merge with existing memory."""

    APPEND: Final[str] = "append"
    """Append to existing memory."""


# =============================================================================
# Memory Provider Names (extending gen_ai.provider.name)
# =============================================================================

class MemoryProviderName:
    """
    Memory provider names for gen_ai.provider.name attribute.

    These extend the existing gen_ai.provider.name values to include
    memory-specific providers.
    """

    # Vector Databases
    PINECONE: Final[str] = "pinecone"
    """Pinecone managed vector database."""

    MILVUS: Final[str] = "milvus"
    """Milvus open-source vector database."""

    WEAVIATE: Final[str] = "weaviate"
    """Weaviate vector database with semantic graph."""

    CHROMA: Final[str] = "chroma"
    """Chroma local/embedded vector store."""

    REDIS: Final[str] = "redis"
    """Redis with vector search (Memorystore)."""

    MEM0: Final[str] = "mem0"
    """Mem0 AI memory layer."""

    # Framework-based memory (in-process)
    LANGCHAIN: Final[str] = "langchain"
    """LangChain in-process memory."""

    LLAMAINDEX: Final[str] = "llamaindex"
    """LlamaIndex in-process memory."""

    CREWAI: Final[str] = "crewai"
    """CrewAI agent framework memory."""

    AUTOGEN: Final[str] = "autogen"
    """Microsoft AutoGen agent framework memory."""

    GOOGLE_ADK: Final[str] = "google_adk"
    """Google Agent Development Kit memory."""

    AZURE_AI: Final[str] = "azure_ai"
    """Azure AI Agent Service memory."""


# =============================================================================
# Attribute Keys
# =============================================================================

class MemoryAttributes:
    """
    Semantic convention attribute keys for memory operations.

    These follow the gen_ai.memory.* namespace pattern.
    """

    # -------------------------------------------------------------------------
    # Memory Store Identification
    # -------------------------------------------------------------------------

    STORE_ID: Final[str] = "gen_ai.memory.store.id"
    """
    The unique identifier of the memory store.

    Type: string
    Requirement Level: conditionally_required (if applicable)
    Examples: ['ms_abc123', 'user-preferences-store']
    """

    STORE_NAME: Final[str] = "gen_ai.memory.store.name"
    """
    Human-readable name of the memory store.

    Type: string
    Requirement Level: recommended
    Examples: ['Customer Support Memory', 'Shopping Preferences']
    """

    # -------------------------------------------------------------------------
    # Memory Item Identification
    # -------------------------------------------------------------------------

    MEMORY_ID: Final[str] = "gen_ai.memory.id"
    """
    The unique identifier of a memory item.

    Type: string
    Requirement Level: conditionally_required (when returned by operation)
    Examples: ['mem_5j66UpCpwteGg4YSxUnt7lPY']
    """

    # -------------------------------------------------------------------------
    # Memory Classification
    # -------------------------------------------------------------------------

    MEMORY_TYPE: Final[str] = "gen_ai.memory.type"
    """
    The type of memory being operated on.

    Type: enum (semantic, episodic, procedural, entity, short_term, long_term)
    Requirement Level: recommended
    Examples: ['semantic', 'episodic', 'long_term']
    """

    MEMORY_SCOPE: Final[str] = "gen_ai.memory.scope"
    """
    The scope of the memory operation.

    Type: enum (user, session, agent, team, global)
    Requirement Level: recommended
    Examples: ['user', 'session', 'agent']
    """

    # -------------------------------------------------------------------------
    # Memory Content (Sensitive - Opt-In)
    # -------------------------------------------------------------------------

    MEMORY_CONTENT: Final[str] = "gen_ai.memory.content"
    """
    The content/value of the memory item.

    WARNING: This attribute may contain sensitive information including user/PII data.
    Instrumentations SHOULD NOT capture this by default.

    Type: any
    Requirement Level: opt_in
    Examples: ['{"preference": "dark_mode", "value": true}']
    """

    MEMORY_QUERY: Final[str] = "gen_ai.memory.query"
    """
    The search query used to retrieve memories.

    WARNING: This attribute may contain sensitive information.

    Type: string
    Requirement Level: opt_in
    Examples: ['user dietary preferences', 'past flight bookings']
    """

    # -------------------------------------------------------------------------
    # Memory Namespace (Multi-tenant Isolation)
    # -------------------------------------------------------------------------

    MEMORY_NAMESPACE: Final[str] = "gen_ai.memory.namespace"
    """
    Namespace for memory isolation (e.g., user_id, tenant_id).

    Type: string
    Requirement Level: conditionally_required (when memory is namespaced)
    Examples: ['user_12345', 'org_acme']
    """

    # -------------------------------------------------------------------------
    # Search Results
    # -------------------------------------------------------------------------

    SEARCH_RESULT_COUNT: Final[str] = "gen_ai.memory.search.result.count"
    """
    Number of memory items returned from a search operation.

    Type: int
    Requirement Level: recommended
    Examples: [3, 10]
    """

    SEARCH_SIMILARITY_THRESHOLD: Final[str] = "gen_ai.memory.search.similarity.threshold"
    """
    Minimum similarity score threshold used for memory search.

    Type: double
    Requirement Level: conditionally_required (when similarity filtering is used)
    Examples: [0.7, 0.85]
    """

    # -------------------------------------------------------------------------
    # Memory Lifecycle
    # -------------------------------------------------------------------------

    EXPIRATION_DATE: Final[str] = "gen_ai.memory.expiration_date"
    """
    Expiration date for the memory in ISO 8601 format.

    Type: string
    Requirement Level: conditionally_required (if expiration is set)
    Examples: ['2025-12-31', '2026-01-15T00:00:00Z']
    """

    IMPORTANCE: Final[str] = "gen_ai.memory.importance"
    """
    Importance score of the memory (0.0 to 1.0).

    Type: double
    Requirement Level: recommended
    Examples: [0.8, 0.95]
    """

    # -------------------------------------------------------------------------
    # Update Strategy
    # -------------------------------------------------------------------------

    UPDATE_STRATEGY: Final[str] = "gen_ai.memory.update.strategy"
    """
    Strategy used when updating memory.

    Type: enum (overwrite, merge, append)
    Requirement Level: recommended
    Examples: ['overwrite', 'merge']
    """


# =============================================================================
# Existing GenAI Attributes (Referenced)
# =============================================================================

class GenAIAttributes:
    """
    Existing GenAI semantic convention attributes referenced by memory operations.

    These are defined in the main gen_ai semantic conventions and are
    used alongside memory-specific attributes.
    """

    OPERATION_NAME: Final[str] = "gen_ai.operation.name"
    """The name of the operation being performed."""

    PROVIDER_NAME: Final[str] = "gen_ai.provider.name"
    """The Generative AI provider as identified by the client or server."""

    AGENT_ID: Final[str] = "gen_ai.agent.id"
    """The unique identifier of the GenAI agent."""

    AGENT_NAME: Final[str] = "gen_ai.agent.name"
    """Human-readable name of the GenAI agent."""

    CONVERSATION_ID: Final[str] = "gen_ai.conversation.id"
    """The unique identifier for a conversation (session, thread)."""

    REQUEST_MODEL: Final[str] = "gen_ai.request.model"
    """The name of the GenAI model a request is being made to."""

    RESPONSE_MODEL: Final[str] = "gen_ai.response.model"
    """The name of the model that generated the response."""

    USAGE_INPUT_TOKENS: Final[str] = "gen_ai.usage.input_tokens"
    """The number of tokens used in the GenAI input (prompt)."""

    USAGE_OUTPUT_TOKENS: Final[str] = "gen_ai.usage.output_tokens"
    """The number of tokens used in the GenAI response (completion)."""


# =============================================================================
# Error Attributes
# =============================================================================

class ErrorAttributes:
    """Error-related attributes from OTEL semantic conventions."""

    ERROR_TYPE: Final[str] = "error.type"
    """
    The type of error that occurred.

    Should match the error code returned by the provider, the canonical name
    of the exception, or another low-cardinality error identifier.
    """


# =============================================================================
# Database Attributes (for provider-specific details)
# =============================================================================

class DatabaseAttributes:
    """
    Database semantic convention attributes for memory providers.

    Memory providers are often backed by databases, and these attributes
    provide additional context about the underlying storage.
    """

    DB_SYSTEM: Final[str] = "db.system"
    """The database management system (DBMS) product."""

    DB_OPERATION: Final[str] = "db.operation"
    """The name of the operation being executed."""

    DB_NAME: Final[str] = "db.name"
    """The name of the database being accessed."""
