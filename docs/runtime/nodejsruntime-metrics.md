<!--- Hugo front matter used to generate the website version of this page:
linkTitle: JS Runtime
--->

# Semantic Conventions for Node.js Runtime Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for Node.js Runtime metrics in OpenTelemetry.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Experimental](#experimental)
  - [Metric: `nodejsruntime.active_handles.count`](#metric-nodejsruntimeactive_handlescount)
  - [Metric: `nodejsruntime.eventloop.lag`](#metric-nodejsruntimeeventlooplag)
  - [Metric: `nodejsruntime.eventloop.utilization`](#metric-nodejsruntimeeventlooputilization)
  - [Metric: `nodejsruntime.gc.duration`](#metric-nodejsruntimegcduration)
  - [Metric: `nodejsruntime.memory.size`](#metric-nodejsruntimememorysize)
  - [Metric: `nodejsruntime.heap.size`](#metric-nodejsruntimeheapsize)
  - [Metric: `nodejsruntime.heap.space`](#metric-nodejsruntimeheapspace)

<!-- tocstop -->

## Experimental

**Status**: [Experimental][DocumentStatus]

**Description:** Experimental Node.js Runtime metrics captured under `nodejsruntime`.

### Metric: `nodejsruntime.active_handles.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.active_handles.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.active_handles.count` | UpDownCounter | `{handles}` | Number of active handles. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.active_handles.count(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | JS Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.lag`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.lag(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.lag` | Gauge | `s` | Event loop lag. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.lag(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.eventloop.lag.type`](/docs/attributes-registry/nodejsruntime.md) | string | The type of the event loop latency. | `min`; `p90` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | JS Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejsruntime.eventloop.lag.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `min` | Event loop minimum latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `max` | Event loop maximum latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mean` | Event loop mean latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `stddev` | Event loop standard deviation latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p50` | Event loop 50 percentile latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p90` | Event loop 90 percentile latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p99` | Event loop 99 percentile latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.eventloop.utilization`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.eventloop.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.eventloop.utilization` | Gauge | `s` | Event loop utilization. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.eventloop.utilization(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | JS Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.gc.duration`

This metric is [recommended][MetricRecommended].

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.01, 0.1, 1, 10 ]`.

<!-- semconv metric.nodejsruntime.gc.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.gc.duration` | Histogram | `s` | Garbage collection duration. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.gc.duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.gc.type`](/docs/attributes-registry/nodejsruntime.md) | string | The type of garbage collection. | `major`; `minor`; `incremental` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | JS Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejsruntime.gc.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `major` | Major (Mark Sweep Compact). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `minor` | Minor (Scavenge). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `incremental` | Incremental (Incremental Marking). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `weakcb` | Weak Callbacks (Process Weak Callbacks). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.memory.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.memory.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.memory.size` | UpDownCounter | `By` | External memory size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.memory.size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.memory.state`](/docs/attributes-registry/nodejsruntime.md) | string | The state of memory. | `total`; `used` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | JS Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejsruntime.memory.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `total` | Total memory. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | Used memory. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.heap.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.heap.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.heap.size` | UpDownCounter | `By` | Heap size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.heap.size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.heap.size.state`](/docs/attributes-registry/nodejsruntime.md) | string | The size of heap memory. | `total`; `used` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | JS Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejsruntime.heap.size.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `total` | Total heap memory size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | Used heap memory size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejsruntime.heap.space`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejsruntime.heap.space(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejsruntime.heap.space` | UpDownCounter | `By` | Heap space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejsruntime.heap.space(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejsruntime.heap.space.state`](/docs/attributes-registry/nodejsruntime.md) | string | The space of heap memory. | `total`; `used` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejsruntime.version`](/docs/attributes-registry/nodejsruntime.md) | string | JS Runtime version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejsruntime.heap.space.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `total` | Total heap memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | Used heap memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
