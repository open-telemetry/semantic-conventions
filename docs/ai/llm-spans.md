<!--- Hugo front matter used to generate the website version of this page:
linkTitle: LLM Calls
--->

# Semantic Conventions for LLM requests

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [LLM Request attributes](#llm-request-attributes)
- [Semantic Conventions for specific LLM technologies](#semantic-conventions-for-specific-llm-technologies)

<!-- tocstop -->

**Span kind:** MUST always be `CLIENT`.

The **span name** SHOULD be set to a low cardinality value representing the request made to an LLM.
It MAY be a name of the API endpoint for the LLM being called.

## LLM Request attributes

These attributes track input data and metadata for a request to an LLM. Each attribute represents a concept that is common to most LLMs.

<!-- semconv ai(tag=llm-request) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.model` | string | The name of the LLM a request is being made to. If the LLM is supplied by a vendor, then the value must be the exact name of the model used. If the LLM is a fine-tuned custom model, the value SHOULD have a more specific name than the base model that's been fine-tuned. | `gpt-4` | Required |
| `llm.prompt` | string | The full prompt string sent to an LLM in a request. If the LLM accepts a more complex input like a JSON object made up of several pieces (such as OpenAI's different message types), this field is that entire JSON object encoded as a string. | `\n\nHuman:You are an AI assistant that tells jokes. Can you tell me a joke about OpenTelemetry?\n\nAssistant:` | Required |
| `llm.max_tokens` | int | The maximum number of tokens the LLM generates for a request. | `100` | Recommended |
| `llm.temperature` | float | The temperature setting for the LLM request. | `0.0` | Recommended |
| `llm.top_p` | float | The top-p setting for the LLM request. | `1.0` | Recommended |
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
<!-- endsemconv -->

## LLM Response attributes

These attributes track output data and metadata for a response from an LLM. Each attribute represents a concept that is common to most LLMs.

<!-- semconv ai(tag=llm-response) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.completion` | string | The full response string from an LLM. If the LLM responds with a more complex output like a JSON object made up of several pieces (such as OpenAI's message choices), this field is the content of the response. If the LLM produces multiple responses, then this field is left blank, and each response is instead captured in an attribute determined by the specific LLM technology semantic convention for responses.| `Why did the developer stop using OpenTelemetry? Because they couldn't trace their steps!` | Required |

## Semantic Conventions for specific LLM technologies

More specific Semantic Conventions are defined for the following database technologies:

* [OpenAI](openai.md): Semantic Conventions for *OpenAI*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
