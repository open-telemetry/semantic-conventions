<!--- Hugo front matter used to generate the website version of this page:
linkTitle: LLM Calls
--->

# Semantic Conventions for LLM requests

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Configuration](#configuration)
- [LLM Request attributes](#llm-request-attributes)
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

<!-- semconv gen_ai.llm.request -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`gen_ai.llm.request.max_tokens`](../attributes-registry/llm.md) | int | The maximum number of tokens the LLM generates for a request. | `100` | Recommended |
| [`gen_ai.llm.request.model`](../attributes-registry/llm.md) | string | The name of the LLM a request is being made to. [1] | `gpt-4` | Required |
| [`gen_ai.llm.request.temperature`](../attributes-registry/llm.md) | double | The temperature setting for the LLM request. | `0.0` | Recommended |
| [`gen_ai.llm.request.top_p`](../attributes-registry/llm.md) | double | The top_p sampling setting for the LLM request. | `1.0` | Recommended |
| [`gen_ai.llm.response.finish_reason`](../attributes-registry/llm.md) | string[] | Array of reasons the model stopped generating tokens, corresponding to each generation received. | `[['stop']]` | Recommended |
| [`gen_ai.llm.response.id`](../attributes-registry/llm.md) | string | The unique identifier for the completion. | `chatcmpl-123` | Recommended |
| [`gen_ai.llm.response.model`](../attributes-registry/llm.md) | string | The name of the LLM a response is being made to. [2] | `gpt-4-0613` | Required |
| [`gen_ai.llm.system`](../attributes-registry/llm.md) | string | The name of the LLM foundation model vendor, if applicable. [3] | `openai` | Recommended |
| [`gen_ai.llm.usage.completion_tokens`](../attributes-registry/llm.md) | int | The number of tokens used in the LLM response (completion). | `180` | Recommended |
| [`gen_ai.llm.usage.prompt_tokens`](../attributes-registry/llm.md) | int | The number of tokens used in the LLM prompt. | `100` | Recommended |

**[1]:** The name of the LLM a request is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model requested. If the LLM is a fine-tuned custom model, the value should have a more specific name than the base model that's been fine-tuned.

**[2]:** The name of the LLM a response is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model actually used. If the LLM is a fine-tuned custom model, the value should have a more specific name than the base model that's been fine-tuned.

**[3]:** The name of the LLM foundation model vendor, if applicable. If not using a vendor-supplied model, this field is left blank.
<!-- endsemconv -->

## Events

In the lifetime of an LLM span, an event for prompts sent and completions received MAY be created, depending on the configuration of the instrumentation.

<!-- semconv gen_ai.llm.content.prompt -->
The event name MUST be `gen_ai.llm.content.prompt`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`gen_ai.llm.prompt`](../attributes-registry/llm.md) | string | The full prompt string sent to an LLM in a request. [1] | `\\n\\nHuman:You are an AI assistant that tells jokes. Can you tell me a joke about OpenTelemetry?\\n\\nAssistant:` | Recommended |

**[1]:** The full prompt sent to an LLM in a request, structured as a JSON in OpenAI's format.
<!-- endsemconv -->

<!-- semconv gen_ai.llm.content.completion -->
The event name MUST be `gen_ai.llm.content.completion`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`gen_ai.llm.completion`](../attributes-registry/llm.md) | string | The full response string from an LLM in a response. [1] | `Why did the developer stop using OpenTelemetry? Because they couldnt trace their steps!` | Recommended |

**[1]:** The full response from an LLM, structured as a JSON in OpenAI's format.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
