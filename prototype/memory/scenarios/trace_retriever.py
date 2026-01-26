#!/usr/bin/env python3
"""
Azure Application Insights Trace Retriever (GenAI Memory Stories)

Retrieves OpenTelemetry traces from App Insights using Azure RBAC (Entra ID) via Azure CLI
(preferred), or legacy API-key mode.

This retriever is tuned for the GenAI Memory story suite:
  - Root spans: name startswith "story_" or "demo_"
  - Span events (from Azure Monitor exporter) in `traces` table:
      - gen_ai.client.inference.operation.details
      - gen_ai.evaluation.result
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

import requests


@dataclass
class GenAIEvent:
    """A GenAI span event exported into App Insights `traces` table."""

    name: str
    timestamp: str
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GenAISpan:
    """Parsed span with optional attached GenAI events."""

    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: str
    duration_ms: float

    # Common GenAI span attributes
    operation_name: Optional[str] = None
    provider_name: Optional[str] = None
    request_model: Optional[str] = None
    response_model: Optional[str] = None
    response_id: Optional[str] = None
    finish_reasons: Optional[List[str]] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    conversation_id: Optional[str] = None

    # Raw attributes for UI/debugging
    attributes: Dict[str, Any] = field(default_factory=dict)

    # Attached span events
    events: List[GenAIEvent] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TraceTree:
    """A complete trace with hierarchical spans."""

    trace_id: str
    root_span: Optional[GenAISpan] = None
    spans: List[GenAISpan] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "root_span": self.root_span.to_dict() if self.root_span else None,
            "spans": [s.to_dict() for s in self.spans],
            "metadata": self.metadata,
        }


class AppInsightsTraceRetriever:
    """
    Retrieves and parses traces from Azure Application Insights.

    Uses the App Insights REST Query API to execute KQL queries and returns structured trace data.
    """

    QUERY_API = "https://api.applicationinsights.io/v1/apps/{app_id}/query"

    _GUID_RE = re.compile(
        r"^[0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12}$"
    )

    def __init__(
        self,
        *,
        app: Optional[str] = None,
        api_key: Optional[str] = None,
        service_name: Optional[str] = None,
    ):
        self.app = (
            app
            or os.environ.get("APPINSIGHTS_RESOURCE_ID")
            or os.environ.get("APPINSIGHTS_APP")
            or os.environ.get("APPINSIGHTS_APP_ID")
        )
        self.api_key = api_key or os.environ.get("APPINSIGHTS_API_KEY")
        self.resource_group = os.environ.get("APPINSIGHTS_RESOURCE_GROUP") or os.environ.get("AZURE_RESOURCE_GROUP")

        self.service_name = (
            service_name
            or os.environ.get("GENAI_MEMORY_VIEWER_SERVICE_NAME")
            or os.environ.get("OTEL_SERVICE_NAME")
            or "genai-memory-stories"
        )

        if not self.app:
            raise ValueError(
                "App Insights identifier required for live trace viewing.\n"
                "Preferred: set APPINSIGHTS_RESOURCE_ID to your App Insights component resource id.\n"
                "Example:\n"
                "  APPINSIGHTS_RESOURCE_ID=/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Insights/components/<name>\n"
            )

        self._use_api_key = bool(self.api_key)
        self.session = requests.Session()
        if self._use_api_key:
            self.session.headers.update({"x-api-key": self.api_key, "Content-Type": "application/json"})

    def _execute_query(self, query: str, timespan: str = "PT1H") -> Dict[str, Any]:
        if self._use_api_key:
            return self._execute_query_api_key(query=query, timespan=timespan)
        return self._execute_query_azure_cli(query=query, timespan=timespan)

    def _execute_query_api_key(self, *, query: str, timespan: str) -> Dict[str, Any]:
        url = self.QUERY_API.format(app_id=self.app)
        payload = {"query": query, "timespan": timespan}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def _execute_query_azure_cli(self, *, query: str, timespan: str) -> Dict[str, Any]:
        if not shutil.which("az"):
            raise RuntimeError("Azure CLI not found. Install Azure CLI and run `az login`.")

        offset = self._timespan_to_kusto(timespan)
        cmd = [
            "az",
            "monitor",
            "app-insights",
            "query",
            "--analytics-query",
            query,
            "--offset",
            offset,
            "--output",
            "json",
            "--only-show-errors",
        ]

        if isinstance(self.app, str) and self.app.strip().lower().startswith("/subscriptions/"):
            cmd.extend(["--ids", self.app.strip()])
        else:
            cmd.extend(["--apps", self.app])
            if not self._GUID_RE.match(self.app) and self.resource_group:
                cmd.extend(["--resource-group", self.resource_group])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            detail = (result.stderr or "").strip() or (result.stdout or "").strip() or "Unknown Azure CLI error"
            raise RuntimeError(
                "Failed to query App Insights via Azure CLI.\n"
                "Ensure:\n"
                "  - `az login` succeeded\n"
                "  - APPINSIGHTS_RESOURCE_ID (or APPINSIGHTS_APP + APPINSIGHTS_RESOURCE_GROUP) is set\n"
                "  - your identity has access (Monitoring Reader / Log Analytics Reader)\n\n"
                f"Azure CLI error:\n{detail}"
            )

        return json.loads(result.stdout)

    def _parse_query_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        if "tables" not in results or not results["tables"]:
            return []

        table = results["tables"][0]
        columns = [col["name"] for col in table.get("columns", [])]
        rows = table.get("rows", [])
        return [dict(zip(columns, row)) for row in rows]

    def get_traces(
        self,
        *,
        timespan: str = "PT1H",
        story_id: Optional[int] = None,
        include_demos: bool = True,
        limit: int = 50,
    ) -> List[TraceTree]:
        window = self._timespan_to_kusto(timespan)

        root_filter = 'name startswith "story_"'
        if story_id is not None:
            root_filter = f'name startswith "story_{int(story_id)}"'
        elif include_demos:
            root_filter = '(name startswith "story_" or name startswith "demo_")'

        query = f"""
        let window = ago({window});
        let roots = dependencies
        | where timestamp > window
        | where cloud_RoleName == "{self.service_name}"
        | where {root_filter}
        | project operation_Id
        | summarize by operation_Id
        | take {limit};

        let spans = dependencies
        | where timestamp > window
        | where operation_Id in (roots)
        | extend traceId = operation_Id
        | extend spanId = id
        | extend parentSpanId = operation_ParentId
        | extend attributes = customDimensions
        | extend durationMs = todouble(duration)
        | project rowType="span", timestamp, traceId, spanId, parentSpanId, name, durationMs, success, attributes;

        let events = traces
        | where timestamp > window
        | where operation_Id in (roots)
        | where message in ("gen_ai.client.inference.operation.details", "gen_ai.evaluation.result")
        | extend traceId = operation_Id
        | extend spanId = operation_ParentId
        | extend attributes = customDimensions
        | project rowType="event", timestamp, traceId, spanId, parentSpanId="", name=message, durationMs=0.0, success=true, attributes;

        union spans, events
        | order by timestamp desc
        """

        results = self._execute_query(query, timespan)
        rows = self._parse_query_results(results)

        spans_by_trace: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        events_by_trace: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        for row in rows:
            trace_id = row.get("traceId")
            if not trace_id:
                continue
            if row.get("rowType") == "event":
                events_by_trace[trace_id].append(row)
            else:
                spans_by_trace[trace_id].append(row)

        traces: List[TraceTree] = []
        for trace_id, span_rows in spans_by_trace.items():
            trace = self._build_trace_tree(trace_id, span_rows)
            self._attach_events(trace, events_by_trace.get(trace_id, []))
            traces.append(trace)

        traces.sort(key=lambda t: (t.metadata.get("start_time") or ""), reverse=True)
        return traces[:limit]

    def get_events(self, *, timespan: str = "PT1H", limit: int = 200) -> List[Dict[str, Any]]:
        query = f"""
        traces
        | where timestamp > ago({self._timespan_to_kusto(timespan)})
        | where message in ("gen_ai.client.inference.operation.details", "gen_ai.evaluation.result")
        | extend traceId = operation_Id, spanId = operation_ParentId
        | project timestamp, traceId, spanId, message, customDimensions
        | order by timestamp desc
        | take {limit}
        """
        return self._parse_query_results(self._execute_query(query, timespan))

    def get_recent_operations(self, *, timespan: str = "PT1H", limit: int = 50) -> List[Dict[str, Any]]:
        query = f"""
        dependencies
        | where timestamp > ago({self._timespan_to_kusto(timespan)})
        | where cloud_RoleName == "{self.service_name}"
        | where name startswith "story_" or name startswith "demo_"
        | summarize
            StartTime = min(timestamp),
            EndTime = max(timestamp),
            SpanCount = count(),
            MemorySpanCount = countif(tostring(customDimensions["gen_ai.operation.name"]) in ("create_memory_store","search_memory","update_memory","delete_memory","delete_memory_store")),
            AgentSpanCount = countif(tostring(customDimensions["gen_ai.operation.name"]) in ("create_agent","invoke_agent","execute_tool"))
          by operation_Id
        | extend Duration = EndTime - StartTime
        | project TraceId = operation_Id, StartTime, EndTime, Duration, SpanCount, MemorySpanCount, AgentSpanCount
        | order by StartTime desc
        | take {limit}
        """
        return self._parse_query_results(self._execute_query(query, timespan))

    def _build_trace_tree(self, trace_id: str, raw_spans: List[Dict[str, Any]]) -> TraceTree:
        trace = TraceTree(trace_id=trace_id)
        spans_by_id: Dict[str, GenAISpan] = {}

        for raw in raw_spans:
            span = self._parse_span(raw)
            spans_by_id[span.span_id] = span
            trace.spans.append(span)

        for span in trace.spans:
            if not span.parent_span_id or span.parent_span_id not in spans_by_id:
                if trace.root_span is None or span.start_time < trace.root_span.start_time:
                    trace.root_span = span

        if trace.root_span:
            attrs = trace.root_span.attributes or {}
            trace.metadata = {
                "story_id": attrs.get("story.id"),
                "story_title": attrs.get("story.title"),
                "scenario_name": attrs.get("scenario.name"),
                "root_span_name": trace.root_span.name,
                "conversation_id": attrs.get("gen_ai.conversation.id") or trace.root_span.conversation_id,
                "start_time": trace.root_span.start_time,
            }

        return trace

    def _parse_span(self, raw: Dict[str, Any]) -> GenAISpan:
        attributes: Any = raw.get("attributes", {})
        if isinstance(attributes, str):
            try:
                attributes = json.loads(attributes)
            except Exception:
                attributes = {}

        def _to_int(value: Any) -> Optional[int]:
            if value is None:
                return None
            try:
                return int(value)
            except Exception:
                return None

        finish_reasons = attributes.get("gen_ai.response.finish_reasons")
        if isinstance(finish_reasons, str):
            try:
                finish_reasons = json.loads(finish_reasons)
            except Exception:
                finish_reasons = [finish_reasons]

        return GenAISpan(
            span_id=str(raw.get("spanId", "")),
            trace_id=str(raw.get("traceId", "")),
            parent_span_id=raw.get("parentSpanId") or None,
            name=str(raw.get("name", "")),
            start_time=str(raw.get("timestamp", "")),
            duration_ms=float(raw.get("durationMs", 0) or 0),
            operation_name=attributes.get("gen_ai.operation.name"),
            provider_name=attributes.get("gen_ai.provider.name"),
            request_model=attributes.get("gen_ai.request.model"),
            response_model=attributes.get("gen_ai.response.model"),
            response_id=attributes.get("gen_ai.response.id"),
            finish_reasons=finish_reasons,
            input_tokens=_to_int(attributes.get("gen_ai.usage.input_tokens")),
            output_tokens=_to_int(attributes.get("gen_ai.usage.output_tokens")),
            agent_id=attributes.get("gen_ai.agent.id"),
            agent_name=attributes.get("gen_ai.agent.name"),
            conversation_id=attributes.get("gen_ai.conversation.id"),
            attributes=attributes,
        )

    def _attach_events(self, trace: TraceTree, event_rows: List[Dict[str, Any]]) -> None:
        spans_by_id: Dict[str, GenAISpan] = {s.span_id: s for s in trace.spans if s.span_id}

        for raw in event_rows:
            span_id = raw.get("spanId")
            if not span_id or span_id not in spans_by_id:
                continue

            attributes: Any = raw.get("attributes", {})
            if isinstance(attributes, str):
                try:
                    attributes = json.loads(attributes)
                except Exception:
                    attributes = {}

            spans_by_id[span_id].events.append(
                GenAIEvent(
                    name=str(raw.get("name") or ""),
                    timestamp=str(raw.get("timestamp") or ""),
                    attributes=attributes if isinstance(attributes, dict) else {},
                )
            )

    def _timespan_to_kusto(self, timespan: str) -> str:
        conversions = {
            "PT15M": "15m",
            "PT30M": "30m",
            "PT1H": "1h",
            "PT2H": "2h",
            "PT6H": "6h",
            "PT12H": "12h",
            "PT24H": "24h",
            "P1D": "1d",
            "P7D": "7d",
            "P30D": "30d",
        }
        return conversions.get(timespan.upper(), "1h")


def get_retriever() -> AppInsightsTraceRetriever:
    app = (
        os.environ.get("APPINSIGHTS_RESOURCE_ID")
        or os.environ.get("APPINSIGHTS_APP")
        or os.environ.get("APPINSIGHTS_APP_ID")
    )
    api_key = os.environ.get("APPINSIGHTS_API_KEY")  # optional legacy

    if not app:
        raise ValueError(
            "App Insights not configured for live trace viewing.\n\n"
            "Entra ID / RBAC mode (recommended):\n"
            "  1) Run: az login\n"
            "  2) Set APPINSIGHTS_RESOURCE_ID to your component resource id, e.g.\n"
            "     /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Insights/components/<name>\n\n"
            "Alternative (legacy API key mode):\n"
            "  - Set APPINSIGHTS_APP_ID (Application ID from API Access blade)\n"
            "  - Set APPINSIGHTS_API_KEY (API key from API Access blade)\n"
        )

    return AppInsightsTraceRetriever(app=app, api_key=api_key)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test App Insights trace retrieval for GenAI Memory stories")
    parser.add_argument("--timespan", default="PT1H", help="Query timespan (ISO 8601)")
    parser.add_argument("--limit", type=int, default=5, help="Max traces")
    args = parser.parse_args()

    retriever = get_retriever()
    print(f"Service filter (cloud_RoleName): {retriever.service_name}")

    ops = retriever.get_recent_operations(timespan=args.timespan, limit=args.limit)
    print(f"Recent operations: {len(ops)}")
    for op in ops[: args.limit]:
        print(f"- {op.get('TraceId', '')[:16]}... spans={op.get('SpanCount')} memory={op.get('MemorySpanCount')}")
