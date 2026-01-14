#!/usr/bin/env python3
"""
Story 6: User Data Lifecycle (Privacy/GDPR)

This scenario demonstrates complete GDPR "right to be forgotten" compliance:
1. Selective memory deletion (specific memory_id)
2. Bulk user data deletion (all items in user scope)
3. Delete by type (all items of a specific type)
4. Delete user's memory store (complete store removal)

Key Attributes Demonstrated:
- gen_ai.memory.scope: user (required for delete_memory)
- gen_ai.memory.id: specific item deletion
- gen_ai.memory.type: type-based deletion
- Cascading deletion traces for compliance

Memory Spans Used:
- delete_memory: Item and bulk deletion
- delete_memory_store: Store removal

Run with:
    python main.py

To export to OTLP:
    GENAI_MEMORY_USE_OTLP=true python main.py
"""

import os
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
    MemoryAttributes,
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


def run_gdpr_lifecycle_scenario():
    """
    Run the GDPR user data lifecycle scenario.

    Story: Alex is a user who exercises various GDPR rights including
    selective deletion, full account deletion, and complete data removal.
    """
    print_section("Story 6: User Data Lifecycle (Privacy/GDPR)")
    print("""
Scenario: DataAware is an AI service that takes privacy seriously.
User Alex exercises their GDPR "right to be forgotten" through
various deletion requests.

Deletion Types:
1. Selective deletion (specific memory by ID)
2. Delete by type (all items of a specific type)
3. Bulk deletion (all user data)
4. Store deletion (remove entire store)
""")

    # Setup tracing
    use_otlp = os.getenv("GENAI_MEMORY_USE_OTLP", "false").lower() == "true"
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"

    tracer = setup_tracing(
        service_name="gdpr-lifecycle-demo",
        use_console=use_console,
        use_otlp=use_otlp,
    )
    span_builder = MemorySpanBuilder(tracer, capture_content=False)

    # User parameters
    user_id = "user_alex_789"
    preferences_store_id = f"store_{user_id}_prefs"
    history_store_id = f"store_{user_id}_history"
    personal_store_id = f"store_{user_id}_personal"

    print(f"\nUser: Alex ({user_id})")
    print(f"Stores:")
    print(f"  - Preferences: {preferences_store_id}")
    print(f"  - History: {history_store_id}")
    print(f"  - Personal: {personal_store_id}")

    run_id = uuid.uuid4().hex[:8]
    with tracer.start_as_current_span(
        f"story_6.gdpr_lifecycle.{run_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            "story.id": 6,
            "story.title": "User Data Lifecycle (Privacy/GDPR)",
            "scenario.name": "progressive_deletion_and_store_removal",
            "story.run_id": run_id,
            "user.id": user_id,
            "deletion.type": "progressive",
            "gdpr.request_id": f"gdpr_{uuid.uuid4().hex[:12]}",
        },
    ):

        # Phase 1: Selective Memory Deletion
        print_section("Phase 1: Selective Memory Deletion")
        print(f"\n  Alex: 'Delete my embarrassing preference about cat videos'")

        specific_memory_id = "pref_embarrassing_001"
        with span_builder.delete_memory_span(
            provider_name="pinecone",
            store_id=preferences_store_id,
            store_name="user-preferences",
            scope=MemoryScope.USER,
            memory_id=specific_memory_id,
        ) as span:
            print_span_info("delete_memory (specific item)", {
                "gen_ai.operation.name": "delete_memory",
                "gen_ai.provider.name": "pinecone",
                "gen_ai.memory.store.id": preferences_store_id,
                "gen_ai.memory.id": specific_memory_id,
                "gen_ai.memory.scope": MemoryScope.USER,
            })

        print(f"\n  Deleted: Memory '{specific_memory_id}'")
        print("  Other preferences preserved")

        # Phase 2: Delete by Type
        print_section("Phase 2: Delete by Memory Type")
        print(f"\n  Alex: 'Delete all my short-term conversation history'")

        with span_builder.delete_memory_span(
            provider_name="chroma",
            store_id=history_store_id,
            store_name="conversation-history",
            scope=MemoryScope.USER,
            memory_type=MemoryType.SHORT_TERM,
        ) as span:
            print_span_info("delete_memory (by type)", {
                "gen_ai.operation.name": "delete_memory",
                "gen_ai.provider.name": "chroma",
                "gen_ai.memory.store.id": history_store_id,
                "gen_ai.memory.scope": MemoryScope.USER,
                "gen_ai.memory.type": MemoryType.SHORT_TERM,
            })

        print(f"\n  Deleted: All {MemoryType.SHORT_TERM} memories")
        print("  Long-term memories preserved")

        # Phase 3: Bulk User Data Deletion
        print_section("Phase 3: Bulk User Data Deletion")
        print(f"\n  Alex: 'Delete all my preference data'")

        with span_builder.delete_memory_span(
            provider_name="pinecone",
            store_id=preferences_store_id,
            store_name="user-preferences",
            scope=MemoryScope.USER,
            # No memory_id = delete all items in scope
        ) as span:
            print_span_info("delete_memory (bulk delete)", {
                "gen_ai.operation.name": "delete_memory",
                "gen_ai.provider.name": "pinecone",
                "gen_ai.memory.store.id": preferences_store_id,
                "gen_ai.memory.store.name": "user-preferences",
                "gen_ai.memory.scope": MemoryScope.USER,
                "(no memory_id)": "deletes all items",
            })

        print(f"\n  Deleted: All items in preferences store")
        print("  Store structure remains (empty)")

        # Phase 4: Delete Another Store's Data
        print_section("Phase 4: Delete History Store Data")
        print(f"\n  Alex: 'Delete all my conversation history'")

        with span_builder.delete_memory_span(
            provider_name="chroma",
            store_id=history_store_id,
            store_name="conversation-history",
            scope=MemoryScope.USER,
        ) as span:
            print_span_info("delete_memory (history store)", {
                "gen_ai.operation.name": "delete_memory",
                "gen_ai.provider.name": "chroma",
                "gen_ai.memory.store.id": history_store_id,
                "gen_ai.memory.scope": MemoryScope.USER,
            })

        print(f"\n  Deleted: All conversation history")

        # Phase 5: Delete Memory Stores
        print_section("Phase 5: Delete Memory Stores (Complete Removal)")
        print(f"\n  Alex: 'Delete my account completely - remove everything'")

        # Delete preferences store
        with span_builder.delete_memory_store_span(
            provider_name="pinecone",
            store_name="user-preferences",
            store_id=preferences_store_id,
        ) as span:
            print_span_info("delete_memory_store (preferences)", {
                "gen_ai.operation.name": "delete_memory_store",
                "gen_ai.provider.name": "pinecone",
                "gen_ai.memory.store.id": preferences_store_id,
                "gen_ai.memory.store.name": "user-preferences",
            })

        # Delete history store
        with span_builder.delete_memory_store_span(
            provider_name="chroma",
            store_name="conversation-history",
            store_id=history_store_id,
        ) as span:
            print_span_info("delete_memory_store (history)", {
                "gen_ai.operation.name": "delete_memory_store",
                "gen_ai.provider.name": "chroma",
                "gen_ai.memory.store.id": history_store_id,
                "gen_ai.memory.store.name": "conversation-history",
            })

        # Delete personal store
        with span_builder.delete_memory_store_span(
            provider_name="pinecone",
            store_name="user-personal",
            store_id=personal_store_id,
        ) as span:
            print_span_info("delete_memory_store (personal)", {
                "gen_ai.operation.name": "delete_memory_store",
                "gen_ai.provider.name": "pinecone",
                "gen_ai.memory.store.id": personal_store_id,
                "gen_ai.memory.store.name": "user-personal",
            })

        print(f"\n  Deleted stores:")
        print(f"    ✓ {preferences_store_id}")
        print(f"    ✓ {history_store_id}")
        print(f"    ✓ {personal_store_id}")
        print("\n  User Alex's data completely removed from system")

    # Show compliance trace summary
    print_section("Compliance Trace Summary")
    print("""
Cascading Deletion Trace:

  gdpr_deletion_request (user_alex_789)
  │
  ├── delete_memory (specific item)
  │   └── memory_id: pref_embarrassing_001
  │
  ├── delete_memory (by type)
  │   └── memory_type: short_term
  │
  ├── delete_memory (bulk - preferences)
  │   └── scope: user, no memory_id
  │
  ├── delete_memory (bulk - history)
  │   └── scope: user
  │
  ├── delete_memory_store (preferences)
  │   └── store_id: store_user_alex_789_prefs
  │
  ├── delete_memory_store (history)
  │   └── store_id: store_user_alex_789_history
  │
  └── delete_memory_store (personal)
      └── store_id: store_user_alex_789_personal

Compliance Verification:
  ✓ All deletion operations traced
  ✓ User scope consistently applied
  ✓ Complete store removal recorded
  ✓ Audit trail available for regulators
""")

    # Summary
    print_section("Scenario Complete!")
    print("""
Trace Summary:
  - 1x delete_memory (specific ID)
  - 1x delete_memory (by type)
  - 2x delete_memory (bulk by scope)
  - 3x delete_memory_store (complete removal)

GDPR Compliance Features:
  1. Selective Deletion: Remove specific memories by ID
  2. Type-Based Deletion: Remove all memories of a type
  3. Bulk Deletion: Remove all user data (scope-based)
  4. Store Deletion: Complete removal of user stores
  5. Audit Trail: All operations traced for compliance

Key Attributes for GDPR:
  - gen_ai.memory.scope: user (always required for delete_memory)
  - gen_ai.memory.id: specific item deletion
  - gen_ai.memory.type: type-based deletion
  - gen_ai.memory.store.id: store identification
""")

    if use_otlp:
        print("Traces exported to OTLP collector.")
    else:
        print("Tip: Set GENAI_MEMORY_USE_OTLP=true to export to a collector.")


if __name__ == "__main__":
    run_gdpr_lifecycle_scenario()
