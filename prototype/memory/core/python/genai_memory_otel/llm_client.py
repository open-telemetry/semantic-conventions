"""
LLM client helper for GenAI Memory prototype stories.

This module provides:
- A small OpenAI client wrapper with a "mock" fallback
- GenAI chat span instrumentation (gen_ai.operation.name=chat)
- Optional GenAI span-events:
  - gen_ai.client.inference.operation.details
  - gen_ai.evaluation.result (helper)

Notes on structured attributes:
The GenAI semantic conventions specify structured payloads for message/tool
attributes when recorded on events. OpenTelemetry Python does not yet support
complex attribute types on spans/events, so this implementation serializes those
payloads to JSON strings as a best-effort fallback.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from opentelemetry.trace import Span, SpanKind, Status, StatusCode

from .attributes import GenAIAttributes, ErrorAttributes
from .exporters import should_capture_content


@dataclass(frozen=True)
class ChatResult:
    content: str
    provider_name: str
    request_model: str
    response_model: Optional[str] = None
    response_id: Optional[str] = None
    finish_reasons: Optional[List[str]] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None


def _safe_json_dumps(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False)
    except Exception:
        # Best-effort fallback.
        return json.dumps(str(value), ensure_ascii=False)


def _to_spec_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert chat messages in {"role": ..., "content": ...} format to the
    gen_ai.*.messages schema shape (role + parts).
    """
    out: List[Dict[str, Any]] = []
    for msg in messages:
        role = str(msg.get("role") or "user")
        content = msg.get("content")
        if content is None:
            content = ""
        out.append(
            {
                "role": role,
                "parts": [{"type": "text", "content": str(content)}],
            }
        )
    return out


def _server_address_from_base_url(base_url: Optional[str]) -> Optional[str]:
    if not base_url:
        return None
    try:
        parsed = urlparse(base_url)
        return parsed.hostname or None
    except Exception:
        return None


def add_inference_details_event(
    span: Span,
    *,
    operation_name: str,
    conversation_id: Optional[str] = None,
    request_model: Optional[str] = None,
    response_model: Optional[str] = None,
    response_id: Optional[str] = None,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    request_temperature: Optional[float] = None,
    request_max_tokens: Optional[int] = None,
    system_instructions: Optional[List[Dict[str, Any]]] = None,
    input_messages: Optional[List[Dict[str, Any]]] = None,
    output_messages: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """
    Emit `gen_ai.client.inference.operation.details` as a span event.

    Message/tool payloads are encoded as JSON strings due to OpenTelemetry Python
    attribute type limitations.
    """
    attrs: Dict[str, Any] = {GenAIAttributes.OPERATION_NAME: operation_name}

    if conversation_id:
        attrs[GenAIAttributes.CONVERSATION_ID] = conversation_id
    if request_model:
        attrs[GenAIAttributes.REQUEST_MODEL] = request_model
    if response_model:
        attrs[GenAIAttributes.RESPONSE_MODEL] = response_model
    if response_id:
        attrs["gen_ai.response.id"] = response_id
    if input_tokens is not None:
        attrs[GenAIAttributes.USAGE_INPUT_TOKENS] = int(input_tokens)
    if output_tokens is not None:
        attrs[GenAIAttributes.USAGE_OUTPUT_TOKENS] = int(output_tokens)
    if request_temperature is not None:
        attrs["gen_ai.request.temperature"] = float(request_temperature)
    if request_max_tokens is not None:
        attrs["gen_ai.request.max_tokens"] = int(request_max_tokens)

    # Opt-in sensitive content
    if system_instructions is not None:
        attrs["gen_ai.system_instructions"] = _safe_json_dumps(system_instructions)
    if input_messages is not None:
        attrs["gen_ai.input.messages"] = _safe_json_dumps(input_messages)
    if output_messages is not None:
        attrs["gen_ai.output.messages"] = _safe_json_dumps(output_messages)

    span.add_event("gen_ai.client.inference.operation.details", attributes=attrs)


def add_evaluation_result_event(
    span: Span,
    *,
    evaluation_name: str,
    score_label: Optional[str] = None,
    score_value: Optional[float] = None,
    explanation: Optional[str] = None,
    response_id: Optional[str] = None,
) -> None:
    """Emit `gen_ai.evaluation.result` as a span event."""
    attrs: Dict[str, Any] = {"gen_ai.evaluation.name": evaluation_name}
    if score_label is not None:
        attrs["gen_ai.evaluation.score.label"] = score_label
    if score_value is not None:
        attrs["gen_ai.evaluation.score.value"] = float(score_value)
    if explanation is not None:
        attrs["gen_ai.evaluation.explanation"] = explanation
    if response_id is not None:
        attrs["gen_ai.response.id"] = response_id
    span.add_event("gen_ai.evaluation.result", attributes=attrs)


class LLMClient:
    """
    Minimal LLM client wrapper (OpenAI + mock fallback).

    Environment variables:
      - DEMO_LLM_MODE: auto|openai|mock
      - DEMO_OPENAI_MODEL: model name
      - OPENAI_API_KEY: auth
      - OPENAI_BASE_URL: optional
    """

    def __init__(self) -> None:
        self._initialized = False
        self._client = None
        self.mode: str = "auto"
        self.model: str = "gpt-4o-mini"
        self.base_url: Optional[str] = None
        self.timeout_seconds: Optional[float] = None

    def _ensure_initialized(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        self.mode = os.environ.get("DEMO_LLM_MODE", "auto").lower()
        self.model = os.environ.get("DEMO_OPENAI_MODEL", os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))
        self.base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_BASE_URL".lower())
        try:
            self.timeout_seconds = float(os.environ.get("DEMO_OPENAI_TIMEOUT_SECONDS", "30"))
        except Exception:
            self.timeout_seconds = 30.0

        if self.mode in ("openai", "auto"):
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key and not api_key.startswith("sk-your"):
                try:
                    from openai import OpenAI  # type: ignore
                except Exception:
                    self.mode = "mock"
                    return

                kwargs: Dict[str, Any] = {"api_key": api_key}
                if self.base_url:
                    kwargs["base_url"] = self.base_url

                self._client = OpenAI(**kwargs)
                self.mode = "openai"
                return

        self.mode = "mock"

    def provider_name(self) -> str:
        self._ensure_initialized()
        return "openai" if self.mode == "openai" else "mock"

    def chat(
        self,
        tracer,
        *,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        conversation_id: Optional[str] = None,
        max_tokens: int = 150,
        temperature: float = 0.7,
        emit_events: bool = True,
        capture_content: Optional[bool] = None,
        evaluation_name: Optional[str] = None,
        evaluation_score_label: Optional[str] = None,
        evaluation_score_value: Optional[float] = None,
        evaluation_explanation: Optional[str] = None,
    ) -> ChatResult:
        """
        Make a chat request and record a GenAI chat span (and optional events).
        """
        self._ensure_initialized()
        capture = should_capture_content() if capture_content is None else bool(capture_content)
        provider = self.provider_name()
        request_model = self.model

        server_address = _server_address_from_base_url(self.base_url) or "api.openai.com"

        # Build OpenAI messages
        chat_messages: List[Dict[str, str]] = []
        if system_prompt:
            chat_messages.append({"role": "system", "content": system_prompt})
        chat_messages.extend(messages)

        with tracer.start_as_current_span(
            f"chat {request_model}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "chat",
                GenAIAttributes.PROVIDER_NAME: provider,
                GenAIAttributes.REQUEST_MODEL: request_model,
                **({GenAIAttributes.CONVERSATION_ID: conversation_id} if conversation_id else {}),
                "server.address": server_address,
                "gen_ai.request.max_tokens": int(max_tokens),
                "gen_ai.request.temperature": float(temperature),
            },
        ) as span:
            # Opt-in content capture on span attributes
            if capture:
                span.set_attribute("gen_ai.input.messages", _safe_json_dumps(_to_spec_messages(messages)))
                if system_prompt:
                    span.set_attribute(
                        "gen_ai.system_instructions",
                        _safe_json_dumps([{"type": "text", "content": system_prompt}]),
                    )

            try:
                if self.mode == "openai" and self._client is not None:
                    response = self._client.chat.completions.create(
                        model=request_model,
                        messages=chat_messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )
                    content = response.choices[0].message.content or ""
                    finish_reason = response.choices[0].finish_reason or "stop"
                    response_id = getattr(response, "id", None)
                    response_model = getattr(response, "model", None) or request_model
                    usage = getattr(response, "usage", None)
                    input_tokens = getattr(usage, "prompt_tokens", None) if usage else None
                    output_tokens = getattr(usage, "completion_tokens", None) if usage else None
                else:
                    # Mock response with predictable output.
                    last_msg = messages[-1]["content"] if messages else ""
                    content = f"[mock] I can help with: {last_msg[:120]}"
                    finish_reason = "stop"
                    response_id = None
                    response_model = request_model
                    input_tokens = len(last_msg.split()) * 2
                    output_tokens = len(content.split()) * 2

                # Recommended response attrs
                span.set_attribute(GenAIAttributes.RESPONSE_MODEL, response_model)
                span.set_attribute("gen_ai.response.finish_reasons", [finish_reason])
                if response_id:
                    span.set_attribute("gen_ai.response.id", response_id)
                if input_tokens is not None:
                    span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, int(input_tokens))
                if output_tokens is not None:
                    span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, int(output_tokens))

                if capture:
                    span.set_attribute(
                        "gen_ai.output.messages",
                        _safe_json_dumps(
                            [
                                {
                                    "role": "assistant",
                                    "parts": [{"type": "text", "content": content}],
                                    "finish_reason": finish_reason,
                                }
                            ]
                        ),
                    )

                if emit_events:
                    add_inference_details_event(
                        span,
                        operation_name="chat",
                        conversation_id=conversation_id,
                        request_model=request_model,
                        response_model=response_model,
                        response_id=response_id,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        request_temperature=temperature,
                        request_max_tokens=max_tokens,
                        system_instructions=(
                            [{"type": "text", "content": system_prompt}] if (capture and system_prompt) else None
                        ),
                        input_messages=_to_spec_messages(messages) if capture else None,
                        output_messages=(
                            [
                                {
                                    "role": "assistant",
                                    "parts": [{"type": "text", "content": content}],
                                    "finish_reason": finish_reason,
                                }
                            ]
                            if capture
                            else None
                        ),
                    )

                if evaluation_name:
                    add_evaluation_result_event(
                        span,
                        evaluation_name=evaluation_name,
                        score_label=evaluation_score_label,
                        score_value=evaluation_score_value,
                        explanation=evaluation_explanation,
                        response_id=response_id,
                    )

                return ChatResult(
                    content=content,
                    provider_name=provider,
                    request_model=request_model,
                    response_model=response_model,
                    response_id=response_id,
                    finish_reasons=[finish_reason],
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                )
            except Exception as exc:
                span.set_status(Status(StatusCode.ERROR, str(exc)))
                span.set_attribute(ErrorAttributes.ERROR_TYPE, type(exc).__name__)
                raise
