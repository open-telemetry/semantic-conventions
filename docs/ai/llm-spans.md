<!--- Hugo front matter used to generate the website version of this page:
linkTitle: LLM Calls
--->

# Semantic Conventions for LLM requests

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Configuration](#configuration)
- [LLM Request attributes](#llm-request-attributes)
- [LLM Response attributes](#llm-response-attributes)
- [Events](#events)

<!-- tocstop -->

A request to an LLM is modeled as a span in a trace.

The **span name** SHOULD be set to a low cardinality value representing the request made to an LLM.
It MAY be a name of the API endpoint for the LLM being called.

## Configuration

Instrumentations for LLMs MUST offer the ability to turn off capture of prompts and completions. This is for three primary reasons:

1. Data privacy concerns. End users of LLM applications may input sensitive information or personally identifiable information (PII) that they do not wish to be sent to a telemetry backend.
2. Data size concerns. Although there is no specified limit to sizes, there are practical limitations in programming languages and telemety systems. Some LLMs allow for extremely large context windows that end users may take full advantage of.
3. Performance concerns. Sending large amounts of data to a telemetry backend may cause performance issues for the application.

By default, these configurations SHOULD NOT capture prompts and completions.

## LLM Request attributes

These attributes track input data and metadata for a request to an LLM. Each attribute represents a concept that is common to most LLMs.

<!-- semconv ai(tag=llm-request) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.vendor` | string | The name of the LLM foundation model vendor, if applicable. If not using a vendor-supplied model, this field is left blank. | `openai` | Recommended |
| `llm.request.model` | string | The name of the LLM a request is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model requested. If the LLM is a fine-tuned custom model, the value SHOULD have a more specific name than the base model that's been fine-tuned. | `gpt-4` | Required |
| `llm.request.max_tokens` | int | The maximum number of tokens the LLM generates for a request. | `100` | Recommended |
| `llm.temperature` | float | The temperature setting for the LLM request. | `0.0` | Recommended |
| `llm.top_p` | float | The top_p sampling setting for the LLM request. | `1.0` | Recommended |
| `llm.stream` | bool | Whether the LLM responds with a stream. | `false` | Recommended |
| `llm.stop_sequences` | array | Array of strings the LLM uses as a stop sequence. | `["stop1"]` | Recommended |

`llm.model` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `gpt-4` | GPT-4 |
| `gpt-4-32k` | GPT-4 with 32k context window |
| `gpt-3.5-turbo` | GPT-3.5-turbo |
| `gpt-3.5-turbo-16k` | GPT-3.5-turbo with 16k context window|
| `claude-instant-1` | Claude Instant (latest version) |
| `claude-2` | Claude 2 (latest version) |
| `other-llm` | Any LLM not listed in this table. Use for any fine-tuned version of a model. |
<!-- endsemconv -->

## LLM Response attributes

These attributes track output data and metadata for a response from an LLM. Each attribute represents a concept that is common to most LLMs.

<!-- semconv ai(tag=llm-response) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.response.id` | string | The unique identifier for the completion. | `chatcmpl-123` | Recommended |
| `llm.response.model` | string | The name of the LLM a response is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model actually used. If the LLM is a fine-tuned custom model, the value SHOULD have a more specific name than the base model that's been fine-tuned. | `gpt-4-0613` | Required |
| `llm.response.finish_reason` | string | The reason the model stopped generating tokens | `stop` | Recommended |
| `llm.usage.prompt_tokens` | int | The number of tokens used in the LLM prompt. | `100` | Recommended |
| `llm.usage.completion_tokens` | int | The number of tokens used in the LLM response (completion). | `180` | Recommended |
| `llm.usage.total_tokens` | int | The total number of tokens used in the LLM prompt and response. | `280` | Recommended |

`llm.response.finish_reason` MUST be one of the following:

| Value  | Description |
|---|---|
| `stop` | If the model hit a natural stop point or a provided stop sequence. |
| `max_tokens` | If the maximum number of tokens specified in the request was reached. |
| `tool_call` | If a function / tool call was made by the model (for models that support such functionality). |
<!-- endsemconv -->

## Events

In the lifetime of an LLM span, an event for prompts sent and completions received MAY be created, depending on the configuration of the instrumentation.

<!-- semconv ai(tag=llm-prompt) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
| `llm.prompt` | string | The full prompt string sent to an LLM in a request. If the LLM accepts a more complex input like a JSON object made up of several pieces (such as OpenAI's different message types), this field is blank, and the response is instead captured in an event determined by the specific LLM technology semantic convention. | `\n\nHuman:You are an AI assistant that tells jokes. Can you tell me a joke about OpenTelemetry?\n\nAssistant:` | Recommended |
<!-- endsemconv -->

<!-- semconv ai(tag=llm-completion) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
| `llm.completion` | string | The full response string from an LLM. If the LLM responds with a more complex output like a JSON object made up of several pieces (such as OpenAI's message choices), this field is the content of the response. If the LLM produces multiple responses, then this field is left blank, and each response is instead captured in an event determined by the specific LLM technology semantic convention.| `Why did the developer stop using OpenTelemetry? Because they couldn't trace their steps!` | Recommended |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
