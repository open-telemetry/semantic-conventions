<!--- Hugo front matter used to generate the website version of this page:
--->

# Large Language Model (LLM)

<!-- toc -->

- [Generic LLM Attributes](#generic-llm-attributes)
  * [Request Attributes](#request-attributes)
  * [Response Attributes](#response-attributes)
  * [Event Attributes](#event-attributes)

<!-- tocstop -->

## Generic LLM Attributes

### Request Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-request) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `gen_ai.llm.request.max_tokens` | int | The maximum number of tokens the LLM generates for a request. | `100` |
| `gen_ai.llm.request.model` | string | The name of the LLM a request is being made to. | `gpt-4` |
| `gen_ai.llm.request.temperature` | double | The temperature setting for the LLM request. | `0.0` |
| `gen_ai.llm.request.top_p` | double | The top_p sampling setting for the LLM request. | `1.0` |
| `gen_ai.llm.system` | string | The name of the LLM foundation model vendor, if applicable. | `openai` |
<!-- endsemconv -->

### Response Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-response) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `gen_ai.llm.response.finish_reason` | string[] | Array of reasons the model stopped generating tokens, corresponding to each generation received. | `[['stop']]` |
| `gen_ai.llm.response.id` | string | The unique identifier for the completion. | `chatcmpl-123` |
| `gen_ai.llm.response.model` | string | The name of the LLM a response is being made to. | `gpt-4-0613` |
| `gen_ai.llm.usage.completion_tokens` | int | The number of tokens used in the LLM response (completion). | `180` |
| `gen_ai.llm.usage.prompt_tokens` | int | The number of tokens used in the LLM prompt. | `100` |
<!-- endsemconv -->

### Event Attributes

<!-- semconv registry.llm(omit_requirement_level,tag=llm-generic-events) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `gen_ai.llm.completion` | string | The full response received from the LLM, as a stringified JSON in OpenAI's format. | `[{'role': 'assistant', 'content': 'The capital of France is Paris.'}]` |
| `gen_ai.llm.prompt` | string | The full prompt sent to an LLM, as a stringified JSON in OpenAI's format. | `[{'role': 'user', 'content': 'What is the capital of France?'}]` |
<!-- endsemconv -->