<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
--->

# Semantic Conventions for OpenAI Metrics

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for OpenAI client metrics.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Chat completions](#chat-completions)
  * [Metric: `openai.chat_completions.tokens`](#metric-openaichat_completionstokens)
  * [Metric: `openai.chat_completions.choices`](#metric-openaichat_completionschoices)
  * [Metric: `openai.chat_completions.duration`](#metric-openaichat_completionsduration)
- [Embeddings](#embeddings)
  * [Metric: `openai.embeddings.tokens`](#metric-openaiembeddingstokens)
  * [Metric: `openai.embeddings.vector_size`](#metric-openaiembeddingsvector_size)
  * [Metric: `openai.embeddings.duration`](#metric-openaiembeddingsduration)
- [Image generation](#image-generation)
  * [Metric: `openai.image_generations.duration`](#metric-openaiimage_generationsduration)

<!-- tocstop -->

## Chat completions

### Metric: `openai.chat_completions.tokens`

**Status**: [Experimental][DocumentStatus]

This metric is required.

<!-- semconv metric.openai.chat_completions.tokens(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `openai.chat_completions.tokens` | Counter | `{token}` | Number of tokens used in prompt and completions |
<!-- endsemconv -->

<!-- semconv metric.openai.chat_completions.tokens(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Required |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Conditionally Required: if and only if operation has ended with an error |
| `openai.usage.type` | string | Describes if tokens were used in prompt or completion | `prompt`; `completion` | Required |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Required |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

### Metric: `openai.chat_completions.choices`

**Status**: [Experimental][DocumentStatus]

This metric is required.

<!-- semconv metric.openai.chat_completions.choices(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `openai.chat_completions.choices` | Counter | `{choice}` | Number of choices returned by chat completions call |
<!-- endsemconv -->

<!-- semconv metric.openai.chat_completions.choices(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Required |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Conditionally Required: if and only if operation has ended with an error |
| `openai.choice.finish_reason` | string | Finish reason for single chat completion choice | `stop`; `length`; `content_filter` | Conditionally Required: if and only if it was returned. |
| `openai.usage.type` | string | Describes if tokens were used in prompt or completion | `prompt`; `completion` | Required |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Required |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->


### Metric: `openai.chat_completions.duration`

**Status**: [Experimental][DocumentStatus]

This metric is required.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/api.md#instrument-advice)
of `[ 0, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.openai.chat_completions.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `openai.chat_completions.duration` | Histogram | `s` | Duration of chat completion operation |
<!-- endsemconv -->

<!-- semconv metric.openai.chat_completions.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Required |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Conditionally Required: if and only if operation has ended with an error |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Required |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

## Embeddings

### Metric: `openai.embeddings.tokens`

**Status**: [Experimental][DocumentStatus]

This metric is required.

<!-- semconv metric.openai.embeddings.tokens(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `openai.embeddings.tokens` | Counter | `{token}` | Number of tokens used in prompt. |
<!-- endsemconv -->

<!-- semconv metric.openai.embeddings.tokens(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Required |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Conditionally Required: if and only if operation has ended with an error |
| `openai.usage.type` | string | Describes if tokens were used in prompt or completion | `prompt` | Recommended |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Required |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

### Metric: `openai.embeddings.vector_size`

**Status**: [Experimental][DocumentStatus]

This metric is required.

<!-- semconv metric.openai.embeddings.vector_size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `openai.embeddings.vector_size` | Counter | `{element}` | The size of returned vector. |
<!-- endsemconv -->

<!-- semconv metric.openai.embeddings.vector_size(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Required |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Conditionally Required: if and only if operation has ended with an error |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Required |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

### Metric: `openai.embeddings.duration`

**Status**: [Experimental][DocumentStatus]

This metric is required.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/api.md#instrument-advice)
of `[ 0, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.openai.embeddings.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `openai.embeddings.duration` | Histogram | `s` | Duration of embeddings operation |
<!-- endsemconv -->

<!-- semconv metric.openai.embeddings.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Required |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Conditionally Required: if and only if operation has ended with an error |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Required |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md

## Image generation

### Metric: `openai.image_generations.duration`

**Status**: [Experimental][DocumentStatus]

This metric is required.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/api.md#instrument-advice)
of `[ 0, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.openai.image_generations.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `openai.image_generations.duration` | Histogram | `s` | Duration of image generations operation |
<!-- endsemconv -->

<!-- semconv metric.openai.image_generations.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Required |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Conditionally Required: if and only if operation has ended with an error |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Required |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md