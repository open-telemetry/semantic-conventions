#!/usr/bin/env python3
"""
GenAI Chat Span Utilities

Provides proper OpenTelemetry instrumentation for GenAI chat operations
following the semantic conventions from:
  docs/gen-ai/gen-ai-spans.md

This module creates chat spans with all required, conditionally required,
and recommended attributes according to the spec.

Attributes Reference (from gen-ai-spans.md):

Required:
  - gen_ai.operation.name: "chat"
  - gen_ai.provider.name: "openai", "mock", etc.

Conditionally Required:
  - gen_ai.request.model: If available
  - gen_ai.conversation.id: When available

Recommended:
  - gen_ai.response.model: Actual model used
  - gen_ai.usage.input_tokens: Token count
  - gen_ai.usage.output_tokens: Token count
  - gen_ai.response.finish_reasons: ["stop"]
  - gen_ai.response.id: Completion ID
  - server.address: API endpoint

Opt-In (sensitive, controlled by environment):
  - gen_ai.input.messages: Input messages
  - gen_ai.output.messages: Output messages
  - gen_ai.system_instructions: System prompt
"""

import json
import os
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode


# =============================================================================
# Semantic Convention Attribute Names
# =============================================================================

# Required
GEN_AI_OPERATION_NAME = "gen_ai.operation.name"
GEN_AI_PROVIDER_NAME = "gen_ai.provider.name"

# Conditionally Required
GEN_AI_REQUEST_MODEL = "gen_ai.request.model"
GEN_AI_CONVERSATION_ID = "gen_ai.conversation.id"

# Recommended
GEN_AI_RESPONSE_MODEL = "gen_ai.response.model"
GEN_AI_RESPONSE_ID = "gen_ai.response.id"
GEN_AI_RESPONSE_FINISH_REASONS = "gen_ai.response.finish_reasons"
GEN_AI_USAGE_INPUT_TOKENS = "gen_ai.usage.input_tokens"
GEN_AI_USAGE_OUTPUT_TOKENS = "gen_ai.usage.output_tokens"
GEN_AI_REQUEST_TEMPERATURE = "gen_ai.request.temperature"
GEN_AI_REQUEST_MAX_TOKENS = "gen_ai.request.max_tokens"
SERVER_ADDRESS = "server.address"

# Opt-In (sensitive)
GEN_AI_INPUT_MESSAGES = "gen_ai.input.messages"
GEN_AI_OUTPUT_MESSAGES = "gen_ai.output.messages"
GEN_AI_SYSTEM_INSTRUCTIONS = "gen_ai.system_instructions"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ChatMessage:
    """A chat message in the conversation."""
    role: str  # "user", "assistant", "system", "tool"
    content: str
    name: Optional[str] = None

    def to_spec_format(self) -> Dict[str, Any]:
        """Convert to the gen_ai.input.messages / gen_ai.output.messages format."""
        message = {
            "role": self.role,
            "parts": [
                {"type": "text", "content": self.content}
            ]
        }
        return message


@dataclass
class ChatRequest:
    """A chat completion request."""
    messages: List[ChatMessage]
    model: str = "gpt-4o"
    temperature: float = 0.0
    max_tokens: int = 256
    system_instructions: Optional[str] = None


@dataclass
class ChatResponse:
    """A chat completion response."""
    content: str
    model: str
    finish_reason: str = "stop"
    response_id: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class ChatConfig:
    """Configuration for chat span instrumentation."""
    provider_name: str = "mock"
    server_address: Optional[str] = None
    capture_content: bool = False  # Opt-in for sensitive content

    @classmethod
    def from_environment(cls) -> "ChatConfig":
        """Create config from environment variables."""
        capture_content = os.environ.get(
            "OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT", "false"
        ).lower() == "true"

        return cls(
            provider_name="openai" if os.environ.get("OPENAI_API_KEY") else "mock",
            server_address="api.openai.com" if os.environ.get("OPENAI_API_KEY") else None,
            capture_content=capture_content,
        )


# =============================================================================
# Chat Span Context Manager
# =============================================================================

class ChatSpanContext:
    """
    Context manager for creating properly instrumented chat spans.

    Usage:
        with ChatSpanContext(tracer, request, conversation_id="conv-123") as ctx:
            # Make LLM call
            response = llm.chat(request.messages)

            # Record the response
            ctx.set_response(ChatResponse(
                content=response.content,
                model=response.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
            ))
    """

    def __init__(
        self,
        tracer: trace.Tracer,
        request: ChatRequest,
        conversation_id: Optional[str] = None,
        config: Optional[ChatConfig] = None,
    ):
        self.tracer = tracer
        self.request = request
        self.conversation_id = conversation_id
        self.config = config or ChatConfig.from_environment()
        self.span: Optional[trace.Span] = None
        self._response: Optional[ChatResponse] = None
        self._span_cm = None

    def __enter__(self) -> "ChatSpanContext":
        # Span name: "{operation_name} {model}"
        span_name = f"chat {self.request.model}"

        self._span_cm = self.tracer.start_as_current_span(
            span_name,
            kind=SpanKind.CLIENT,
        )
        self.span = self._span_cm.__enter__()

        # Required attributes
        self.span.set_attribute(GEN_AI_OPERATION_NAME, "chat")
        self.span.set_attribute(GEN_AI_PROVIDER_NAME, self.config.provider_name)

        # Conditionally Required
        self.span.set_attribute(GEN_AI_REQUEST_MODEL, self.request.model)
        if self.conversation_id:
            self.span.set_attribute(GEN_AI_CONVERSATION_ID, self.conversation_id)

        # Recommended request attributes
        if self.request.temperature is not None:
            self.span.set_attribute(GEN_AI_REQUEST_TEMPERATURE, self.request.temperature)
        if self.request.max_tokens:
            self.span.set_attribute(GEN_AI_REQUEST_MAX_TOKENS, self.request.max_tokens)
        if self.config.server_address:
            self.span.set_attribute(SERVER_ADDRESS, self.config.server_address)

        # Opt-in content capture
        if self.config.capture_content:
            # Format messages according to spec
            input_messages = [m.to_spec_format() for m in self.request.messages]
            self.span.set_attribute(GEN_AI_INPUT_MESSAGES, json.dumps(input_messages))

            if self.request.system_instructions:
                system_instructions = [{"type": "text", "content": self.request.system_instructions}]
                self.span.set_attribute(GEN_AI_SYSTEM_INSTRUCTIONS, json.dumps(system_instructions))

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            if exc_type:
                self.span.set_status(Status(StatusCode.ERROR, str(exc_val)))
                self.span.set_attribute("error.type", exc_type.__name__)
            else:
                self.span.set_status(Status(StatusCode.OK))
            if self._span_cm is not None:
                self._span_cm.__exit__(exc_type, exc_val, exc_tb)
        return False

    def set_response(self, response: ChatResponse):
        """Set the response attributes on the span."""
        self._response = response

        if self.span:
            # Recommended response attributes
            self.span.set_attribute(GEN_AI_RESPONSE_MODEL, response.model)
            self.span.set_attribute(GEN_AI_RESPONSE_FINISH_REASONS, [response.finish_reason])

            if response.response_id:
                self.span.set_attribute(GEN_AI_RESPONSE_ID, response.response_id)

            if response.input_tokens is not None:
                self.span.set_attribute(GEN_AI_USAGE_INPUT_TOKENS, response.input_tokens)
            if response.output_tokens is not None:
                self.span.set_attribute(GEN_AI_USAGE_OUTPUT_TOKENS, response.output_tokens)

            # Opt-in content capture
            if self.config.capture_content:
                output_messages = [{
                    "role": "assistant",
                    "parts": [{"type": "text", "content": response.content}],
                    "finish_reason": response.finish_reason
                }]
                self.span.set_attribute(GEN_AI_OUTPUT_MESSAGES, json.dumps(output_messages))


# =============================================================================
# High-Level Chat Function
# =============================================================================

def create_chat_span(
    tracer: trace.Tracer,
    request: ChatRequest,
    conversation_id: Optional[str] = None,
    config: Optional[ChatConfig] = None,
) -> ChatSpanContext:
    """
    Create a chat span context manager.

    Args:
        tracer: OpenTelemetry tracer
        request: ChatRequest with messages and model
        conversation_id: Optional conversation ID for correlation
        config: Optional ChatConfig for instrumentation settings

    Returns:
        ChatSpanContext to use as context manager

    Example:
        tracer = trace.get_tracer("my-service")
        request = ChatRequest(
            messages=[ChatMessage(role="user", content="Hello!")],
            model="gpt-4o"
        )

        with create_chat_span(tracer, request, conversation_id="conv-123") as ctx:
            response = call_llm(request)
            ctx.set_response(ChatResponse(
                content=response.text,
                model=response.model,
                input_tokens=100,
                output_tokens=50
            ))
    """
    return ChatSpanContext(tracer, request, conversation_id, config)


# =============================================================================
# Mock LLM for Testing
# =============================================================================

class MockLLM:
    """
    Mock LLM that returns deterministic responses.
    Estimates token counts for realistic instrumentation.
    """

    MODEL_NAME = "mock-llm-v1"

    def __init__(self):
        self.response_id_counter = 0

    def chat(self, messages: List[ChatMessage], system_prompt: Optional[str] = None) -> ChatResponse:
        """Generate a mock response based on the last user message."""
        self.response_id_counter += 1

        # Find last user message
        user_content = ""
        for msg in reversed(messages):
            if msg.role == "user":
                user_content = msg.content.lower()
                break

        # Generate response based on content
        if "contact" in user_content or "email" in user_content:
            content = "You can reach support at support@example.com or call 555-123-4567."
        elif "weather" in user_content:
            content = "The weather is currently 72°F and sunny."
        elif "capital" in user_content and "france" in user_content:
            content = "The capital of France is Paris."
        elif "hello" in user_content or "hi" in user_content:
            content = "Hello! How can I assist you today?"
        elif "account" in user_content:
            content = "Your account is in good standing. Account ID: ACC-12345."
        else:
            content = "I understand your request. Let me help you with that."

        # Estimate tokens (rough approximation)
        input_tokens = sum(len(m.content.split()) * 1.3 for m in messages)
        if system_prompt:
            input_tokens += len(system_prompt.split()) * 1.3
        output_tokens = len(content.split()) * 1.3

        return ChatResponse(
            content=content,
            model=self.MODEL_NAME,
            finish_reason="stop",
            response_id=f"mock-{self.response_id_counter}",
            input_tokens=int(input_tokens),
            output_tokens=int(output_tokens),
        )


# =============================================================================
# Convenience Function for Stories
# =============================================================================

def instrumented_chat(
    tracer: trace.Tracer,
    user_message: str,
    conversation_id: Optional[str] = None,
    model: str = "gpt-4o",
    system_prompt: Optional[str] = None,
    llm: Optional[MockLLM] = None,
) -> tuple[str, ChatResponse]:
    """
    Make an instrumented chat call with proper span attributes.

    This is a convenience function for stories that handles:
    1. Creating the ChatRequest
    2. Creating the properly instrumented chat span
    3. Calling the LLM (mock or real)
    4. Setting response attributes

    Args:
        tracer: OpenTelemetry tracer
        user_message: The user's message
        conversation_id: Optional conversation ID
        model: Model name (default: gpt-4o)
        system_prompt: Optional system prompt
        llm: Optional LLM instance (uses MockLLM if not provided)

    Returns:
        Tuple of (response_content, ChatResponse)
    """
    if llm is None:
        llm = MockLLM()

    messages = [ChatMessage(role="user", content=user_message)]

    request = ChatRequest(
        messages=messages,
        model=model,
        system_instructions=system_prompt,
    )

    config = ChatConfig.from_environment()
    # Override provider based on LLM type
    if isinstance(llm, MockLLM):
        config.provider_name = "mock"
        config.server_address = None

    with create_chat_span(tracer, request, conversation_id, config) as ctx:
        response = llm.chat(messages, system_prompt)
        ctx.set_response(response)

    return response.content, response
