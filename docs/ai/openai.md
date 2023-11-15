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

The span name for OpenAI chat completions SHOULD be `openai_chat_completion` 
to maintain consistency and clarity in telemetry data.

## Request Attributes

These are the attributes when instrumenting OpenAI LLM requests with the 
`/chat/completions` endpoint.

<!-- semconv llm.openai(tag=llm-request-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.model` | string | The name of OpenAI Model a request is being made to. | `gpt-4` | Required |
| `llm.max_tokens` | int | The maximum number of tokens the LLM generates for a request. | `100` | Recommended |
| `llm.temperature` | float | The temperature setting for the LLM request. | `0.0` | Recommended |
| `llm.top_p` | float | The top_p sampling setting for the LLM request. | `1.0` | Recommended |
| `llm.stream` | bool | Whether the LLM responds with a stream. | `false` | Recommended |
| `llm.stop_sequences` | array | Array of strings the LLM uses as a stop sequence. | `["stop1"]` | Recommended |
| `llm.openai.presence_penalty` | float | If present, the `presence_penalty` used in an OpenAI request. Value is between -2.0 and 2.0. | `-0.5` | Recommended |
| `llm.openai.frequency_penalty` | float | If present, the `frequency_penalty` used in an OpenAI request. Value is between -2.0 and 2.0. | `-0.5` | Recommended |
| `llm.openai.logit_bias` | string | If present, the JSON-encoded string of a `logit_bias` used in an OpenAI request. | `{2435:-100, 640:-100}` | Recommended |
| `llm.openai.user` | string | If present, the `user` used in an OpenAI request. | `bob` | Opt-in |
| `llm.openai.response_format` | string | An object specifying the format that the model must output. Either `text` or `json_object` | `text` | Recommended |
| `llm.openai.seed` | integer | Seed used in request to improve determinism. | `1234` | Recommended |

### Request Events

Recording details about Messages and Tools for each request MAY be included as 
Span Events. 

Instrumentations SHOULD require an explicit configuration for which events to 
record. 

#### Message Events

Message event name SHOULD be `llm.openai.message`. 

| `role` | string | The role of the messages author, can be one of `system`, `user`, `assistant`, or `tool` | `system` | Required |
| `content` | string | The content for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `Why did the developer stop using OpenTelemetry? Because they couldn't trace their steps!` | Required |
| `tool_call_id` | string | If role is `tool`, then this tool call that this message is responding to. | `call_BP08xxEhU60txNjnz3z9R4h9` | Conditionally Required: If `role` is `tool`. |

### Tools Events

Tools event name SHOULD be `llm.openai.tool`.

| `type` | string | They type of the tool. Currently, only `function` is supported. | `function` | Required |
| `function.name` | string | The name of the function to be called. | `get_weather` | Required !
| `function.description` | string | A description of what the function does, used by the model to choose when and how to call the function. | `` | Required |
| `function.parameters` | string | JSON-encoded string of the parameter object for the function. | `{"type": "object", "properties": {}}` | Required | 

### OpenAI Chat completion response attributes

Attributes for chat completion responses SHOULD follow these conventions:

<!-- semconv llm.openai(tag=llm-response-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.openai.finish_reason` | string | The reason the OpenAI model stopped generating tokens | `stop` | Recommended |
| `llm.openai.id` | string | The unique identifier for the chat completion. | `chatcmpl-123` | Recommended |
| `llm.openai.created` | int | The UNIX timestamp (in seconds) if when the completion was created. | `1677652288` | Recommended |
| `llm.openai.usage.prompt_tokens` | int | The number of tokens in the prompt passed as input. | `500` | Recommended |
| `llm.openai.usage.completion_tokens` | int | The number of tokens generated in the completion. | `100` | Recommended |
| `llm.openai.usage.total_tokens` | int | The total number of tokens used in both the prompt and the generated completion. | `600` | Recommended |
| `llm.openai.system_fingerprint` | string | This fingerprint represents the backend configuration that the model runs with. | asdf987123 | Recommended |

### Choice Events

Recording details about Choices in each response MAY be included as 
Span Events. 

Choice event name SHOULD be `llm.openai.choice`. 

If there is more than one `tool_call`, separate events SHOULD be used.

| `type` | string | Either `delta` or `message`. | `message` | Required |
| `finish_reason` | string | The reason the OpenAI model stopped generating tokens for this chunk. | `stop` | Recommended |
| `role` | string | The assigned role for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `system` | Required |
| `content` | string | The content for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `Why did the developer stop using OpenTelemetry? Because they couldn't trace their steps!` | Required |
| `tool_call.id` | string | If exists, the ID of the tool call. | `call_BP08xxEhU60txNjnz3z9R4h9` | Required |
| `tool_call.type` | string | Currently only `function` is supported. | `function` | Required |
| `tool_call.function.name` | string | If exists, the name of a function call for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `get_weather_report` | Required |
| `tool_call.function.arguments` | string | If exists, the arguments to call a function call with for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `{"type": "object", "properties": {"some":"data"}}` | Required |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
