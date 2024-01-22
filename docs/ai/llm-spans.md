<!--- Hugo front matter used to generate the website version of this page:
linkTitle: LLM Calls
--->

# Semantic Conventions for LLM Spans

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Configuration](#configuration)
- [LLM Request attributes](#llm-request-attributes)
- [LLM Response attributes](#llm-response-attributes)
- [LLM Span Events](#llm-span-events)

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

<!-- semconv llm.request -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`llm.request.max_tokens`](../attributes-registry/llm.md) | int | The maximum number of tokens the LLM generates for a request. | `100` | Recommended |
| [`llm.request.model`](../attributes-registry/llm.md) | string | The name of the LLM a request is being made to. [1] | `gpt-4` | Required |
| [`llm.stop_sequences`](../attributes-registry/llm.md) | string | Array of strings the LLM uses as a stop sequence. | `stop1` | Recommended |
| [`llm.stream`](../attributes-registry/llm.md) | boolean | Whether the LLM responds with a stream. | `False` | Recommended |
| [`llm.temperature`](../attributes-registry/llm.md) | double | The temperature setting for the LLM request. | `0.0` | Recommended |
| [`llm.top_p`](../attributes-registry/llm.md) | double | The top_p sampling setting for the LLM request. | `1.0` | Recommended |
| [`llm.vendor`](../attributes-registry/llm.md) | string | The name of the LLM foundation model vendor, if applicable. [2] | `openai` | Recommended |

**[1]:** The name of the LLM a request is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model requested. If the LLM is a fine-tuned custom model, the value should have a more specific name than the base model that's been fine-tuned.

**[2]:** The name of the LLM foundation model vendor, if applicable. If not using a vendor-supplied model, this field is left blank.
<!-- endsemconv -->

## LLM Response attributes

These attributes track output data and metadata for a response from an LLM. Each attribute represents a concept that is common to most LLMs.

<!-- semconv llm.response -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`llm.response.finish_reason`](../attributes-registry/llm.md) | string | The reason the model stopped generating tokens. | `stop` | Recommended |
| [`llm.response.id`](../attributes-registry/llm.md) | string | The unique identifier for the completion. | `chatcmpl-123` | Recommended |
| [`llm.response.model`](../attributes-registry/llm.md) | string | The name of the LLM a response is being made to. [1] | `gpt-4-0613` | Required |
| [`llm.usage.completion_tokens`](../attributes-registry/llm.md) | int | The number of tokens used in the LLM response (completion). | `180` | Recommended |
| [`llm.usage.prompt_tokens`](../attributes-registry/llm.md) | int | The number of tokens used in the LLM prompt. | `100` | Recommended |
| [`llm.usage.total_tokens`](../attributes-registry/llm.md) | int | The total number of tokens used in the LLM prompt and response. | `280` | Recommended |

**[1]:** The name of the LLM a response is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model actually used. If the LLM is a fine-tuned custom model, the value should have a more specific name than the base model that's been fine-tuned.
<!-- endsemconv -->

## LLM Span Events

In the lifetime of an LLM span, an event for prompts sent and completions received MAY be created, depending on the configuration of the instrumentation.

<!-- semconv llm.events -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`llm.completion`](../attributes-registry/llm.md) | string | The full response string from an LLM in a response. [1] | `Why did the developer stop using OpenTelemetry? Because they couldnt trace their steps!` | Recommended |
| [`llm.prompt`](../attributes-registry/llm.md) | string | The full prompt string sent to an LLM in a request. [2] | `\\n\\nHuman:You are an AI assistant that tells jokes. Can you tell me a joke about OpenTelemetry?\\n\\nAssistant:` | Recommended |

**[1]:** The full response string from an LLM. If the LLM responds with a more complex output like a JSON object made up of several pieces (such as OpenAI's message choices), this field is the content of the response. If the LLM produces multiple responses, then this field is left blank, and each response is instead captured in an event determined by the specific LLM technology semantic convention.

**[2]:** The full prompt string sent to an LLM in a request. If the LLM accepts a more complex input like a JSON object, this field is blank, and the response is instead captured in an event determined by the specific LLM technology semantic convention.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md