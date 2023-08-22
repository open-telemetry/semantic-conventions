<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Runtime Environment
--->

# Semantic Conventions for JVM Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for JVM metrics in OpenTelemetry.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [JVM Memory](#jvm-memory)
  * [Metric: `jvm.memory.usage`](#metric-jvmmemoryusage)
  * [Metric: `jvm.memory.committed`](#metric-jvmmemorycommitted)
  * [Metric: `jvm.memory.limit`](#metric-jvmmemorylimit)
  * [Metric: `jvm.memory.usage_after_last_gc`](#metric-jvmmemoryusage_after_last_gc)
- [JVM Garbage Collection](#jvm-garbage-collection)
  * [Metric: `jvm.gc.duration`](#metric-jvmgcduration)
- [JVM Threads](#jvm-threads)
  * [Metric: `jvm.thread.count`](#metric-jvmthreadcount)
- [JVM Classes](#jvm-classes)
  * [Metric: `jvm.class.loaded`](#metric-jvmclassloaded)
  * [Metric: `jvm.class.unloaded`](#metric-jvmclassunloaded)
  * [Metric: `jvm.class.count`](#metric-jvmclasscount)
- [JVM CPU](#jvm-cpu)
  * [Metric: `jvm.cpu.time`](#metric-jvmcputime)
  * [Metric: `jvm.cpu.count`](#metric-jvmcpucount)
  * [Metric: `jvm.cpu.recent_utilization`](#metric-jvmcpurecent_utilization)
- [Very experimental](#very-experimental)
  * [Metric: `jvm.memory.init`](#metric-jvmmemoryinit)
  * [Metric: `jvm.system.cpu.utilization`](#metric-jvmsystemcpuutilization)
  * [Metric: `jvm.system.cpu.load_1m`](#metric-jvmsystemcpuload_1m)
  * [Metric: `jvm.buffer.memory.usage`](#metric-jvmbuffermemoryusage)
  * [Metric: `jvm.buffer.memory.limit`](#metric-jvmbuffermemorylimit)
  * [Metric: `jvm.buffer.count`](#metric-jvmbuffercount)

<!-- tocstop -->

## JVM Memory

**Description:** Java Virtual Machine (JVM) metrics captured under the namespace `jvm.memory.*`

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
| `jvm.memory.type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `jvm.memory.pool.name` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`jvm.memory.type` MUST be one of the following:

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
| `jvm.memory.type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `jvm.memory.pool.name` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`jvm.memory.type` MUST be one of the following:

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
| `jvm.memory.type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `jvm.memory.pool.name` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`jvm.memory.type` MUST be one of the following:

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
| `jvm.memory.type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `jvm.memory.pool.name` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`jvm.memory.type` MUST be one of the following:

| Value  | Description |
|---|---|
| `heap` | Heap memory. |
| `non_heap` | Non-heap memory |
<!-- endsemconv -->

## JVM Garbage Collection

**Description:** Java Virtual Machine (JVM) metrics captured under the namespace `jvm.gc.*`

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
| `jvm.gc.name` | string | Name of the garbage collector. [1] | `G1 Young Generation`; `G1 Old Generation` | Recommended |
| `jvm.gc.action` | string | Name of the garbage collector action. [2] | `end of minor GC`; `end of major GC` | Recommended |

**[1]:** Garbage collector name is generally obtained via [GarbageCollectionNotificationInfo#getGcName()](https://docs.oracle.com/en/java/javase/11/docs/api/jdk.management/com/sun/management/GarbageCollectionNotificationInfo.html#getGcName()).

**[2]:** Garbage collector action is generally obtained via [GarbageCollectionNotificationInfo#getGcAction()](https://docs.oracle.com/en/java/javase/11/docs/api/jdk.management/com/sun/management/GarbageCollectionNotificationInfo.html#getGcAction()).
<!-- endsemconv -->

## JVM Threads

**Description:** Java Virtual Machine (JVM) metrics captured under the namespace `jvm.thread.*`

### Metric: `jvm.thread.count`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`ThreadMXBean#getDaemonThreadCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ThreadMXBean.html#getDaemonThreadCount--) and
[`ThreadMXBean#getThreadCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ThreadMXBean.html#getThreadCount--).
Note that this is the number of platform threads (as opposed to virtual threads).

<!-- semconv metric.jvm.thread.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.thread.count` | UpDownCounter | `{thread}` | Number of executing platform threads. |
<!-- endsemconv -->

<!-- semconv metric.jvm.thread.count(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`thread.daemon`](../general/attributes.md) | boolean | Whether the thread is daemon or not. |  | Recommended |
<!-- endsemconv -->

## JVM Classes

**Description:** Java Virtual Machine (JVM) metrics captured under the namespace `jvm.class.*`

### Metric: `jvm.class.loaded`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`ClassLoadingMXBean#getTotalLoadedClassCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ClassLoadingMXBean.html#getTotalLoadedClassCount--).

<!-- semconv metric.jvm.class.loaded(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.class.loaded` | Counter | `{class}` | Number of classes loaded since JVM start. |
<!-- endsemconv -->

<!-- semconv metric.jvm.class.loaded(full) -->
<!-- endsemconv -->

### Metric: `jvm.class.unloaded`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`ClassLoadingMXBean#getUnloadedClassCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ClassLoadingMXBean.html#getUnloadedClassCount--).

<!-- semconv metric.jvm.class.unloaded(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.class.unloaded` | Counter | `{class}` | Number of classes unloaded since JVM start. |
<!-- endsemconv -->

<!-- semconv metric.jvm.class.unloaded(full) -->
<!-- endsemconv -->

### Metric: `jvm.class.count`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`ClassLoadingMXBean#getLoadedClassCount()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/ClassLoadingMXBean.html#getLoadedClassCount--).

<!-- semconv metric.jvm.class.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.class.count` | UpDownCounter | `{class}` | Number of classes currently loaded. |
<!-- endsemconv -->

<!-- semconv metric.jvm.class.count(full) -->
<!-- endsemconv -->

## JVM CPU

**Description:** Java Virtual Machine (JVM) metrics captured under the namespace `jvm.cpu.*`

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

## Very experimental

**Description:** Very experimental Java Virtual Machine (JVM) metrics captured under `jvm.`

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
| `jvm.memory.type` | string | The type of memory. | `heap`; `non_heap` | Recommended |
| `jvm.memory.pool.name` | string | Name of the memory pool. [1] | `G1 Old Gen`; `G1 Eden space`; `G1 Survivor Space` | Recommended |

**[1]:** Pool names are generally obtained via [MemoryPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/MemoryPoolMXBean.html#getName()).

`jvm.memory.type` MUST be one of the following:

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

### Metric: `jvm.buffer.memory.usage`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`BufferPoolMXBean#getMemoryUsed()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/BufferPoolMXBean.html#getMemoryUsed--).

<!-- semconv metric.jvm.buffer.memory.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.buffer.memory.usage` | UpDownCounter | `By` | Measure of memory used by buffers. |
<!-- endsemconv -->

<!-- semconv metric.jvm.buffer.memory.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `jvm.buffer.pool.name` | string | Name of the buffer pool. [1] | `mapped`; `direct` | Recommended |

**[1]:** Pool names are generally obtained via [BufferPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/BufferPoolMXBean.html#getName()).
<!-- endsemconv -->

### Metric: `jvm.buffer.memory.limit`

This metric is [recommended][MetricRecommended].
This metric is obtained from [`BufferPoolMXBean#getTotalCapacity()`](https://docs.oracle.com/javase/8/docs/api/java/lang/management/BufferPoolMXBean.html#getTotalCapacity--).

<!-- semconv metric.jvm.buffer.memory.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `jvm.buffer.memory.limit` | UpDownCounter | `By` | Measure of total memory capacity of buffers. |
<!-- endsemconv -->

<!-- semconv metric.jvm.buffer.memory.limit(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `jvm.buffer.pool.name` | string | Name of the buffer pool. [1] | `mapped`; `direct` | Recommended |

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
| `jvm.buffer.pool.name` | string | Name of the buffer pool. [1] | `mapped`; `direct` | Recommended |

**[1]:** Pool names are generally obtained via [BufferPoolMXBean#getName()](https://docs.oracle.com/en/java/javase/11/docs/api/java.management/java/lang/management/BufferPoolMXBean.html#getName()).
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
[MetricOptIn]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/metric-requirement-level.md#opt-in
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/metric-requirement-level.md#recommended
