<!--- Hugo front matter used to generate the website version of this page:
--->

# Large Language Model (LLM)

<!-- toc -->

- [Generic LLM Attributes](#generic-llm-attributes)
  * [Request Attributes](#request-attributes)
  * [Response Attributes](#response-attributes)
  * [Event Attributes](#event-attributes)
- [OpenAI Attributes](#openai-attributes)
  * [Request Attributes](#request-attributes-1)
  * [Response Attributes](#response-attributes-1)
  * [Event Attributes](#event-attributes-1)

<!-- tocstop -->

## Generic LLM Attributes

### Request Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-request) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `llm.request.max_tokens` | int | The maximum number of tokens the LLM generates for a request. | `100` |
| `llm.request.model` | string | The name of the LLM a request is being made to. | `gpt-4` |
| `llm.stop_sequences` | string | Array of strings the LLM uses as a stop sequence. | `stop1` |
| `llm.stream` | boolean | Whether the LLM responds with a stream. | `False` |
| `llm.temperature` | double | The temperature setting for the LLM request. | `0.0` |
| `llm.top_p` | double | The top_p sampling setting for the LLM request. | `1.0` |
| `llm.vendor` | string | The name of the LLM foundation model vendor, if applicable. | `openai` |
<!-- endsemconv -->

### Response Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-response) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `llm.response.finish_reason` | string | The reason the model stopped generating tokens. | `stop` |
| `llm.response.id` | string | The unique identifier for the completion. | `chatcmpl-123` |
| `llm.response.model` | string | The name of the LLM a response is being made to. | `gpt-4-0613` |
| `llm.usage.completion_tokens` | int | The number of tokens used in the LLM response (completion). | `180` |
| `llm.usage.prompt_tokens` | int | The number of tokens used in the LLM prompt. | `100` |
| `llm.usage.total_tokens` | int | The total number of tokens used in the LLM prompt and response. | `280` |
<!-- endsemconv -->

### Event Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-events) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `llm.completion` | string | The full response string from an LLM in a response. | `Why did the developer stop using OpenTelemetry? Because they couldnt trace their steps!` |
| `llm.prompt` | string | The full prompt string sent to an LLM in a request. | `\\n\\nHuman:You are an AI assistant that tells jokes. Can you tell me a joke about OpenTelemetry?\\n\\nAssistant:` |
<!-- endsemconv -->

## OpenAI Attributes

### Request Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=tech-specific-openai-request) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `llm.openai.frequency_penalty` | double | If present, the `frequency_penalty` used in an OpenAI request. Value is between -2.0 and 2.0. | `-0.5` |
| `llm.openai.logit_bias` | string | If present, the JSON-encoded string of a `logit_bias` used in an OpenAI request | `{2435:-100, 640:-100}` |
| `llm.openai.presence_penalty` | double | If present, the `presence_penalty` used in an OpenAI request. Value is between -2.0 and 2.0. | `-0.5` |
| `llm.openai.response_format` | string | An object specifying the format that the model must output. Either `text` or `json_object` | `text` |
| `llm.openai.seed` | int | Seed used in request to improve determinism. | `1234` |
| `llm.openai.user` | string | If present, the `user` used in an OpenAI request. | `bob` |

`llm.openai.response_format` MUST be one of the following:

| Value  | Description |
|---|---|
| `text` | text |
| `json_object` | json_object |
<!-- endsemconv -->

### Response Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=tech-specific-openai-response) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `llm.openai.created` | int | The UNIX timestamp (in seconds) if when the completion was created. | `1677652288` |
| `llm.openai.system_fingerprint` | string | This fingerprint represents the backend configuration that the model runs with. | `asdf987123` |
<!-- endsemconv -->

### Event Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=tech-specific-openai-events) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `llm.openai.choice.type` | string | The type of the choice, either `delta` or `message`. | `message` |
| `llm.openai.content` | string | The content for a given OpenAI response. | `Why did the developer stop using OpenTelemetry? Because they couldn't trace their steps!` |
| `llm.openai.finish_reason` | string | The reason the OpenAI model stopped generating tokens for this chunk. | `stop` |
| `llm.openai.function.arguments` | string | If exists, the arguments to call a function call with for a given OpenAI response, denoted by `<index>`. The value for `<index>` starts with 0, where 0 is the first message. | `{"type": "object", "properties": {"some":"data"}}` |
| `llm.openai.function.description` | string | A description of what the function does, used by the model to choose when and how to call the function. | `Gets the current weather for a location` |
| `llm.openai.function.name` | string | The name of the function to be called. | `get_weather` |
| `llm.openai.function.parameters` | string | JSON-encoded string of the parameter object for the function. | `{"type": "object", "properties": {}}` |
| `llm.openai.role` | string | The role of the prompt author, can be one of `system`, `user`, `assistant`, or `tool` | `user` |
| `llm.openai.tool_call.id` | string | If role is `tool` or `function`, then this tool call that this message is responding to. | `get_current_weather` |
| `llm.openai.tool_call.type` | string | The type of the tool. Currently, only `function` is supported. | `function` |

`llm.openai.choice.type` MUST be one of the following:

| Value  | Description |
|---|---|
| `delta` | delta |
| `message` | message |

`llm.openai.role` MUST be one of the following:

| Value  | Description |
|---|---|
| `system` | system |
| `user` | user |
| `assistant` | assistant |
| `tool` | tool |

`llm.openai.tool_call.type` MUST be one of the following:

| Value  | Description |
|---|---|
| `function` | function |
<!-- endsemconv -->