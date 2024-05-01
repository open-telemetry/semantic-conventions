<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Node.js
--->

# Semantic Conventions for Node.js Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for Node.js metrics in OpenTelemetry.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Experimental](#experimental)
  - [Metric: `nodejs.active_handles.count`](#metric-nodejsactive_handlescount)
  - [Metric: `nodejs.active_requests.count`](#metric-nodejsactive_requestscount)
  - [Metric: `nodejs.eventloop.lag`](#metric-nodejseventlooplag)
  - [Metric: `nodejs.gc.duration`](#metric-nodejsgcduration)
  - [Metric: `nodejs.memory.size`](#metric-nodejsmemorysize)

<!-- tocstop -->

## Experimental

**Status**: [Experimental][DocumentStatus]

**Description:** Experimental Node.js metrics captured under `nodejs.`

### Metric: `nodejs.active_handles.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejs.active_handles.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejs.active_handles.count` | UpDownCounter | `{handles}` | Number of active handles. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejs.active_handles.count(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejs.version`](/docs/attributes-registry/nodejs.md) | string | Node.js version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejs.active_requests.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejs.active_requests.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejs.active_requests.count` | UpDownCounter | `{requests}` | Number of active requests. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejs.active_requests.count(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejs.version`](/docs/attributes-registry/nodejs.md) | string | Node.js version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejs.eventloop.lag`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejs.eventloop.lag(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejs.eventloop.lag` | Counter | `s` | Event loop lag. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejs.eventloop.lag(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejs.eventloop.lag.type`](/docs/attributes-registry/nodejs.md) | string | The type of memory. | `min`; `p90` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejs.version`](/docs/attributes-registry/nodejs.md) | string | Node.js version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejs.eventloop.lag.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `min` | Event loop minimum latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `max` | Event loop maximum latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `avg` | Event loop average latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p50` | Event loop 50 percentile latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p90` | Event loop 90 percentile latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `p99` | Event loop 99 percentile latency. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejs.gc.duration`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejs.gc.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejs.gc.duration` | Counter | `s` | Garbage collection duration. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejs.gc.duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejs.gc.type`](/docs/attributes-registry/nodejs.md) | string | The type of garbage collection. | `major`; `minor`; `incremental` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejs.version`](/docs/attributes-registry/nodejs.md) | string | Node.js version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejs.gc.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `major` | Major (Mark Sweep Compact). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `minor` | Minor (Scavenge). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `incremental` | Incremental (Incremental Marking). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `weakcb` | Weak Callbacks (Process Weak Callbacks). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `nodejs.memory.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.nodejs.memory.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `nodejs.memory.size` | UpDownCounter | `By` | Memory size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.nodejs.memory.size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`nodejs.memory.state`](/docs/attributes-registry/nodejs.md) | string | The state of memory. | `total`; `used` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejs.memory.type`](/docs/attributes-registry/nodejs.md) | string | The type of memory. | `heap`; `external` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`nodejs.version`](/docs/attributes-registry/nodejs.md) | string | Node.js version. | `v22.0.0`; `v21.7.3` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejs.memory.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `total` | Total memory. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | Used memory | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`nodejs.memory.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `heap` | Heap memory. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `external` | External memory | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
