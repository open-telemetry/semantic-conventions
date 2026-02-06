#!/usr/bin/env python3
"""
Story 4: Enterprise Multi-Tenant SaaS

This scenario demonstrates a B2B SaaS platform with tenant isolation:
1. Tenant onboarding: Create namespaced memory store
2. Tenant-scoped search: Data isolated by namespace
3. Global knowledge search: Shared product documentation
4. Tenant offboarding: Delete entire tenant store

Key Attributes Demonstrated:
- gen_ai.memory.namespace: tenant isolation
- gen_ai.memory.scope: global (tenant stores + shared stores)
- gen_ai.memory.store.id/name: store lifecycle

Memory Spans Used:
- create_memory_store: Tenant onboarding
- search_memory: Tenant and global searches
- delete_memory_store: Tenant offboarding

Run with:
    python main.py

To export to OTLP:
    GENAI_MEMORY_USE_OTLP=true python main.py
"""

import os
import json
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
    LLMClient,
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


def run_multi_tenant_scenario():
    """
    Run the multi-tenant SaaS scenario.

    Story: CloudAssist is a B2B SaaS platform providing AI assistants
    to enterprise customers. Each tenant has isolated data via namespaces.
    """
    print_section("Story 4: Enterprise Multi-Tenant SaaS")
    print("""
Scenario: CloudAssist provides AI assistants to enterprise customers.
Each customer (tenant) has isolated data, but all tenants share access
to CloudAssist's global product documentation.

Tenant Lifecycle:
1. ACME Corp signs up - namespaced store created
2. ACME employees use the assistant (isolated data)
3. ACME employees search global product docs (shared)
4. ACME's contract ends - entire namespace deleted
""")

    # Setup tracing
    use_otlp = os.getenv("GENAI_MEMORY_USE_OTLP", "false").lower() == "true"
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="cloudassist-saas",
        use_console=use_console,
        use_otlp=use_otlp,
        capture_content=capture_content,
    )
    span_builder = MemorySpanBuilder(tracer, capture_content=capture_content)

    # Tenant parameters
    tenant_id = "acme_corp"
    tenant_namespace = f"tenant_{tenant_id}"
    tenant_store_id = f"store_tenant_{tenant_id}"
    global_store_id = "store_global_docs"
    user_id = "user_alice_acme"

    print(f"\nPlatform: CloudAssist")
    print(f"Tenant: {tenant_id}")
    print(f"Namespace: {tenant_namespace}")
    print(f"Global Docs Store: {global_store_id}")

    # Correlate this run as a single trace for the viewer.
    llm = LLMClient()
    agent_provider = llm.provider_name()
    conversation_id = f"conv_tenant_{uuid.uuid4().hex[:8]}"
    print(f"Conversation ID: {conversation_id}")

    with tracer.start_as_current_span(
        f"story_4.multi_tenant_saas.{conversation_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            "story.id": 4,
            "story.title": "Enterprise Multi-Tenant SaaS",
            "scenario.name": "tenant_isolation_and_offboarding",
            "tenant.id": tenant_id,
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ):
        with tracer.start_as_current_span(
            "invoke_agent CloudAssistant",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "invoke_agent",
                GenAIAttributes.PROVIDER_NAME: agent_provider,
                GenAIAttributes.REQUEST_MODEL: llm.model,
                "server.address": "api.openai.com",
                GenAIAttributes.AGENT_NAME: "CloudAssistant",
                GenAIAttributes.CONVERSATION_ID: conversation_id,
                "tenant.id": tenant_id,
            },
        ) as agent_span:
            agent_request = (
                "Onboard tenant ACME Corp, store tenant data with strict isolation, "
                "and later offboard by deleting all tenant memory."
            )
            if capture_content:
                agent_span.set_attribute(
                    "gen_ai.input.messages",
                    json.dumps(
                        [{"role": "user", "parts": [{"type": "text", "content": agent_request}]}],
                        ensure_ascii=False,
                    ),
                )

            # 1. Tenant Onboarding - Create namespaced store
            print_section("Step 1: Tenant Onboarding")
            print(f"\n  ACME Corp signs up for CloudAssist")

            with span_builder.create_memory_store_span(
                provider_name="pinecone",
                store_name="tenant-store",
                scope=MemoryScope.GLOBAL,
                memory_type=MemoryType.LONG_TERM,
                namespace=tenant_namespace,
            ) as span:
                span.set_attribute(MemoryAttributes.STORE_ID, tenant_store_id)
                print_span_info("create_memory_store (tenant)", {
                    "gen_ai.operation.name": "create_memory_store",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.name": "tenant-store",
                    "gen_ai.memory.store.id": tenant_store_id,
                    "gen_ai.memory.scope": MemoryScope.GLOBAL,
                    "gen_ai.memory.type": MemoryType.LONG_TERM,
                    "gen_ai.memory.namespace": tenant_namespace,
                })

            print(f"\n  Created isolated store for {tenant_id}")
            print(f"  Namespace: {tenant_namespace}")

            # 2. Tenant stores some data
            print_section("Step 2: Tenant Stores Data")
            print(f"\n  Alice (ACME) stores Q4 sales projections")

            doc_id = f"doc_{uuid.uuid4().hex[:12]}"
            with span_builder.update_memory_span(
                provider_name="pinecone",
                store_id=tenant_store_id,
                memory_id=doc_id,
                memory_type=MemoryType.LONG_TERM,
                namespace=tenant_namespace,
            ) as span:
                print_span_info("update_memory (tenant data)", {
                    "gen_ai.operation.name": "update_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": tenant_store_id,
                    "gen_ai.memory.id": doc_id,
                    "gen_ai.memory.namespace": tenant_namespace,
                })

            print("\n  Data stored in ACME's isolated namespace")

            # 3. Tenant-scoped search
            print_section("Step 3: Tenant-Scoped Search")
            print(f"\n  Alice searches for Q4 projections")

            with span_builder.search_memory_span(
                provider_name="pinecone",
                store_id=tenant_store_id,
                store_name="tenant-store",
                query="Q4 sales projections",
                memory_type=MemoryType.LONG_TERM,
                namespace=tenant_namespace,
            ) as span:
                span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 12)
                print_span_info("search_memory (tenant-scoped)", {
                    "gen_ai.operation.name": "search_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": tenant_store_id,
                    "gen_ai.memory.query": "Q4 sales projections" if capture_content else "(opt-in disabled)",
                    "gen_ai.memory.namespace": tenant_namespace,
                    "gen_ai.memory.type": MemoryType.LONG_TERM,
                    "gen_ai.memory.search.result.count": 12,
                })

            print("\n  Found 12 results (all from ACME's namespace)")
            print("  Other tenants' data is completely isolated")

            # 4. Global knowledge search (shared across tenants)
            print_section("Step 4: Global Knowledge Search")
            print(f"\n  Alice searches CloudAssist product docs (shared)")

            with span_builder.search_memory_span(
                provider_name="weaviate",
                store_id=global_store_id,
                store_name="global-docs",
                query="how to export reports",
                memory_type=MemoryType.LONG_TERM,
            ) as span:
                span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 5)
                print_span_info("search_memory (global docs)", {
                    "gen_ai.operation.name": "search_memory",
                    "gen_ai.provider.name": "weaviate",
                    "gen_ai.memory.store.id": global_store_id,
                    "gen_ai.memory.store.name": "global-docs",
                    "gen_ai.memory.query": "how to export reports" if capture_content else "(opt-in disabled)",
                    "gen_ai.memory.type": MemoryType.LONG_TERM,
                    "gen_ai.memory.search.result.count": 5,
                })

            print("\n  Found 5 results from shared product documentation")
            print("  All tenants can access global docs")

            # 5. Simulate another tenant search (shows isolation)
            print_section("Step 5: Demonstrate Tenant Isolation")
            print(f"\n  TechCo (different tenant) searches...")

            techco_namespace = "tenant_techco"
            techco_store_id = "store_tenant_techco"

            with span_builder.search_memory_span(
                provider_name="pinecone",
                store_id=techco_store_id,
                store_name="tenant-store",
                query="Q4 sales projections",
                memory_type=MemoryType.LONG_TERM,
                namespace=techco_namespace,
            ) as span:
                span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 8)
                print_span_info("search_memory (TechCo tenant)", {
                    "gen_ai.operation.name": "search_memory",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": techco_store_id,
                    "gen_ai.memory.namespace": techco_namespace,
                    "gen_ai.memory.search.result.count": 8,
                })

            print("\n  TechCo found 8 results (only their data)")
            print("  ACME's 12 results are NOT visible to TechCo")

            # 6. Tenant Offboarding - Delete store
            print_section("Step 6: Tenant Offboarding")
            print(f"\n  ACME's contract ends - deleting all their data")

            with span_builder.delete_memory_store_span(
                provider_name="pinecone",
                store_name="tenant-store",
                store_id=tenant_store_id,
                namespace=tenant_namespace,
            ) as span:
                print_span_info("delete_memory_store (offboarding)", {
                    "gen_ai.operation.name": "delete_memory_store",
                    "gen_ai.provider.name": "pinecone",
                    "gen_ai.memory.store.id": tenant_store_id,
                    "gen_ai.memory.store.name": "tenant-store",
                    "gen_ai.memory.namespace": tenant_namespace,
                })

            print(f"\n  Deleted: All data in namespace '{tenant_namespace}'")
            print("  ACME's data completely removed from platform")

            if capture_content:
                agent_span.set_attribute(
                    "gen_ai.output.messages",
                    json.dumps(
                        [
                            {
                                "role": "assistant",
                                "parts": [
                                    {
                                        "type": "text",
                                        "content": (
                                            f"Completed tenant lifecycle for {tenant_id}: onboarded store, "
                                            "verified isolation, and deleted tenant namespace on offboarding."
                                        ),
                                    }
                                ],
                            }
                        ],
                        ensure_ascii=False,
                    ),
                )

            agent_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 350)
            agent_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 120)

    # Summary
    print_section("Scenario Complete!")
    print("""
Trace Summary:
  - 1x create_memory_store (tenant onboarding with namespace)
  - 1x update_memory (tenant stores data)
  - 3x search_memory (tenant, global, other tenant)
  - 1x delete_memory_store (tenant offboarding)

Key Observability Insights:
  - Namespace attribute ensures complete tenant isolation
  - Global store has no namespace (accessible to all)
  - Tenant offboarding deletes entire namespace
  - Search result counts help verify isolation is working
  - Traces provide audit trail for compliance
""")

    if use_otlp:
        print("Traces exported to OTLP collector.")
    else:
        print("Tip: Set GENAI_MEMORY_USE_OTLP=true to export to a collector.")


if __name__ == "__main__":
    run_multi_tenant_scenario()
