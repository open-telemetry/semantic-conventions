#!/usr/bin/env python3
"""
Azure Application Insights Trace Retriever

Retrieves OpenTelemetry traces from App Insights using Azure RBAC (Entra ID).
Parses the traces into a hierarchical structure suitable for visualization.

Prerequisites:
    1. Azure App Insights resource with trace data
    2. You have access via Entra ID (Azure RBAC) and have run `az login`

Environment Variables:
    APPINSIGHTS_RESOURCE_ID - (Recommended) Azure resource id of your App Insights component
      Example:
        /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Insights/components/<name>

    OR

    APPINSIGHTS_APP - App identifier accepted by `az monitor app-insights query --apps`:
      - application GUID (API Access blade)
      - Azure resource name (requires APPINSIGHTS_RESOURCE_GROUP)
      - fully-qualified Azure resource id

    Optional:
      APPINSIGHTS_RESOURCE_GROUP - required when APPINSIGHTS_APP is just a name

Usage:
    from trace_retriever import AppInsightsTraceRetriever

    retriever = AppInsightsTraceRetriever()
    traces = retriever.get_guardian_traces(timespan="PT1H")
"""

import os
import sys
import json
import re
import shutil
import subprocess
import requests
from collections import defaultdict
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from urllib.parse import urlencode


@dataclass
class SecurityFinding:
    """A security finding event from a guardian span."""
    risk_category: str
    risk_severity: str
    risk_score: float
    policy_id: Optional[str] = None
    policy_name: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Any] = None


@dataclass
class GuardianSpan:
    """Parsed apply_guardrail span with findings."""
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: str
    end_time: str
    duration_ms: float

    # Guardian-specific attributes
    guardian_name: Optional[str] = None
    guardian_provider: Optional[str] = None
    guardian_version: Optional[str] = None
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    decision: Optional[str] = None
    agent_id: Optional[str] = None
    conversation_id: Optional[str] = None

    # GenAI chat span attributes (gen-ai-spans.md)
    operation_name: Optional[str] = None
    provider_name: Optional[str] = None
    request_model: Optional[str] = None
    response_model: Optional[str] = None
    response_id: Optional[str] = None
    finish_reasons: Optional[List[str]] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

    # Findings
    findings: List[SecurityFinding] = field(default_factory=list)

    # Raw attributes for debugging
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        d = asdict(self)
        return d


@dataclass
class TraceTree:
    """A complete trace with hierarchical spans."""
    trace_id: str
    root_span: Optional[GuardianSpan] = None
    spans: List[GuardianSpan] = field(default_factory=list)
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

    Uses the App Insights REST Query API to execute KQL queries
    and returns structured trace data.
    """

    # Legacy API endpoint (API Key auth). Kept for backward compatibility.
    QUERY_API = "https://api.applicationinsights.io/v1/apps/{app_id}/query"

    _GUID_RE = re.compile(
        r"^[0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12}$"
    )

    def __init__(self, app: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the retriever.

        Args:
            app: App identifier for queries. Recommended: Azure resource id of the App Insights component.
            api_key: Optional legacy App Insights API Key (API Access blade). If provided, uses the REST Query API.
        """
        self.app = (
            app
            or os.environ.get("APPINSIGHTS_RESOURCE_ID")
            or os.environ.get("APPINSIGHTS_APP")
            or os.environ.get("APPINSIGHTS_APP_ID")  # legacy name (may contain GUID)
        )
        self.api_key = api_key or os.environ.get("APPINSIGHTS_API_KEY")
        self.resource_group = os.environ.get("APPINSIGHTS_RESOURCE_GROUP") or os.environ.get("AZURE_RESOURCE_GROUP")

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
            self.session.headers.update({
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
            })

    def _execute_query(self, query: str, timespan: str = "PT1H") -> Dict[str, Any]:
        """
        Execute a KQL query against App Insights.

        Args:
            query: KQL query string
            timespan: ISO 8601 duration (e.g., PT1H, PT24H, P7D)

        Returns:
            Query results as dictionary
        """
        if self._use_api_key:
            return self._execute_query_api_key(query=query, timespan=timespan)
        return self._execute_query_azure_cli(query=query, timespan=timespan)

    def _execute_query_api_key(self, query: str, timespan: str) -> Dict[str, Any]:
        """Execute a query via the legacy App Insights Query REST API (API Key auth)."""
        url = self.QUERY_API.format(app_id=self.app)
        payload = {"query": query, "timespan": timespan}

        response = self.session.post(url, json=payload)
        if response.status_code == 401:
            raise PermissionError(
                "App Insights API authentication failed.\n"
                "If API keys are disabled for your org, do not set APPINSIGHTS_API_KEY;\n"
                "instead use Entra ID by setting APPINSIGHTS_RESOURCE_ID and running `az login`."
            )
        if response.status_code == 400:
            error_detail = response.json().get("error", {}).get("message", "Unknown error")
            raise ValueError(f"Invalid query: {error_detail}")

        response.raise_for_status()
        return response.json()

    def _execute_query_azure_cli(self, query: str, timespan: str) -> Dict[str, Any]:
        """
        Execute a query using Azure CLI (Entra ID / RBAC).

        Requires:
          - `az` installed
          - `az login` already performed
          - App Insights query permissions (e.g., Monitoring Reader on the component)
        """
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

        # Prefer resource id when available.
        if isinstance(self.app, str) and self.app.strip().lower().startswith("/subscriptions/"):
            cmd.extend(["--ids", self.app.strip()])
        else:
            cmd.extend(["--apps", self.app])
            # If it's just a name (not a GUID), resource group is required.
            if not self._GUID_RE.match(self.app) and self.resource_group:
                cmd.extend(["--resource-group", self.resource_group])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            stderr = (result.stderr or "").strip()
            stdout = (result.stdout or "").strip()
            detail = stderr or stdout or "Unknown Azure CLI error"
            raise RuntimeError(
                "Failed to query App Insights via Azure CLI.\n"
                "Ensure:\n"
                "  - `az login` succeeded\n"
                "  - APPINSIGHTS_RESOURCE_ID (or APPINSIGHTS_APP + APPINSIGHTS_RESOURCE_GROUP) is set\n"
                "  - your identity has access (Monitoring Reader / Log Analytics Reader)\n\n"
                f"Azure CLI error:\n{detail}"
            )

        try:
            return json.loads(result.stdout)
        except Exception as exc:
            raise RuntimeError(f"Failed to parse Azure CLI output as JSON: {exc}") from exc

    def _parse_query_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse App Insights query results into a list of dictionaries.

        App Insights returns data in a columnar format:
        {
            "tables": [{
                "name": "PrimaryResult",
                "columns": [{"name": "col1", "type": "string"}, ...],
                "rows": [["val1", ...], ...]
            }]
        }
        """
        if "tables" not in results or not results["tables"]:
            return []

        table = results["tables"][0]
        columns = [col["name"] for col in table.get("columns", [])]
        rows = table.get("rows", [])

        return [dict(zip(columns, row)) for row in rows]

    def get_guardian_traces(
        self,
        timespan: str = "PT1H",
        story_id: Optional[int] = None,
        limit: int = 100
    ) -> List[TraceTree]:
        """
        Retrieve guardian traces from App Insights.

        Args:
            timespan: ISO 8601 duration for query window
            story_id: Optional story ID to filter by
            limit: Maximum number of traces to return

        Returns:
            List of TraceTree objects with parsed spans
        """
        window = self._timespan_to_kusto(timespan)
        story_root_filter = 'name startswith "story_"'
        if story_id is not None:
            story_root_filter = f'name startswith "story_{int(story_id)}"'

        # Single query returns both spans (dependencies) and finding events (traces).
        query = f"""
        let window = ago({window});
        let roots = dependencies
        | where timestamp > window
        | where cloud_RoleName == "genai-guardian-stories"
        | where {story_root_filter}
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

        let findings = traces
        | where timestamp > window
        | where operation_Id in (roots)
        | where message == "gen_ai.security.finding"
        | extend traceId = operation_Id
        | extend spanId = operation_ParentId
        | extend attributes = customDimensions
        | project rowType="finding", timestamp, traceId, spanId, parentSpanId="", name=message, durationMs=0.0, success=true, attributes;

        union spans, findings
        | order by timestamp desc
        """

        results = self._execute_query(query, timespan)
        rows = self._parse_query_results(results)

        spans_by_trace = defaultdict(list)  # traceId -> span rows
        finding_rows_by_trace = defaultdict(list)  # traceId -> finding rows

        for row in rows:
            trace_id = row.get("traceId")
            if not trace_id:
                continue
            if row.get("rowType") == "finding":
                finding_rows_by_trace[trace_id].append(row)
            else:
                spans_by_trace[trace_id].append(row)

        traces: List[TraceTree] = []
        for trace_id, span_rows in spans_by_trace.items():
            trace = self._build_trace_tree(trace_id, span_rows)
            self._attach_findings(trace, finding_rows_by_trace.get(trace_id, []))

            # Only include traces that have at least one guardian evaluation span.
            if any(s.name and "apply_guardrail" in s.name for s in trace.spans):
                traces.append(trace)

        # Newest first (best-effort)
        traces.sort(key=lambda t: (t.metadata.get("start_time") or ""), reverse=True)
        return traces[:limit]

    def get_guardian_events(self, timespan: str = "PT1H", limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve gen_ai.security.finding events.

        Note: when exporting OpenTelemetry span events to App Insights via the Azure Monitor exporter,
        these events appear in the `traces` table as MessageData (not `customEvents`).

        Args:
            timespan: ISO 8601 duration for query window
            limit: Maximum events to return

        Returns:
            List of security finding events
        """
        query = f"""
        traces
        | where message == "gen_ai.security.finding"
        | where timestamp > ago({self._timespan_to_kusto(timespan)})
        | extend
            riskCategory = tostring(customDimensions["gen_ai.security.risk.category"]),
            riskSeverity = tostring(customDimensions["gen_ai.security.risk.severity"]),
            riskScore = todouble(customDimensions["gen_ai.security.risk.score"]),
            policyId = tostring(customDimensions["gen_ai.security.policy.id"]),
            policyName = tostring(customDimensions["gen_ai.security.policy.name"]),
            traceId = operation_Id,
            spanId = operation_ParentId
        | project
            timestamp,
            traceId,
            spanId,
            riskCategory,
            riskSeverity,
            riskScore,
            policyId,
            policyName,
            customDimensions
        | order by timestamp desc
        | take {limit}
        """

        results = self._execute_query(query, timespan)
        return self._parse_query_results(results)

    def get_recent_operations(self, timespan: str = "PT1H", limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent operations/traces with summary info.

        Returns a list of unique trace IDs with metadata for the UI to display.
        """
        query = f"""
        dependencies
        | where timestamp > ago({self._timespan_to_kusto(timespan)})
        | where name startswith "story_" or name startswith "demo_"
        | summarize
            StartTime = min(timestamp),
            EndTime = max(timestamp),
            SpanCount = count(),
            GuardianCount = countif(name contains "apply_guardrail")
          by operation_Id
        | extend Duration = EndTime - StartTime
        | project
            TraceId = operation_Id,
            StartTime,
            EndTime,
            Duration,
            SpanCount,
            GuardianCount
        | order by StartTime desc
        | take {limit}
        """

        results = self._execute_query(query, timespan)
        return self._parse_query_results(results)

    def _build_trace_tree(self, trace_id: str, raw_spans: List[Dict]) -> TraceTree:
        """Build a TraceTree from raw span data."""
        trace = TraceTree(trace_id=trace_id)

        spans_by_id: Dict[str, GuardianSpan] = {}

        for raw in raw_spans:
            span = self._parse_span(raw)
            spans_by_id[span.span_id] = span
            trace.spans.append(span)

        # Find root span (no parent or parent not in this trace)
        for span in trace.spans:
            if not span.parent_span_id or span.parent_span_id not in spans_by_id:
                if trace.root_span is None or span.start_time < trace.root_span.start_time:
                    trace.root_span = span

        # Extract metadata from root span
        if trace.root_span:
            trace.metadata = {
                "story_id": trace.root_span.attributes.get("story.id"),
                "story_title": trace.root_span.attributes.get("story.title"),
                "scenario_name": trace.root_span.attributes.get("scenario.name"),
                "root_span_name": trace.root_span.name,
                "conversation_id": (
                    trace.root_span.attributes.get("gen_ai.conversation.id")
                    or trace.root_span.conversation_id
                ),
                "tenant_id": trace.root_span.attributes.get("tenant.id"),
                "start_time": trace.root_span.start_time,
            }

        return trace

    def _parse_span(self, raw: Dict[str, Any]) -> GuardianSpan:
        """Parse a raw span dictionary into a GuardianSpan."""
        # Parse attributes (stored as JSON string in App Insights)
        attributes = raw.get("attributes", {})
        if isinstance(attributes, str):
            try:
                attributes = json.loads(attributes)
            except json.JSONDecodeError:
                attributes = {}

        # Helper to safely parse integer values
        def _to_int(value: Any) -> Optional[int]:
            if value is None:
                return None
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

        # Parse finish_reasons - could be a string or list
        finish_reasons = attributes.get("gen_ai.response.finish_reasons")
        if isinstance(finish_reasons, str):
            try:
                finish_reasons = json.loads(finish_reasons)
            except json.JSONDecodeError:
                finish_reasons = [finish_reasons]

        span = GuardianSpan(
            span_id=raw.get("spanId", ""),
            trace_id=raw.get("traceId", ""),
            parent_span_id=raw.get("parentSpanId"),
            name=raw.get("name", ""),
            start_time=str(raw.get("timestamp", "")),
            end_time="",  # App Insights doesn't give end time directly
            duration_ms=float(raw.get("durationMs", 0) or 0),

            # Guardian attributes
            guardian_name=attributes.get("gen_ai.guardian.name"),
            guardian_provider=attributes.get("gen_ai.guardian.provider.name"),
            guardian_version=attributes.get("gen_ai.guardian.version"),
            target_type=attributes.get("gen_ai.security.target.type"),
            target_id=attributes.get("gen_ai.security.target.id"),
            decision=attributes.get("gen_ai.security.decision.type"),
            agent_id=attributes.get("gen_ai.agent.id"),
            conversation_id=attributes.get("gen_ai.conversation.id"),

            # GenAI chat span attributes (gen-ai-spans.md)
            operation_name=attributes.get("gen_ai.operation.name"),
            provider_name=attributes.get("gen_ai.provider.name"),
            request_model=attributes.get("gen_ai.request.model"),
            response_model=attributes.get("gen_ai.response.model"),
            response_id=attributes.get("gen_ai.response.id"),
            finish_reasons=finish_reasons,
            input_tokens=_to_int(attributes.get("gen_ai.usage.input_tokens")),
            output_tokens=_to_int(attributes.get("gen_ai.usage.output_tokens")),

            attributes=attributes,
        )

        return span

    def _attach_findings(self, trace: TraceTree, finding_rows: List[Dict[str, Any]]) -> None:
        """Attach finding events (span events) to their parent spans in the trace tree."""
        spans_by_id: Dict[str, GuardianSpan] = {s.span_id: s for s in trace.spans if s.span_id}

        for raw in finding_rows:
            span_id = raw.get("spanId")
            if not span_id or span_id not in spans_by_id:
                continue

            attributes = raw.get("attributes", {})
            if isinstance(attributes, str):
                try:
                    attributes = json.loads(attributes)
                except json.JSONDecodeError:
                    attributes = {}

            def _to_float(value: Any, default: float = 0.0) -> float:
                try:
                    return float(value)
                except Exception:
                    return default

            finding = SecurityFinding(
                risk_category=str(attributes.get("gen_ai.security.risk.category") or ""),
                risk_severity=str(attributes.get("gen_ai.security.risk.severity") or ""),
                risk_score=_to_float(attributes.get("gen_ai.security.risk.score"), 0.0),
                policy_id=attributes.get("gen_ai.security.policy.id"),
                policy_name=attributes.get("gen_ai.security.policy.name"),
                timestamp=str(raw.get("timestamp", "")) if raw.get("timestamp") is not None else None,
                metadata=attributes.get("gen_ai.security.risk.metadata"),
            )

            spans_by_id[span_id].findings.append(finding)

    def _timespan_to_kusto(self, timespan: str) -> str:
        """
        Convert ISO 8601 duration to Kusto timespan format.

        PT1H -> 1h
        PT30M -> 30m
        P1D -> 1d
        P7D -> 7d
        """
        # Simple conversion for common cases
        conversions = {
            "PT1H": "1h",
            "PT2H": "2h",
            "PT6H": "6h",
            "PT12H": "12h",
            "PT24H": "24h",
            "PT30M": "30m",
            "PT15M": "15m",
            "P1D": "1d",
            "P7D": "7d",
            "P30D": "30d",
        }
        return conversions.get(timespan.upper(), "1h")


def get_retriever() -> AppInsightsTraceRetriever:
    """
    Factory function to get the App Insights retriever.

    Returns:
        AppInsightsTraceRetriever instance

    Raises:
        ValueError: If App Insights credentials are not configured
    """
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

    parser = argparse.ArgumentParser(description="Test App Insights trace retrieval")
    parser.add_argument("--timespan", default="PT1H", help="Query timespan (ISO 8601)")
    args = parser.parse_args()

    try:
        retriever = get_retriever()
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    print("=" * 60)
    print("  App Insights Trace Retriever Test")
    print("=" * 60)

    print("\n1. Recent Operations:")
    ops = retriever.get_recent_operations(timespan=args.timespan, limit=5)
    for op in ops:
        print(f"   - {op.get('TraceId', 'N/A')[:16]}... "
              f"({op.get('SpanCount', 0)} spans, {op.get('GuardianCount', 0)} guardians)")

    print("\n2. Guardian Traces:")
    traces = retriever.get_guardian_traces(timespan=args.timespan, limit=3)
    for trace in traces:
        print(f"\n   Trace: {trace.trace_id[:16]}...")
        print(f"   Story: {trace.metadata.get('story_title', 'Unknown')}")
        print(f"   Spans: {len(trace.spans)}")
        for span in trace.spans[:5]:
            decision = span.decision or "N/A"
            findings_count = len(span.findings)
            print(f"     - {span.name} [{decision}] ({findings_count} findings)")

    print("\n3. Security Events:")
    events = retriever.get_guardian_events(timespan=args.timespan, limit=5)
    for event in events:
        print(f"   - [{event.get('riskSeverity', 'N/A')}] "
              f"{event.get('riskCategory', 'N/A')} "
              f"(score: {event.get('riskScore', 0):.2f})")

    print("\n" + "=" * 60)
