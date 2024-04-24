<!--- Hugo front matter used to generate the website version of this page:
linkTitle: LLM metrics
--->

# Semantic Conventions for LLM Metrics

**Status**: [Experimental][DocumentStatus]

The conventions described in this section are specific to LLM clients.

**Disclaimer:** These are initial LLM client metric instruments
and attributes but more may be added in the future.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [LLM Requests](#llm-requests)
  - [Metric: `gen_ai.usage.tokens`](#metric-gen_aiusagetokens)
  - [Metrics: `gen_ai.request.duration`](#metrics-gen_airequestduration)

<!-- tocstop -->

## LLM Requests

The following metric instruments describe LLM request operations.

### Metric: `gen_ai.usage.tokens`

This metric is [required][MetricRequired].

<!-- semconv metric.gen_ai.usage.tokens(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `gen_ai.usage.tokens` | Histogram | `tokens` | LLM usage attributes | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.gen_ai.usage.tokens(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`gen_ai.response.model`](../attributes-registry/llm.md) | string | The name of the LLM a response was generated from. | `gpt-4-0613` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gen_ai.usage.token_type`](../attributes-registry/llm.md) | string | The type of token being counted. | `prompt`; `completion` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`error.type`](../attributes-registry/error.md) | string | Describes a class of error the operation ended with. [2] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` if the operation ended in an error | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[2]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
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

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

### Metrics: `gen_ai.request.duration`

This metric is [required][MetricRequired].

<!-- semconv metric.gen_ai.request.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `gen_ai.request.duration` | Histogram | `s` | LLM request duration | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.gen_ai.request.duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`gen_ai.response.model`](../attributes-registry/llm.md) | string | The name of the LLM a response was generated from. | `gpt-4-0613` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`error.type`](../attributes-registry/error.md) | string | Describes a class of error the operation ended with. [2] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` if the operation ended in an error | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[2]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
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

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
[MetricRequired]: /docs/general/metric-requirement-level.md#required
