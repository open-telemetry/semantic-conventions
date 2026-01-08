#!/usr/bin/env python3
"""
GenAI Security Guardian Story Scenario Runner

This script provides a CLI to run specific story scenarios from prototype_story.plan.md.
Each story emits complete traces demonstrating the apply_guardrail span patterns.

Supported backends (via otel_bootstrap.py):
- Azure Application Insights
- Laminar (LMNR)
- Langfuse
- Traceloop
- Console (local debugging)

Usage:
    # Run specific story:
    python story_runner.py --story 5

    # Run multiple stories:
    python story_runner.py --story 5 7 10

    # Run all stories:
    python story_runner.py --all

    # List available stories:
    python story_runner.py --list

    # With specific exporter:
    python story_runner.py --story 5 --exporters console
"""

import argparse
import sys
import os
import time

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opentelemetry import trace


# ============================================================================
# Story Registry
# ============================================================================

STORY_REGISTRY = {
    4: {
        "title": "Enterprise RAG Access Control — Knowledge + Memory Guardrails",
        "module": "stories.story_4_enterprise_rag_access_control",
        "function": "run_enterprise_rag_scenario",
        "description": "Demonstrates knowledge_query/result and memory_store/retrieve guardrails in a RAG workflow",
        "target_types": ["knowledge_query", "knowledge_result", "memory_store", "memory_retrieve"],
        "decision_types": ["allow", "deny", "modify"],
        "key_features": ["RAG access control", "result filtering/redaction", "memory protection"],
    },
    5: {
        "title": "Multi-Tenant SaaS Platform — Tenant Isolation & SLA Monitoring",
        "module": "stories.story_5_multi_tenant",
        "function": "run_multi_tenant_scenario",
        "description": "Demonstrates per-tenant security policies with tenant.id attributes",
        "target_types": ["llm_input", "llm_output"],
        "decision_types": ["allow", "warn", "deny", "modify"],
        "key_features": ["tenant.id attribute", "per-tenant policy tracking", "SLA metrics"],
    },
    7: {
        "title": "AI Agent Orchestration — Multi-Agent Security Boundary",
        "module": "stories.story_7_multi_agent",
        "function": "run_multi_agent_scenario",
        "description": "Demonstrates nested agent spans with gen_ai.agent.id attribution",
        "target_types": ["tool_call", "tool_definition", "message"],
        "decision_types": ["allow", "warn", "audit", "deny"],
        "key_features": ["nested invoke_agent spans", "agent.id attribution", "delegation guards"],
    },
    10: {
        "title": "Progressive Jailbreak Detection — Conversation-Level Security",
        "module": "stories.story_10_progressive_jailbreak",
        "function": "run_progressive_jailbreak_scenario",
        "description": "Demonstrates conversation correlation with gen_ai.conversation.id",
        "target_types": ["llm_input"],
        "decision_types": ["allow", "warn", "deny"],
        "key_features": ["gen_ai.conversation.id correlation", "multi-turn analysis", "escalating risk scores"],
    },
    11: {
        "title": "Guardian Error Handling — Timeout + Fallback",
        "module": "stories.story_11_guardian_error_handling",
        "function": "run_guardian_error_scenario",
        "description": "Demonstrates guardian failure via error.type and a downstream fallback decision",
        "target_types": ["llm_input"],
        "decision_types": ["warn", "deny"],
        "key_features": ["error.type on apply_guardrail", "fail-open vs fail-closed policies"],
    },
}


# ============================================================================
# Tracing Setup
# ============================================================================

def setup_tracing(exporters: list = None, enable_console: bool = False):
    """Configure OpenTelemetry tracing with selected backends."""
    from otel_bootstrap import configure_tracing, ExporterType

    # Map string names to ExporterType
    exporter_map = {
        "appinsights": ExporterType.APP_INSIGHTS,
        "app_insights": ExporterType.APP_INSIGHTS,
        "azure": ExporterType.APP_INSIGHTS,
        "laminar": ExporterType.LAMINAR,
        "lmnr": ExporterType.LAMINAR,
        "langfuse": ExporterType.LANGFUSE,
        "traceloop": ExporterType.TRACELOOP,
        "console": ExporterType.CONSOLE,
    }

    selected = None
    if exporters:
        selected = []
        for name in exporters:
            if name.lower() in exporter_map:
                selected.append(exporter_map[name.lower()])
            else:
                print(f"[WARN] Unknown exporter: {name}")

    return configure_tracing(
        service_name="genai-guardian-stories",
        service_version="0.1.0",
        environment="prototype",
        exporters=selected,
        enable_console=enable_console,
        disable_batch=True,  # Immediate export for demos
    )


# ============================================================================
# Story Execution
# ============================================================================

def list_stories():
    """Print available stories."""
    print("\n" + "=" * 80)
    print("  Available Story Scenarios")
    print("=" * 80)

    for story_id, info in sorted(STORY_REGISTRY.items()):
        print(f"\n  Story {story_id}: {info['title']}")
        print(f"    {info['description']}")
        print(f"    Target Types: {', '.join(info['target_types'])}")
        print(f"    Decision Types: {', '.join(info['decision_types'])}")
        print(f"    Key Features: {', '.join(info['key_features'])}")

    print("\n" + "=" * 80)


def run_story(story_id: int, tracer_provider):
    """Run a specific story scenario."""
    if story_id not in STORY_REGISTRY:
        print(f"[ERROR] Story {story_id} not found. Use --list to see available stories.")
        return False

    info = STORY_REGISTRY[story_id]
    module_name = info["module"]
    func_name = info["function"]

    print(f"\n{'=' * 80}")
    print(f"  Running Story {story_id}: {info['title']}")
    print(f"{'=' * 80}")

    # Import and run the story
    try:
        module = __import__(module_name, fromlist=[func_name])
        run_func = getattr(module, func_name)

        # Each story function emits one-or-more scenario root spans (one trace per scenario).
        # Avoid wrapping in a "story_*" span to keep trace retrieval unambiguous.
        run_func()

        print(f"\n  [OK] Story {story_id} completed successfully!")
        return True

    except ImportError as e:
        print(f"\n  [ERROR] Failed to import story module: {e}")
        return False
    except Exception as e:
        print(f"\n  [ERROR] Story {story_id} failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_stories(tracer_provider):
    """Run all available story scenarios."""
    print("\n" + "=" * 80)
    print("  Running All Story Scenarios")
    print("=" * 80)

    results = {}
    for story_id in sorted(STORY_REGISTRY.keys()):
        success = run_story(story_id, tracer_provider)
        results[story_id] = success
        time.sleep(1)  # Allow traces to flush between stories

    # Summary
    print("\n" + "=" * 80)
    print("  Story Execution Summary")
    print("=" * 80)
    for story_id, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  Story {story_id}: {status}")

    return all(results.values())


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Run GenAI Security Guardian story scenarios"
    )
    parser.add_argument(
        "--story", "-s",
        type=int,
        nargs="+",
        help="Story number(s) to run (e.g., --story 5 7 10)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all available stories"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available stories"
    )
    parser.add_argument(
        "--exporters", "-e",
        type=str,
        help="Comma-separated list of exporters: appinsights,laminar,langfuse,traceloop,console"
    )
    parser.add_argument(
        "--console",
        action="store_true",
        help="Enable console output for debugging"
    )
    parser.add_argument(
        "--capture-content",
        action="store_true",
        help=(
            "Opt-in to capturing sensitive GenAI content attributes on spans "
            "(gen_ai.input.messages, gen_ai.output.messages, gen_ai.security.content.*.value)."
        ),
    )

    args = parser.parse_args()

    # List stories
    if args.list:
        list_stories()
        return

    # Must specify either --story or --all
    if not args.story and not args.all:
        parser.print_help()
        print("\nError: Specify --story <number> or --all to run scenarios")
        sys.exit(1)

    # Parse exporters
    exporters = None
    if args.exporters:
        exporters = [e.strip() for e in args.exporters.split(",")]

    # Load environment
    try:
        from dotenv import load_dotenv
        env_candidates = [
            os.path.join(os.path.dirname(__file__), ".env.local"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.local"),
        ]
        for env_file in env_candidates:
            if os.path.exists(env_file):
                load_dotenv(env_file)
                print(f"[OK] Loaded environment from {env_file}")
                break
    except ImportError:
        pass
    if args.capture_content:
        os.environ["OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT"] = "true"
        print("[WARN] Content capture enabled (OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT=true). Do not use real secrets/PII.")

    # Setup tracing
    print("\n" + "=" * 80)
    print("  GenAI Security Guardian - Story Scenario Runner")
    print("=" * 80)

    provider = setup_tracing(exporters, enable_console=args.console)

    # Patch GuardianTracer to use global provider
    import otel_guardian_utils
    from otel_guardian_utils import _GuardianSpanContext

    class GlobalGuardianTracer:
        """GuardianTracer that uses the global TracerProvider."""

        def __init__(self, service_name="story-guardian", service_version="0.1.0", enable_console_export=False):
            self.provider = trace.get_tracer_provider()
            self.tracer = trace.get_tracer(
                service_name,
                service_version,
                schema_url="https://opentelemetry.io/schemas/1.28.0"
            )

        def get_tracer(self):
            return self.tracer

        def add_processor(self, processor):
            pass

        @staticmethod
        def hash_content(content: str, algorithm: str = "sha256") -> str:
            import hashlib
            hash_obj = hashlib.new(algorithm)
            hash_obj.update(content.encode('utf-8'))
            return f"{algorithm}:{hash_obj.hexdigest()[:16]}..."

        def create_guardian_span(self, guardian_config, target_type, target_id=None,
                                agent_id=None, conversation_id=None):
            return _GuardianSpanContext(
                self.tracer, f"apply_guardrail {guardian_config.name}",
                guardian_config, target_type, target_id, agent_id, conversation_id
            )

        def add_security_finding(self, span, finding):
            attributes = {
                otel_guardian_utils.GEN_AI_SECURITY_RISK_CATEGORY: finding.risk_category,
                otel_guardian_utils.GEN_AI_SECURITY_RISK_SEVERITY: finding.risk_severity,
                otel_guardian_utils.GEN_AI_SECURITY_RISK_SCORE: finding.risk_score,
            }
            if finding.policy_id:
                attributes[otel_guardian_utils.GEN_AI_SECURITY_POLICY_ID] = finding.policy_id
            if finding.policy_name:
                attributes[otel_guardian_utils.GEN_AI_SECURITY_POLICY_NAME] = finding.policy_name
            if finding.policy_version:
                attributes[otel_guardian_utils.GEN_AI_SECURITY_POLICY_VERSION] = finding.policy_version
            if finding.metadata:
                attributes[otel_guardian_utils.GEN_AI_SECURITY_RISK_METADATA] = finding.metadata
            span.add_event(otel_guardian_utils.GEN_AI_SECURITY_FINDING_EVENT, attributes=attributes)

    otel_guardian_utils.GuardianTracer = GlobalGuardianTracer
    print("[OK] GuardianTracer patched to use global provider\n")

    # Run stories
    if args.all:
        success = run_all_stories(provider)
    else:
        success = True
        for story_id in args.story:
            if not run_story(story_id, provider):
                success = False
            time.sleep(1)

    # Flush traces
    print("\n" + "=" * 80)
    print("  Flushing traces to configured backends...")
    print("=" * 80)

    time.sleep(2)
    try:
        trace.get_tracer_provider().force_flush(timeout_millis=30000)
        print("\n[OK] Traces flushed successfully!")
    except Exception as e:
        print(f"\n[WARN] Flush warning: {e}")

    print("\n" + "-" * 80)
    print("Check your trace backends:")
    print("  - App Insights: dependencies | where name contains 'apply_guardrail'")
    print("  - Laminar: https://www.lmnr.ai/")
    print("  - Langfuse: https://us.cloud.langfuse.com/")
    print("  - Traceloop: https://app.traceloop.com/")
    print("-" * 80)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
