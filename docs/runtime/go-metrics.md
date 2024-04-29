<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Go Runtime
--->

# Semantic Conventions for Go Runtime Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for Go runtime metrics in OpenTelemetry.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Go Memory](#go-memory)
  - [Metric: `go.memory.used`](#metric-gomemoryused)
  - [Metric: `go.memory.limit`](#metric-gomemorylimit)
  - [Metric: `go.memory.allocated`](#metric-gomemoryallocated)
  - [Metric: `go.memory.allocations`](#metric-gomemoryallocations)
- [Go Garbage Collection](#go-garbage-collection)
  - [Metric: `go.memory.gc.target`](#metric-gomemorygctarget)
  - [Metric: `go.memory.gc.user_target`](#metric-gomemorygcuser_target)
- [Go Threads](#go-threads)
  - [Metric: `go.thread.limit`](#metric-gothreadlimit)
- [Go Scheduler](#go-scheduler)
  - [Metric: `go.schedule.duration`](#metric-goscheduleduration)

<!-- tocstop -->

## Go Memory

**Description:** Go runtime metrics captured under the namespace `go.memory.*`

### Metric: `go.memory.used`

This metric is [recommended][MetricRecommended].
This metric is obtained from Go's [`runtime/metrics`][RuntimeMetrics] package using `/memory/classes` metrics.

<!-- semconv metric.go.memory.used(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.used` | UpDownCounter | `By` | Virtual memory mapped by the Go runtime. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.go.memory.used(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `go.memory.type` | string | The type of memory. | `released`; `stack` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`go.memory.type` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `released` | Memory that is completely free and has been returned to the underlying system. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `stack` | Memory allocated from the heap that is reserved for stack space, whether or not it is currently in-use. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | All memory mapped by the Go runtime into the current process as read-write, excluding other categories of memory usage. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `go.memory.limit`

This metric is [recommended][MetricRecommended].
This metric is obtained from Go's [`runtime/metrics`][RuntimeMetrics] package using `/gc/gomemlimit:bytes`.

<!-- semconv metric.go.memory.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.limit` | UpDownCounter | `By` | Go runtime memory limit configured by the user, otherwise math.MaxInt64. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.go.memory.limit(full) -->
<!-- endsemconv -->

### Metric: `go.memory.allocated`

This metric is [recommended][MetricRecommended].
This metric is obtained from Go's [`runtime/metrics`][RuntimeMetrics] package using `/gc/heap/allocs:bytes`.

<!-- semconv metric.go.memory.allocated(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.allocated` | Counter | `By` | Memory allocated to the heap by the application. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.go.memory.allocated(full) -->
<!-- endsemconv -->

### Metric: `go.memory.allocations`

This metric is [recommended][MetricRecommended].
This metric is obtained from Go's [`runtime/metrics`][RuntimeMetrics] package using `/gc/heap/allocs:objects`.

<!-- semconv metric.go.memory.allocations(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.allocations` | Counter | `{allocation}` | Count of allocations to the heap by the application. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.go.memory.allocations(full) -->
<!-- endsemconv -->

## Go Garbage Collection

**Description:** Go metrics captured under the namespace `go.memory.gc.*`

### Metric: `go.memory.gc.target`

This metric is [recommended][MetricRecommended].
This metric is obtained from Go's [`runtime/metrics`][RuntimeMetrics] package using `/gc/heap/goal:bytes`.

<!-- semconv metric.go.memory.gc.target(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.gc.target` | UpDownCounter | `By` | Heap size target for the end of the GC cycle. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.go.memory.gc.target(full) -->
<!-- endsemconv -->

### Metric: `go.memory.gc.user_target`

This metric is [recommended][MetricRecommended].
This metric is obtained from Go's [`runtime/metrics`][RuntimeMetrics] package using `/gc/gogc:percent`.

<!-- semconv metric.go.memory.gc.user_target(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.gc.user_target` | UpDownCounter | `1` | Heap size target ratio for the end of the GC cycle, as configured by the user. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The value range is [0.0,1.0].
<!-- endsemconv -->

<!-- semconv metric.go.memory.gc.user_target(full) -->
<!-- endsemconv -->

## Go Threads

**Description:** Go metrics captured under the namespace `go.thread.*`

### Metric: `go.thread.limit`

This metric is [recommended][MetricRecommended].
This metric is obtained from Go's [`runtime/metrics`][RuntimeMetrics] package `/sched/gomaxprocs:threads`.

<!-- semconv metric.go.thread.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.thread.limit` | UpDownCounter | `{thread}` | The number of OS threads that can execute user-level Go code simultaneously. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.go.thread.limit(full) -->
<!-- endsemconv -->

## Go Scheduler

**Description:** Go metrics captured under the namespace `go.schedule.*`

### Metric: `go.schedule.duration`

This metric is [recommended][MetricRecommended].
This metric is obtained from Go's [`runtime/metrics`][RuntimeMetrics] package `/sched/latencies:seconds`.

<!-- semconv metric.go.schedule.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.schedule.duration` | Histogram | `s` | The time goroutines have spent in the scheduler in a runnable state before actually running. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.go.schedule.duration(full) -->
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
[RuntimeMetrics]: https://pkg.go.dev/runtime/metrics
