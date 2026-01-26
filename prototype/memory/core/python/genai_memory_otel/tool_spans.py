"""
Tool span helpers for GenAI semantic conventions.

Implements the `execute_tool` span from:
  semantic-conventions/docs/gen-ai/gen-ai-spans.md#execute-tool-span
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional

from opentelemetry.trace import Span, SpanKind, Status, StatusCode

from .attributes import ErrorAttributes, GenAIAttributes
from .exporters import should_capture_content


def _safe_json_dumps(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False)
    except Exception:
        return json.dumps(str(value), ensure_ascii=False)


@contextmanager
def execute_tool_span(
    tracer,
    *,
    tool_name: str,
    tool_type: Optional[str] = None,
    tool_description: Optional[str] = None,
    tool_call_id: Optional[str] = None,
    arguments: Optional[Any] = None,
    result: Optional[Any] = None,
    capture_content: Optional[bool] = None,
    extra_attributes: Optional[Dict[str, Any]] = None,
) -> Generator[Span, None, None]:
    """
    Create an `execute_tool` INTERNAL span.

    Opt-in attributes (`gen_ai.tool.call.arguments`, `gen_ai.tool.call.result`) are only
    recorded when `capture_content` (or GENAI_MEMORY_CAPTURE_CONTENT) is enabled.
    """
    capture = should_capture_content() if capture_content is None else bool(capture_content)

    attrs: Dict[str, Any] = {
        GenAIAttributes.OPERATION_NAME: "execute_tool",
        "gen_ai.tool.name": tool_name,
    }
    if tool_type:
        attrs["gen_ai.tool.type"] = tool_type
    if tool_description:
        attrs["gen_ai.tool.description"] = tool_description
    if tool_call_id:
        attrs["gen_ai.tool.call.id"] = tool_call_id

    if capture and arguments is not None:
        attrs["gen_ai.tool.call.arguments"] = _safe_json_dumps(arguments)
    if capture and result is not None:
        attrs["gen_ai.tool.call.result"] = _safe_json_dumps(result)

    if extra_attributes:
        attrs.update(extra_attributes)

    with tracer.start_as_current_span(
        f"execute_tool {tool_name}",
        kind=SpanKind.INTERNAL,
        attributes=attrs,
    ) as span:
        try:
            yield span
        except Exception as exc:
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            span.set_attribute(ErrorAttributes.ERROR_TYPE, type(exc).__name__)
            raise

