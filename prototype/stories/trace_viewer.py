#!/usr/bin/env python3
"""
GenAI Security Guardian Trace Viewer

A Flask-based web server that provides:
1. REST API endpoints for trace data from App Insights
2. A web UI for visualizing guardian spans and security findings
3. Live polling for real-time trace updates

Usage:
    # Start the server
    python trace_viewer.py

    # Specify port
    python trace_viewer.py --port 8080

Environment Variables:
    APPINSIGHTS_RESOURCE_ID - (Recommended) Azure resource id of the App Insights component
    APPINSIGHTS_APP - Alternative identifier for `az monitor app-insights query`

    Notes:
      - Queries use Entra ID / RBAC via Azure CLI (`az login`) by default.
      - Legacy API-key mode is supported if APPINSIGHTS_API_KEY is set.
"""

import os
import sys
import json
import argparse
import webbrowser
from datetime import datetime, timezone
from threading import Timer
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stories.trace_retriever import get_retriever, TraceTree, GuardianSpan, AppInsightsTraceRetriever

# Create Flask app
app = Flask(__name__)
CORS(app)

# Global retriever instance
_retriever = None
_retriever_error = None


def get_trace_retriever():
    """Get the global trace retriever instance."""
    global _retriever, _retriever_error
    return _retriever, _retriever_error


# =============================================================================
# API Endpoints
# =============================================================================

@app.route("/api/traces", methods=["GET"])
def get_traces():
    """
    Get guardian traces from App Insights.

    Query Parameters:
        timespan: ISO 8601 duration (default: PT1H)
        story_id: Filter by story ID (optional)
        limit: Max traces to return (default: 50)
    """
    retriever, error = get_trace_retriever()
    if error:
        return jsonify({"error": error, "config_error": True}), 503
    if not retriever:
        return jsonify({"error": "Retriever not initialized"}), 500

    timespan = request.args.get("timespan", "PT1H")
    story_id = request.args.get("story_id", type=int)
    limit = request.args.get("limit", 50, type=int)

    try:
        traces = retriever.get_guardian_traces(
            timespan=timespan,
            story_id=story_id,
            limit=limit
        )
        return jsonify({
            "traces": [t.to_dict() for t in traces],
            "count": len(traces),
            "timespan": timespan,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/traces/<trace_id>", methods=["GET"])
def get_trace(trace_id: str):
    """Get a specific trace by ID."""
    retriever, error = get_trace_retriever()
    if error:
        return jsonify({"error": error, "config_error": True}), 503
    if not retriever:
        return jsonify({"error": "Retriever not initialized"}), 500

    try:
        traces = retriever.get_guardian_traces(timespan="PT24H", limit=200)
        for trace in traces:
            if trace.trace_id == trace_id:
                return jsonify(trace.to_dict())
        return jsonify({"error": "Trace not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/events", methods=["GET"])
def get_events():
    """
    Get security finding events.

    Query Parameters:
        timespan: ISO 8601 duration (default: PT1H)
        limit: Max events to return (default: 100)
    """
    retriever, error = get_trace_retriever()
    if error:
        return jsonify({"error": error, "config_error": True}), 503
    if not retriever:
        return jsonify({"error": "Retriever not initialized"}), 500

    timespan = request.args.get("timespan", "PT1H")
    limit = request.args.get("limit", 100, type=int)

    try:
        events = retriever.get_guardian_events(timespan=timespan, limit=limit)
        return jsonify({
            "events": events,
            "count": len(events),
            "timespan": timespan,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/operations", methods=["GET"])
def get_operations():
    """
    Get recent operations summary.

    Query Parameters:
        timespan: ISO 8601 duration (default: PT1H)
        limit: Max operations to return (default: 50)
    """
    retriever, error = get_trace_retriever()
    if error:
        return jsonify({"error": error, "config_error": True}), 503
    if not retriever:
        return jsonify({"error": "Retriever not initialized"}), 500

    timespan = request.args.get("timespan", "PT1H")
    limit = request.args.get("limit", 50, type=int)

    try:
        operations = retriever.get_recent_operations(timespan=timespan, limit=limit)
        return jsonify({
            "operations": operations,
            "count": len(operations),
            "timespan": timespan,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    retriever, error = get_trace_retriever()
    return jsonify({
        "status": "healthy" if retriever else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "retriever_type": type(retriever).__name__ if retriever else "None",
        "config_error": error,
    })


# =============================================================================
# Web UI
# =============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenAI Security Guardian - Trace Viewer</title>
    <style>
        :root {
            --bg-primary: #1a1a2e;
            --bg-secondary: #16213e;
            --bg-tertiary: #0f3460;
            --text-primary: #eaeaea;
            --text-secondary: #a0a0a0;
            --accent-blue: #4da6ff;
            --accent-green: #4ade80;
            --accent-yellow: #fbbf24;
            --accent-red: #f87171;
            --accent-purple: #a78bfa;
            --border-color: #2d3748;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }

        /* Header */
        .header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            font-size: 1.5rem;
            color: var(--accent-blue);
        }

        .header-controls {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .header-toggle {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.875rem;
            color: var(--text-secondary);
            user-select: none;
            cursor: pointer;
            white-space: nowrap;
        }

        .header-toggle input[type="checkbox"] {
            width: 16px;
            height: 16px;
            cursor: pointer;
            accent-color: var(--accent-blue);
        }

        .loading-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: var(--text-secondary);
            white-space: nowrap;
        }

        .spinner.spinner-small {
            width: 14px;
            height: 14px;
            border-width: 2px;
            margin: 0;
        }

        .header-controls select,
        .header-controls button {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
        }

        .header-controls button:hover {
            background: var(--accent-blue);
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-green);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Main Layout */
        .main-container {
            display: grid;
            grid-template-columns: 350px 1fr;
            height: calc(100vh - 60px);
        }

        /* Sidebar - Trace List */
        .sidebar {
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            overflow-y: auto;
        }

        .sidebar-header {
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }

        .trace-item {
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: background 0.2s;
        }

        .trace-item:hover {
            background: var(--bg-tertiary);
        }

        .trace-item.selected {
            background: var(--bg-tertiary);
            border-left: 3px solid var(--accent-blue);
        }

        .trace-item-title {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .trace-item-subtitle {
            font-size: 0.75rem;
            color: var(--text-secondary);
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
            margin-bottom: 0.25rem;
            word-break: break-word;
        }

        .trace-item-meta {
            font-size: 0.75rem;
            color: var(--text-secondary);
            display: flex;
            gap: 1rem;
        }

        .trace-item-badges {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }

        .badge {
            font-size: 0.65rem;
            padding: 0.15rem 0.5rem;
            border-radius: 9999px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .badge-allow { background: rgba(74, 222, 128, 0.2); color: var(--accent-green); }
        .badge-warn { background: rgba(251, 191, 36, 0.2); color: var(--accent-yellow); }
        .badge-deny { background: rgba(248, 113, 113, 0.2); color: var(--accent-red); }
        .badge-modify { background: rgba(167, 139, 250, 0.2); color: var(--accent-purple); }
        .badge-audit { background: rgba(77, 166, 255, 0.2); color: var(--accent-blue); }

        /* Main Content - Trace Details */
        .content {
            padding: 1.5rem;
            overflow-y: auto;
        }

        .content-header {
            margin-bottom: 1.5rem;
        }

        .content-header h2 {
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
        }

        .content-header-meta {
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        /* Span Tree */
        .span-tree {
            margin-top: 1rem;
        }

        .span-node {
            margin-bottom: 1rem;
        }

        .span-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            margin-left: var(--indent, 0);
        }

        .span-card.guardian {
            border-left: 3px solid var(--accent-blue);
        }

        .span-card.agent {
            border-left: 3px solid var(--accent-purple);
        }

        .span-card.chat {
            border-left: 3px solid var(--accent-yellow);
        }

        .span-card.root {
            border-left: 3px solid var(--accent-green);
        }

        /* Chat span tokens display */
        .token-usage {
            display: flex;
            gap: 1rem;
            padding: 0.5rem;
            background: var(--bg-tertiary);
            border-radius: 4px;
            font-size: 0.75rem;
            margin-top: 0.5rem;
        }

        .token-usage-item {
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .token-label {
            color: var(--text-secondary);
        }

        .token-value {
            font-family: 'Monaco', 'Menlo', monospace;
            font-weight: 600;
        }

        .token-value.input { color: var(--accent-blue); }
        .token-value.output { color: var(--accent-green); }

        /* Opt-in content display */
        details.sensitive-content {
            margin-top: 0.75rem;
            background: var(--bg-tertiary);
            border: 1px dashed var(--border-color);
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
        }

        details.sensitive-content summary {
            cursor: pointer;
            color: var(--text-secondary);
            font-size: 0.75rem;
            text-transform: uppercase;
            user-select: none;
        }

        .message-section {
            margin-top: 0.75rem;
        }

        .message-section-title {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .message-row {
            display: flex;
            gap: 0.5rem;
            margin-top: 0.35rem;
            align-items: flex-start;
        }

        .message-role {
            min-width: 90px;
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            padding-top: 0.35rem;
        }

        .message-content {
            flex: 1;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.75rem;
            white-space: pre-wrap;
            word-break: break-word;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.5rem 0.6rem;
        }

        .span-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
        }

        .span-name {
            font-weight: 600;
            font-size: 0.95rem;
        }

        .span-duration {
            font-size: 0.75rem;
            color: var(--text-secondary);
            background: var(--bg-tertiary);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }

        .span-attributes {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 0.75rem;
            font-size: 0.8rem;
        }

        .span-attr {
            background: var(--bg-tertiary);
            padding: 0.5rem;
            border-radius: 4px;
        }

        .span-attr-key {
            color: var(--text-secondary);
            font-size: 0.7rem;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .span-attr-value {
            font-family: 'Monaco', 'Menlo', monospace;
            word-break: break-all;
        }

        /* Findings Section */
        .findings-section {
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }

        .findings-header {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .finding-card {
            background: var(--bg-tertiary);
            border-radius: 6px;
            padding: 0.75rem;
            margin-top: 0.5rem;
        }

        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .finding-category {
            font-weight: 600;
            font-size: 0.85rem;
        }

        .finding-score {
            font-size: 0.75rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
        }

        .score-low { background: rgba(74, 222, 128, 0.2); color: var(--accent-green); }
        .score-medium { background: rgba(251, 191, 36, 0.2); color: var(--accent-yellow); }
        .score-high { background: rgba(248, 113, 113, 0.2); color: var(--accent-red); }
        .score-critical { background: rgba(248, 113, 113, 0.4); color: #ff6b6b; }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-secondary);
        }

        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        /* Config Error */
        .config-error {
            padding: 1.5rem;
            color: var(--text-secondary);
        }

        .config-error-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .config-error h3 {
            color: var(--accent-yellow);
            margin-bottom: 0.75rem;
        }

        .config-error p {
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }

        .config-code {
            background: var(--bg-tertiary);
            border-radius: 6px;
            padding: 0.75rem;
            margin: 0.75rem 0;
        }

        .config-code code {
            display: block;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.75rem;
            color: var(--accent-green);
            margin: 0.25rem 0;
        }

        .config-steps {
            background: var(--bg-tertiary);
            border-radius: 6px;
            padding: 0.75rem;
            margin: 0.75rem 0;
            font-size: 0.8rem;
        }

        .config-steps ol {
            margin-left: 1.25rem;
            margin-top: 0.5rem;
        }

        .config-steps li {
            margin: 0.25rem 0;
        }

        .config-note {
            font-style: italic;
            color: var(--accent-blue);
            margin-top: 1rem;
        }

        /* Loading */
        .loading {
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
        }

        .spinner {
            width: 30px;
            height: 30px;
            border: 3px solid var(--border-color);
            border-top-color: var(--accent-blue);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Tabs */
        .tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }

        .tab {
            padding: 0.5rem 1rem;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .tab:hover {
            color: var(--text-primary);
            background: var(--bg-tertiary);
        }

        .tab.active {
            color: var(--accent-blue);
            background: var(--bg-tertiary);
        }

        /* JSON View */
        .json-view {
            background: var(--bg-tertiary);
            border-radius: 8px;
            padding: 1rem;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.8rem;
            overflow-x: auto;
            white-space: pre-wrap;
            max-height: 500px;
            overflow-y: auto;
        }

        .json-key { color: var(--accent-purple); }
        .json-string { color: var(--accent-green); }
        .json-number { color: var(--accent-yellow); }
        .json-boolean { color: var(--accent-blue); }
        .json-null { color: var(--accent-red); }
    </style>
</head>
<body>
    <header class="header">
        <h1>GenAI Security Guardian - Trace Viewer</h1>
        <div class="header-controls">
            <select id="timespan-select">
                <option value="PT15M">Last 15 minutes</option>
                <option value="PT1H" selected>Last 1 hour</option>
                <option value="PT6H">Last 6 hours</option>
                <option value="PT24H">Last 24 hours</option>
                <option value="P7D">Last 7 days</option>
            </select>
            <select id="story-filter">
                <option value="">All Stories</option>
                <option value="4">Story 4: RAG + Memory</option>
                <option value="5">Story 5: Multi-Tenant</option>
                <option value="7">Story 7: Multi-Agent</option>
                <option value="10">Story 10: Jailbreak</option>
                <option value="11">Story 11: Guardian Errors</option>
            </select>
            <label class="header-toggle" title="Toggle display of apply_guardrail spans and security findings">
                <input type="checkbox" id="toggle-security" checked>
                Show security spans
            </label>
            <div class="loading-indicator" id="loading-indicator" style="display: none;" aria-live="polite">
                <div class="spinner spinner-small"></div>
                <span>Querying App Insights…</span>
            </div>
            <button onclick="refreshTraces()" id="refresh-button">Refresh</button>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span id="status-text">Connected</span>
            </div>
        </div>
    </header>

    <div class="main-container">
        <aside class="sidebar">
            <div class="sidebar-header">Traces</div>
            <div id="trace-list">
                <div class="loading">
                    <div class="spinner"></div>
                    Loading traces...
                </div>
            </div>
        </aside>

        <main class="content">
            <div id="trace-details">
                <div class="empty-state">
                    <div class="empty-state-icon">📊</div>
                    <h3>Select a trace to view details</h3>
                    <p>Choose a trace from the sidebar to see guardian spans and security findings.</p>
                </div>
            </div>
        </main>
    </div>

	    <script>
	        // State
	        const FETCH_ALL_TIMESPAN = 'P7D';
	        const FETCH_ALL_LIMIT = 500;
	        const TIMESPAN_MS = {
	            'PT15M': 15 * 60 * 1000,
	            'PT1H': 60 * 60 * 1000,
	            'PT6H': 6 * 60 * 60 * 1000,
	            'PT24H': 24 * 60 * 60 * 1000,
	            'P7D': 7 * 24 * 60 * 60 * 1000,
	        };

	        let allTraces = [];
	        let traces = [];
	        let selectedTrace = null;
	        let pollInterval = null;
	        let showSecuritySpans = true;
	        let isLoading = false;
	        let fetchInFlight = false;

	        function setLoading(loading) {
	            isLoading = Boolean(loading);
	            const indicator = document.getElementById('loading-indicator');
	            if (indicator) {
	                indicator.style.display = isLoading ? 'flex' : 'none';
	            }

	            const refreshButton = document.getElementById('refresh-button');
	            if (refreshButton) {
	                refreshButton.disabled = isLoading;
	            }
	        }

	        function applyUiFilters() {
	            const storyFilter = document.getElementById('story-filter').value;
	            const timespanFilter = document.getElementById('timespan-select').value;
	            const windowMs = TIMESPAN_MS[timespanFilter] ?? TIMESPAN_MS['PT1H'];
	            const cutoff = Date.now() - windowMs;

	            const filtered = (allTraces || []).filter(t => {
	                const storyId = t?.metadata?.story_id;
	                const matchesStory = !storyFilter || String(storyId) === String(parseInt(storyFilter, 10));

	                const start = Date.parse(t?.metadata?.start_time || t?.root_span?.start_time || '');
	                const matchesTime = !Number.isFinite(start) ? true : start >= cutoff;

	                return matchesStory && matchesTime;
	            });

	            filtered.sort((a, b) => {
	                const aTime = Date.parse(a?.metadata?.start_time || '') || 0;
	                const bTime = Date.parse(b?.metadata?.start_time || '') || 0;
	                return bTime - aTime; // newest first
	            });

	            traces = filtered;

	            if (selectedTrace && !traces.some(t => t.trace_id === selectedTrace.trace_id)) {
	                selectedTrace = null;
	            }
	        }

        // API Functions
        async function fetchTraces() {
            if (fetchInFlight) {
                return;
            }
            fetchInFlight = true;
            setLoading(true);
            renderTraceList();

            const selectedTraceId = selectedTrace?.trace_id || null;
            const url = `/api/traces?timespan=${FETCH_ALL_TIMESPAN}&limit=${FETCH_ALL_LIMIT}`;

            try {
                const response = await fetch(url);
                const data = await response.json();

                if (data.config_error) {
                    showConfigError(data.error);
                    updateStatus('Not Configured', false);
                    return;
                }

                if (data.error) {
                    throw new Error(data.error);
                }

                allTraces = data.traces || [];
                selectedTrace = selectedTraceId ? allTraces.find(t => t.trace_id === selectedTraceId) : null;

                applyUiFilters();
                renderTraceList();
                renderTraceDetails();
                updateStatus('Connected', true);
            } catch (error) {
                console.error('Failed to fetch traces:', error);
                updateStatus('Error: ' + error.message, false);
            } finally {
                fetchInFlight = false;
                setLoading(false);
            }
        }

        function showConfigError(errorMessage) {
            const container = document.getElementById('trace-list');
            container.innerHTML = `
                <div class="config-error">
                    <div class="config-error-icon">⚠️</div>
                    <h3>App Insights Not Configured</h3>
                    <p>Set the following environment variables:</p>
                    <div class="config-code">
                        <code>az login</code>
                        <code>export APPINSIGHTS_RESOURCE_ID=/subscriptions/&lt;sub&gt;/resourceGroups/&lt;rg&gt;/providers/Microsoft.Insights/components/&lt;name&gt;</code>
                    </div>
                    <div class="config-steps">
                        <strong>To find these values:</strong>
                        <ol>
                            <li>Go to Azure Portal</li>
                            <li>Navigate to your Application Insights resource</li>
                            <li>Copy the Resource ID from the Overview page (or JSON view)</li>
                            <li>Ensure your identity has access (e.g., Monitoring Reader)</li>
                        </ol>
                    </div>
                    <p class="config-note">Restart the server after setting environment variables.</p>
                </div>
            `;

            const detailsContainer = document.getElementById('trace-details');
            detailsContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📡</div>
                    <h3>Live Traces from App Insights</h3>
                    <p>This viewer displays real-time traces from Azure Application Insights.</p>
                    <p>Configure your App Insights credentials to see live guardian traces.</p>
                </div>
            `;
        }

        // Render Functions
        function renderTraceList() {
            const container = document.getElementById('trace-list');

            if (isLoading && (!allTraces || allTraces.length === 0)) {
                container.innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        Loading traces...
                    </div>
                `;
                return;
            }

            if (traces.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">🔍</div>
                        <p>No traces found</p>
                        <p style="font-size: 0.8rem">Try adjusting the time range or run some stories</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = traces.map(trace => {
                const isSelected = selectedTrace && selectedTrace.trace_id === trace.trace_id;
                const title = trace.metadata?.story_title || 'Unknown Trace';
                const subtitle = trace.metadata?.root_span_name || trace.root_span?.name || trace.metadata?.scenario_name || '';
                const spanCount = trace.spans?.length || 0;
                const guardianSpans = trace.spans?.filter(s => s.name?.includes('apply_guardrail')) || [];

                // Collect unique decisions
                const decisions = [...new Set(guardianSpans.map(s => s.decision).filter(Boolean))];

                return `
                    <div class="trace-item ${isSelected ? 'selected' : ''}"
                         onclick="selectTrace('${trace.trace_id}')">
                        <div class="trace-item-title">${escapeHtml(title)}</div>
                        ${subtitle ? `<div class="trace-item-subtitle">${escapeHtml(subtitle)}</div>` : ''}
                        <div class="trace-item-meta">
                            <span>${spanCount} spans</span>
                            <span>${guardianSpans.length} guardians</span>
                        </div>
                        <div class="trace-item-badges">
                            ${decisions.map(d => `<span class="badge badge-${d}">${d}</span>`).join('')}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function selectTrace(traceId) {
            selectedTrace = traces.find(t => t.trace_id === traceId);
            renderTraceList();
            renderTraceDetails();
        }

        function renderTraceDetails() {
            const container = document.getElementById('trace-details');

            if (!selectedTrace) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📊</div>
                        <h3>Select a trace to view details</h3>
                    </div>
                `;
                return;
            }

            const title = selectedTrace.metadata?.story_title || 'Trace Details';
            const scenarioName = selectedTrace.metadata?.scenario_name;
            const rootSpanName = selectedTrace.metadata?.root_span_name || selectedTrace.root_span?.name;
            const conversationId = selectedTrace.metadata?.conversation_id;
            const tenantId = selectedTrace.metadata?.tenant_id;
            const startTime = selectedTrace.metadata?.start_time;
            const formattedTime = startTime ? formatLocalTime(startTime) : 'Unknown';

            container.innerHTML = `
                <div class="content-header">
                    <h2>${escapeHtml(title)}</h2>
                    <div class="content-header-meta">
                        ${scenarioName ? `Scenario: ${escapeHtml(scenarioName)}<br>` : ''}
                        ${tenantId ? `Tenant: ${escapeHtml(tenantId)}<br>` : ''}
                        ${conversationId ? `Conversation ID: ${escapeHtml(conversationId)}<br>` : ''}
                        ${rootSpanName ? `Root span: ${escapeHtml(rootSpanName)}<br>` : ''}
                        Trace ID: ${selectedTrace.trace_id}<br>
                        Time: ${formattedTime}
                    </div>
                </div>

                <div class="tabs">
                    <button class="tab active" onclick="showTab('spans')">Spans</button>
                    <button class="tab" onclick="showTab('json')">Raw JSON</button>
                </div>

                <div id="tab-content-spans" class="span-tree">
                    ${renderSpanTree(selectedTrace.spans)}
                </div>

                <div id="tab-content-json" style="display: none;">
                    <div class="json-view">${syntaxHighlight(JSON.stringify(selectedTrace, null, 2))}</div>
                </div>
            `;
        }

	        function renderSpanTree(spans) {
	            if (!spans || spans.length === 0) {
	                return '<div class="empty-state">No spans found</div>';
	            }

	            // Apply global span filters (e.g., hide security spans)
	            const fullSpanMap = new Map(spans.map(s => [s.span_id, s]));

	            function isSecuritySpan(span) {
	                return span?.name?.includes('apply_guardrail') || span?.operation_name === 'apply_guardrail';
	            }

	            function isSpanVisible(span) {
	                return showSecuritySpans || !isSecuritySpan(span);
	            }

	            const parentCache = new Map();
	            function findVisibleParentId(span) {
	                if (!span) return null;
	                if (parentCache.has(span.span_id)) {
	                    return parentCache.get(span.span_id);
	                }

	                let parentId = span.parent_span_id;
	                while (parentId) {
	                    const parent = fullSpanMap.get(parentId);
	                    if (!parent) {
	                        parentCache.set(span.span_id, null);
	                        return null;
	                    }
	                    if (isSpanVisible(parent)) {
	                        parentCache.set(span.span_id, parentId);
	                        return parentId;
	                    }
	                    parentId = parent.parent_span_id;
	                }

	                parentCache.set(span.span_id, null);
	                return null;
	            }

	            function parseTurnIndex(spanName) {
	                if (!spanName) return null;
	                const match = /^turn_(\d+)$/.exec(spanName);
	                if (!match) return null;
	                const idx = Number(match[1]);
	                return Number.isFinite(idx) ? idx : null;
	            }

	            function spanSortKey(span) {
	                const turnIdx = parseTurnIndex(span?.name);
	                const ts = Date.parse(span?.start_time || '');
	                const timeKey = Number.isFinite(ts) ? ts : null;
	                return { turnIdx, timeKey, name: span?.name || '' };
	            }

	            function compareSpans(a, b) {
	                const aKey = spanSortKey(a);
	                const bKey = spanSortKey(b);

	                if (aKey.turnIdx !== null && bKey.turnIdx !== null) {
	                    return aKey.turnIdx - bKey.turnIdx;
	                }

	                // Otherwise sort chronologically (oldest -> newest).
	                if (aKey.timeKey !== null && bKey.timeKey !== null) {
	                    if (aKey.timeKey !== bKey.timeKey) return aKey.timeKey - bKey.timeKey;
	                } else if (aKey.timeKey !== null) {
	                    return -1;
	                } else if (bKey.timeKey !== null) {
	                    return 1;
	                }

	                return aKey.name.localeCompare(bKey.name);
	            }

	            const visibleSpans = spans.filter(isSpanVisible).slice().sort(compareSpans);

	            // Build parent-child relationships
	            const spanMap = new Map(visibleSpans.map(s => [s.span_id, s]));
	            const children = new Map();

	            visibleSpans.forEach(span => {
	                const visibleParentId = findVisibleParentId(span);
	                if (!visibleParentId) return;
	                if (!children.has(visibleParentId)) {
	                    children.set(visibleParentId, []);
	                }
	                children.get(visibleParentId).push(span);
	            });

	            // Ensure stable, predictable ordering (turn_1, turn_2, ...).
	            for (const [parentId, childList] of children.entries()) {
	                childList.sort(compareSpans);
	                children.set(parentId, childList);
	            }

	            // Find root spans
	            const rootSpans = visibleSpans.filter(s => !findVisibleParentId(s)).sort(compareSpans);

	            function renderSpan(span, depth = 0) {
	                const isGuardian = span.name?.includes('apply_guardrail');
	                const isAgent = span.name?.includes('invoke_agent') || span.name?.includes('create_agent');
	                const isChat = span.name?.startsWith('chat ') || span.operation_name === 'chat';
	                const cardClass = isGuardian ? 'guardian' : (isAgent ? 'agent' : (isChat ? 'chat' : (depth === 0 ? 'root' : '')));

	                const indent = depth * 24;
	                const childSpans = (children.get(span.span_id) || []).slice().sort(compareSpans);

                // Check for token usage
                const hasTokenUsage = span.input_tokens !== undefined || span.output_tokens !== undefined;

                return `
                    <div class="span-node">
                        <div class="span-card ${cardClass}" style="--indent: ${indent}px">
                            <div class="span-header">
                                <div class="span-name">${escapeHtml(span.name || 'Unknown')}</div>
                                <div class="span-duration">${span.duration_ms?.toFixed(2) || '?'}ms</div>
                            </div>

                            <div class="span-attributes">
                                ${span.decision ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Decision</div>
                                        <div class="span-attr-value">
                                            <span class="badge badge-${span.decision}">${span.decision}</span>
                                        </div>
                                    </div>
                                ` : ''}

                                ${span.operation_name ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Operation</div>
                                        <div class="span-attr-value">${escapeHtml(span.operation_name)}</div>
                                    </div>
                                ` : ''}

                                ${span.provider_name ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Provider</div>
                                        <div class="span-attr-value">${escapeHtml(span.provider_name)}</div>
                                    </div>
                                ` : ''}

                                ${span.request_model ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Request Model</div>
                                        <div class="span-attr-value">${escapeHtml(span.request_model)}</div>
                                    </div>
                                ` : ''}

                                ${span.response_model ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Response Model</div>
                                        <div class="span-attr-value">${escapeHtml(span.response_model)}</div>
                                    </div>
                                ` : ''}

                                ${span.response_id ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Response ID</div>
                                        <div class="span-attr-value">${escapeHtml(span.response_id)}</div>
                                    </div>
                                ` : ''}

                                ${span.finish_reasons ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Finish Reason</div>
                                        <div class="span-attr-value">${escapeHtml(Array.isArray(span.finish_reasons) ? span.finish_reasons.join(', ') : span.finish_reasons)}</div>
                                    </div>
                                ` : ''}

                                ${span.target_type ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Target Type</div>
                                        <div class="span-attr-value">${escapeHtml(span.target_type)}</div>
                                    </div>
                                ` : ''}

                                ${span.agent_id ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Agent ID</div>
                                        <div class="span-attr-value">${escapeHtml(span.agent_id)}</div>
                                    </div>
                                ` : ''}

                                ${span.conversation_id ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Conversation ID</div>
                                        <div class="span-attr-value">${escapeHtml(span.conversation_id)}</div>
                                    </div>
                                ` : ''}

                                ${span.guardian_name ? `
                                    <div class="span-attr">
                                        <div class="span-attr-key">Guardian</div>
                                        <div class="span-attr-value">${escapeHtml(span.guardian_name)}</div>
                                    </div>
                                ` : ''}
                            </div>

                            ${hasTokenUsage ? `
                                <div class="token-usage">
                                    <div class="token-usage-item">
                                        <span class="token-label">Input Tokens:</span>
                                        <span class="token-value input">${span.input_tokens ?? '-'}</span>
                                    </div>
                                    <div class="token-usage-item">
                                        <span class="token-label">Output Tokens:</span>
                                        <span class="token-value output">${span.output_tokens ?? '-'}</span>
                                    </div>
                                    <div class="token-usage-item">
                                        <span class="token-label">Total:</span>
                                        <span class="token-value">${(span.input_tokens || 0) + (span.output_tokens || 0)}</span>
                                    </div>
                                </div>
                            ` : ''}

                            ${renderSensitiveContent(span)}

                            ${span.findings && span.findings.length > 0 ? `
                                <div class="findings-section">
                                    <div class="findings-header">Security Findings (${span.findings.length})</div>
                                    ${span.findings.map(f => renderFinding(f)).join('')}
                                </div>
                            ` : ''}
                        </div>
                        ${childSpans.map(child => renderSpan(child, depth + 1)).join('')}
                    </div>
                `;
            }

            return rootSpans.map(span => renderSpan(span)).join('');
        }

        function renderFinding(finding) {
            const scoreClass = getScoreClass(finding.risk_score);
            return `
                <div class="finding-card">
                    <div class="finding-header">
                        <span class="finding-category">${escapeHtml(finding.risk_category || 'Unknown')}</span>
                        <span class="finding-score ${scoreClass}">
                            ${finding.risk_severity || 'unknown'} (${(finding.risk_score || 0).toFixed(2)})
                        </span>
                    </div>
                    ${finding.policy_name ? `
                        <div style="font-size: 0.75rem; color: var(--text-secondary);">
                            Policy: ${escapeHtml(finding.policy_name)}
                        </div>
                    ` : ''}
                </div>
            `;
        }

        function getScoreClass(score) {
            if (score >= 0.8) return 'score-critical';
            if (score >= 0.6) return 'score-high';
            if (score >= 0.4) return 'score-medium';
            return 'score-low';
        }

        function tryParseJson(value) {
            if (value === undefined || value === null) return null;
            if (typeof value !== 'string') return value;
            try {
                return JSON.parse(value);
            } catch (e) {
                return value;
            }
        }

        function messageToText(message) {
            if (!message) return '';
            const parts = message.parts;
            if (!Array.isArray(parts)) return '';
            return parts.map(p => {
                if (!p) return '';
                if (p.type === 'text') return p.content ?? '';
                return `[${p.type || 'part'}]`;
            }).join('');
        }

        function renderTextSection(title, value) {
            const asString = (typeof value === 'string') ? value : JSON.stringify(value, null, 2);
            return `
                <div class="message-section">
                    <div class="message-section-title">${escapeHtml(title)}</div>
                    <div class="message-content">${escapeHtml(asString)}</div>
                </div>
            `;
        }

        function renderMessagesSection(title, rawValue) {
            const parsed = tryParseJson(rawValue);
            if (!Array.isArray(parsed)) {
                return renderTextSection(title, rawValue);
            }
            const rows = parsed.map(m => `
                <div class="message-row">
                    <div class="message-role">${escapeHtml(m?.role || 'unknown')}</div>
                    <div class="message-content">${escapeHtml(messageToText(m))}</div>
                </div>
            `).join('');
            return `
                <div class="message-section">
                    <div class="message-section-title">${escapeHtml(title)}</div>
                    ${rows}
                </div>
            `;
        }

	        function renderSensitiveContent(span) {
	            const attrs = span?.attributes || {};

            const systemInstructions = attrs['gen_ai.system_instructions'];
            const inputMessages = attrs['gen_ai.input.messages'];
            const outputMessages = attrs['gen_ai.output.messages'];
            const guardianInput = attrs['gen_ai.security.content.input.value'];
            const guardianOutput = attrs['gen_ai.security.content.output.value'];

            if (!systemInstructions && !inputMessages && !outputMessages && !guardianInput && !guardianOutput) {
                return '';
            }

            const sections = [];
            if (systemInstructions) sections.push(renderTextSection('System Instructions', systemInstructions));
            if (inputMessages) sections.push(renderMessagesSection('Input Messages', inputMessages));
            if (outputMessages) sections.push(renderMessagesSection('Output Messages', outputMessages));
            if (guardianInput) sections.push(renderTextSection('Guardian Input', guardianInput));
            if (guardianOutput) sections.push(renderTextSection('Guardian Output', guardianOutput));

	            return `
	                <details class="sensitive-content" open>
	                    <summary>Sensitive content (opt-in)</summary>
	                    ${sections.join('')}
	                </details>
	            `;
	        }

        // Tab switching
        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('[id^="tab-content-"]').forEach(c => c.style.display = 'none');

            event.target.classList.add('active');
            document.getElementById(`tab-content-${tabName}`).style.display = 'block';
        }

        // Utility functions
        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function formatLocalTime(isoString) {
            if (!isoString) return 'Unknown';
            try {
                const date = new Date(isoString);
                if (isNaN(date.getTime())) return isoString;
                return date.toLocaleString(undefined, {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    timeZoneName: 'short'
                });
            } catch (e) {
                return isoString;
            }
        }

        function syntaxHighlight(json) {
            json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            return json.replace(/("(\\\\u[a-zA-Z0-9]{4}|\\\\[^u]|[^\\\\"])*"(\\s*:)?|\\b(true|false|null)\\b|-?\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d+)?)/g, function (match) {
                let cls = 'json-number';
                if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'json-key';
                    } else {
                        cls = 'json-string';
                    }
                } else if (/true|false/.test(match)) {
                    cls = 'json-boolean';
                } else if (/null/.test(match)) {
                    cls = 'json-null';
                }
                return '<span class="' + cls + '">' + match + '</span>';
            });
        }

        function updateStatus(text, healthy) {
            document.getElementById('status-text').textContent = text;
            const dot = document.querySelector('.status-dot');
            dot.style.background = healthy ? 'var(--accent-green)' : 'var(--accent-red)';
        }

        function refreshTraces() {
            fetchTraces();
        }

	        // Event listeners
	        document.getElementById('timespan-select').addEventListener('change', () => {
	            applyUiFilters();
	            renderTraceList();
	            renderTraceDetails();
	        });
	        document.getElementById('story-filter').addEventListener('change', () => {
	            applyUiFilters();
	            renderTraceList();
	            renderTraceDetails();
	        });
	        document.getElementById('toggle-security').addEventListener('change', (event) => {
	            showSecuritySpans = Boolean(event.target.checked);
	            try { localStorage.setItem('otel_demo_show_security_spans', String(showSecuritySpans)); } catch (e) {}
	            renderTraceDetails();
	        });

	        // Restore persisted UI preferences.
	        try {
	            const saved = localStorage.getItem('otel_demo_show_security_spans');
	            if (saved !== null) {
	                showSecuritySpans = saved === 'true';
	                document.getElementById('toggle-security').checked = showSecuritySpans;
	            }
	        } catch (e) {}

        // Start polling
        function startPolling() {
            fetchTraces();
            pollInterval = setInterval(fetchTraces, 10000); // Poll every 10 seconds
        }

        // Initialize
        startPolling();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    """Serve the main UI."""
    return render_template_string(HTML_TEMPLATE)


# =============================================================================
# Server Management
# =============================================================================

def open_browser(port: int):
    """Open the browser to the trace viewer."""
    webbrowser.open(f"http://localhost:{port}")


def run_server(port: int = 5050, open_browser_on_start: bool = True):
    """
    Start the trace viewer server.

    Args:
        port: Port to run on
        open_browser_on_start: Open browser when server starts
    """
    global _retriever, _retriever_error

    print("\n" + "=" * 60)
    print("  GenAI Security Guardian - Trace Viewer")
    print("=" * 60)
    print(f"  Server: http://localhost:{port}")

    # Load environment variables from .env.local if available.
    try:
        from dotenv import load_dotenv
        env_candidates = [
            os.path.join(os.path.dirname(__file__), ".env.local"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.local"),
        ]
        for env_file in env_candidates:
            if os.path.exists(env_file):
                load_dotenv(env_file)
                print(f"  [OK] Loaded environment from {env_file}")
                break
    except ImportError:
        pass

    # Try to initialize the retriever
    try:
        _retriever = get_retriever()
        _retriever_error = None
        mode = "API Key" if getattr(_retriever, "_use_api_key", False) else "Entra ID (Azure CLI)"
        print(f"  Data Source: Azure Application Insights (Live via {mode})")
        app_display = getattr(_retriever, "app", None) or ""
        if isinstance(app_display, str) and len(app_display) > 64:
            app_display = "..." + app_display[-61:]
        print(f"  App: {app_display}")
    except ValueError as e:
        _retriever = None
        _retriever_error = str(e)
        print(f"  [WARNING] App Insights not configured!")
        print(f"  The UI will show configuration instructions.")

    print("=" * 60 + "\n")

    if open_browser_on_start:
        Timer(1.5, lambda: open_browser(port)).start()

    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="GenAI Security Guardian Trace Viewer - Live traces from App Insights"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=5050,
        help="Port to run server on (default: 5050)"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't open browser on start"
    )

    args = parser.parse_args()

    run_server(
        port=args.port,
        open_browser_on_start=not args.no_browser
    )


if __name__ == "__main__":
    main()
