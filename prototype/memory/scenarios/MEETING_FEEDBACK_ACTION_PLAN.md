# GenAI Memory Semantic Conventions - Meeting Feedback Action Plan

**PR:** https://github.com/open-telemetry/semantic-conventions/pull/3250
**Date:** 2026-01-26
**Status:** Addressing reviewer feedback

---

## Summary of Meeting Comments

| # | Comment | Priority | Status |
|---|---------|----------|--------|
| 1 | Need to define metrics for the operation (i.e., duration) | High | DONE |
| 2 | Is a separate span for memory operations needed or should we expand agent span with additional operation "memory"? | High | DONE |
| 3 | Can we leverage OTel DB operation? Need to identify what is unique for memory and why do we need it? | High | DONE |
| 4 | A LangChain example may be helpful | Medium | DONE |
| 5 | Can we leverage database operations in OTel instead of specific memory? Why is memory specific to gen_ai? | High | DONE |
| 6 | How different is memory from existing retrieval in gen_ai? | High | DONE |

---

## Why Memory Matters for Observability (Executive Summary)

This section provides a comprehensive answer to reviewers' questions about why memory operations warrant dedicated semantic conventions in OpenTelemetry, distinct from both database (`db.*`) and retrieval (`gen_ai.retrieval.*`) conventions.

### The Challenge: Stateful AI Systems

Unlike traditional stateless API calls, GenAI agents maintain **persistent state** across interactions. This state—called "memory"—fundamentally changes how agents behave, making observability critical for understanding, debugging, and optimizing AI systems.

### Memory vs. Database vs. Retrieval: Three-Way Comparison

| Aspect | Database (`db.*`) | Retrieval (`gen_ai.retrieval.*`) | Memory (`gen_ai.memory.*`) |
|--------|-------------------|----------------------------------|----------------------------|
| **Purpose** | Store and query data | Fetch grounding context from external sources | Manage persistent agent state |
| **Data ownership** | External system | External knowledge bases | Agent-owned context |
| **Lifecycle** | Application manages | Read-only (fetch) | Full CRUD (create, read, update, delete) |
| **Scope** | Physical (schema, database) | Data source ID | Semantic (user, session, agent, team, global) |
| **Typical use** | `SELECT * FROM users WHERE id = ?` | RAG from documentation | "What did this user tell me before?" |
| **Agent awareness** | None | None | Agent ID, conversation ID, importance scoring |
| **OTel conventions** | Stable (`db.*`) | Development (`gen_ai.retrieval.*`) | Proposed (`gen_ai.memory.*`) |

> **Note on stability:** Both `gen_ai.retrieval.*` and the proposed `gen_ai.memory.*` conventions are at **development** stability level. Memory conventions follow the same maturity path as other GenAI conventions.

### Why Not Just Use `db.*` Conventions?

Memory operations are *semantically different* from database operations:

1. **Semantic vs. Physical Scope**: Memory uses semantic isolation (user, session, agent) vs. database's physical isolation (schema, namespace)
2. **AI Context**: Memory carries `gen_ai.agent.id`, `gen_ai.conversation.id` — meaningless for databases
3. **Importance Scoring**: Memory items have `gen_ai.memory.importance` (0.0-1.0) affecting retrieval/retention
4. **Similarity Search**: Memory uses `gen_ai.memory.search.similarity.threshold` — fundamental to vector-based retrieval
5. **Memory is an Abstraction, Not a Storage System**: Memory providers vary widely in their underlying implementation—some use vector databases (Pinecone, Chroma), others use in-memory stores, key-value caches, or custom backends. Not all memory providers use a database at all, and those that do may not emit `db.*` spans. Requiring `db.*` conventions would be impossible for non-database backends and would conflate the semantic layer (memory) with the infrastructure layer (storage).

**Example contrast:**

```
# Database span (OTel db.* conventions)
db.system.name: postgresql
db.operation.name: SELECT
db.collection.name: users
db.query.text: SELECT * FROM users WHERE id = ?

# Memory span (proposed gen_ai.memory.* conventions)
gen_ai.operation.name: search_memory
gen_ai.memory.scope: user
gen_ai.memory.query: "user dietary preferences"
gen_ai.memory.search.similarity.threshold: 0.7
gen_ai.conversation.id: conv_12345
gen_ai.agent.id: support_bot
```

### Why Not Just Use `retrieval` Operation?

The existing `retrieval` operation is designed for RAG (Retrieval-Augmented Generation):

| Scenario | Use `retrieval` | Use `search_memory` |
|----------|-----------------|---------------------|
| Search product documentation | ✓ | |
| Query external API for facts | ✓ | |
| RAG from knowledge base | ✓ | |
| Find user's past preferences | | ✓ |
| Recall conversation context | | ✓ |
| Multi-agent shared state | | ✓ |

**Key differences:**

- **Retrieval** = External knowledge (read-only, agent doesn't modify source)
- **Memory** = Agent-owned state (full CRUD, stateful, lifecycle semantics)

### Key Observability Benefits

| Benefit | Without Memory Observability | With Memory Observability |
|---------|------------------------------|---------------------------|
| **Debugging** | Guess what agent "knew" | See exact memory state at failure |
| **Performance** | Can't isolate memory latency | Track `gen_ai.client.memory.operation.duration` per operation |
| **Compliance** | Manual audit trails | Automatic tracking of store/delete by scope |
| **Cost** | Hidden vector DB costs | Correlate costs with memory operations |

### Unique Attributes for GenAI Memory

These attributes capture AI-specific semantics not present in `db.*` or `retrieval`:

| Attribute | Purpose | Why unique to memory? |
|-----------|---------|----------------------|
| `gen_ai.memory.scope` | user, session, agent, team, global | Semantic isolation (not physical) |
| `gen_ai.memory.type` | short_term, long_term | Memory tier affects retention |
| `gen_ai.memory.importance` | 0.0-1.0 score | Affects retrieval ranking and retention |
| `gen_ai.memory.update.strategy` | overwrite, merge, append | Semantic merge (not SQL UPSERT) |
| `gen_ai.agent.id` | Which agent accessed memory | Multi-agent debugging |
| `gen_ai.conversation.id` | Links to conversation flow | Debug "why did agent forget?" |
| `gen_ai.memory.search.similarity.threshold` | Vector similarity cutoff | Fundamental to semantic memory |

### Recommendation: Hybrid Approach

1. Instrumentations **MAY** emit `gen_ai.memory.*` attributes for AI-specific observability
2. Instrumentations **MAY** additionally emit `db.*` attributes when the underlying storage is a database, for infrastructure-level correlation
3. Memory spans carry GenAI-specific semantic meaning that `db.*` alone cannot express
4. This approach supports memory providers that don't use databases while enabling deeper infrastructure insights for those that do

---

## Comment 1: Define Metrics for Memory Operations

### Current State
The PR defines only spans (`model/gen-ai/spans.yaml`), no metrics are defined for memory operations.

### Required Action
Add memory operation metrics to `model/gen-ai/metrics.yaml` following the existing pattern from `gen_ai.client.operation.duration`.

### Proposed Metrics

```yaml
# File: model/gen-ai/metrics.yaml (additions)

# Memory Operation Duration
- id: metric.gen_ai.client.memory.operation.duration
  type: metric
  metric_name: gen_ai.client.memory.operation.duration
  stability: development
  brief: "Duration of GenAI memory operations"
  instrument: histogram
  unit: "s"
  attributes:
    - ref: gen_ai.operation.name
      requirement_level: required
      note: >
        One of: search_memory, update_memory, delete_memory,
        create_memory_store, delete_memory_store
    - ref: gen_ai.provider.name
      requirement_level: required
    - ref: gen_ai.memory.store.name
      requirement_level: recommended
    - ref: error.type
      requirement_level:
        conditionally_required: if the operation ended in an error

# Memory Search Result Count (for monitoring retrieval quality)
- id: metric.gen_ai.client.memory.search.result.count
  type: metric
  metric_name: gen_ai.client.memory.search.result.count
  stability: development
  brief: "Number of memory items returned from search operations"
  instrument: histogram
  unit: "{item}"
  attributes:
    - ref: gen_ai.operation.name
      requirement_level: required
    - ref: gen_ai.provider.name
      requirement_level: required
    - ref: gen_ai.memory.store.name
      requirement_level: recommended
```

### Bucket Boundaries
Following existing gen_ai metrics pattern:
- Duration: `0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24, 20.48, 40.96, 81.92`
- Result count: `0, 1, 5, 10, 25, 50, 100, 250, 500, 1000`

### Files to Modify
- `model/gen-ai/metrics.yaml` - Add metric definitions
- `docs/gen-ai/gen-ai-metrics.md` - Will be auto-generated

### Acceptance Criteria
- [ ] `gen_ai.client.memory.operation.duration` metric defined
- [ ] `gen_ai.client.memory.search.result.count` metric defined
- [ ] Metrics use same attributes as spans for correlation
- [ ] `make registry-generation` passes

---

## Comment 2: Separate Span vs. Expand Agent Span

### Current State
The PR defines separate spans for each memory operation:
- `span.gen_ai.create_memory_store.client`
- `span.gen_ai.search_memory.client`
- `span.gen_ai.update_memory.client`
- `span.gen_ai.delete_memory.client`
- `span.gen_ai.delete_memory_store.client`

### Analysis

#### Option A: Separate Memory Spans (Current Approach)
**Pros:**
- Clear separation of concerns
- Memory operations can be children of agent spans
- Allows detailed timing per operation
- Consistent with database span patterns (`db.operation.name`)
- Enables dedicated metrics per operation type

**Cons:**
- More span types to maintain
- Potentially redundant if memory is always part of agent workflow

#### Option B: Expand Agent Span with `gen_ai.operation.name: memory`
**Pros:**
- Simpler model (fewer span types)
- Memory becomes "just another agent operation"

**Cons:**
- Loses granularity (can't distinguish search vs update vs delete)
- Would need sub-attributes like `gen_ai.memory.operation` anyway
- Inconsistent with database conventions which have separate operation spans

### Recommendation: Keep Separate Spans

**Justification:**
1. **Follows Database Pattern**: OTel database conventions define separate client spans per operation with `db.operation.name` distinguishing them. Memory operations follow this same pattern.

2. **Agent Span is Orchestration**: The agent span (`invoke_agent`) represents the orchestration layer. Memory operations are I/O operations that happen *within* an agent invocation, similar to how database calls happen within a service request.

3. **Trace Hierarchy**:
```
invoke_agent (agent span)
├── search_memory (memory span - retrieves context)
├── chat (inference span - LLM call)
└── update_memory (memory span - stores result)
```

4. **Enables Correlation**: Separate spans allow:
   - Duration metrics per operation type
   - Error rates per operation
   - Performance analysis (which memory operation is slow?)

### Documentation Update
Add a section to `docs/gen-ai/non-normative/memory_implementation_gen_ai_spec.md` explaining:
- Memory spans are children of agent/inference spans
- Why separate spans (not expanded agent) is the right model
- Comparison to database span patterns

### Files to Modify
- `docs/gen-ai/non-normative/memory_implementation_gen_ai_spec.md` - Add rationale section

---

## Comment 3: Leverage OTel DB Operations - What's Unique?

### Current State
Database semantic conventions define:
- `db.system.name` - Database product (postgresql, redis, etc.)
- `db.operation.name` - Operation type (SELECT, INSERT, etc.)
- `db.collection.name` - Table/collection
- `db.namespace` - Database/schema name
- `db.query.text` - The query (sanitized)

### Analysis: Memory vs Database

| Aspect | Database (OTel DB) | GenAI Memory | Unique to Memory? |
|--------|-------------------|--------------|-------------------|
| **System** | `db.system.name` (postgresql) | `gen_ai.provider.name` (pinecone, chroma) | No - same concept |
| **Operation** | `db.operation.name` (SELECT) | `gen_ai.operation.name` (search_memory) | No - same concept |
| **Target** | `db.collection.name` (users) | `gen_ai.memory.store.name` | No - same concept |
| **Query** | `db.query.text` | `gen_ai.memory.query` | No - same concept |
| **Namespace** | `db.namespace` | `gen_ai.memory.namespace` | No - same concept |
| **Scope** | N/A | `gen_ai.memory.scope` (user, session, agent) | **YES** |
| **Memory Type** | N/A | `gen_ai.memory.type` (short_term, long_term) | **YES** |
| **Importance** | N/A | `gen_ai.memory.importance` | **YES** |
| **Expiration** | TTL (Redis-specific) | `gen_ai.memory.expiration_date` | Partial |
| **Update Strategy** | N/A (UPSERT is operation) | `gen_ai.memory.update.strategy` (merge, append) | **YES** |
| **Agent Context** | N/A | `gen_ai.agent.id`, `gen_ai.conversation.id` | **YES** |
| **Similarity Search** | N/A | `gen_ai.memory.search.similarity.threshold` | **YES** |

### What's Unique to GenAI Memory?

1. **Semantic Scope** (`gen_ai.memory.scope`)
   - Database: Physical isolation (schema, database)
   - Memory: Semantic isolation (user, session, agent, team, global)
   - Memory scopes are *conceptual boundaries* for AI context, not just data partitions

2. **Memory Type** (`gen_ai.memory.type`)
   - short_term: Conversation context, ephemeral
   - long_term: Persistent user preferences, learned patterns
   - Databases don't have this semantic distinction

3. **Agent Attribution** (`gen_ai.agent.id`)
   - Which AI agent accessed/modified the memory?
   - Critical for multi-agent debugging and compliance
   - Databases don't track "who" at this semantic level

4. **Conversation Linking** (`gen_ai.conversation.id`)
   - Links memory operations to conversation flow
   - Essential for debugging "why did the agent forget?"
   - Database operations don't have this context

5. **Importance Scoring** (`gen_ai.memory.importance`)
   - Memory items have semantic importance (0.0-1.0)
   - Affects retrieval and retention decisions
   - Databases have no equivalent

6. **Similarity-Based Retrieval**
   - `gen_ai.memory.search.similarity.threshold`
   - `gen_ai.memory.search.result.count`
   - Vector similarity is fundamental to memory retrieval
   - Traditional databases use exact matching or full-text search

7. **Update Strategies** (`gen_ai.memory.update.strategy`)
   - `merge`: Combine new information with existing
   - `append`: Add to existing memory
   - `overwrite`: Replace entirely
   - Databases have UPSERT, but not semantic merge/append

### Why Not Just Use db.* Attributes?

1. **Semantic Gap**: `db.operation.name: SELECT` doesn't capture that this is a *semantic memory search* for AI context.

2. **Missing Context**: Database conventions lack agent_id, conversation_id, scope - critical for AI observability.

3. **Different Consumers**: AI engineers need memory-specific dashboards, not generic database monitoring.

4. **Correlation**: Memory operations must correlate with `gen_ai.*` spans (chat, invoke_agent), not with generic service requests.

### Recommendation

**Hybrid Approach:**
1. Memory spans ARE database operations at the infrastructure level
2. But they carry GenAI-specific semantic meaning
3. Instrumentations MAY also emit `db.*` attributes for infrastructure correlation
4. `gen_ai.memory.*` attributes provide AI-specific observability

### Documentation Update
Create a comparison table in the implementation guide showing:
- What can be reused from db.* conventions
- What's unique to gen_ai.memory.*
- When to use which

### Files to Modify
- `docs/gen-ai/non-normative/memory_implementation_gen_ai_spec.md` - Add comparison section

---

## Comment 4: LangChain Example

### Current State
The prototype uses custom instrumentation code. No LangChain-specific example exists.

### Required Action
Create a LangChain memory example showing:
1. How existing LangChain memory classes map to our conventions
2. How to instrument LangChain's `ConversationBufferMemory`, `VectorStoreRetrieverMemory`, etc.
3. Integration with `opentelemetry-instrumentation-langchain`

### LangChain Memory Classes to Cover

| LangChain Class | Maps to Operation | Key Attributes |
|-----------------|-------------------|----------------|
| `ConversationBufferMemory` | update_memory, search_memory | scope: session, type: short_term |
| `ConversationSummaryMemory` | update_memory (with merge) | scope: session, strategy: merge |
| `VectorStoreRetrieverMemory` | search_memory | similarity.threshold, result.count |
| `EntityMemory` | update_memory, search_memory | scope: user, type: long_term |

### Proposed Example Structure

```
prototype/memory/scenarios/langchain_example/
├── README.md                    # How LangChain memory maps to conventions
├── python/
│   ├── main.py                  # End-to-end LangChain example
│   ├── conversation_memory.py   # ConversationBufferMemory instrumentation
│   ├── vector_memory.py         # VectorStoreRetrieverMemory instrumentation
│   └── requirements.txt         # langchain, opentelemetry deps
```

### Example Code Outline

```python
# langchain_example/python/main.py

from langchain.memory import ConversationBufferMemory, VectorStoreRetrieverMemory
from langchain.chains import ConversationChain
from opentelemetry import trace

tracer = trace.get_tracer("langchain-memory-example")

def instrumented_memory_save(memory, inputs, outputs):
    """Wrap LangChain memory.save_context with OTel span"""
    with tracer.start_as_current_span("update_memory") as span:
        span.set_attribute("gen_ai.operation.name", "update_memory")
        span.set_attribute("gen_ai.provider.name", "langchain")
        span.set_attribute("gen_ai.memory.type", "short_term")
        span.set_attribute("gen_ai.memory.scope", "session")
        # ... call original method
        memory.save_context(inputs, outputs)

def instrumented_memory_load(memory, inputs):
    """Wrap LangChain memory.load_memory_variables with OTel span"""
    with tracer.start_as_current_span("search_memory") as span:
        span.set_attribute("gen_ai.operation.name", "search_memory")
        span.set_attribute("gen_ai.provider.name", "langchain")
        result = memory.load_memory_variables(inputs)
        span.set_attribute("gen_ai.memory.search.result.count", len(result.get("history", [])))
        return result
```

### Files to Create
- `prototype/memory/scenarios/langchain_example/README.md`
- `prototype/memory/scenarios/langchain_example/python/main.py`
- `prototype/memory/scenarios/langchain_example/python/requirements.txt`

### Files to Modify
- `prototype/memory/scenarios/README.md` - Add LangChain example to table
- `prototype/memory/scenarios/story_runner.py` - Add langchain scenario

---

## Comment 5: Why Memory Specific to GenAI?

### Core Question
Why can't we just use `db.*` conventions for memory operations?

### Answer: Memory is Semantically Different

#### 1. Memory is About AI Context, Not Data Storage

| Database Operation | Memory Operation |
|-------------------|------------------|
| Store customer record | Remember user preference |
| Query orders table | Recall relevant context |
| Update inventory count | Learn from interaction |
| Delete old logs | Forget outdated information |

Memory operations have *semantic intent* (remember, recall, learn, forget) that databases don't capture.

#### 2. Memory Operations Are AI-Native

```
# Database span
db.operation.name: SELECT
db.collection.name: users
db.query.text: SELECT * FROM users WHERE id = ?

# Memory span
gen_ai.operation.name: search_memory
gen_ai.memory.scope: user
gen_ai.memory.query: "user dietary preferences"
gen_ai.memory.search.similarity.threshold: 0.7
gen_ai.conversation.id: conv_12345
gen_ai.agent.id: support_bot
```

The memory span carries AI context (conversation, agent, similarity) that's meaningless for databases.

#### 3. Memory Crosses Multiple Storage Systems

A single "memory" might involve:
- Vector database (Pinecone) for semantic search
- Key-value store (Redis) for session state
- Document database (MongoDB) for user profiles

Memory is an *abstraction* over storage, not a storage system itself.

#### 4. Memory Has Lifecycle Semantics

- **Expiration**: Memory items expire based on semantic rules (24h session, 30d preference)
- **Importance**: Items have importance scores affecting retention
- **Scope propagation**: Deleting user scope cascades to all related items

These are AI-specific lifecycle concerns.

### Recommendation

Add a section to the spec explaining:
1. Memory as an abstraction layer over storage
2. Why gen_ai.* namespace (AI-specific observability)
3. When instrumentations should ALSO emit db.* attributes

### Files to Modify
- `docs/gen-ai/non-normative/memory_implementation_gen_ai_spec.md` - Add "Why GenAI-Specific?" section

---

## Comment 6: Memory vs Existing Retrieval

### Current State
GenAI semantic conventions already define a `retrieval` operation:
- `gen_ai.operation.name: retrieval`
- `gen_ai.retrieval.query.text`
- `gen_ai.retrieval.documents`
- `gen_ai.data_source.id`

### Analysis: Retrieval vs Memory

| Aspect | Retrieval | Memory |
|--------|-----------|--------|
| **Purpose** | Fetch grounding context from external sources | Manage persistent agent state |
| **Data Source** | External documents, knowledge bases | Agent's learned context |
| **Lifecycle** | Read-only (fetch) | Full CRUD (create, read, update, delete) |
| **Scope** | Global knowledge | User/session/agent-specific |
| **Persistence** | External system manages | Agent manages lifecycle |
| **Examples** | RAG from documentation | Remember user preferences, conversation history |

### Key Differences

#### 1. Retrieval is Read-Only, Memory is CRUD
```
# Retrieval: Only fetches
retrieval → documents

# Memory: Full lifecycle
create_memory_store → store created
search_memory → results  (like retrieval)
update_memory → item stored
delete_memory → item removed
delete_memory_store → store removed
```

#### 2. Retrieval is External, Memory is Agent-Owned
- **Retrieval**: "What does the documentation say about X?"
  - Source: External knowledge base
  - Agent doesn't modify the source

- **Memory**: "What did this user tell me before?"
  - Source: Agent's own persistent state
  - Agent creates, updates, and deletes

#### 3. Retrieval is Stateless, Memory is Stateful
- **Retrieval**: Same query → same results (assuming static docs)
- **Memory**: Results change based on prior agent interactions

#### 4. Overlap: search_memory ≈ retrieval
`search_memory` IS similar to `retrieval`:
- Both query for relevant context
- Both return results with scores
- Both use similarity thresholds

**BUT** `search_memory` operates on *agent-managed memory*, not external knowledge.

### Recommendation

#### Option A: search_memory is a Specialized Retrieval
- `search_memory` extends `retrieval` semantics
- Add `gen_ai.memory.*` attributes to distinguish
- Document that `search_memory` is "retrieval from agent memory"

#### Option B: Keep Distinct (Current Approach)
- `retrieval`: External knowledge (RAG)
- `search_memory`: Agent memory (context)
- Different operations with different attributes

### Proposed Resolution
**Keep distinct but document the relationship:**

1. **Retrieval** = Fetch from external knowledge sources (documents, APIs)
   - Use when: RAG, document search, external API calls
   - Attributes: `gen_ai.retrieval.*`, `gen_ai.data_source.id`

2. **search_memory** = Query agent's persistent memory
   - Use when: Recall user preferences, conversation history, agent state
   - Attributes: `gen_ai.memory.*`, `gen_ai.agent.id`, `gen_ai.conversation.id`

3. **When to use which:**
   | Scenario | Operation |
   |----------|-----------|
   | Search product documentation | `retrieval` |
   | Find user's past preferences | `search_memory` |
   | Query external API for facts | `retrieval` |
   | Recall conversation context | `search_memory` |
   | RAG from knowledge base | `retrieval` |
   | Multi-agent shared state | `search_memory` (team scope) |

### Files to Modify
- `docs/gen-ai/non-normative/memory_implementation_gen_ai_spec.md` - Add "Memory vs Retrieval" section

---

## PR Files Summary

### YAML Files Modified (Source of Truth)

| File | Purpose | Changes |
|------|---------|---------|
| `model/gen-ai/registry.yaml` | Attribute definitions | Added `gen_ai.memory.*` attributes |
| `model/gen-ai/spans.yaml` | Span definitions | Added memory operation spans |
| `.chloggen/gen-ai-memory-ops.yaml` | Changelog entry | New enhancement entry |

### Generated Markdown (Auto-Generated)

These files are auto-generated by `make registry-generation` from the YAML:

| File | Generated From |
|------|----------------|
| `docs/registry/attributes/gen-ai.md` | `model/gen-ai/registry.yaml` |
| `docs/gen-ai/gen-ai-spans.md` | `model/gen-ai/spans.yaml` |
| `docs/gen-ai/gen-ai-metrics.md` | `model/gen-ai/metrics.yaml` |

### Manually Written Documentation

| File | Purpose |
|------|---------|
| `docs/gen-ai/non-normative/memory_implementation_gen_ai_spec.md` | Implementation guide (non-normative) |

### Provider-Specific Docs (Updated to Include New Enum Values)

These docs render the `gen_ai.operation.name` enum, so they show the new memory operations:

- `docs/gen-ai/aws-bedrock.md`
- `docs/gen-ai/azure-ai-inference.md`
- `docs/gen-ai/openai.md`
- `docs/gen-ai/gen-ai-agent-spans.md`
- `docs/gen-ai/gen-ai-events.md`
- `docs/gen-ai/mcp.md`

---

## Action Items Checklist

### High Priority (Must Address Before Merge)

- [x] **Metrics**: Add `gen_ai.client.memory.operation.duration` metric to `model/gen-ai/metrics.yaml`
- [x] **Rationale Doc**: Add section explaining why separate spans (not expanded agent)
- [x] **DB Comparison**: Add table comparing `gen_ai.memory.*` vs `db.*` attributes
- [x] **Retrieval Comparison**: Add section explaining memory vs retrieval distinction

### Medium Priority (Strengthens Proposal)

- [x] **LangChain Example**: Create `prototype/memory/scenarios/story{1,2,3}_*/python/langchain.py`
- [x] **Why GenAI-Specific**: Add rationale section to implementation guide

### Low Priority (Nice to Have)

- [x] **Additional Metrics**: Added `gen_ai.client.memory.search.result.count` histogram
- [ ] **Mem0/MemGPT Examples**: Show mapping to other memory frameworks

---

## Next Steps

1. Update `model/gen-ai/metrics.yaml` with memory metrics
2. Expand `docs/gen-ai/non-normative/memory_implementation_gen_ai_spec.md` with:
   - Why separate spans (not expanded agent)
   - Memory vs DB comparison table
   - Memory vs Retrieval distinction
   - Why GenAI-specific namespace
3. Create LangChain example in prototype
4. Run `make registry-generation` to update generated docs
5. Request re-review from GenAI approvers

---

## References

- [OTel Database Spans](https://opentelemetry.io/docs/specs/semconv/db/database-spans/)
- [OTel Database Conventions](https://opentelemetry.io/docs/specs/semconv/db/)
- [GenAI Metrics](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-metrics.md)
- [LangChain OTel Instrumentation](https://pypi.org/project/opentelemetry-instrumentation-langchain/)
- [LangSmith OpenTelemetry](https://docs.langchain.com/langsmith/trace-with-opentelemetry)
