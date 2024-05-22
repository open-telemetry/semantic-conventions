<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Generative AI metrics
--->

# Semantic Conventions for Generative AI Client Metrics

**Status**: [Experimental][DocumentStatus]

The conventions described in this section are specific to Generative AI client
applications.

**Disclaimer:** These are initial Generative AI client metric instruments
and attributes but more may be added in the future.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Generative AI Client Metrics](#generative-ai-client-metrics)
  - [Metric: `gen_ai.client.token.usage`](#metric-gen_aiclienttokenusage)
  - [Metric: `gen_ai.client.operation.duration`](#metric-gen_aiclientoperationduration)

<!-- tocstop -->

## Generative AI Client Metrics

The following metric instruments describe Generative AI operations. An
operation may be a request to an LLM, a function call, or some other
distinct action within a larger Generative AI workflow.

### Metric: `gen_ai.client.token.usage`

This metric is [recommended][MetricRecommended] when an operation involves the usage
of tokens and the count is readily available.

For example, if GenAI system returns usage information in the streaming response, it SHOULD be used. Or if GenAI system returns each token independently, instrumentation SHOULD count number of output tokens and record the result.

If instrumentation cannot efficiently obtain number of input and/or output tokens, it MAY allow users to enable offline token counting. Otherwise it MUST NOT report usage metric.

When systems report both used tokens and billable tokens, instrumentation MUST report billable tokens.

This metric SHOULD be specified with [ExplicitBucketBoundaries] of [1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304, 16777216, 67108864].

<!-- semconv metric.gen_ai.client.token.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `gen_ai.client.token.usage` | Histogram | `{token}` | Measures number of input and output tokens used | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.gen_ai.client.token.usage(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`gen_ai.operation.name`](/docs/attributes-registry/gen-ai.md) | string | The name of the operation being performed. | `chat`; `completion` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.request.model`](/docs/attributes-registry/gen-ai.md) | string | The name of the LLM a request is being made to. | `gpt-4` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.system`](/docs/attributes-registry/gen-ai.md) | string | The Generative AI product as identified by the client instrumentation. [1] | `openai` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.token.type`](/docs/attributes-registry/gen-ai.md) | string | The type of token being counted. | `input`; `output` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [2] | `80`; `8080`; `443` | `Conditionally Required` If `sever.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`gen_ai.response.model`](/docs/attributes-registry/gen-ai.md) | string | The name of the LLM a response was generated from. | `gpt-4-0613` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [3] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** The actual GenAI product may differ from the one identified by the client. For example, when using OpenAI client libraries to communicate with Mistral, the `gen_ai.system` is set to `openai` based on the instrumentation's best knowledge.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[3]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

`gen_ai.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `openai` | OpenAI | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`gen_ai.token.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `input` | Input tokens (prompt, input, etc.) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `output` | Output tokens (completion, response, etc.) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `gen_ai.client.operation.duration`

This metric is [required][MetricRequired].

This metric SHOULD be specified with [ExplicitBucketBoundaries] of [ 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12,10.24, 20.48, 40.96, 81.92].

<!-- semconv metric.gen_ai.client.operation.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `gen_ai.client.operation.duration` | Histogram | `s` | GenAI operation duration | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.gen_ai.client.operation.duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`gen_ai.operation.name`](/docs/attributes-registry/gen-ai.md) | string | The name of the operation being performed. | `chat`; `completion` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.request.model`](/docs/attributes-registry/gen-ai.md) | string | The name of the LLM a request is being made to. | `gpt-4` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.system`](/docs/attributes-registry/gen-ai.md) | string | The Generative AI product as identified by the client instrumentation. [1] | `openai` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [2] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` if the operation ended in an error | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [3] | `80`; `8080`; `443` | `Conditionally Required` If `sever.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`gen_ai.response.model`](/docs/attributes-registry/gen-ai.md) | string | The name of the LLM a response was generated from. | `gpt-4-0613` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [4] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** The actual GenAI product may differ from the one identified by the client. For example, when using OpenAI client libraries to communicate with Mistral, the `gen_ai.system` is set to `openai` based on the instrumentation's best knowledge.

**[2]:** The cardinality of `error.type` SHOULD be low.

When working across multiple models, it is RECOMMENDED to use a common set of error types.

Additional details may be captured in domain-specific attributes.

**[3]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[4]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

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
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
[ExplicitBucketBoundaries]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/metrics/api.md#instrument-advisory-parameters
