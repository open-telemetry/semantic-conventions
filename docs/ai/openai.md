<!--- Hugo front matter used to generate the website version of this page:
linkTitle: OpenAI
--->

# Semantic Conventions for OpenAI

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [OpenAI](https://www.microsoft.com/sql-server) extend the [LLM Semantic Conventions](llm-spans.md)
that describe common LLM request attributes in addition to the Semantic Conventions
described on this page.

## OpenAI LLM request attributes

These are additional attributes when instrumenting OpenAI LLM requests.

<!-- semconv llm.openai(tag=llm-request-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.openai.messages.<index>.role` | string | The assigned role for a given OpenAI request, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `system` | Required |
| `llm.openai.messages.<index>.message` | string | The message for a given OpenAI request, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `You are an AI system that tells jokes about OpenTelemetry.` | Required |
| `llm.openai.messages.<index>.name` | string | If present, the message for a given OpenAI request, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `You are an AI system that tells jokes about OpenTelemetry.` | Required |
| `llm.openai.messages.<index>.function_call.name` | string | If present, name of an OpenAI function for a given OpenAI request, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `get_weather_forecast` | Required |
| `llm.openai.messages.<index>.function_call.arguments` | string | If present, the arguments to call a function call with for an OpenAI function for a given OpenAI request, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `{"type": "object", "properties": {}}` | Required |
| `llm.openai.functions.<index>.name` | string | If present, name of an OpenAI function for a given OpenAI request, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `get_weather_forecast` | Required |
| `llm.openai.functions.<index>.parameters` | string | If present, JSON-encoded string of the parameter object of an OpenAI function for a given OpenAI request, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `{"type": "object", "properties": {}}` | Required |
| `llm.openai.functions.<index>.description` | string | If present, description of an OpenAI function for a given OpenAI request, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `Gets the weather forecast.` | Required |
| `llm.openai.n` | int | If present, the number of messages an OpenAI request responds with. | `2` | Recommended |
| `llm.openai.presence_penalty` | float | If present, the `presence_penalty` used in an OpenAI request. Value is between -2.0 and 2.0. | `-0.5` | Recommended |
| `llm.openai.frequency_penalty` | float | If present, the `frequency_penalty` used in an OpenAI request. Value is between -2.0 and 2.0. | `-0.5` | Recommended |
| `llm.openai.logit_bias` | string | If present, the JSON-encoded string of a `logit_bias` used in an OpenAI request. | `{2435:-100, 640:-100}` | Recommended |
| `llm.openai.user` | string | If present, the `user` used in an OpenAI request. | `bob` | Recommended |

## OpenAI LLM response attributes

These are additional attributes when instrumenting OpenAI LLM responses.

<!-- semconv llm.openai(tag=llm-response-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.openai.choices.<index>.role` | string | The assigned role for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `system` | Required |
| `llm.openai.choices.<index>.content` | string | The content for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `Why did the developer stop using OpenTelemetry? Because they couldn't trace their steps!` | Required |
| `llm.openai.choices.<index>.function_call.name` | string | If exists, the name of a function call for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `get_weather_report` | Required |
| `llm.openai.choices.<index>.function_call.arguments` | string | If exists, the arguments to call a function call with for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `{"type": "object", "properties": {"some":"data"}}` | Required |
| `llm.openai.finish_reason` | string | The reason the OpenAI model stopped generating tokens | `stop` | Recommended |
| `llm.openai.id` | string | The unique identifier for the chat completion. | `chatcmpl-123` | Recommended |
| `llm.openai.created` | int | The UNIX timestamp (in seconds) if when the completion was created. | `1677652288` | Recommended |
| `llm.openai.model` | string | The name of the model used for the completion. | `gpt-3.5-turbo` | Recommended |
| `llm.openai.usage.prompt_tokens` | int | The number of tokens in the prompt passed as input. | `500` | Recommended |
| `llm.openai.usage.completion_tokens` | int | The number of tokens generated in the completion. | `100` | Recommended |
| `llm.openai.usage.total_tokens` | int | The total number of tokens used in both the prompt and the generated completion. | `600` | Recommended |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
