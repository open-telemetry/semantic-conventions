#!/usr/bin/env python3
"""
GenAI Security Guardian - Run Stories and View Traces

This script provides a single command to:
1. Execute story scenarios (which emit traces to App Insights)
2. Wait for traces to be ingested
3. Launch the browser-based trace viewer

This is the main entry point for demonstrating the Security Guardian prototype.

Prerequisites:
    1. Azure App Insights with trace export configured:
       - APPLICATIONINSIGHTS_CONNECTION_STRING (for trace export)

    2. App Insights query access via Entra ID (Azure RBAC):
       - Run `az login`
       - Set APPINSIGHTS_RESOURCE_ID (recommended) or APPINSIGHTS_APP

Usage:
    # Run all stories and launch viewer:
    python run_and_view.py

    # Run specific stories:
    python run_and_view.py --story 5 7

    # Just launch viewer (no story execution):
    python run_and_view.py --viewer-only

    # Run stories without launching viewer:
    python run_and_view.py --no-viewer

    # Run with specific exporter:
    python run_and_view.py --exporters appinsights
"""

import argparse
import os
import sys
import time
import subprocess
import webbrowser
from threading import Thread
from typing import List, Optional

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_environment():
    """Load environment variables from .env.local if available."""
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
                return True
    except ImportError:
        pass
    return False


def check_credentials():
    """Check if required credentials are configured."""
    issues = []

    # Check trace export credentials
    if not os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        issues.append("APPLICATIONINSIGHTS_CONNECTION_STRING not set (required for trace export)")

    # Check query credentials (Entra ID / RBAC via Azure CLI)
    if not (
        os.environ.get("APPINSIGHTS_RESOURCE_ID")
        or os.environ.get("APPINSIGHTS_APP")
        or os.environ.get("APPINSIGHTS_APP_ID")  # legacy (may be GUID)
    ):
        issues.append("APPINSIGHTS_RESOURCE_ID not set (required for trace viewer)")

    return issues


def run_stories(story_ids: Optional[List[int]] = None, exporters: Optional[str] = None):
    """
    Run story scenarios using story_runner.py.

    Args:
        story_ids: List of story IDs to run, or None for all
        exporters: Comma-separated list of exporters
    """
    print("\n" + "=" * 70)
    print("  Phase 1: Running Story Scenarios")
    print("=" * 70)

    # Build command
    cmd = [sys.executable, "-m", "stories.story_runner"]

    if story_ids:
        cmd.extend(["--story"] + [str(s) for s in story_ids])
    else:
        cmd.append("--all")

    if exporters:
        cmd.extend(["--exporters", exporters])

    print(f"\n  Running: {' '.join(cmd)}\n")

    # Run in the prototype directory
    prototype_dir = os.path.dirname(os.path.dirname(__file__))

    result = subprocess.run(
        cmd,
        cwd=prototype_dir,
        env=os.environ.copy()
    )

    if result.returncode != 0:
        print(f"\n[WARN] Story execution returned non-zero exit code: {result.returncode}")

    return result.returncode == 0


def wait_for_ingestion(seconds: int = 10):
    """
    Wait for traces to be ingested into App Insights.

    App Insights typically has a delay of a few seconds for trace ingestion.
    """
    print("\n" + "=" * 70)
    print("  Phase 2: Waiting for Trace Ingestion")
    print("=" * 70)
    print(f"\n  Waiting {seconds} seconds for traces to be ingested into App Insights...")

    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r  {i} seconds remaining...")
        sys.stdout.flush()
        time.sleep(1)

    print("\r  Done!                          ")


def launch_viewer(port: int = 5050, background: bool = True):
    """
    Launch the trace viewer server.

    Args:
        port: Port to run on
        background: Run in background thread
    """
    print("\n" + "=" * 70)
    print("  Phase 3: Launching Trace Viewer")
    print("=" * 70)

    from stories.trace_viewer import run_server

    if background:
        # Run server in background thread
        server_thread = Thread(
            target=run_server,
            kwargs={"port": port, "open_browser_on_start": True},
            daemon=True
        )
        server_thread.start()
        print(f"\n  Trace viewer running at http://localhost:{port}")
        print("  Press Ctrl+C to stop\n")

        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nShutting down...")
    else:
        run_server(port=port, open_browser_on_start=True)


def main():
    parser = argparse.ArgumentParser(
        description="Run GenAI Security Guardian stories and launch trace viewer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_and_view.py                    # Run all stories and launch viewer
  python run_and_view.py --story 5 7        # Run specific stories
  python run_and_view.py --viewer-only      # Just launch viewer
  python run_and_view.py --no-viewer        # Run stories without viewer

Environment Variables:
  APPLICATIONINSIGHTS_CONNECTION_STRING  - For trace export
  APPINSIGHTS_RESOURCE_ID                - For trace viewer queries (Entra ID / RBAC)
  APPINSIGHTS_APP                        - Alternative identifier for `az monitor app-insights query`
        """
    )

    parser.add_argument(
        "--story", "-s",
        type=int,
        nargs="+",
        help="Story number(s) to run (e.g., --story 5 7 10)"
    )
    parser.add_argument(
        "--exporters", "-e",
        type=str,
        default="appinsights",
        help="Comma-separated exporters (default: appinsights)"
    )
    parser.add_argument(
        "--viewer-only",
        action="store_true",
        help="Skip story execution, just launch viewer"
    )
    parser.add_argument(
        "--no-viewer",
        action="store_true",
        help="Run stories without launching viewer"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=5050,
        help="Port for trace viewer (default: 5050)"
    )
    parser.add_argument(
        "--wait", "-w",
        type=int,
        default=10,
        help="Seconds to wait for trace ingestion (default: 10)"
    )
    parser.add_argument(
        "--capture-content",
        action="store_true",
        help=(
            "Opt-in to capturing sensitive GenAI content attributes on spans "
            "(gen_ai.input.messages, gen_ai.output.messages, gen_ai.security.content.*.value)."
        ),
    )
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip credential checks"
    )

    args = parser.parse_args()

    # Print banner
    print("\n" + "=" * 70)
    print("  GenAI Security Guardian - Run & View")
    print("=" * 70)

    # Load environment
    load_environment()
    if args.capture_content:
        os.environ["OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT"] = "true"
        print("[WARN] Content capture enabled (OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT=true). Do not use real secrets/PII.")

    # Check credentials
    if not args.skip_checks:
        issues = check_credentials()
        if issues:
            print("\n[WARNING] Configuration issues detected:\n")
            for issue in issues:
                print(f"  - {issue}")
            print("\n  Set these environment variables or add them to .env.local")
            print("  Use --skip-checks to bypass this warning\n")

            if not args.viewer_only:
                response = input("Continue anyway? [y/N]: ")
                if response.lower() != 'y':
                    sys.exit(1)

    # Execute workflow
    if args.viewer_only:
        # Just launch viewer
        launch_viewer(port=args.port, background=False)
    elif args.no_viewer:
        # Run stories without viewer
        success = run_stories(story_ids=args.story, exporters=args.exporters)
        sys.exit(0 if success else 1)
    else:
        # Full workflow: run stories, wait, launch viewer
        success = run_stories(story_ids=args.story, exporters=args.exporters)

        if success:
            wait_for_ingestion(seconds=args.wait)

        launch_viewer(port=args.port, background=True)


if __name__ == "__main__":
    main()
