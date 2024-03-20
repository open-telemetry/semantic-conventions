<!--- Hugo front matter used to generate the website version of this page:
linkTitle: System
--->

# Semantic Conventions for System Metrics

**Status**: [Experimental][DocumentStatus]

This document describes instruments and attributes for common system level
metrics in OpenTelemetry. Consider the [general metric semantic
conventions](/docs/general/metrics.md#general-metric-semantic-conventions) when creating
instruments not explicitly defined in the specification.

The `system.*` namespace SHOULD be exclusively used to report hosts' metrics.
The `system.*` namespace SHOULD only be used when the metrics are collected from within the target system. (physical servers, virtual machines etc).
Metrics collected from technology-specific, well-defined APIs (e.g. Kubelet's API or container runtimes)
should be reported under their respective namespace (e.g. k8s.*, container.*).
Resource attributes related to a host, SHOULD be reported under the `host.*` namespace.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Processor Metrics](#processor-metrics)
  * [Metric: `system.cpu.time`](#metric-systemcputime)
  * [Metric: `system.cpu.utilization`](#metric-systemcpuutilization)
  * [Metric: `system.cpu.physical.count`](#metric-systemcpuphysicalcount)
  * [Metric: `system.cpu.logical.count`](#metric-systemcpulogicalcount)
  * [Metric: `system.cpu.frequency`](#metric-systemcpufrequency)
- [Memory Metrics](#memory-metrics)
  * [Metric: `system.memory.usage`](#metric-systemmemoryusage)
  * [Metric: `system.memory.limit`](#metric-systemmemorylimit)
  * [Metric: `system.memory.utilization`](#metric-systemmemoryutilization)
- [Paging/Swap Metrics](#pagingswap-metrics)
  * [Metric: `system.paging.usage`](#metric-systempagingusage)
  * [Metric: `system.paging.utilization`](#metric-systempagingutilization)
  * [Metric: `system.paging.faults`](#metric-systempagingfaults)
  * [Metric: `system.paging.operations`](#metric-systempagingoperations)
- [Disk Controller Metrics](#disk-controller-metrics)
  * [Metric: `system.disk.io`](#metric-systemdiskio)
  * [Metric: `system.disk.operations`](#metric-systemdiskoperations)
  * [Metric: `system.disk.io_time`](#metric-systemdiskio_time)
  * [Metric: `system.disk.operation_time`](#metric-systemdiskoperation_time)
  * [Metric: `system.disk.merged`](#metric-systemdiskmerged)
- [Filesystem Metrics](#filesystem-metrics)
  * [Metric: `system.filesystem.usage`](#metric-systemfilesystemusage)
  * [Metric: `system.filesystem.utilization`](#metric-systemfilesystemutilization)
- [Network Metrics](#network-metrics)
  * [Metric: `system.network.dropped`](#metric-systemnetworkdropped)
  * [Metric: `system.network.packets`](#metric-systemnetworkpackets)
  * [Metric: `system.network.errors`](#metric-systemnetworkerrors)
  * [Metric: `system.network.io`](#metric-systemnetworkio)
  * [Metric: `system.network.connections`](#metric-systemnetworkconnections)
- [Aggregate System Process Metrics](#aggregate-system-process-metrics)
  * [Metric: `system.process.count`](#metric-systemprocesscount)
  * [Metric: `system.process.created`](#metric-systemprocesscreated)
- [`system.{os}.` - OS Specific System Metrics](#systemos---os-specific-system-metrics)
  * [Metric: `system.linux.memory.available`](#metric-systemlinuxmemoryavailable)

<!-- tocstop -->

> **Warning** Existing instrumentations and collector that are using<!-- markdown-link-check-disable-next-line -->
> [v1.21.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.21.0/docs/system/system-metrics.md)
> (or prior):
>
> * SHOULD NOT adopt any breaking changes from document until the system
>   semantic conventions are marked stable. Conventions include, but are not
>   limited to, attributes, metric names, and unit of measure.
> * SHOULD introduce a control mechanism to allow users to opt-in to the new
>   conventions once the migration plan is finalized.

## Processor Metrics

**Description:** System level processor metrics captured under the namespace `system.cpu`.

### Metric: `system.cpu.time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.cpu.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.cpu.time` | Counter | `s` | Seconds each logical CPU spent on each mode |
<!-- endsemconv -->

<!-- semconv metric.system.cpu.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.cpu.logical_number` | int | The logical CPU number [0..n-1] | `1` | Recommended |
| `system.cpu.state` | string | The state of the CPU | `idle`; `interrupt` | Recommended |

`system.cpu.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `user` | user |
| `system` | system |
| `nice` | nice |
| `idle` | idle |
| `iowait` | iowait |
| `interrupt` | interrupt |
| `steal` | steal |
<!-- endsemconv -->

### Metric: `system.cpu.utilization`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.cpu.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.cpu.utilization` | Gauge | `1` | Difference in system.cpu.time since the last measurement, divided by the elapsed time and number of logical CPUs |
<!-- endsemconv -->

<!-- semconv metric.system.cpu.utilization(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.cpu.logical_number` | int | The logical CPU number [0..n-1] | `1` | Recommended |
| `system.cpu.state` | string | The state of the CPU | `idle`; `interrupt` | Recommended |

`system.cpu.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `user` | user |
| `system` | system |
| `nice` | nice |
| `idle` | idle |
| `iowait` | iowait |
| `interrupt` | interrupt |
| `steal` | steal |
<!-- endsemconv -->

### Metric: `system.cpu.physical.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.cpu.physical.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.cpu.physical.count` | UpDownCounter | `{cpu}` | Reports the number of actual physical processor cores on the hardware |
<!-- endsemconv -->

<!-- semconv metric.system.cpu.physical.count(full) -->
<!-- endsemconv -->

### Metric: `system.cpu.logical.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.cpu.logical.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.cpu.logical.count` | UpDownCounter | `{cpu}` | Reports the number of logical (virtual) processor cores created by the operating system to manage multitasking |
<!-- endsemconv -->

<!-- semconv metric.system.cpu.logical.count(full) -->
<!-- endsemconv -->

### Metric: `system.cpu.frequency`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.cpu.frequency(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.cpu.frequency` | Gauge | `{Hz}` | Reports the current frequency of the CPU in Hz |
<!-- endsemconv -->

<!-- semconv metric.system.cpu.frequency(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.cpu.logical_number` | int | The logical CPU number [0..n-1] | `1` | Recommended |
<!-- endsemconv -->

## Memory Metrics

**Description:** System level memory metrics capture under the namespace `system.memory`.
This does not include [paging/swap memory](#pagingswap-metrics).

### Metric: `system.memory.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.memory.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.memory.usage` | UpDownCounter | `By` | Reports memory in use by state. [1] |

**[1]:** The sum over all `system.memory.state` values SHOULD equal the total memory
available on the system, that is `system.memory.limit`.
<!-- endsemconv -->

<!-- semconv metric.system.memory.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.memory.state` | string | The memory state | `free`; `cached` | Recommended |

`system.memory.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `used` | used |
| `free` | free |
| `shared` | shared |
| `buffers` | buffers |
| `cached` | cached |
<!-- endsemconv -->

### Metric: `system.memory.limit`

This metric is [opt-in][MetricOptIn].

<!-- semconv metric.system.memory.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.memory.limit` | UpDownCounter | `By` | Total memory available in the system. [1] |

**[1]:** Its value SHOULD equal the sum of `system.memory.state` over all states.
<!-- endsemconv -->

<!-- semconv metric.system.memory.limit(full) -->
<!-- endsemconv -->

### Metric: `system.memory.utilization`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.memory.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.memory.utilization` | Gauge | `1` |  |
<!-- endsemconv -->

<!-- semconv metric.system.memory.utilization(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.memory.state` | string | The memory state | `free`; `cached` | Recommended |

`system.memory.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `used` | used |
| `free` | free |
| `shared` | shared |
| `buffers` | buffers |
| `cached` | cached |
<!-- endsemconv -->

## Paging/Swap Metrics

**Description:** System level paging/swap memory metrics captured under the namespace `system.paging`.

### Metric: `system.paging.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.paging.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.paging.usage` | UpDownCounter | `By` | Unix swap or windows pagefile usage |
<!-- endsemconv -->

<!-- semconv metric.system.paging.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.paging.state` | string | The memory paging state | `free` | Recommended |

`system.paging.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `used` | used |
| `free` | free |
<!-- endsemconv -->

### Metric: `system.paging.utilization`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.paging.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.paging.utilization` | Gauge | `1` |  |
<!-- endsemconv -->

<!-- semconv metric.system.paging.utilization(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.paging.state` | string | The memory paging state | `free` | Recommended |

`system.paging.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `used` | used |
| `free` | free |
<!-- endsemconv -->

### Metric: `system.paging.faults`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.paging.faults(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.paging.faults` | Counter | `{fault}` |  |
<!-- endsemconv -->

<!-- semconv metric.system.paging.faults(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.paging.type` | string | The memory paging type | `minor` | Recommended |

`system.paging.type` MUST be one of the following:

| Value  | Description |
|---|---|
| `major` | major |
| `minor` | minor |
<!-- endsemconv -->

### Metric: `system.paging.operations`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.paging.operations(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.paging.operations` | Counter | `{operation}` |  |
<!-- endsemconv -->

<!-- semconv metric.system.paging.operations(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.paging.direction` | string | The paging access direction | `in` | Recommended |
| `system.paging.type` | string | The memory paging type | `minor` | Recommended |

`system.paging.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `in` | in |
| `out` | out |

`system.paging.type` MUST be one of the following:

| Value  | Description |
|---|---|
| `major` | major |
| `minor` | minor |
<!-- endsemconv -->

## Disk Controller Metrics

**Description:** System level disk performance metrics captured under the namespace `system.disk`.

### Metric: `system.disk.io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.disk.io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.disk.io` | Counter | `By` |  |
<!-- endsemconv -->

<!-- semconv metric.system.disk.io(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`disk.io.direction`](../attributes-registry/disk.md) | string | The disk IO operation direction. | `read` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |

`disk.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `read` | read |
| `write` | write |
<!-- endsemconv -->

### Metric: `system.disk.operations`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.disk.operations(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.disk.operations` | Counter | `{operation}` |  |
<!-- endsemconv -->

<!-- semconv metric.system.disk.operations(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`disk.io.direction`](../attributes-registry/disk.md) | string | The disk IO operation direction. | `read` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |

`disk.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `read` | read |
| `write` | write |
<!-- endsemconv -->

### Metric: `system.disk.io_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.disk.io_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.disk.io_time` | Counter | `s` | Time disk spent activated [1] |

**[1]:** The real elapsed time ("wall clock") used in the I/O path (time from operations running in parallel are not counted). Measured as:

- Linux: Field 13 from [procfs-diskstats](https://www.kernel.org/doc/Documentation/ABI/testing/procfs-diskstats)
- Windows: The complement of
  ["Disk\% Idle Time"](https://learn.microsoft.com/archive/blogs/askcore/windows-performance-monitor-disk-counters-explained#windows-performance-monitor-disk-counters-explained)
  performance counter: `uptime * (100 - "Disk\% Idle Time") / 100`
<!-- endsemconv -->

<!-- semconv metric.system.disk.io_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.device` | string | The device identifier | `(identifier)` | Recommended |
<!-- endsemconv -->

### Metric: `system.disk.operation_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.disk.operation_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.disk.operation_time` | Counter | `s` | Sum of the time each operation took to complete [1] |

**[1]:** Because it is the sum of time each request took, parallel-issued requests each contribute to make the count grow. Measured as:

- Linux: Fields 7 & 11 from [procfs-diskstats](https://www.kernel.org/doc/Documentation/ABI/testing/procfs-diskstats)
- Windows: "Avg. Disk sec/Read" perf counter multiplied by "Disk Reads/sec" perf counter (similar for Writes)
<!-- endsemconv -->

<!-- semconv metric.system.disk.operation_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`disk.io.direction`](../attributes-registry/disk.md) | string | The disk IO operation direction. | `read` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |

`disk.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `read` | read |
| `write` | write |
<!-- endsemconv -->

### Metric: `system.disk.merged`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.disk.merged(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.disk.merged` | Counter | `{operation}` |  |
<!-- endsemconv -->

<!-- semconv metric.system.disk.merged(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`disk.io.direction`](../attributes-registry/disk.md) | string | The disk IO operation direction. | `read` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |

`disk.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `read` | read |
| `write` | write |
<!-- endsemconv -->

## Filesystem Metrics

**Description:** System level filesystem metrics captured under the namespace `system.filesystem`.

### Metric: `system.filesystem.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.filesystem.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.filesystem.usage` | UpDownCounter | `By` |  |
<!-- endsemconv -->

<!-- semconv metric.system.filesystem.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.device` | string | The device identifier | `(identifier)` | Recommended |
| `system.filesystem.mode` | string | The filesystem mode | `rw, ro` | Recommended |
| `system.filesystem.mountpoint` | string | The filesystem mount path | `/mnt/data` | Recommended |
| `system.filesystem.state` | string | The filesystem state | `used` | Recommended |
| `system.filesystem.type` | string | The filesystem type | `ext4` | Recommended |

`system.filesystem.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `used` | used |
| `free` | free |
| `reserved` | reserved |

`system.filesystem.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `fat32` | fat32 |
| `exfat` | exfat |
| `ntfs` | ntfs |
| `refs` | refs |
| `hfsplus` | hfsplus |
| `ext4` | ext4 |
<!-- endsemconv -->

### Metric: `system.filesystem.utilization`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.filesystem.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.filesystem.utilization` | Gauge | `1` |  |
<!-- endsemconv -->

<!-- semconv metric.system.filesystem.utilization(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.device` | string | The device identifier | `(identifier)` | Recommended |
| `system.filesystem.mode` | string | The filesystem mode | `rw, ro` | Recommended |
| `system.filesystem.mountpoint` | string | The filesystem mount path | `/mnt/data` | Recommended |
| `system.filesystem.state` | string | The filesystem state | `used` | Recommended |
| `system.filesystem.type` | string | The filesystem type | `ext4` | Recommended |

`system.filesystem.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `used` | used |
| `free` | free |
| `reserved` | reserved |

`system.filesystem.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `fat32` | fat32 |
| `exfat` | exfat |
| `ntfs` | ntfs |
| `refs` | refs |
| `hfsplus` | hfsplus |
| `ext4` | ext4 |
<!-- endsemconv -->

## Network Metrics

**Description:** System level network metrics captured under the namespace `system.network`.

### Metric: `system.network.dropped`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.network.dropped(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.network.dropped` | Counter | `{packet}` | Count of packets that are dropped or discarded even though there was no error [1] |

**[1]:** Measured as:

- Linux: the `drop` column in `/proc/dev/net` ([source](https://web.archive.org/web/20180321091318/http://www.onlamp.com/pub/a/linux/2000/11/16/LinuxAdmin.html))
- Windows: [`InDiscards`/`OutDiscards`](https://docs.microsoft.com/windows/win32/api/netioapi/ns-netioapi-mib_if_row2)
  from [`GetIfEntry2`](https://docs.microsoft.com/windows/win32/api/netioapi/nf-netioapi-getifentry2)
<!-- endsemconv -->

<!-- semconv metric.system.network.dropped(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.io.direction`](../attributes-registry/network.md) | string | The network IO operation direction. | `transmit` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |

`network.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `transmit` | transmit |
| `receive` | receive |
<!-- endsemconv -->

### Metric: `system.network.packets`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.network.packets(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.network.packets` | Counter | `{packet}` |  |
<!-- endsemconv -->

<!-- semconv metric.system.network.packets(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.io.direction`](../attributes-registry/network.md) | string | The network IO operation direction. | `transmit` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |

`network.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `transmit` | transmit |
| `receive` | receive |
<!-- endsemconv -->

### Metric: `system.network.errors`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.network.errors(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.network.errors` | Counter | `{error}` | Count of network errors detected [1] |

**[1]:** Measured as:

- Linux: the `errs` column in `/proc/dev/net` ([source](https://web.archive.org/web/20180321091318/http://www.onlamp.com/pub/a/linux/2000/11/16/LinuxAdmin.html)).
- Windows: [`InErrors`/`OutErrors`](https://docs.microsoft.com/windows/win32/api/netioapi/ns-netioapi-mib_if_row2)
  from [`GetIfEntry2`](https://docs.microsoft.com/windows/win32/api/netioapi/nf-netioapi-getifentry2).
<!-- endsemconv -->

<!-- semconv metric.system.network.errors(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.io.direction`](../attributes-registry/network.md) | string | The network IO operation direction. | `transmit` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |

`network.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `transmit` | transmit |
| `receive` | receive |
<!-- endsemconv -->

### Metric: `system.network.io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.network.io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.network.io` | Counter | `By` |  |
<!-- endsemconv -->

<!-- semconv metric.system.network.io(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.io.direction`](../attributes-registry/network.md) | string | The network IO operation direction. | `transmit` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |

`network.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `transmit` | transmit |
| `receive` | receive |
<!-- endsemconv -->

### Metric: `system.network.connections`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.network.connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.network.connections` | UpDownCounter | `{connection}` |  |
<!-- endsemconv -->

<!-- semconv metric.system.network.connections(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.transport`](../attributes-registry/network.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [1] | `tcp`; `udp` | Recommended |
| `system.device` | string | The device identifier | `(identifier)` | Recommended |
| `system.network.state` | string | A stateless protocol MUST NOT set this attribute | `close_wait` | Recommended |

**[1]:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. |
| `unix` | Unix domain socket |

`system.network.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `close` | close |
| `close_wait` | close_wait |
| `closing` | closing |
| `delete` | delete |
| `established` | established |
| `fin_wait_1` | fin_wait_1 |
| `fin_wait_2` | fin_wait_2 |
| `last_ack` | last_ack |
| `listen` | listen |
| `syn_recv` | syn_recv |
| `syn_sent` | syn_sent |
| `time_wait` | time_wait |
<!-- endsemconv -->
## Aggregate System Process Metrics

**Description:** System level aggregate process metrics captured under the namespace `system.process`.
For metrics at the individual process level, see [process metrics](process-metrics.md).

### Metric: `system.process.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.process.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.process.count` | UpDownCounter | `{process}` | Total number of processes in each state |
<!-- endsemconv -->

<!-- semconv metric.system.process.count(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `system.process.status` | string | The process state, e.g., [Linux Process State Codes](https://man7.org/linux/man-pages/man1/ps.1.html#PROCESS_STATE_CODES) | `running` | Recommended |

`system.process.status` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `running` | running |
| `sleeping` | sleeping |
| `stopped` | stopped |
| `defunct` | defunct |
<!-- endsemconv -->

### Metric: `system.process.created`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.system.process.created(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.process.created` | Counter | `{process}` | Total number of processes created over uptime of the host |
<!-- endsemconv -->

<!-- semconv metric.system.process.created(full) -->
<!-- endsemconv -->

## `system.{os}.` - OS Specific System Metrics

Instrument names for system level metrics that have different and conflicting
meaning across multiple OSes should be prefixed with `system.{os}.` and
follow the hierarchies listed above for different entities like CPU, memory,
and network.

For example, [UNIX load
average](https://wikipedia.org/wiki/Load_(computing)) over a given
interval is not well standardized and its value across different UNIX like
OSes may vary despite being under similar load:

> Without getting into the vagaries of every Unix-like operating system in
existence, the load average more or less represents the average number of
processes that are in the running (using the CPU) or runnable (waiting for
the CPU) states. One notable exception exists: Linux includes processes in
uninterruptible sleep states, typically waiting for some I/O activity to
complete. This can markedly increase the load average on Linux systems.

([source of
quote](https://github.com/torvalds/linux/blob/e4cbce4d131753eca271d9d67f58c6377f27ad21/kernel/sched/loadavg.c#L11-L18),
[linux source
code](https://github.com/torvalds/linux/blob/e4cbce4d131753eca271d9d67f58c6377f27ad21/kernel/sched/loadavg.c#L11-L18))

An instrument for load average over 1 minute on Linux could be named
`system.linux.cpu.load_1m`, reusing the `cpu` name proposed above and having
an `{os}` prefix to split this metric across OSes.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/metric-requirement-level.md#recommended
[MetricOptIn]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/metrics/metric-requirement-level.md#opt-in

### Metric: `system.linux.memory.available`

<!-- semconv metric.system.linux.memory.available(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `system.linux.memory.available` | UpDownCounter | `By` | An estimate of how much memory is available for starting new applications, without causing swapping [1] |

**[1]:** This is an alternative to `system.memory.usage` metric with `state=free`.
Linux starting from 3.14 exports "available" memory. It takes "free" memory as a baseline, and then factors in kernel-specific values.
This is supposed to be more accurate than just "free" memory.
For reference, see the calculations [here](https://superuser.com/a/980821).
See also `MemAvailable` in [/proc/meminfo](https://man7.org/linux/man-pages/man5/proc.5.html).
<!-- endsemconv -->
