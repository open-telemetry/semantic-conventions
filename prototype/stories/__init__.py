"""
GenAI Security Guardian Story Scenarios

This package contains runnable implementations of the stories described in
prototype_story.plan.md. Each story demonstrates a specific use case for
the apply_guardrail span and gen_ai.security.finding event.

Stories:
- Story 4: Enterprise RAG Access Control
- Story 5: Multi-Tenant SaaS Platform
- Story 7: Multi-Agent Security Boundary
- Story 10: Progressive Jailbreak Detection
- Story 11: Guardian Error Handling

Usage:
    # Run stories and view traces in browser:
    python prototype/stories/run_and_view.py

    # Run specific stories:
    python prototype/stories/run_and_view.py --story 5 7

    # Just launch trace viewer:
    python prototype/stories/run_and_view.py --viewer-only

    # Run all stories (without viewer):
    python prototype/stories/story_runner.py --all

    # List available stories:
    python prototype/stories/story_runner.py --list

Trace Viewer:
    The trace viewer provides a browser-based UI for visualizing live traces
    from Azure Application Insights. It shows guardian spans, security findings,
    and the hierarchical structure of traces.

    Requirements:
    - APPLICATIONINSIGHTS_CONNECTION_STRING (for trace export)
    - APPINSIGHTS_RESOURCE_ID (for querying traces via Entra ID / RBAC)
    - az login (required for trace viewer queries)
"""

__all__ = [
    "run_enterprise_rag_scenario",
    "run_multi_tenant_scenario",
    "run_multi_agent_scenario",
    "run_progressive_jailbreak_scenario",
    "run_guardian_error_scenario",
]


def __getattr__(name: str):
    # Keep package imports light so `python -m stories.story_runner` can patch
    # tracing utilities before importing story modules.
    if name == "run_enterprise_rag_scenario":
        from .story_4_enterprise_rag_access_control import run_enterprise_rag_scenario
        return run_enterprise_rag_scenario
    if name == "run_multi_tenant_scenario":
        from .story_5_multi_tenant import run_multi_tenant_scenario
        return run_multi_tenant_scenario
    if name == "run_multi_agent_scenario":
        from .story_7_multi_agent import run_multi_agent_scenario
        return run_multi_agent_scenario
    if name == "run_progressive_jailbreak_scenario":
        from .story_10_progressive_jailbreak import run_progressive_jailbreak_scenario
        return run_progressive_jailbreak_scenario
    if name == "run_guardian_error_scenario":
        from .story_11_guardian_error_handling import run_guardian_error_scenario
        return run_guardian_error_scenario
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
