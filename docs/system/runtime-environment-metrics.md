<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Runtime Environment
--->

# Semantic Conventions for Runtime Environment Metrics

**Status**: [Experimental][DocumentStatus]

This document includes semantic conventions for runtime environment level
metrics in OpenTelemetry. Also consider the [general
metric](/docs/general/metrics.md#general-metric-semantic-conventions), [system
metrics](system-metrics.md) and [OS Process metrics](process-metrics.md)
semantic conventions when instrumenting runtime environments.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Metric Instruments](#metric-instruments)
  * [Runtime Environment Specific Metrics - `process.runtime.{environment}.`](#runtime-environment-specific-metrics---processruntimeenvironment)
- [Attributes](#attributes)
- [JVM Metrics](#jvm-metrics)
  * [Metric: `jvm.memory.usage`](#metric-jvmmemoryusage)
  * [Metric: `jvm.memory.committed`](#metric-jvmmemorycommitted)
  * [Metric: `jvm.memory.limit`](#metric-jvmmemorylimit)
  * [Metric: `jvm.memory.usage_after_last_gc`](#metric-jvmmemoryusage_after_last_gc)
  * [Metric: `jvm.gc.duration`](#metric-jvmgcduration)
  * [Metric: `jvm.threads.count`](#metric-jvmthreadscount)
  * [Metric: `jvm.classes.loaded`](#metric-jvmclassesloaded)
  * [Metric: `jvm.classes.unloaded`](#metric-jvmclassesunloaded)
  * [Metric: `jvm.classes.current_loaded`](#metric-jvmclassescurrent_loaded)
  * [Metric: `jvm.cpu.time`](#metric-jvmcputime)
  * [Metric: `jvm.cpu.count`](#metric-jvmcpucount)
  * [Metric: `jvm.cpu.recent_utilization`](#metric-jvmcpurecent_utilization)
- [JVM Metrics (Experimental)](#jvm-metrics-experimental)
  * [Metric: `jvm.memory.init`](#metric-jvmmemoryinit)
  * [Metric: `jvm.system.cpu.utilization`](#metric-jvmsystemcpuutilization)
  * [Metric: `jvm.system.cpu.load_1m`](#metric-jvmsystemcpuload_1m)
  * [Metric: `jvm.buffer.usage`](#metric-jvmbufferusage)
  * [Metric: `jvm.buffer.limit`](#metric-jvmbufferlimit)
  * [Metric: `jvm.buffer.count`](#metric-jvmbuffercount)

<!-- tocstop -->

## Metric Instruments

Runtime environments vary widely in their terminology, implementation, and
relative values for a given metric. For example, Go and Python are both
garbage collected languages, but comparing heap usage between the Go and
CPython runtimes directly is not meaningful. For this reason, this document
does not propose any standard top-level runtime metric instruments. See [OTEP
108](https://github.com/open-telemetry/oteps/pull/108/files) for additional
discussion.

### Runtime Environment Specific Metrics - `process.runtime.{environment}.`

Metrics specific to a certain runtime environment should be prefixed with
`process.runtime.{environment}.` and follow the semantic conventions outlined in
[general metric semantic
conventions](/docs/general/metrics.md#general-metric-semantic-conventions). Authors of
runtime instrumentations are responsible for the choice of `{environment}` to
avoid ambiguity when interpreting a metric's name or values.

For example, some programming languages have multiple runtime environments
that vary significantly in their implementation, like [Python which has many
implementations](https://wiki.python.org/moin/PythonImplementations). For
such languages, consider using specific `{environment}` prefixes to avoid
ambiguity, like `process.runtime.cpython.` and `process.runtime.pypy.`.

There are other dimensions even within a given runtime environment to
consider, for example pthreads vs green thread implementations.

## Attributes

[`process.runtime`](/docs/resource/process.md#process-runtimes) resource attributes SHOULD be included on runtime metric events as appropriate.

## JVM Metrics

**Description:** Java Virtual Machine (JVM) metrics captured under the namespace `jvm.`

### Metric: `jvm.memory.usage`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`MemoryPoolMXBean#getUsage()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/MemoryPoolMXBean.html#getUsage--).

<!-- semconv metric.jvm.memory.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.memory.usage` | UpDownCounter | `By` | Measure of memory used. |
<!-- endsemconv -->

<!-- semconv metric.jvm.memory.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `pool` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`type` MUST be one of the following:

| Value  | Description |
|---|---|
| `heap` | Heap memory. |
| `non_heap` | Non-heap memory |
<!-- endsemconv -->

### Metric: `jvm.memory.committed`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`MemoryPoolMXBean#getUsage()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/MemoryPoolMXBean.html#getUsage--).

<!-- semconv metric.jvm.memory.committed(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.memory.committed` | UpDownCounter | `By` | Measure of memory committed. |
<!-- endsemconv -->

<!-- semconv metric.jvm.memory.committed(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `pool` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`type` MUST be one of the following:

| Value  | Description |
|---|---|
| `heap` | Heap memory. |
| `non_heap` | Non-heap memory |
<!-- endsemconv -->

### Metric: `jvm.memory.limit`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`MemoryPoolMXBean#getUsage()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/MemoryPoolMXBean.html#getUsage--).

<!-- semconv metric.jvm.memory.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.memory.limit` | UpDownCounter | `By` | Measure of max obtainable memory. |
<!-- endsemconv -->

<!-- semconv metric.jvm.memory.limit(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `pool` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`type` MUST be one of the following:

| Value  | Description |
|---|---|
| `heap` | Heap memory. |
| `non_heap` | Non-heap memory |
<!-- endsemconv -->

### Metric: `jvm.memory.usage_after_last_gc`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`MemoryPoolMXBean#getCollectionUsage()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/MemoryPoolMXBean.html#getCollectionUsage--).

<!-- semconv metric.jvm.memory.usage_after_last_gc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.memory.usage_after_last_gc` | UpDownCounter | `By` | Measure of memory used, as measured after the most recent garbage collection event on this pool. |
<!-- endsemconv -->

<!-- semconv metric.jvm.memory.usage_after_last_gc(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `pool` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`type` MUST be one of the following:

| Value  | Description |
|---|---|
| `heap` | Heap memory. |
| `non_heap` | Non-heap memory |
<!-- endsemconv -->

### Metric: `jvm.gc.duration`

This metric is [recommended][MetricRecommended].
This metric is obtained by subscribing to
[`GarbageCollectionNotificationInfo`](https://docs.oracle.com/javase/8/docs/jre/api/management/extension/com/sun/management/GarbageCollectionNotificationInfo.html) events provided by [`GarbageCollectorMXBean`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/GarbageCollectorMXBean.html). The duration value is obtained from [`GcInfo`](https://docs.oracle.com/javase/8/docs/jre/api/management/extension/com/sun/management/GcInfo.html#getDuration--)

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/api.md#instrument-advice)
of `[]` (single bucket histogram capturing count, sum, min, max).

<!-- semconv metric.jvm.gc.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.gc.duration` | Histogram | `s` | Duration of JVM garbage collection actions. |
<!-- endsemconv -->

<!-- semconv metric.jvm.gc.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `gc` | string | Name of the garbage collector. [1] | `G1 Young Generation`; `G1 Old Generation` | Recommended |
| `action` | string | Name of the garbage collector action. [2] | `end of minor GC`; `end of major GC` | Recommended |

**[1]:** Garbage collector name is generally obtained via [GarbageCollectionNotificationInfo#getGcName()](https://docs.oracle.com/en/java/javase/11/docs/api/jdk.management/com/sun/management/GarbageCollectionNotificationInfo.html#getGcName()).

**[2]:** Garbage collector action is generally obtained via [GarbageCollectionNotificationInfo#getGcAction()](https://docs.oracle.com/en/java/javase/11/docs/api/jdk.management/com/sun/management/GarbageCollectionNotificationInfo.html#getGcAction()).
<!-- endsemconv -->

### Metric: `jvm.threads.count`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`ThreadMXBean#getDaemonThreadCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ThreadMXBean.html#getDaemonThreadCount--) and
[`ThreadMXBean#getThreadCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ThreadMXBean.html#getThreadCount--).
Note that this is the number of platform threads (as opposed to virtual threads).

<!-- semconv metric.jvm.threads.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.threads.count` | UpDownCounter | `{thread}` | Number of executing platform threads. |
<!-- endsemconv -->

<!-- semconv metric.jvm.threads.count(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `daemon` | boolean | Whether the thread is daemon or not. |  | Recommended |
<!-- endsemconv -->

### Metric: `jvm.classes.loaded`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`ClassLoadingMXBean#getTotalLoadedClassCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ClassLoadingMXBean.html#getTotalLoadedClassCount--).

<!-- semconv metric.jvm.classes.loaded(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.classes.loaded` | Counter | `{class}` | Number of classes loaded since JVM start. |
<!-- endsemconv -->

<!-- semconv metric.jvm.classes.loaded(full) -->
<!-- endsemconv -->

### Metric: `jvm.classes.unloaded`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`ClassLoadingMXBean#getUnloadedClassCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ClassLoadingMXBean.html#getUnloadedClassCount--).

<!-- semconv metric.jvm.classes.unloaded(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.classes.unloaded` | Counter | `{class}` | Number of classes unloaded since JVM start. |
<!-- endsemconv -->

<!-- semconv metric.jvm.classes.unloaded(full) -->
<!-- endsemconv -->

### Metric: `jvm.classes.current_loaded`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`ClassLoadingMXBean#getLoadedClassCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ClassLoadingMXBean.html#getLoadedClassCount--).

<!-- semconv metric.jvm.classes.current_loaded(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.classes.current_loaded` | UpDownCounter | `{class}` | Number of classes currently loaded. |
<!-- endsemconv -->

<!-- semconv metric.jvm.classes.current_loaded(full) -->
<!-- endsemconv -->

### Metric: `jvm.cpu.time`

This metric is [recommended][MetricRecommended].

This metric is obtained from [`com.sun.management.OperatingSystemMXBean#getProcessCpuTime()`](https://docs.oracle.com/en/java/javase/17/docs/api/jdk.management/com/sun/management/OperatingSystemMXBean.html#getProcessCpuTime()) on HotSpot
and [`com.ibm.lang.management.OperatingSystemMXBean#getProcessCpuTime()`](https://www.ibm.com/docs/api/v1/content/SSYKE2_8.0.0/openj9/api/jdk8/jre/management/extension/com/ibm/lang/management/OperatingSystemMXBean.html#getProcessCpuTime--) on J9.

<!-- semconv metric.jvm.cpu.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.cpu.time` | Counter | `s` | CPU time used by the process as reported by the JVM. |
<!-- endsemconv -->

<!-- semconv metric.jvm.cpu.time(full) -->
<!-- endsemconv -->

### Metric: `jvm.cpu.count`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`Runtime#availableProcessors()`](https://docs.oracle.com/javase/8/docs/api/java/lang/Runtime.html#availableProcessors--).
Note that this is always an integer value (i.e. fractional or millicores are not represented).

<!-- semconv metric.jvm.cpu.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.cpu.count` | UpDownCounter | `{cpu}` | Number of processors available to the Java virtual machine. |
<!-- endsemconv -->

<!-- semconv metric.jvm.cpu.count(full) -->
<!-- endsemconv -->

### Metric: `jvm.cpu.recent_utilization`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`com.sun.management.OperatingSystemMXBean#getProcessCpuLoad()`](https://docs.oracle.com/en/java/javase/17/docs/api/jdk.management/com/sun/management/OperatingSystemMXBean.html#getProcessCpuLoad()) on HotSpot
and [`com.ibm.lang.management.OperatingSystemMXBean#getProcessCpuLoad()`](https://www.ibm.com/docs/api/v1/content/SSYKE2_8.0.0/openj9/api/jdk8/jre/management/extension/com/ibm/lang/management/OperatingSystemMXBean.html#getProcessCpuLoad--) on J9.
Note that the JVM does not provide a definition of what "recent" means.

<!-- semconv metric.jvm.cpu.recent_utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.cpu.recent_utilization` | Gauge | `1` | Recent CPU utilization for the process as reported by the JVM. [1] |

**[1]:** The value range is [0.0,1.0]. This utilization is not defined as being for the specific interval since last measurement (unlike `system.cpu.utilization`). [Reference](https://docs.oracle.com/en/java/javase/17/docs/api/jdk.management/com/sun/management/OperatingSystemMXBean.html#getProcessCpuLoad()).
<!-- endsemconv -->

<!-- semconv metric.jvm.cpu.recent_utilization(full) -->
<!-- endsemconv -->

## JVM Metrics (Experimental)

**Description:** Experimental Java Virtual Machine (JVM) metrics captured under `jvm.`

### Metric: `jvm.memory.init`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`MemoryPoolMXBean#getUsage()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/MemoryPoolMXBean.html#getUsage--).

<!-- semconv metric.jvm.memory.init(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.memory.init` | UpDownCounter | `By` | Measure of initial memory requested. |
<!-- endsemconv -->

<!-- semconv metric.jvm.memory.init(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `pool` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`type` MUST be one of the following:

| Value  | Description |
|---|---|
| `heap` | Heap memory. |
| `non_heap` | Non-heap memory |
<!-- endsemconv -->

### Metric: `jvm.system.cpu.utilization`

This metric is [Opt-In][MetricOptIn].
This metric is obtained from [`com.sun.management.OperatingSystemMXBean#getSystemCpuLoad()`](https://docs.oracle.com/en/java/javase/17/docs/api/jdk.management/com/sun/management/OperatingSystemMXBean.html#getSystemCpuLoad()) on Java version 8..13, [`com.sun.management.OperatingSystemMXBean#getCpuLoad()`](https://docs.oracle.com/en/java/javase/17/docs/api/jdk.management/com/sun/management/OperatingSystemMXBean.html#getCpuLoad()) on Java version 14+,
and [`com.ibm.lang.management.OperatingSystemMXBean#getSystemCpuLoad()`](https://www.ibm.com/docs/api/v1/content/SSYKE2_8.0.0/openj9/api/jdk8/jre/management/extension/com/ibm/lang/management/OperatingSystemMXBean.html) on J9.

<!-- semconv metric.jvm.system.cpu.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.system.cpu.utilization` | Gauge | `1` | Recent CPU utilization for the whole system as reported by the JVM. [1] |

**[1]:** The value range is [0.0,1.0]. This utilization is not defined as being for the specific interval since last measurement (unlike `system.cpu.utilization`). [Reference](https://docs.oracle.com/en/java/javase/17/docs/api/jdk.management/com/sun/management/OperatingSystemMXBean.html#getCpuLoad()).
<!-- endsemconv -->

<!-- semconv metric.jvm.system.cpu.utilization(full) -->
<!-- endsemconv -->

### Metric: `jvm.system.cpu.load_1m`

This metric is [Opt-In][MetricOptIn].
This metric is obtained from [`OperatingSystemMXBean#getSystemLoadAverage()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/OperatingSystemMXBean.html#getSystemLoadAverage--).

<!-- semconv metric.jvm.system.cpu.load_1m(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.system.cpu.load_1m` | Gauge | `{run_queue_item}` | Average CPU load of the whole system for the last minute as reported by the JVM. [1] |

**[1]:** The value range is [0,n], where n is the number of CPU cores - or a negative number if the value is not available. This utilization is not defined as being for the specific interval since last measurement (unlike `system.cpu.utilization`). [Reference](https://docs.oracle.com/en/java/javase/17/docs/api/java.management/java/lang/management/OperatingSystemMXBean.html#getSystemLoadAverage()).
<!-- endsemconv -->

<!-- semconv metric.jvm.system.cpu.load_1m(full) -->
<!-- endsemconv -->

### Metric: `jvm.buffer.usage`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`BufferPoolMXBean#getMemoryUsed()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/BufferPoolMXBean.html#getMemoryUsed--).

<!-- semconv metric.jvm.buffer.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.buffer.usage` | UpDownCounter | `By` | Measure of memory used by buffers. |
<!-- endsemconv -->

<!-- semconv metric.jvm.buffer.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool` | string | Name of the buffer pool. [1] | `mapped`; `direct` | Recommended |

**[1]:** Pool names are generally obtained via [BufferPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/BufferPoolMXBean.html#getName()).
<!-- endsemconv -->

### Metric: `jvm.buffer.limit`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`BufferPoolMXBean#getTotalCapacity()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/BufferPoolMXBean.html#getTotalCapacity--).

<!-- semconv metric.jvm.buffer.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.buffer.limit` | UpDownCounter | `By` | Measure of total memory capacity of buffers. |
<!-- endsemconv -->

<!-- semconv metric.jvm.buffer.limit(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool` | string | Name of the buffer pool. [1] | `mapped`; `direct` | Recommended |

**[1]:** Pool names are generally obtained via [BufferPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/BufferPoolMXBean.html#getName()).
<!-- endsemconv -->

### Metric: `jvm.buffer.count`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`BufferPoolMXBean#getCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/BufferPoolMXBean.html#getCount--).

<!-- semconv metric.jvm.buffer.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.buffer.count` | UpDownCounter | `{buffer}` | Number of buffers in the pool. |
<!-- endsemconv -->

<!-- semconv metric.jvm.buffer.count(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool` | string | Name of the buffer pool. [1] | `mapped`; `direct` | Recommended |

**[1]:** Pool names are generally obtained via [BufferPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/BufferPoolMXBean.html#getName()).
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
[MetricOptIn]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/metric-requirement-level.md#opt-in
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/metric-requirement-level.md#recommended
