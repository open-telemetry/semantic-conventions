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

The **span name** SHOULD be set to a low cardinality value describing an operation made to an LLM.
For example, the API name such as [Create chat completion](https://platform.openai.com/docs/api-reference/chat/create)

## Configuration

Instrumentations for LLMs MAY capture prompts and completions.
Instrumentations that support it, MUST offer the ability to turn off capture of prompts and completions. This is for three primary reasons:

1. Data privacy concerns. End users of LLM applications may input sensitive information or personally identifiable information (PII) that they do not wish to be sent to a telemetry backend.
2. Data size concerns. Although there is no specified limit to sizes, there are practical limitations in programming languages and telemety systems. Some LLMs allow for extremely large context windows that end users may take full advantage of.
3. Performance concerns. Sending large amounts of data to a telemetry backend may cause performance issues for the application.

By default, these configurations SHOULD NOT capture prompts and completions.

## LLM Request attributes

These attributes track input data and metadata for a request to an LLM. Each attribute represents a concept that is common to most LLMs.

<!-- semconv gen_ai.request -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`gen_ai.request.max_tokens`](../attributes-registry/gen-ai.md) | int | The maximum number of tokens the LLM generates for a request. | `100` | Recommended |
| [`gen_ai.request.model`](../attributes-registry/gen-ai.md) | string | The name of the LLM a request is being made to. [1] | `gpt-4` | Required |
| [`gen_ai.request.temperature`](../attributes-registry/gen-ai.md) | double | The temperature setting for the LLM request. | `0.0` | Recommended |
| [`gen_ai.request.top_p`](../attributes-registry/gen-ai.md) | double | The top_p sampling setting for the LLM request. | `1.0` | Recommended |
| [`gen_ai.response.finish_reasons`](../attributes-registry/gen-ai.md) | string[] | Array of reasons the model stopped generating tokens, corresponding to each generation received. | `[stop]` | Recommended |
| [`gen_ai.response.id`](../attributes-registry/gen-ai.md) | string | The unique identifier for the completion. | `chatcmpl-123` | Recommended |
| [`gen_ai.response.model`](../attributes-registry/gen-ai.md) | string | The name of the LLM a response is being made to. [2] | `gpt-4-0613` | Conditionally Required: if response was received |
| [`gen_ai.system`](../attributes-registry/gen-ai.md) | string | The name of the LLM foundation model vendor. [3] | `openai` | Required |
| [`gen_ai.usage.completion_tokens`](../attributes-registry/gen-ai.md) | int | The number of tokens used in the LLM response (completion). | `180` | Recommended |
| [`gen_ai.usage.prompt_tokens`](../attributes-registry/gen-ai.md) | int | The number of tokens used in the LLM prompt. | `100` | Recommended |

**[1]:** The name of the LLM a request is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model requested. If the LLM is a fine-tuned custom model, the value should have a more specific name than the base model that's been fine-tuned.

**[2]:** The name of the LLM serving a response. If the LLM is supplied by a vendor, then the value must be the exact name of the model actually used. If the LLM is a fine-tuned custom model, the value should have a more specific name than the base model that's been fine-tuned.

**[3]:** If not using a vendor-supplied model, provide a custom friendly name, such as a name of the company or project. If the instrumetnation reports any attributes specific to a custom model, the value provided in the `gen_ai.system` SHOULD match the custom attribute namespace segment. For example, if `gen_ai.system` is set to `the_best_llm`, custom attributes should be added in the `gen_ai.the_best_llm.*` namespace. If none of above options apply, the instrumentation should set `_OTHER`.
<!-- endsemconv -->

## Events

In the lifetime of an LLM span, an event for prompts sent and completions received MAY be created, depending on the configuration of the instrumentation.

<!-- semconv gen_ai.content.prompt -->
The event name MUST be `gen_ai.content.prompt`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`gen_ai.prompt`](../attributes-registry/gen-ai.md) | string | The full prompt sent to an LLM. [1] | `[{'role': 'user', 'content': 'What is the capital of France?'}]` | Recommended |

**[1]:** It's RECOMMENDED to format prompts as JSON string matching [OpenAI messages format](https://platform.openai.com/docs/guides/text-generation)
<!-- endsemconv -->

<!-- semconv gen_ai.content.completion -->
The event name MUST be `gen_ai.content.completion`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`gen_ai.completion`](../attributes-registry/gen-ai.md) | string | The full response received from the LLM. [1] | `[{'role': 'assistant', 'content': 'The capital of France is Paris.'}]` | Recommended |

**[1]:** It's RECOMMENDED to format completions as JSON string matching [OpenAI messages format](https://platform.openai.com/docs/guides/text-generation)
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
