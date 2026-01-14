#!/usr/bin/env python3
"""
GenAI Memory Stories - Run & View

Single command to:
1) Load credentials from an env file (default: `.env.local` next to this script)
2) Run the GenAI Memory story suite (exports traces to App Insights)
3) Wait for ingestion
4) Launch the browser-based trace viewer
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from threading import Thread
from typing import List, Optional


DEFAULT_SHARED_ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env.local")


def _load_env_file(path: str) -> bool:
    """Load KEY=VALUE lines from an env file into os.environ (best-effort)."""
    if not path or not os.path.exists(path):
        return False

    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv(path, override=False)
        print(f"[OK] Loaded environment from {path}")
        return True
    except Exception:
        # Fallback: minimal parser (no variable expansion).
        loaded = False
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[len("export ") :].strip()
                if "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if not key or key in os.environ:
                    continue
                os.environ[key] = val
                loaded = True
        if loaded:
            print(f"[OK] Loaded environment from {path} (manual parser)")
        return loaded


def check_credentials() -> List[str]:
    issues: List[str] = []

    if not os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        issues.append("APPLICATIONINSIGHTS_CONNECTION_STRING not set (required for trace export)")

    if not (
        os.environ.get("APPINSIGHTS_RESOURCE_ID")
        or os.environ.get("APPINSIGHTS_APP")
        or os.environ.get("APPINSIGHTS_APP_ID")
    ):
        issues.append("APPINSIGHTS_RESOURCE_ID not set (required for trace viewer queries)")

    if not os.environ.get("OPENAI_API_KEY"):
        issues.append("OPENAI_API_KEY not set (stories will fall back to mock LLM)")

    return issues


def run_stories(
    *,
    story_ids: Optional[List[str]] = None,
    include_demos: bool = True,
    include_big_demo: bool = False,
) -> bool:
    print("\n" + "=" * 70)
    print("  Phase 1: Running Story Scenarios")
    print("=" * 70)

    scenarios_dir = os.path.dirname(os.path.abspath(__file__))
    runner = os.path.join(scenarios_dir, "story_runner.py")

    cmd = [sys.executable, runner]

    if story_ids:
        cmd.extend(["--story"] + [str(s) for s in story_ids])
    else:
        cmd.append("--all")

    if include_demos:
        cmd.append("--include-demos")
    if include_big_demo:
        cmd.append("--include-big-demo")

    print(f"\n  Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=scenarios_dir, env=os.environ.copy())
    if result.returncode != 0:
        print(f"\n[WARN] Story execution returned non-zero exit code: {result.returncode}")
    return result.returncode == 0


def wait_for_ingestion(seconds: int = 10) -> None:
    print("\n" + "=" * 70)
    print("  Phase 2: Waiting for Trace Ingestion")
    print("=" * 70)
    print(f"\n  Waiting {seconds} seconds for traces to be ingested into App Insights...")

    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r  {i} seconds remaining...")
        sys.stdout.flush()
        time.sleep(1)

    print("\r  Done!                          ")


def launch_viewer(port: int = 5050, background: bool = True) -> None:
    print("\n" + "=" * 70)
    print("  Phase 3: Launching Trace Viewer")
    print("=" * 70)

    from trace_viewer import run_server

    if background:
        server_thread = Thread(target=run_server, kwargs={"port": port, "open_browser_on_start": True}, daemon=True)
        server_thread.start()
        print(f"\n  Trace viewer running at http://localhost:{port}")
        print("  Press Ctrl+C to stop\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nShutting down...")
    else:
        run_server(port=port, open_browser_on_start=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run GenAI Memory story scenarios and launch the App Insights trace viewer"
    )
    parser.add_argument("--env-file", type=str, default=DEFAULT_SHARED_ENV_FILE, help="Env file to load")
    parser.add_argument(
        "--story",
        "-s",
        nargs="+",
        help="Story number(s) to run (1-6) or scenario keys (see --list in story_runner.py)",
    )
    parser.add_argument(
        "--exporters",
        "-e",
        type=str,
        default="appinsights",
        help="Comma-separated exporters to use (default: appinsights)",
    )
    parser.add_argument(
        "--service-name",
        type=str,
        default="genai-memory-stories",
        help="OTEL service.name / cloud_RoleName to use (default: genai-memory-stories)",
    )
    parser.add_argument("--viewer-only", action="store_true", help="Skip story execution, just launch viewer")
    parser.add_argument("--no-viewer", action="store_true", help="Run stories without launching viewer")
    parser.add_argument("--port", "-p", type=int, default=5050, help="Port for trace viewer (default: 5050)")
    parser.add_argument("--wait", "-w", type=int, default=10, help="Seconds to wait for trace ingestion (default: 10)")
    parser.add_argument("--capture-content", action="store_true", help="Opt-in to capturing sensitive content")
    parser.add_argument("--stories-only", action="store_true", help="Do not run demos")
    parser.add_argument("--include-big-demo", action="store_true", help="Also run the comprehensive memory spans demo")
    parser.add_argument("--skip-checks", action="store_true", help="Skip credential checks")

    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("  GenAI Memory Stories - Run & View")
    print("=" * 70)

    # Load shared env (OpenAI + App Insights creds).
    _load_env_file(args.env_file)

    # Force a single service.name for easy App Insights filtering.
    os.environ["OTEL_SERVICE_NAME"] = args.service_name
    os.environ["GENAI_MEMORY_EXPORTERS"] = args.exporters
    os.environ["GENAI_MEMORY_USE_SIMPLE_PROCESSOR"] = "true"

    if args.capture_content:
        os.environ["GENAI_MEMORY_CAPTURE_CONTENT"] = "true"
        print("[WARN] Content capture enabled (GENAI_MEMORY_CAPTURE_CONTENT=true). Do not use secrets/PII.")

    if not args.skip_checks:
        issues = check_credentials()
        if issues:
            print("\n[WARNING] Configuration issues detected:\n")
            for issue in issues:
                print(f"  - {issue}")
            print("\n  Fix these in your env file or shell, or pass --skip-checks.\n")
            if not args.viewer_only:
                response = input("Continue anyway? [y/N]: ")
                if response.lower() != "y":
                    sys.exit(1)

    if args.viewer_only:
        launch_viewer(port=args.port, background=False)
        return

    include_demos = not args.stories_only

    if args.no_viewer:
        ok = run_stories(
            story_ids=args.story,
            include_demos=include_demos,
            include_big_demo=args.include_big_demo,
        )
        sys.exit(0 if ok else 1)

    ok = run_stories(
        story_ids=args.story,
        include_demos=include_demos,
        include_big_demo=args.include_big_demo,
    )
    if ok:
        wait_for_ingestion(seconds=int(args.wait))
    launch_viewer(port=args.port, background=True)


if __name__ == "__main__":
    main()
