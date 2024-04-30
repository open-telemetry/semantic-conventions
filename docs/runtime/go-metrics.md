<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Go Runtime
--->

# Semantic Conventions for Go Runtime Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for Go runtime metrics in OpenTelemetry.
These metrics are obtained from Go's [`runtime/metrics`][RuntimeMetrics] package.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Go Memory](#go-memory)
  - [Metric: `go.memory.used`](#metric-gomemoryused)
  - [Metric: `go.memory.released`](#metric-gomemoryreleased)
  - [Metric: `go.memory.limit`](#metric-gomemorylimit)
  - [Metric: `go.memory.allocated`](#metric-gomemoryallocated)
  - [Metric: `go.memory.allocations`](#metric-gomemoryallocations)
- [Go Garbage Collection](#go-garbage-collection)
  - [Metric: `go.memory.gc.goal`](#metric-gomemorygcgoal)
  - [Metric: `go.memory.gc.user_goal`](#metric-gomemorygcuser_goal)
- [Go Goroutines](#go-goroutines)
  - [Metric: `go.goroutine.count`](#metric-gogoroutinecount)
- [Go Threads](#go-threads)
  - [Metric: `go.thread.limit`](#metric-gothreadlimit)
- [Go Scheduler](#go-scheduler)
  - [Metric: `go.schedule.duration`](#metric-goscheduleduration)

<!-- tocstop -->

## Go Memory

**Description:** Go runtime metrics captured under the namespace `go.memory.*`

### Metric: `go.memory.used`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.memory.used(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.used` | UpDownCounter | `By` | Memory used by the Go runtime. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `(/memory/classes/total:bytes - /memory/classes/heap/released:bytes)`.
<!-- endsemconv -->

<!-- semconv metric.go.memory.used(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `go.memory.type` | string | The type of memory. | `other`; `stack` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`go.memory.type` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `stack` | Memory allocated from the heap that is reserved for stack space, whether or not it is currently in-use. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | Memory used by the Go runtime, excluding other categories of memory usage. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/memory/classes/heap/stacks:bytes`.
<!-- endsemconv -->

### Metric: `go.memory.released`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.memory.released(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.released` | UpDownCounter | `By` | Memory that is completely free and has been returned to the underlying system. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/memory/classes/heap/released:bytes`.
<!-- endsemconv -->

<!-- semconv metric.go.memory.released(full) -->
<!-- endsemconv -->

### Metric: `go.memory.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.memory.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.limit` | UpDownCounter | `By` | Go runtime memory limit configured by the user, if a limit exists. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/gc/gomemlimit:bytes`. This metric is excluded if the limit obtained from the Go runtime is math.MaxInt64.
<!-- endsemconv -->

<!-- semconv metric.go.memory.limit(full) -->
<!-- endsemconv -->

### Metric: `go.memory.allocated`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.memory.allocated(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.allocated` | Counter | `By` | Memory allocated to the heap by the application. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/gc/heap/allocs:bytes`.
<!-- endsemconv -->

<!-- semconv metric.go.memory.allocated(full) -->
<!-- endsemconv -->

### Metric: `go.memory.allocations`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.memory.allocations(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.allocations` | Counter | `{allocation}` | Count of allocations to the heap by the application. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/gc/heap/allocs:objects`.
<!-- endsemconv -->

<!-- semconv metric.go.memory.allocations(full) -->
<!-- endsemconv -->

## Go Garbage Collection

**Description:** Go metrics captured under the namespace `go.memory.gc.*`

### Metric: `go.memory.gc.goal`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.memory.gc.goal(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.gc.goal` | UpDownCounter | `By` | Heap size target for the end of the GC cycle. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/gc/heap/goal:bytes`.
<!-- endsemconv -->

<!-- semconv metric.go.memory.gc.goal(full) -->
<!-- endsemconv -->

### Metric: `go.memory.gc.user_goal`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.memory.gc.user_goal(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.memory.gc.user_goal` | UpDownCounter | `1` | Heap size target ratio for the end of the GC cycle, as configured by the user. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The value range is [0.0,1.0]. Computed from `/gc/gogc:percent`.
<!-- endsemconv -->

<!-- semconv metric.go.memory.gc.user_goal(full) -->
<!-- endsemconv -->

## Go Goroutines

**Description:** Go metrics captured under the namespace `go.goroutine.*`

### Metric: `go.goroutine.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.goroutine.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.goroutine.count` | UpDownCounter | `{goroutine}` | Count of live goroutines. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/sched/goroutines:goroutines`.
<!-- endsemconv -->

<!-- semconv metric.go.goroutine.count(full) -->
<!-- endsemconv -->

## Go Threads

**Description:** Go metrics captured under the namespace `go.thread.*`

### Metric: `go.thread.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.thread.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.thread.limit` | UpDownCounter | `{thread}` | The number of OS threads that can execute user-level Go code simultaneously. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/sched/gomaxprocs:threads`.
<!-- endsemconv -->

<!-- semconv metric.go.thread.limit(full) -->
<!-- endsemconv -->

## Go Scheduler

**Description:** Go metrics captured under the namespace `go.schedule.*`

### Metric: `go.schedule.duration`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.go.schedule.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `go.schedule.duration` | Histogram | `s` | The time goroutines have spent in the scheduler in a runnable state before actually running. [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Computed from `/sched/latencies:seconds`.
<!-- endsemconv -->

<!-- semconv metric.go.schedule.duration(full) -->
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
[RuntimeMetrics]: https://pkg.go.dev/runtime/metrics
