#!/usr/bin/env python3
"""
GenAI Memory Stories Trace Viewer

Flask-based UI for visualizing GenAI memory + agent traces stored in Azure Application Insights.
"""

from __future__ import annotations

import argparse
import json
import os
import webbrowser
from datetime import datetime, timezone
from threading import Timer

from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS

from trace_retriever import get_retriever

app = Flask(__name__)
CORS(app)

_retriever = None
_retriever_error = None


def get_trace_retriever():
    global _retriever, _retriever_error
    return _retriever, _retriever_error


# =============================================================================
# API
# =============================================================================


@app.route("/api/traces", methods=["GET"])
def api_get_traces():
    retriever, error = get_trace_retriever()
    if error:
        return jsonify({"error": error, "config_error": True}), 503
    if not retriever:
        return jsonify({"error": "Retriever not initialized"}), 500

    timespan = request.args.get("timespan", "PT1H")
    story_id = request.args.get("story_id", type=int)
    limit = request.args.get("limit", 50, type=int)
    include_demos = request.args.get("include_demos", "true").lower() == "true"

    try:
        traces = retriever.get_traces(
            timespan=timespan,
            story_id=story_id,
            include_demos=include_demos,
            limit=limit,
        )
        return jsonify({"traces": [t.to_dict() for t in traces], "count": len(traces), "timespan": timespan})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/traces/<trace_id>", methods=["GET"])
def api_get_trace(trace_id: str):
    retriever, error = get_trace_retriever()
    if error:
        return jsonify({"error": error, "config_error": True}), 503
    if not retriever:
        return jsonify({"error": "Retriever not initialized"}), 500

    try:
        traces = retriever.get_traces(timespan="PT24H", limit=200, include_demos=True)
        for trace in traces:
            if trace.trace_id == trace_id:
                return jsonify(trace.to_dict())
        return jsonify({"error": "Trace not found"}), 404
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/events", methods=["GET"])
def api_get_events():
    retriever, error = get_trace_retriever()
    if error:
        return jsonify({"error": error, "config_error": True}), 503
    if not retriever:
        return jsonify({"error": "Retriever not initialized"}), 500

    timespan = request.args.get("timespan", "PT1H")
    limit = request.args.get("limit", 200, type=int)

    try:
        events = retriever.get_events(timespan=timespan, limit=limit)
        return jsonify({"events": events, "count": len(events), "timespan": timespan})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/operations", methods=["GET"])
def api_get_operations():
    retriever, error = get_trace_retriever()
    if error:
        return jsonify({"error": error, "config_error": True}), 503
    if not retriever:
        return jsonify({"error": "Retriever not initialized"}), 500

    timespan = request.args.get("timespan", "PT1H")
    limit = request.args.get("limit", 50, type=int)

    try:
        operations = retriever.get_recent_operations(timespan=timespan, limit=limit)
        return jsonify({"operations": operations, "count": len(operations), "timespan": timespan})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/health", methods=["GET"])
def api_health():
    retriever, error = get_trace_retriever()
    return jsonify(
        {
            "status": "healthy" if retriever else "degraded",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "retriever_type": type(retriever).__name__ if retriever else "None",
            "config_error": error,
        }
    )


# =============================================================================
# UI
# =============================================================================


HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenAI Memory Stories - Trace Viewer</title>
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

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }

        .header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 { font-size: 1.5rem; color: var(--accent-blue); }

        .header-controls { display: flex; gap: 1rem; align-items: center; }

        .header-controls select,
        .header-controls button {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
        }

        .header-controls button:hover { background: var(--accent-blue); }

        .status-indicator { display: flex; align-items: center; gap: 0.5rem; }
        .status-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--accent-green); }
        .status-dot.disconnected { background: var(--accent-red); }

        .main-container { display: flex; height: calc(100vh - 80px); }

        .sidebar {
            width: 380px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            overflow-y: auto;
        }

        .sidebar-header {
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            font-weight: 600;
        }

        .trace-item {
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            transition: background 0.2s;
        }

        .trace-item:hover { background: rgba(77, 166, 255, 0.1); }
        .trace-item.selected { background: rgba(77, 166, 255, 0.2); border-left: 3px solid var(--accent-blue); }

        .trace-item-title { font-weight: 600; margin-bottom: 0.25rem; }
        .trace-item-subtitle { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem; }

        .trace-item-meta { display: flex; gap: 1rem; font-size: 0.75rem; color: var(--text-secondary); }

        .trace-item-badges { margin-top: 0.5rem; display: flex; flex-wrap: wrap; gap: 0.25rem; }

        .badge {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 999px;
            font-size: 0.7rem;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.06);
        }

        .content { flex: 1; overflow-y: auto; padding: 1rem; }

        .content-header {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border-color);
        }

        .content-header h2 { color: var(--accent-blue); margin-bottom: 0.5rem; }
        .content-header-meta { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.4; }

        .tabs { display: flex; gap: 0.5rem; margin-bottom: 1rem; }

        .tab {
            background: var(--bg-secondary);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
        }
        .tab.active { color: var(--accent-blue); background: var(--bg-tertiary); }

        .span-tree { display: flex; flex-direction: column; gap: 0.5rem; }

        .span-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            margin-left: var(--indent, 0px);
            border-left: 4px solid var(--accent-blue);
        }

        .span-card.root { border-left-color: var(--accent-blue); }
        .span-card.agent { border-left-color: var(--accent-purple); }
        .span-card.chat { border-left-color: var(--accent-green); }
        .span-card.memory { border-left-color: var(--accent-blue); }
        .span-card.tool { border-left-color: var(--accent-yellow); }

        .span-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
        .span-name { font-weight: 600; }
        .span-duration { font-size: 0.85rem; color: var(--text-secondary); }

        .span-attributes {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 0.5rem 1rem;
        }

        .span-attr { display: flex; flex-direction: column; gap: 0.15rem; }
        .span-attr-key { font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }
        .span-attr-value { font-size: 0.85rem; word-break: break-word; }

        .span-events { margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px dashed var(--border-color); }
        .span-events-title { font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }

        .event-item { border: 1px solid var(--border-color); border-radius: 10px; padding: 0.75rem; background: rgba(255,255,255,0.03); }
        .event-item summary { cursor: pointer; font-weight: 600; }
        .event-item .event-meta { margin-top: 0.5rem; font-size: 0.75rem; color: var(--text-secondary); }

        .loading { padding: 2rem; text-align: center; color: var(--text-secondary); }
        .spinner { width: 30px; height: 30px; border: 3px solid var(--border-color); border-top: 3px solid var(--accent-blue); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 1rem; }
        @keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }

        .empty-state { text-align: center; padding: 3rem; color: var(--text-secondary); }
        .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; }

        .config-error { padding: 2rem; color: var(--text-primary); }
        .config-error h3 { margin: 0.75rem 0; }
        .config-code code { display: block; background: var(--bg-tertiary); padding: 0.5rem; border-radius: 6px; margin: 0.5rem 0; font-family: 'Monaco', 'Menlo', monospace; font-size: 0.8rem; overflow-x: auto; }

        .json-view {
            background: var(--bg-tertiary);
            border-radius: 8px;
            padding: 1rem;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.8rem;
            overflow-x: auto;
            white-space: pre-wrap;
            max-height: 520px;
            overflow-y: auto;
        }

        .json-key { color: var(--accent-purple); }
        .json-string { color: var(--accent-green); }
        .json-number { color: var(--accent-yellow); }
        .json-boolean { color: var(--accent-blue); }
        .json-null { color: var(--accent-red); }

        .banner {
            margin-top: 0.75rem;
            padding: 0.75rem 1rem;
            border-radius: 10px;
            border: 1px solid var(--border-color);
            background: rgba(251, 191, 36, 0.10);
        }
        .banner strong { color: var(--accent-yellow); }
        .banner code {
            display: inline-block;
            background: var(--bg-tertiary);
            padding: 0.1rem 0.35rem;
            border-radius: 6px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.8rem;
        }

        .sensitive-content { margin-top: 0.75rem; border: 1px solid var(--border-color); border-radius: 10px; padding: 0.75rem; background: rgba(255,255,255,0.03); }
        .sensitive-content summary { cursor: pointer; font-weight: 600; color: var(--accent-yellow); }
        .message-section { margin-top: 0.75rem; }
        .message-section-title { font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem; text-transform: uppercase; letter-spacing: 0.05em; }
        .message-row { display: flex; gap: 0.75rem; padding: 0.5rem; border-radius: 8px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); margin-bottom: 0.5rem; }
        .message-role { min-width: 90px; font-weight: 600; color: var(--accent-blue); }
        .message-content { flex: 1; font-family: 'Monaco', 'Menlo', monospace; font-size: 0.8rem; white-space: pre-wrap; overflow-wrap: anywhere; }
    </style>
</head>
<body>
    <header class="header">
        <h1>GenAI Memory Stories - Trace Viewer</h1>
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
                <option value="1">Story 1: Customer Support</option>
                <option value="2">Story 2: Shopping Assistant</option>
                <option value="3">Story 3: Multi-Agent Research</option>
                <option value="4">Story 4: Multi-Tenant SaaS</option>
                <option value="5">Story 5: Compliance Audit</option>
                <option value="6">Story 6: GDPR Lifecycle</option>
            </select>
            <select id="demo-filter">
                <option value="true" selected>Include demos</option>
                <option value="false">Stories only</option>
            </select>
            <button onclick="refreshTraces()">Refresh</button>
            <div class="status-indicator">
                <div id="status-dot" class="status-dot"></div>
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
                    <p>Choose a trace from the sidebar to see memory + agent spans and GenAI events.</p>
                </div>
            </div>
        </main>
    </div>

    <script>
        let traces = [];
        let selectedTrace = null;

        async function fetchTraces() {
            const timespan = document.getElementById('timespan-select').value;
            const storyFilter = document.getElementById('story-filter').value;
            const includeDemos = document.getElementById('demo-filter').value;

            let url = `/api/traces?timespan=${timespan}&limit=50&include_demos=${includeDemos}`;
            if (storyFilter) {
                url += `&story_id=${storyFilter}`;
            }

            try {
                const response = await fetch(url);
                const data = await response.json();

                if (data.config_error) {
                    showConfigError(data.error);
                    updateStatus('Not Configured', false);
                    return;
                }
                if (data.error) throw new Error(data.error);

                traces = data.traces || [];
                renderTraceList();
                updateStatus('Connected', true);
            } catch (error) {
                console.error('Failed to fetch traces:', error);
                updateStatus('Error: ' + error.message, false);
            }
        }

        function updateStatus(text, connected) {
            document.getElementById('status-text').textContent = text;
            const dot = document.getElementById('status-dot');
            dot.classList.toggle('disconnected', !connected);
        }

        function showConfigError(errorMessage) {
            const container = document.getElementById('trace-list');
            container.innerHTML = `
                <div class="config-error">
                    <div class="empty-state-icon">⚠️</div>
                    <h3>App Insights Not Configured</h3>
                    <p>Set the following environment variables and ensure you're logged in:</p>
                    <div class="config-code">
                        <code>az login</code>
                        <code>export APPINSIGHTS_RESOURCE_ID=/subscriptions/&lt;sub&gt;/resourceGroups/&lt;rg&gt;/providers/Microsoft.Insights/components/&lt;name&gt;</code>
                        <code>export OTEL_SERVICE_NAME=genai-memory-stories</code>
                    </div>
                    <p style="margin-top: 0.5rem; color: var(--text-secondary);">${escapeHtml(errorMessage || '')}</p>
                </div>
            `;
        }

        function renderTraceList() {
            const container = document.getElementById('trace-list');

            if (!traces || traces.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">🔍</div>
                        <p>No traces found</p>
                        <p style="font-size: 0.8rem">Try adjusting the time range or run the stories</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = traces.map(trace => {
                const isSelected = selectedTrace && selectedTrace.trace_id === trace.trace_id;
                const rootAttrs = trace.root_span?.attributes || {};

                const title = trace.metadata?.story_title
                    || rootAttrs["demo.title"]
                    || trace.metadata?.root_span_name
                    || trace.root_span?.name
                    || 'Trace';

                const subtitle = trace.metadata?.scenario_name
                    || trace.metadata?.root_span_name
                    || trace.root_span?.name
                    || '';

                const spanCount = trace.spans?.length || 0;
                const chatCount = (trace.spans || []).filter(s => s.operation_name === 'chat').length;
                const agentCount = (trace.spans || []).filter(s => ['invoke_agent','create_agent'].includes(s.operation_name)).length;
                const toolCount = (trace.spans || []).filter(s => s.operation_name === 'execute_tool').length;
                const memoryCount = (trace.spans || []).filter(s => ['create_memory_store','search_memory','update_memory','delete_memory','delete_memory_store'].includes(s.operation_name)).length;
                const eventCount = (trace.spans || []).reduce((acc, s) => acc + ((s.events || []).length), 0);

                return `
                    <div class="trace-item ${isSelected ? 'selected' : ''}" onclick="selectTrace('${trace.trace_id}')">
                        <div class="trace-item-title">${escapeHtml(title)}</div>
                        ${subtitle ? `<div class="trace-item-subtitle">${escapeHtml(subtitle)}</div>` : ''}
                        <div class="trace-item-meta">
                            <span>${spanCount} spans</span>
                            <span>${memoryCount} memory</span>
                            <span>${agentCount} agent</span>
                            <span>${chatCount} chat</span>
                            <span>${toolCount} tool</span>
                            <span>${eventCount} events</span>
                        </div>
                        <div class="trace-item-badges">
                            ${trace.metadata?.story_id ? `<span class="badge">story_${trace.metadata.story_id}</span>` : ''}
                            ${rootAttrs["demo.id"] ? `<span class="badge">${escapeHtml(rootAttrs["demo.id"])}</span>` : ''}
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
            if (!selectedTrace) return;

            const rootAttrs = selectedTrace.root_span?.attributes || {};

            const title = selectedTrace.metadata?.story_title
                || rootAttrs["demo.title"]
                || 'Trace Details';

            const scenarioName = selectedTrace.metadata?.scenario_name;
            const rootSpanName = selectedTrace.metadata?.root_span_name || selectedTrace.root_span?.name;
            const conversationId = selectedTrace.metadata?.conversation_id;
            const startTime = selectedTrace.metadata?.start_time;
            const formattedTime = startTime ? formatLocalTime(startTime) : 'Unknown';
            const hasSensitiveContent = (selectedTrace.spans || []).some(spanHasSensitiveContent);

            container.innerHTML = `
                <div class="content-header">
                    <h2>${escapeHtml(title)}</h2>
                    <div class="content-header-meta">
                        ${scenarioName ? `Scenario: ${escapeHtml(scenarioName)}<br>` : ''}
                        ${conversationId ? `Conversation ID: ${escapeHtml(conversationId)}<br>` : ''}
                        ${rootSpanName ? `Root span: ${escapeHtml(rootSpanName)}<br>` : ''}
                        Trace ID: ${selectedTrace.trace_id}<br>
                        Time: ${formattedTime}
                    </div>
                    ${!hasSensitiveContent ? `
                        <div class="banner">
                            <strong>No input/output messages recorded.</strong>
                            Content capture is opt-in — rerun with <code>python3 prototype/memory/scenarios/run_and_view.py --capture-content</code>
                            (or set <code>GENAI_MEMORY_CAPTURE_CONTENT=true</code>).
                        </div>
                    ` : ''}
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

        function showTab(tabName) {
            document.getElementById('tab-content-spans').style.display = tabName === 'spans' ? 'block' : 'none';
            document.getElementById('tab-content-json').style.display = tabName === 'json' ? 'block' : 'none';
            document.querySelectorAll('.tab').forEach(btn => btn.classList.remove('active'));
            document.querySelector(`.tab[onclick="showTab('${tabName}')"]`).classList.add('active');
        }

        function classifySpan(span, depth) {
            const op = span.operation_name || '';
            if (depth === 0) return 'root';
            if (op === 'chat' || (span.name || '').startsWith('chat ')) return 'chat';
            if (op === 'execute_tool' || (span.name || '').startsWith('execute_tool')) return 'tool';
            if (op === 'invoke_agent' || op === 'create_agent' || (span.name || '').includes('invoke_agent') || (span.name || '').includes('create_agent')) return 'agent';
            if (['create_memory_store','search_memory','update_memory','delete_memory','delete_memory_store'].includes(op)) return 'memory';
            return '';
        }

        function tryParseJson(value) {
            if (value === undefined || value === null) return null;
            if (typeof value !== 'string') return value;
            try { return JSON.parse(value); } catch (_) { return value; }
        }

        function messageToText(message) {
            if (!message) return '';
            const parts = message.parts;
            if (!Array.isArray(parts)) return '';
            return parts.map(p => {
                if (!p) return '';
                if (p.type === 'text') return p.content ?? '';
                if (p.type === 'tool_call') return `[tool_call${p.name ? `:${p.name}` : ''}]`;
                if (p.type === 'tool_call_response') return `[tool_call_response]`;
                return `[${p.type || 'part'}]`;
            }).join('');
        }

        function getSensitiveAttr(span, key) {
            const attrs = span?.attributes || {};
            if (attrs[key] !== undefined && attrs[key] !== null) return attrs[key];
            const events = span?.events || [];
            for (const ev of events) {
                const evAttrs = ev?.attributes || {};
                if (evAttrs[key] !== undefined && evAttrs[key] !== null) return evAttrs[key];
            }
            return undefined;
        }

        function spanHasSensitiveContent(span) {
            const keys = ['gen_ai.system_instructions','gen_ai.input.messages','gen_ai.output.messages'];
            return keys.some(k => getSensitiveAttr(span, k) !== undefined);
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
            const systemInstructions = getSensitiveAttr(span, 'gen_ai.system_instructions');
            const inputMessages = getSensitiveAttr(span, 'gen_ai.input.messages');
            const outputMessages = getSensitiveAttr(span, 'gen_ai.output.messages');

            if (systemInstructions === undefined && inputMessages === undefined && outputMessages === undefined) {
                return '';
            }

            const sections = [];
            if (systemInstructions !== undefined) sections.push(renderTextSection('System Instructions', systemInstructions));
            if (inputMessages !== undefined) sections.push(renderMessagesSection('Input Messages', inputMessages));
            if (outputMessages !== undefined) sections.push(renderMessagesSection('Output Messages', outputMessages));

            return `
                <details class="sensitive-content">
                    <summary>Sensitive content (opt-in)</summary>
                    ${sections.join('')}
                </details>
            `;
        }

        function renderSpanTree(spans) {
            if (!spans || spans.length === 0) return '<div class="empty-state">No spans found</div>';

            const spanMap = new Map(spans.map(s => [s.span_id, s]));
            const children = new Map();
            spans.forEach(span => {
                if (span.parent_span_id) {
                    if (!children.has(span.parent_span_id)) children.set(span.parent_span_id, []);
                    children.get(span.parent_span_id).push(span);
                }
            });

            const rootSpans = spans.filter(s => !s.parent_span_id || !spanMap.has(s.parent_span_id));
            rootSpans.sort((a, b) => (a.start_time || '').localeCompare(b.start_time || ''));

            function renderSpan(span, depth = 0) {
                const indent = depth * 24;
                const cardClass = classifySpan(span, depth);
                const childSpans = children.get(span.span_id) || [];
                childSpans.sort((a, b) => (a.start_time || '').localeCompare(b.start_time || ''));

                const attrs = span.attributes || {};

                const memStoreName = attrs["gen_ai.memory.store.name"];
                const memStoreId = attrs["gen_ai.memory.store.id"];
                const memId = attrs["gen_ai.memory.id"];
                const memType = attrs["gen_ai.memory.type"];
                const memScope = attrs["gen_ai.memory.scope"];
                const memNs = attrs["gen_ai.memory.namespace"];
                const memImportance = attrs["gen_ai.memory.importance"];
                const memExpiry = attrs["gen_ai.memory.expiration_date"];
                const memUpdateStrategy = attrs["gen_ai.memory.update.strategy"];
                const memResultCount = attrs["gen_ai.memory.search.result.count"];
                const memSim = attrs["gen_ai.memory.search.similarity.threshold"];

                const toolName = attrs["gen_ai.tool.name"];
                const toolType = attrs["gen_ai.tool.type"];
                const toolCallId = attrs["gen_ai.tool.call.id"];

                return `
                    <div class="span-node">
                        <div class="span-card ${cardClass}" style="--indent: ${indent}px">
                            <div class="span-header">
                                <div class="span-name">${escapeHtml(span.name || 'Unknown')}</div>
                                <div class="span-duration">${span.duration_ms?.toFixed(2) || '?'}ms</div>
                            </div>

                            <div class="span-attributes">
                                ${span.operation_name ? `<div class="span-attr"><div class="span-attr-key">Operation</div><div class="span-attr-value">${escapeHtml(span.operation_name)}</div></div>` : ''}
                                ${span.provider_name ? `<div class="span-attr"><div class="span-attr-key">Provider</div><div class="span-attr-value">${escapeHtml(span.provider_name)}</div></div>` : ''}
                                ${span.request_model ? `<div class="span-attr"><div class="span-attr-key">Request Model</div><div class="span-attr-value">${escapeHtml(span.request_model)}</div></div>` : ''}
                                ${span.response_model ? `<div class="span-attr"><div class="span-attr-key">Response Model</div><div class="span-attr-value">${escapeHtml(span.response_model)}</div></div>` : ''}
                                ${span.response_id ? `<div class="span-attr"><div class="span-attr-key">Response ID</div><div class="span-attr-value">${escapeHtml(span.response_id)}</div></div>` : ''}
                                ${span.finish_reasons ? `<div class="span-attr"><div class="span-attr-key">Finish</div><div class="span-attr-value">${escapeHtml(Array.isArray(span.finish_reasons) ? span.finish_reasons.join(', ') : span.finish_reasons)}</div></div>` : ''}
                                ${(span.input_tokens !== null && span.input_tokens !== undefined) ? `<div class="span-attr"><div class="span-attr-key">Input Tokens</div><div class="span-attr-value">${escapeHtml(String(span.input_tokens))}</div></div>` : ''}
                                ${(span.output_tokens !== null && span.output_tokens !== undefined) ? `<div class="span-attr"><div class="span-attr-key">Output Tokens</div><div class="span-attr-value">${escapeHtml(String(span.output_tokens))}</div></div>` : ''}
                                ${span.agent_name ? `<div class="span-attr"><div class="span-attr-key">Agent</div><div class="span-attr-value">${escapeHtml(span.agent_name)}</div></div>` : ''}
                                ${span.agent_id ? `<div class="span-attr"><div class="span-attr-key">Agent ID</div><div class="span-attr-value">${escapeHtml(span.agent_id)}</div></div>` : ''}
                                ${span.conversation_id ? `<div class="span-attr"><div class="span-attr-key">Conversation</div><div class="span-attr-value">${escapeHtml(span.conversation_id)}</div></div>` : ''}

                                ${memStoreName ? `<div class="span-attr"><div class="span-attr-key">Store Name</div><div class="span-attr-value">${escapeHtml(memStoreName)}</div></div>` : ''}
                                ${memStoreId ? `<div class="span-attr"><div class="span-attr-key">Store ID</div><div class="span-attr-value">${escapeHtml(memStoreId)}</div></div>` : ''}
                                ${memId ? `<div class="span-attr"><div class="span-attr-key">Memory ID</div><div class="span-attr-value">${escapeHtml(memId)}</div></div>` : ''}
                                ${memType ? `<div class="span-attr"><div class="span-attr-key">Memory Type</div><div class="span-attr-value">${escapeHtml(memType)}</div></div>` : ''}
                                ${memScope ? `<div class="span-attr"><div class="span-attr-key">Scope</div><div class="span-attr-value">${escapeHtml(memScope)}</div></div>` : ''}
                                ${memNs ? `<div class="span-attr"><div class="span-attr-key">Namespace</div><div class="span-attr-value">${escapeHtml(memNs)}</div></div>` : ''}
                                ${(memImportance !== null && memImportance !== undefined) ? `<div class="span-attr"><div class="span-attr-key">Importance</div><div class="span-attr-value">${escapeHtml(String(memImportance))}</div></div>` : ''}
                                ${memExpiry ? `<div class="span-attr"><div class="span-attr-key">Expiration</div><div class="span-attr-value">${escapeHtml(memExpiry)}</div></div>` : ''}
                                ${memUpdateStrategy ? `<div class="span-attr"><div class="span-attr-key">Update Strategy</div><div class="span-attr-value">${escapeHtml(memUpdateStrategy)}</div></div>` : ''}
                                ${(memResultCount !== null && memResultCount !== undefined) ? `<div class="span-attr"><div class="span-attr-key">Result Count</div><div class="span-attr-value">${escapeHtml(String(memResultCount))}</div></div>` : ''}
                                ${(memSim !== null && memSim !== undefined) ? `<div class="span-attr"><div class="span-attr-key">Similarity</div><div class="span-attr-value">${escapeHtml(String(memSim))}</div></div>` : ''}

                                ${toolName ? `<div class="span-attr"><div class="span-attr-key">Tool</div><div class="span-attr-value">${escapeHtml(toolName)}</div></div>` : ''}
                                ${toolType ? `<div class="span-attr"><div class="span-attr-key">Tool Type</div><div class="span-attr-value">${escapeHtml(toolType)}</div></div>` : ''}
                                ${toolCallId ? `<div class="span-attr"><div class="span-attr-key">Tool Call ID</div><div class="span-attr-value">${escapeHtml(toolCallId)}</div></div>` : ''}
                            </div>

                            ${renderSensitiveContent(span)}

                            ${(span.events && span.events.length) ? `
                                <div class="span-events">
                                    <div class="span-events-title">Events (${span.events.length})</div>
                                    ${span.events.map(ev => {
                                        const evAttrs = ev.attributes || {};
                                        const evTitle = ev.name;
                                        let evSummary = '';
                                        if (ev.name === 'gen_ai.evaluation.result') {
                                            const name = evAttrs['gen_ai.evaluation.name'] || '';
                                            const label = evAttrs['gen_ai.evaluation.score.label'] || '';
                                            const value = evAttrs['gen_ai.evaluation.score.value'];
                                            evSummary = `${name}${label ? ` — ${label}` : ''}${(value !== undefined && value !== null) ? ` (${value})` : ''}`;
                                        } else if (ev.name === 'gen_ai.client.inference.operation.details') {
                                            const model = evAttrs['gen_ai.request.model'] || '';
                                            evSummary = model ? `model=${model}` : '';
                                        }
                                        const json = JSON.stringify(evAttrs, null, 2);
                                        return `
                                            <details class="event-item">
                                                <summary>${escapeHtml(evTitle)}${evSummary ? ` — ${escapeHtml(evSummary)}` : ''}</summary>
                                                <div class="event-meta">Time: ${escapeHtml(formatLocalTime(ev.timestamp || ''))}</div>
                                                <div class="json-view">${syntaxHighlight(json)}</div>
                                            </details>
                                        `;
                                    }).join('')}
                                </div>
                            ` : ''}
                        </div>
                        ${childSpans.map(child => renderSpan(child, depth + 1)).join('')}
                    </div>
                `;
            }

            return rootSpans.map(s => renderSpan(s, 0)).join('');
        }

        function formatLocalTime(isoString) {
            try {
                const date = new Date(isoString);
                return date.toLocaleString();
            } catch (_) {
                return isoString;
            }
        }

        function escapeHtml(text) {
            if (text === null || text === undefined) return '';
            return String(text)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        function syntaxHighlight(json) {
            if (typeof json !== 'string') {
                json = JSON.stringify(json, null, 2);
            }
            json = escapeHtml(json);
            return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                let cls = 'json-number';
                if (/^"/.test(match)) {
                    cls = /:$/.test(match) ? 'json-key' : 'json-string';
                } else if (/true|false/.test(match)) {
                    cls = 'json-boolean';
                } else if (/null/.test(match)) {
                    cls = 'json-null';
                }
                return `<span class="${cls}">${match}</span>`;
            });
        }

        function refreshTraces() { fetchTraces(); }

        document.getElementById('timespan-select').addEventListener('change', fetchTraces);
        document.getElementById('story-filter').addEventListener('change', fetchTraces);
        document.getElementById('demo-filter').addEventListener('change', fetchTraces);

        fetchTraces();
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)


def open_browser(port: int) -> None:
    webbrowser.open(f"http://localhost:{port}", new=2)


def run_server(port: int = 5050, open_browser_on_start: bool = True) -> None:
    global _retriever, _retriever_error

    print("\n" + "=" * 60)
    print("  GenAI Memory Stories - Trace Viewer")
    print("=" * 60)
    print(f"  Server: http://localhost:{port}")

    try:
        _retriever = get_retriever()
        _retriever_error = None
        mode = "API Key" if getattr(_retriever, "_use_api_key", False) else "Entra ID (Azure CLI)"
        print(f"  Data Source: Azure Application Insights (Live via {mode})")
        print(f"  Service Filter (cloud_RoleName): {getattr(_retriever, 'service_name', '')}")
    except ValueError as exc:
        _retriever = None
        _retriever_error = str(exc)
        print("  [WARNING] App Insights not configured!")

    print("=" * 60 + "\n")

    if open_browser_on_start:
        Timer(1.5, lambda: open_browser(port)).start()

    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="GenAI Memory Stories Trace Viewer - Live traces from App Insights")
    parser.add_argument("--port", "-p", type=int, default=5050, help="Port to run server on (default: 5050)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser on start")
    args = parser.parse_args()

    run_server(port=args.port, open_browser_on_start=not args.no_browser)


if __name__ == "__main__":
    main()
