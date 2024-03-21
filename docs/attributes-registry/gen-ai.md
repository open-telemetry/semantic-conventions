<!--- Hugo front matter used to generate the website version of this page:
--->

# Large Language Model (LLM)

<!-- toc -->

- [Generic LLM Attributes](#generic-llm-attributes)
  - [Request Attributes](#request-attributes)
  - [Response Attributes](#response-attributes)
  - [Event Attributes](#event-attributes)

<!-- tocstop -->

## Generic LLM Attributes

### Request Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-request) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `gen_ai.request.max_tokens` | int | The maximum number of tokens the LLM generates for a request. | `100` |
| `gen_ai.request.model` | string | The name of the LLM a request is being made to. | `gpt-4` |
| `gen_ai.request.temperature` | double | The temperature setting for the LLM request. | `0.0` |
| `gen_ai.request.top_p` | double | The top_p sampling setting for the LLM request. | `1.0` |
| `gen_ai.system` | string | The name of the LLM foundation model vendor, if applicable. | `openai` |

`gen_ai.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `OpenAI` | OpenAI models like GPT, DALL-E, Sora, etc. |
<!-- endsemconv -->

### Response Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-response) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `gen_ai.response.finish_reasons` | string[] | Array of reasons the model stopped generating tokens, corresponding to each generation received. | `[['stop']]` |
| `gen_ai.response.id` | string | The unique identifier for the completion. | `chatcmpl-123` |
| `gen_ai.response.model` | string | The name of the LLM a response is being made to. | `gpt-4-0613` |
| `gen_ai.usage.completion_tokens` | int | The number of tokens used in the LLM response (completion). | `180` |
| `gen_ai.usage.prompt_tokens` | int | The number of tokens used in the LLM prompt. | `100` |
<!-- endsemconv -->

### Event Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-events) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `gen_ai.completion` | string | The full response received from the LLM, as a stringified JSON in OpenAI's format. | `[{'role': 'assistant', 'content': 'The capital of France is Paris.'}]` |
| `gen_ai.prompt` | string | The full prompt sent to an LLM, as a stringified JSON in OpenAI's format. | `[{'role': 'user', 'content': 'What is the capital of France?'}]` |
<!-- endsemconv -->