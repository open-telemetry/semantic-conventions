# Story 6: User Data Lifecycle (Privacy/GDPR)

Complete GDPR "right to be forgotten" compliance demonstration, from selective deletion to full data removal.

## Narrative

**Context**: DataAware is an AI service that takes privacy seriously. They implement full GDPR compliance, including the "right to be forgotten." This story walks through the complete data lifecycle from storage to deletion.

**User Journey**: Alex is a DataAware user who exercises various deletion rights:

1. **Selective Deletion**: Delete a specific embarrassing preference
2. **Delete by Type**: Remove all short-term conversation history
3. **Bulk Deletion**: Delete all preferences data
4. **Full Removal**: Delete entire user account and all stores

## Why Memory Observability Matters

- **Deletion Verification**: Prove that data was actually deleted
- **Audit Trail**: Maintain records of deletion requests and completions
- **Cascading Deletes**: Track all stores/items affected by a deletion request

## Architecture

### Deletion Hierarchy

```mermaid
flowchart TD
    A[GDPR Deletion Request] --> B{Deletion Type?}

    B -->|Specific Item| C[delete_memory<br/>with memory_id]
    B -->|By Type| D[delete_memory<br/>with memory_type]
    B -->|All User Data| E[delete_memory<br/>scope: user]
    B -->|Full Account| F[delete_memory_store<br/>all user stores]

    C --> G[(Single Item<br/>Removed)]
    D --> H[(All Items<br/>of Type Removed)]
    E --> I[(All User Items<br/>Removed)]
    F --> J[(Stores<br/>Deleted)]

    G --> K[Audit Trace]
    H --> K
    I --> K
    J --> K
```

### GDPR Deletion Sequence

```mermaid
sequenceDiagram
    participant Alex as User Alex
    participant System as DataAware
    participant Prefs as Preferences Store
    participant History as History Store
    participant Personal as Personal Store
    participant Audit as Audit Trail

    Note over Alex: Selective Deletion

    rect rgb(255, 250, 240)
        Alex->>System: Delete specific preference
        System->>Prefs: delete_memory<br/>memory_id: pref_001
        Prefs-->>Audit: Deletion logged
    end

    Note over Alex: Delete by Type

    rect rgb(255, 250, 240)
        Alex->>System: Delete short-term history
        System->>History: delete_memory<br/>type: short_term
        History-->>Audit: Bulk deletion logged
    end

    Note over Alex: Full Account Deletion

    rect rgb(255, 240, 240)
        Alex->>System: Delete everything

        System->>Prefs: delete_memory<br/>scope: user
        Prefs-->>Audit: All items deleted

        System->>History: delete_memory<br/>scope: user
        History-->>Audit: All items deleted

        System->>Prefs: delete_memory_store
        Prefs-->>Audit: Store removed

        System->>History: delete_memory_store
        History-->>Audit: Store removed

        System->>Personal: delete_memory_store
        Personal-->>Audit: Store removed
    end

    System-->>Alex: Deletion complete
```

### Data Lifecycle State

```mermaid
stateDiagram-v2
    [*] --> Active: User creates account

    Active --> Active: update_memory (data grows)
    Active --> Active: search_memory (data accessed)

    Active --> PartialDeletion: Selective delete request

    state PartialDeletion {
        [*] --> ItemDeleted: delete_memory (id)
        [*] --> TypeDeleted: delete_memory (type)
        ItemDeleted --> [*]
        TypeDeleted --> [*]
    }

    PartialDeletion --> Active: Partial deletion complete

    Active --> BulkDeletion: Full deletion request

    state BulkDeletion {
        [*] --> ClearStores: delete_memory (scope)
        ClearStores --> RemoveStores: delete_memory_store
        RemoveStores --> [*]
    }

    BulkDeletion --> Deleted: All data removed
    Deleted --> [*]: Audit trail preserved
```

## Technical Breakdown

### Deletion Operations

| Operation | Use Case | Key Attributes |
|-----------|----------|----------------|
| `delete_memory` + `memory_id` | Delete specific item | scope, memory_id |
| `delete_memory` + `memory_type` | Delete by type | scope, memory_type |
| `delete_memory` (scope only) | Bulk delete all items | scope |
| `delete_memory_store` | Remove entire store | store_id, store_name |

### Spans Generated

| Phase | Operation | Key Attributes |
|-------|-----------|----------------|
| 1 | `delete_memory` | memory_id=pref_embarrassing_001, scope=user |
| 2 | `delete_memory` | memory_type=short_term, scope=user |
| 3 | `delete_memory` | scope=user (bulk) |
| 4 | `delete_memory` | scope=user (history store) |
| 5 | `delete_memory_store` | store_id (preferences) |
| 6 | `delete_memory_store` | store_id (history) |
| 7 | `delete_memory_store` | store_id (personal) |

### Cascading Deletion Trace

```json
{
  "trace_id": "gdpr_delete_alex_123",
  "name": "gdpr_deletion_request",
  "attributes": {
    "user.id": "user_alex_789",
    "deletion.type": "full_account",
    "gdpr.request_id": "gdpr_abc123"
  },
  "spans": [
    {
      "name": "delete_memory user-preferences",
      "attributes": {
        "gen_ai.operation.name": "delete_memory",
        "gen_ai.memory.store.id": "store_user_alex_789_prefs",
        "gen_ai.memory.id": "pref_embarrassing_001",
        "gen_ai.memory.scope": "user"
      }
    },
    {
      "name": "delete_memory conversation-history",
      "attributes": {
        "gen_ai.operation.name": "delete_memory",
        "gen_ai.memory.store.id": "store_user_alex_789_history",
        "gen_ai.memory.type": "short_term",
        "gen_ai.memory.scope": "user"
      }
    },
    {
      "name": "delete_memory_store user-preferences",
      "attributes": {
        "gen_ai.operation.name": "delete_memory_store",
        "gen_ai.memory.store.id": "store_user_alex_789_prefs"
      }
    }
  ]
}
```

## Running the Scenario

```bash
# Activate virtual environment
source ../../../.venv/bin/activate

# Run the scenario
python python/main.py

# With OTLP export for audit storage
GENAI_MEMORY_USE_OTLP=true python python/main.py
```

## Expected Output

```
======================================================================
  Story 6: User Data Lifecycle (Privacy/GDPR)
======================================================================

Scenario: DataAware is an AI service that takes privacy seriously...

======================================================================
  Phase 1: Selective Memory Deletion
======================================================================

  Alex: 'Delete my embarrassing preference about cat videos'

  [delete_memory (specific item)]
    gen_ai.operation.name: delete_memory
    gen_ai.memory.id: pref_embarrassing_001
    gen_ai.memory.scope: user

======================================================================
  Phase 5: Delete Memory Stores (Complete Removal)
======================================================================

  [delete_memory_store (preferences)]
    gen_ai.memory.store.id: store_user_alex_789_prefs
    ...

  Deleted stores:
    ✓ store_user_alex_789_prefs
    ✓ store_user_alex_789_history
    ✓ store_user_alex_789_personal

  User Alex's data completely removed from system
```

## GDPR Compliance Features

### Deletion Types

| Type | Attribute Pattern | Result |
|------|-------------------|--------|
| Selective | `scope` + `memory_id` | Single item deleted |
| By Type | `scope` + `memory_type` | All items of type deleted |
| Bulk | `scope` only | All items deleted |
| Complete | `delete_memory_store` | Store removed |

### Audit Trail Requirements

For GDPR compliance, traces should include:

1. **Request Identification**: `gdpr.request_id`
2. **User Identification**: `user.id`
3. **Deletion Scope**: `gen_ai.memory.scope`
4. **Affected Items**: `gen_ai.memory.id` (when specific)
5. **Affected Stores**: `gen_ai.memory.store.id`
6. **Timestamp**: Automatic via span timing

### Compliance Report Generation

```python
def generate_deletion_report(trace_id: str) -> dict:
    """Generate GDPR compliance report from trace."""
    return {
        "trace_id": trace_id,
        "user_id": "user_alex_789",
        "deletion_requests": [
            {"type": "specific", "memory_id": "pref_001"},
            {"type": "bulk", "scope": "user"},
        ],
        "stores_deleted": [
            "store_user_alex_789_prefs",
            "store_user_alex_789_history",
            "store_user_alex_789_personal"
        ],
        "completion_time": "2025-01-07T12:00:00Z",
        "verified": True
    }
```

## Related Stories

- [Story 2: Shopping Assistant](../story2_shopping_assistant/) - User scope deletion
- [Story 4: Multi-Tenant SaaS](../story4_multi_tenant_saas/) - Tenant offboarding
- [Story 5: Compliance Audit](../story5_compliance_audit/) - Audit trail verification
