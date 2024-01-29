<!--- Hugo front matter used to generate the website version of this page:
linkTitle: OpenAI
--->

# Semantic Conventions for OpenAI Spans

**Status**: [Experimental][DocumentStatus]

This document outlines the Semantic Conventions specific to
[OpenAI](https://platform.openai.com/) spans, extending the general semantics
found in the [LLM Semantic Conventions](llm-spans.md). These conventions are
designed to standardize telemetry data for OpenAI interactions, particularly
focusing on the `/chat/completions` endpoint. By following to these guidelines,
developers can ensure consistent, meaningful, and easily interpretable telemetry
data across different applications and platforms.

## Chat Completions

The span name for OpenAI chat completions SHOULD be `openai.chat`
to maintain consistency and clarity in telemetry data.

## Request Attributes

These are the attributes when instrumenting OpenAI LLM requests with the
`/chat/completions` endpoint.

<!-- semconv llm.openai -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`llm.request.is_stream`](../attributes-registry/llm.md) | boolean | Whether the LLM responds with a stream. | `False` | Recommended |
| [`llm.request.max_tokens`](../attributes-registry/llm.md) | int | The maximum number of tokens the LLM generates for a request. | `100` | Recommended |
| [`llm.request.model`](../attributes-registry/llm.md) | string | The name of the LLM a request is being made to. [1] | `gpt-4` | Required |
| [`llm.request.openai.logit_bias`](../attributes-registry/llm.md) | string | If present, the JSON-encoded string of a `logit_bias` used in an OpenAI request | `{2435:-100, 640:-100}` | Recommended |
| [`llm.request.openai.presence_penalty`](../attributes-registry/llm.md) | double | If present, the `presence_penalty` used in an OpenAI request. Value is between -2.0 and 2.0. | `-0.5` | Recommended |
| [`llm.request.openai.response_format`](../attributes-registry/llm.md) | string | An object specifying the format that the model must output. Either `text` or `json_object` | `text` | Recommended |
| [`llm.request.openai.seed`](../attributes-registry/llm.md) | int | Seed used in request to improve determinism. | `1234` | Recommended |
| [`llm.request.openai.user`](../attributes-registry/llm.md) | string | If present, the `user` used in an OpenAI request. | `bob` | Recommended |
| [`llm.request.stop_sequences`](../attributes-registry/llm.md) | string | Array of strings the LLM uses as a stop sequence. | `stop1` | Recommended |
| [`llm.request.temperature`](../attributes-registry/llm.md) | double | The temperature setting for the LLM request. | `0.0` | Recommended |
| [`llm.request.top_p`](../attributes-registry/llm.md) | double | The top_p sampling setting for the LLM request. | `1.0` | Recommended |
| [`llm.response.finish_reason`](../attributes-registry/llm.md) | string | The reason the model stopped generating tokens. | `stop` | Recommended |
| [`llm.response.id`](../attributes-registry/llm.md) | string[] | The unique identifier for the completion. | `[chatcmpl-123]` | Recommended |
| [`llm.response.openai.created`](../attributes-registry/llm.md) | int | The UNIX timestamp (in seconds) if when the completion was created. | `1677652288` | Recommended |
| [`llm.response.openai.system_fingerprint`](../attributes-registry/llm.md) | string | This fingerprint represents the backend configuration that the model runs with. | `asdf987123` | Recommended |
| [`llm.system`](../attributes-registry/llm.md) | string | The name of the LLM foundation model vendor, if applicable. | `openai`; `microsoft` | Recommended |
| [`llm.usage.completion_tokens`](../attributes-registry/llm.md) | int | The number of tokens used in the LLM response (completion). | `180` | Recommended |
| [`llm.usage.prompt_tokens`](../attributes-registry/llm.md) | int | The number of tokens used in the LLM prompt. | `100` | Recommended |
| [`llm.usage.total_tokens`](../attributes-registry/llm.md) | int | The total number of tokens used in the LLM prompt and response. | `280` | Recommended |

**[1]:** The name of the LLM a request is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model requested. If the LLM is a fine-tuned custom model, the value should have a more specific name than the base model that's been fine-tuned.
<!-- endsemconv -->

## Request Events

In the lifetime of an LLM span, an event for prompts sent and completions received MAY be created, depending on the configuration of the instrumentation.
Because OpenAI uses a more complex prompt structure, these events will be used instead of the generic ones detailed in the [LLM Semantic Conventions](llm-spans.md).

### Prompt Events

Prompt event name SHOULD be `llm.content.openai.prompt`.

<!-- semconv llm.content.openai.prompt -->
The event name MUST be `llm.content.openai.prompt`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`llm.openai.content`](../attributes-registry/llm.md) | string | The content for a given OpenAI response. | `Why did the developer stop using OpenTelemetry? Because they couldn't trace their steps!` | Required |
| [`llm.openai.role`](../attributes-registry/llm.md) | string | The role of the prompt author, can be one of `system`, `user`, `assistant`, or `tool` | `user` | Required |
| [`llm.openai.tool_call.id`](../attributes-registry/llm.md) | string | If role is `tool` or `function`, then this tool call that this message is responding to. | `get_current_weather` | Conditionally Required: Required if the prompt role is `tool`. |
<!-- endsemconv -->

### Tools Events

Tools event name SHOULD be `llm.content.openai.tool`, specifying potential tools or functions the LLM can use.

<!-- semconv llm.content.openai.tool -->
The event name MUST be `llm.content.openai.tool`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`llm.openai.function.description`](../attributes-registry/llm.md) | string | A description of what the function does, used by the model to choose when and how to call the function. | `Gets the current weather for a location` | Required |
| [`llm.openai.function.name`](../attributes-registry/llm.md) | string | The name of the function to be called. | `get_weather` | Required |
| [`llm.openai.function.parameters`](../attributes-registry/llm.md) | string | JSON-encoded string of the parameter object for the function. | `{"type": "object", "properties": {}}` | Required |
| [`llm.openai.tool.type`](../attributes-registry/llm.md) | string | The type of the tool. Currently, only `function` is supported. | `function` | Required |
<!-- endsemconv -->

### Choice Events

Recording details about Choices in each response MAY be included as
Span Events.

Choice event name SHOULD be `llm.content.openai.choice`.

If there is more than one `choice`, separate events SHOULD be used.

<!-- semconv llm.content.openai.completion.choice -->
The event name MUST be `llm.content.openai.completion.choice`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`llm.openai.choice.type`](../attributes-registry/llm.md) | string | The type of the choice, either `delta` or `message`. | `message` | Required |
| [`llm.openai.content`](../attributes-registry/llm.md) | string | The content for a given OpenAI response. | `Why did the developer stop using OpenTelemetry? Because they couldn't trace their steps!` | Required |
| [`llm.openai.function.arguments`](../attributes-registry/llm.md) | string | If exists, the arguments to call a function call with for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `{"type": "object", "properties": {"some":"data"}}` | Conditionally Required: [1] |
| [`llm.openai.function.name`](../attributes-registry/llm.md) | string | The name of the function to be called. | `get_weather` | Conditionally Required: [2] |
| [`llm.openai.role`](../attributes-registry/llm.md) | string | The role of the prompt author, can be one of `system`, `user`, `assistant`, or `tool` | `user` | Required |
| [`llm.openai.tool.type`](../attributes-registry/llm.md) | string | The type of the tool. Currently, only `function` is supported. | `function` | Conditionally Required: [3] |
| [`llm.openai.tool_call.id`](../attributes-registry/llm.md) | string | If role is `tool` or `function`, then this tool call that this message is responding to. | `get_current_weather` | Conditionally Required: [4] |
| [`llm.response.finish_reason`](../attributes-registry/llm.md) | string | The reason the model stopped generating tokens. | `stop` | Recommended |

**[1]:** Required if the choice is the result of a tool call of type `function`.

**[2]:** Required if the choice is the result of a tool call of type `function`.

**[3]:** Required if the choice is the result of a tool call.

**[4]:** Required if the choice is the result of a tool call.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
