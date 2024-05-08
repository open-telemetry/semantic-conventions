<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Node.js Runtime
--->

# Semantic Conventions for Node.js Runtime Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for Node.js Runtime metrics in OpenTelemetry.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Experimental](#experimental)
  - [Metric: `nodejsruntime.eventloop.delay`](#metric-nodejsruntimeeventloopdelay)
  - [Metric: `nodejsruntime.eventloop.utilization`](#metric-nodejsruntimeeventlooputilization)

<!-- tocstop -->

## Experimental

**Status**: [Experimental][DocumentStatus]

**Description:** Experimental Node.js Runtime metrics captured under `nodejsruntime`.

### Metric: `nodejsruntime.eventloop.delay`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.delay(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.delay` | Gauge | `s` | Event loop delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.delay(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.eventloop.delay.type`](/docs/attributes-registry/nodejsruntime.md) | string | The type of the event loop delay. | `min`; `p90` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejsruntime.eventloop.delay.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `min` | Event loop minimum delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `max` | Event loop maximum delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mean` | Event loop mean delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `stddev` | Event loop standard deviation delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p50` | Event loop 50 percentile delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p90` | Event loop 90 percentile delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p99` | Event loop 99 percentile delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.utilization`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.utilization` | Gauge | `1` | Event loop utilization. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The value range is [0.0,1.0].
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.utilization(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
