<!--- Hugo front matter used to generate the website version of this page:
linkTitle: V8 JS Engine Runtime
--->

# Semantic Conventions for V8 JS Engine Runtime Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for V8 JS Engine Runtime metrics in OpenTelemetry. This engine is used in some javascript runtime such as Node.js and Deno.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Experimental](#experimental)
  - [Metric: `v8jsengineruntime.gc.duration`](#metric-v8jsengineruntimegcduration)
  - [Metric: `v8jsengineruntime.memory.size`](#metric-v8jsengineruntimememorysize)
  - [Metric: `v8jsengineruntime.heap.size`](#metric-v8jsengineruntimeheapsize)
  - [Metric: `v8jsengineruntime.heap.space_size`](#metric-v8jsengineruntimeheapspace_size)
  - [Metric: `v8jsengineruntime.heap.space_used_size`](#metric-v8jsengineruntimeheapspace_used_size)
  - [Metric: `v8jsengineruntime.heap.space_available_size`](#metric-v8jsengineruntimeheapspace_available_size)
  - [Metric: `v8jsengineruntime.heap.physical_space_size`](#metric-v8jsengineruntimeheapphysical_space_size)

<!-- tocstop -->

## Experimental

**Status**: [Experimental][DocumentStatus]

**Description:** Experimental V8 JS Engine Runtime metrics captured under `v8jsengineruntime`.

### Metric: `v8jsengineruntime.gc.duration`

This metric is [recommended][MetricRecommended].

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.01, 0.1, 1, 10 ]`.

<!-- semconv metric.veightjsengineruntime.gc.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `v8jsengineruntime.gc.duration` | Histogram | `s` | Garbage collection duration. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.veightjsengineruntime.gc.duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`v8jsengineruntime.gc.type`](/docs/attributes-registry/v8jsengineruntime.md) | string | The type of garbage collection. | `major`; `minor`; `incremental` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`v8jsengineruntime.gc.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `major` | Major (Mark Sweep Compact). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `minor` | Minor (Scavenge). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `incremental` | Incremental (Incremental Marking). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `weakcb` | Weak Callbacks (Process Weak Callbacks). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `v8jsengineruntime.memory.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.veightjsengineruntime.memory.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `v8jsengineruntime.memory.size` | UpDownCounter | `By` | External memory size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.veightjsengineruntime.memory.size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`v8jsengineruntime.memory.state`](/docs/attributes-registry/v8jsengineruntime.md) | string | The state of memory. | `total`; `used` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`v8jsengineruntime.memory.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `total` | Total memory. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | Used memory. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `v8jsengineruntime.heap.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.veightjsengineruntime.heap.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `v8jsengineruntime.heap.size` | UpDownCounter | `By` | Heap size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.veightjsengineruntime.heap.size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`v8jsengineruntime.heap.size.state`](/docs/attributes-registry/v8jsengineruntime.md) | string | The size of heap memory. | `total`; `used` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`v8jsengineruntime.heap.size.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `total` | Total heap memory size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | Used heap memory size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `v8jsengineruntime.heap.space_size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.veightjsengineruntime.heap.space_size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `v8jsengineruntime.heap.space_size` | UpDownCounter | `By` | Heap space size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.veightjsengineruntime.heap.space_size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`v8jsengineruntime.heap.space.name`](/docs/attributes-registry/v8jsengineruntime.md) | string | The name of the space type of heap memory. | `new_space`; `old_space`; `code_space` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`v8jsengineruntime.heap.space.name` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `new_space` | New memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `old_space` | Old memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code_space` | Code memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `map_space` | Map memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `large_object_space` | Large object memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `v8jsengineruntime.heap.space_used_size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.veightjsengineruntime.heap.space_used_size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `v8jsengineruntime.heap.space_used_size` | UpDownCounter | `By` | Heap space used size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.veightjsengineruntime.heap.space_used_size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`v8jsengineruntime.heap.space.name`](/docs/attributes-registry/v8jsengineruntime.md) | string | The name of the space type of heap memory. | `new_space`; `old_space`; `code_space` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`v8jsengineruntime.heap.space.name` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `new_space` | New memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `old_space` | Old memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code_space` | Code memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `map_space` | Map memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `large_object_space` | Large object memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `v8jsengineruntime.heap.space_available_size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.veightjsengineruntime.heap.space_available_size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `v8jsengineruntime.heap.space_available_size` | UpDownCounter | `By` | Heap space available size. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.veightjsengineruntime.heap.space_available_size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`v8jsengineruntime.heap.space.name`](/docs/attributes-registry/v8jsengineruntime.md) | string | The name of the space type of heap memory. | `new_space`; `old_space`; `code_space` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`v8jsengineruntime.heap.space.name` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `new_space` | New memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `old_space` | Old memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code_space` | Code memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `map_space` | Map memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `large_object_space` | Large object memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `v8jsengineruntime.heap.physical_space_size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.veightjsengineruntime.heap.physical_space_size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `v8jsengineruntime.heap.physical_space_size` | UpDownCounter | `By` | Heap space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.veightjsengineruntime.heap.physical_space_size(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`v8jsengineruntime.heap.space.name`](/docs/attributes-registry/v8jsengineruntime.md) | string | The name of the space type of heap memory. | `new_space`; `old_space`; `code_space` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`v8jsengineruntime.heap.space.name` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `new_space` | New memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `old_space` | Old memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code_space` | Code memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `map_space` | Map memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `large_object_space` | Large object memory space. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
