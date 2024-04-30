<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Generative AI metrics
--->

# Semantic Conventions for Generative AI Metrics

**Status**: [Experimental][DocumentStatus]

The conventions described in this section are specific to Generative AI
applications.

**Disclaimer:** These are initial Generative AI client metric instruments
and attributes but more may be added in the future.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Generative AI Operations](#generative-ai-operations)
  - [Metric: `gen_ai.token.usage`](#metric-gen_aitokenusage)
  - [Metric: `gen_ai.operation.duration`](#metric-gen_aioperationduration)

<!-- tocstop -->

## Generative AI Operations

The following metric instruments describe Generative AI operations. An
operation may be a request to an LLM, a function call, or some other
distinct action within a larger Generative AI workflow.

### Metric: `gen_ai.token.usage`

This metric is [required][MetricRequired] when an operation involves the usage
of tokens.

<!-- semconv metric.gen_ai.token.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `gen_ai.token.usage` | Histogram | `{token}` | Measures number of input and output tokens used | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.gen_ai.token.usage(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`gen_ai.operation.name`](../attributes-registry/llm.md) | string | The name of the operation being performed. | `chat`; `completion` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.system`](../attributes-registry/llm.md) | string | The name of the LLM foundation model vendor. | `openai` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.usage.token_type`](../attributes-registry/llm.md) | string | The type of token being counted. | `prompt`; `completion` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [2] | `80`; `8080`; `443` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`error.type`](../attributes-registry/error.md) | string | Describes a class of error the operation ended with. [3] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` if the operation ended in an error | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`gen_ai.request.model`](../attributes-registry/llm.md) | string | The name of the LLM a request is being made to. | `gpt-4` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.response.model`](../attributes-registry/llm.md) | string | The name of the LLM a response was generated from. | `gpt-4-0613` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[3]:** The `error.type` SHOULD be predictable, and SHOULD have low cardinality.

When `error.type` is set to a type (e.g., an exception type), its
canonical class name identifying the type within the artifact SHOULD be used.

Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low.
Telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

If a specific domain defines its own set of error identifiers (such as HTTP or gRPC status codes),
it's RECOMMENDED to:

* Use a domain-specific attribute
* Set `error.type` to capture all errors, regardless of whether they are defined within the domain-specific set or not.

`gen_ai.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `openai` | OpenAI | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`gen_ai.usage.token_type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `input` | Input tokens (Embeddings) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `prompt` | Prompt tokens | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `completion` | Completion tokens | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

### Metric: `gen_ai.operation.duration`

This metric is [required][MetricRequired].

<!-- semconv metric.gen_ai.operation.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `gen_ai.operation.duration` | Histogram | `s` | GenAI operation duration | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.gen_ai.operation.duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`gen_ai.operation.name`](../attributes-registry/llm.md) | string | The name of the operation being performed. | `chat`; `completion` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.system`](../attributes-registry/llm.md) | string | The name of the LLM foundation model vendor. | `openai` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [2] | `80`; `8080`; `443` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`error.type`](../attributes-registry/error.md) | string | Describes a class of error the operation ended with. [3] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` if the operation ended in an error | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`gen_ai.request.model`](../attributes-registry/llm.md) | string | The name of the LLM a request is being made to. | `gpt-4` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.response.model`](../attributes-registry/llm.md) | string | The name of the LLM a response was generated from. | `gpt-4-0613` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[3]:** The `error.type` SHOULD be predictable, and SHOULD have low cardinality.

When `error.type` is set to a type (e.g., an exception type), its
canonical class name identifying the type within the artifact SHOULD be used.

Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low.
Telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

If a specific domain defines its own set of error identifiers (such as HTTP or gRPC status codes),
it's RECOMMENDED to:

* Use a domain-specific attribute
* Set `error.type` to capture all errors, regardless of whether they are defined within the domain-specific set or not.

`gen_ai.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `openai` | OpenAI | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
[MetricRequired]: /docs/general/metric-requirement-level.md#required
