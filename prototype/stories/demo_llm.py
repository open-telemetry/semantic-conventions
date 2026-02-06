#!/usr/bin/env python3
"""
Story helper: optional real LLM calls.

Stories are designed to run fully offline, but when `DEMO_LLM_MODE=openai`
and `OPENAI_API_KEY` is set (typically via `prototype/stories/.env.local`),
they can call a real OpenAI model via `prototype/demo_chat.py` (stdlib HTTP).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from urllib.parse import urlparse

from demo_chat import MockChatModel, get_chat_model


Message = Dict[str, str]


@dataclass(frozen=True)
class DemoLLMRuntime:
    provider_name: str
    model_name: str
    server_address: Optional[str]


def _server_address_from_base_url(base_url: str) -> Optional[str]:
    if not base_url:
        return None
    try:
        parsed = urlparse(base_url)
    except Exception:
        return None
    return parsed.hostname


def estimate_tokens(text: str) -> int:
    # Rough approximation: ~1.3 tokens/word (good enough for demos).
    return int(len((text or "").split()) * 1.3)


def estimate_message_tokens(messages: List[Message]) -> int:
    return sum(estimate_tokens(m.get("content", "")) for m in messages)


class DemoLLM:
    def __init__(self, mode: Optional[str] = None):
        self._model = get_chat_model(mode)
        self.runtime = self._detect_runtime()

    def _detect_runtime(self) -> DemoLLMRuntime:
        if isinstance(self._model, MockChatModel):
            return DemoLLMRuntime(provider_name="mock", model_name="mock-llm", server_address=None)

        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        return DemoLLMRuntime(
            provider_name="openai",
            model_name=os.environ.get("DEMO_OPENAI_MODEL", "gpt-4o-mini"),
            server_address=_server_address_from_base_url(base_url) or "api.openai.com",
        )

    def invoke(self, messages: List[Message]) -> str:
        return self._model.invoke(messages)

