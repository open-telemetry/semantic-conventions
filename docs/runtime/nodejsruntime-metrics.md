<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Node.js Runtime
--->

# Semantic Conventions for Node.js Runtime Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for Node.js Runtime metrics in OpenTelemetry.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Experimental](#experimental)
  - [Metric: `nodejsruntime.eventloop.delay.min`](#metric-nodejsruntimeeventloopdelaymin)
  - [Metric: `nodejsruntime.eventloop.delay.max`](#metric-nodejsruntimeeventloopdelaymax)
  - [Metric: `nodejsruntime.eventloop.delay.mean`](#metric-nodejsruntimeeventloopdelaymean)
  - [Metric: `nodejsruntime.eventloop.delay.stddev`](#metric-nodejsruntimeeventloopdelaystddev)
  - [Metric: `nodejsruntime.eventloop.delay.p50`](#metric-nodejsruntimeeventloopdelayp50)
  - [Metric: `nodejsruntime.eventloop.delay.p90`](#metric-nodejsruntimeeventloopdelayp90)
  - [Metric: `nodejsruntime.eventloop.delay.p99`](#metric-nodejsruntimeeventloopdelayp99)
  - [Metric: `nodejsruntime.eventloop.utilization`](#metric-nodejsruntimeeventlooputilization)

<!-- tocstop -->

## Experimental

**Status**: [Experimental][DocumentStatus]

**Description:** Experimental Node.js Runtime metrics captured under `nodejsruntime`.

### Metric: `nodejsruntime.eventloop.delay.min`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.delay.min(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.delay.min` | Gauge | `s` | Event loop minimum delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.delay.min(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.delay.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.delay.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.delay.max` | Gauge | `s` | Event loop maximum delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.delay.max(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.delay.mean`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.delay.mean(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.delay.mean` | Gauge | `s` | Event loop mean delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.delay.mean(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.delay.stddev`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.delay.stddev(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.delay.stddev` | Gauge | `s` | Event loop standard deviation delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.delay.stddev(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.delay.p50`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.delay.pfifty(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.delay.p50` | Gauge | `s` | Event loop 50 percentile delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.delay.pfifty(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.delay.p90`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.delay.ninety(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.delay.p90` | Gauge | `s` | Event loop 90 percentile delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.delay.ninety(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.delay.p99`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.delay.ninety_nine(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.delay.p99` | Gauge | `s` | Event loop 99 percentile delay. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.delay.ninety_nine(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | Node.js Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
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
