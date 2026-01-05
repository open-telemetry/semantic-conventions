#!/usr/bin/env python3
"""
Demo chat models for prototype scripts.

Default behavior is "auto":
- If `OPENAI_API_KEY` is set, use a real OpenAI chat completion call.
- Otherwise, run fully offline (mock).

Environment variables:
  - DEMO_LLM_MODE: "auto" (default) | "mock" | "openai"
  - DEMO_OPENAI_MODEL: model name (default: "gpt-4o-mini")
  - DEMO_OPENAI_API: "auto" (default) | "responses" | "chat_completions"
  - OPENAI_API_KEY: required when DEMO_LLM_MODE=openai
  - OPENAI_BASE_URL: optional (default: "https://api.openai.com/v1")
  - DEMO_OPENAI_TIMEOUT_SECONDS: optional (default: 30)
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Optional


Message = Dict[str, str]


class ChatModelError(RuntimeError):
    pass


@dataclass(frozen=True)
class OpenAIChatConfig:
    api_key: str
    model: str = "gpt-4o-mini"
    base_url: str = "https://api.openai.com/v1"
    timeout_seconds: int = 30
    temperature: float = 0.0
    max_tokens: int = 256


class MockChatModel:
    """Deterministic, offline chat model for demos."""

    def invoke(self, messages: List[Message]) -> str:
        user_msg = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_msg = msg.get("content", "")
                break

        prompt = user_msg.lower()

        if "support" in prompt and "email" in prompt:
            return (
                "You can reach support at support@example.com or call 555-123-4567."
            )
        if "weather" in prompt:
            return "Seattle: 55°F, light rain."
        if "capital of france" in prompt:
            return "Paris."
        if "2 + 2" in prompt or "2+2" in prompt:
            return "2 + 2 = 4."

        return "I can help with that. What would you like to do next?"


class OpenAIChatModel:
    """Minimal OpenAI Chat Completions client using stdlib HTTP."""

    def __init__(self, config: OpenAIChatConfig):
        self._config = config

    def invoke(self, messages: List[Message]) -> str:
        api_mode = os.environ.get("DEMO_OPENAI_API", "auto").strip().lower()
        if api_mode not in {"auto", "responses", "chat_completions"}:
            raise ChatModelError(f"Unsupported DEMO_OPENAI_API: {api_mode!r}")

        # Heuristic: newer models (e.g., gpt-4.1) are best supported via Responses.
        if api_mode == "auto":
            api_mode = "responses" if self._config.model.startswith("gpt-4.1") else "chat_completions"

        if api_mode == "responses":
            return self._invoke_responses(messages)

        try:
            return self._invoke_chat_completions(messages)
        except ChatModelError as exc:
            # Fallback for models not supported on Chat Completions.
            msg = str(exc).lower()
            if "chat/completions" in msg or "not supported" in msg or "model" in msg:
                return self._invoke_responses(messages)
            raise

    def _request_json(self, path: str, payload: Dict) -> Dict:
        url = self._config.base_url.rstrip("/") + path
        request = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self._config.api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=self._config.timeout_seconds) as resp:
                body = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            try:
                body = exc.read().decode("utf-8", "replace")
            except Exception:
                body = ""

            detail = body.strip()
            try:
                data = json.loads(body)
                error = data.get("error") if isinstance(data, dict) else None
                if isinstance(error, dict) and error.get("message"):
                    detail = str(error["message"])
            except Exception:
                pass

            raise ChatModelError(f"OpenAI request failed ({exc.code}): {detail or exc.reason}") from None
        except Exception as exc:
            raise ChatModelError(f"OpenAI request failed: {exc}") from exc

        try:
            return json.loads(body)
        except Exception as exc:
            raise ChatModelError(f"OpenAI response parse failed: {exc}") from exc

    def _invoke_chat_completions(self, messages: List[Message]) -> str:
        data = self._request_json(
            "/chat/completions",
            {
                "model": self._config.model,
                "messages": messages,
                "temperature": self._config.temperature,
                "max_tokens": self._config.max_tokens,
            },
        )
        try:
            return data["choices"][0]["message"]["content"]
        except Exception as exc:
            raise ChatModelError(f"OpenAI chat.completions parse failed: {exc}") from exc

    def _invoke_responses(self, messages: List[Message]) -> str:
        input_items = []
        for msg in messages:
            role = msg.get("role", "user")
            text = msg.get("content", "")

            # Responses API distinguishes between user/system inputs vs prior assistant outputs.
            # If you include assistant turns for context, they must be encoded as output_text.
            part_type = "output_text" if role == "assistant" else "input_text"

            input_items.append(
                {
                    "role": role,
                    "content": [{"type": part_type, "text": text}],
                }
            )
        data = self._request_json(
            "/responses",
            {
                "model": self._config.model,
                "input": input_items,
                "temperature": self._config.temperature,
                "max_output_tokens": self._config.max_tokens,
            },
        )

        # Common convenience field.
        output_text = data.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text

        output = data.get("output", [])
        chunks: List[str] = []
        if isinstance(output, list):
            for item in output:
                if not isinstance(item, dict) or item.get("type") != "message":
                    continue
                content = item.get("content", [])
                if not isinstance(content, list):
                    continue
                for part in content:
                    if not isinstance(part, dict):
                        continue
                    if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                        chunks.append(part["text"])

        if chunks:
            return "\n".join(chunks).strip()

        raise ChatModelError("OpenAI responses parse failed: no output_text found")


def _get_env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ChatModelError(f"Invalid int for {name}: {value!r}") from exc


def get_chat_model(mode: Optional[str] = None):
    """
    Return a chat model for demos.

    Modes:
      - auto: openai if OPENAI_API_KEY is set, else mock (default)
      - mock: offline deterministic model
      - openai: real OpenAI call (requires OPENAI_API_KEY)
    """
    selected_mode = (mode or os.environ.get("DEMO_LLM_MODE", "auto")).strip().lower()

    if selected_mode == "mock":
        return MockChatModel()

    if selected_mode == "auto":
        if os.environ.get("OPENAI_API_KEY"):
            selected_mode = "openai"
        else:
            return MockChatModel()

    if selected_mode != "openai":
        raise ChatModelError(f"Unsupported DEMO_LLM_MODE: {selected_mode!r}")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ChatModelError("DEMO_LLM_MODE=openai requires OPENAI_API_KEY")

    model = os.environ.get("DEMO_OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    timeout_seconds = _get_env_int("DEMO_OPENAI_TIMEOUT_SECONDS", 30)

    return OpenAIChatModel(
        OpenAIChatConfig(
            api_key=api_key,
            model=model,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
        )
    )
