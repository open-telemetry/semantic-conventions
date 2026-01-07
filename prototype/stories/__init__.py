"""
GenAI Security Guardian Story Scenarios

This package contains runnable implementations of the stories described in
prototype_story.plan.md. Each story demonstrates a specific use case for
the apply_guardrail span and gen_ai.security.finding event.

Stories:
- Story 5: Multi-Tenant SaaS Platform
- Story 7: Multi-Agent Security Boundary
- Story 10: Progressive Jailbreak Detection

Usage:
    # Run from repo root:
    python prototype/stories/story_runner.py --story 5

    # Or run as a module from within `prototype/`:
    cd prototype && python -m stories.story_runner --story 5

    # Run all stories:
    python prototype/stories/story_runner.py --all

    # List available stories:
    python prototype/stories/story_runner.py --list
"""

from .story_5_multi_tenant import run_multi_tenant_scenario
from .story_7_multi_agent import run_multi_agent_scenario
from .story_10_progressive_jailbreak import run_progressive_jailbreak_scenario

__all__ = [
    "run_multi_tenant_scenario",
    "run_multi_agent_scenario",
    "run_progressive_jailbreak_scenario",
]
