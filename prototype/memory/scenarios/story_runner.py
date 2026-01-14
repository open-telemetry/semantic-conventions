#!/usr/bin/env python3
"""
GenAI Memory Stories - Scenario Runner

Runs the Python scenarios under `prototype/memory/scenarios/*/python/main.py`.

This is designed to be called by `run_and_view.py` so each story runs in a
fresh Python process (clean tracer provider per story).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Scenario:
    key: str
    title: str
    path: str  # relative to this file's directory


SCENARIOS: Dict[str, Scenario] = {
    "1": Scenario("1", "Story 1: Customer Support Agent", "story1_customer_support/python/main.py"),
    "2": Scenario("2", "Story 2: Shopping Assistant", "story2_shopping_assistant/python/main.py"),
    "3": Scenario("3", "Story 3: Multi-Agent Research Crew", "story3_multi_agent_research/python/main.py"),
    "4": Scenario("4", "Story 4: Multi-Tenant SaaS", "story4_multi_tenant_saas/python/main.py"),
    "5": Scenario("5", "Story 5: Compliance Audit & Debugging", "story5_compliance_audit/python/main.py"),
    "6": Scenario("6", "Story 6: GDPR Lifecycle", "story6_gdpr_lifecycle/python/main.py"),
    "demo_customer_support_agent": Scenario(
        "demo_customer_support_agent",
        "Demo: Customer Support Agent (end-to-end)",
        "customer_support_agent/python/main.py",
    ),
    "demo_all_memory_spans": Scenario(
        "demo_all_memory_spans",
        "Demo: All Memory Spans (comprehensive)",
        "all_memory_spans_demo/python/main.py",
    ),
}


def _run_script(*, scenarios_dir: str, rel_path: str, env: dict) -> bool:
    cmd = [sys.executable, os.path.join(scenarios_dir, rel_path)]
    result = subprocess.run(cmd, cwd=scenarios_dir, env=env)
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run GenAI Memory story scenarios")
    parser.add_argument("--list", "-l", action="store_true", help="List available scenarios")
    parser.add_argument(
        "--story",
        "-s",
        nargs="+",
        help="Scenario keys to run (1-6, demo_customer_support_agent, demo_all_memory_spans)",
    )
    parser.add_argument("--all", "-a", action="store_true", help="Run stories 1-6")
    parser.add_argument("--include-demos", action="store_true", help="Also run demo_customer_support_agent")
    parser.add_argument("--include-big-demo", action="store_true", help="Also run demo_all_memory_spans")
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds to sleep between scenarios (default: 1.0)")

    args = parser.parse_args()

    if args.list:
        print("\nAvailable scenarios:")
        for key, info in SCENARIOS.items():
            print(f"  - {key}: {info.title} ({info.path})")
        return

    selected: List[str] = []
    if args.story:
        selected = args.story
    elif args.all or not args.story:
        selected = ["1", "2", "3", "4", "5", "6"]

    if args.include_demos and "demo_customer_support_agent" not in selected:
        selected.append("demo_customer_support_agent")
    if args.include_big_demo and "demo_all_memory_spans" not in selected:
        selected.append("demo_all_memory_spans")

    scenarios_dir = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()

    results: Dict[str, bool] = {}

    for key in selected:
        info = SCENARIOS.get(str(key))
        if not info:
            print(f"[WARN] Unknown scenario key: {key}")
            results[str(key)] = False
            continue

        print("\n" + "=" * 80)
        print(f"Running: {info.title}")
        print("=" * 80)
        ok = _run_script(scenarios_dir=scenarios_dir, rel_path=info.path, env=env)
        results[info.key] = ok
        if not ok:
            print(f"[ERROR] Scenario failed: {info.key}")
        time.sleep(max(0.0, float(args.sleep)))

    print("\n" + "=" * 80)
    print("Scenario Execution Summary")
    print("=" * 80)
    for key, ok in results.items():
        print(f"- {key}: {'PASS' if ok else 'FAIL'}")

    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
