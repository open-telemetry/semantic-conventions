<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Process
--->

# Semantic Conventions for OS Process Metrics

**Status**: [Experimental][DocumentStatus]

This document describes instruments and attributes for common OS process level
metrics in OpenTelemetry. Also consider the [general metric semantic
conventions](/docs/general/metrics.md#general-metric-semantic-conventions) when creating
instruments not explicitly defined in this document. OS process metrics are
not related to the runtime environment of the program, and should take
measurements from the operating system. For runtime environment metrics see
[semantic conventions for runtime environment
metrics](runtime-environment-metrics.md).

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Semantic Conventions for OS Process Metrics](#semantic-conventions-for-os-process-metrics)
  - [Metric Instruments](#metric-instruments)
    - [Metric: `process.cpu.time`](#metric-processcputime)
    - [Metric: `process.cpu.utilization`](#metric-processcpuutilization)
    - [Metric: `process.memory.usage`](#metric-processmemoryusage)
    - [Metric: `process.memory.virtual`](#metric-processmemoryvirtual)
    - [Metric: `process.disk.io`](#metric-processdiskio)
    - [Metric: `process.network.io`](#metric-processnetworkio)
    - [Metric: `process.threads`](#metric-processthreads)
    - [Metric: `process.threads`](#metric-processthreads-1)
    - [Metric: `process.context_switches`](#metric-processcontext_switches)
    - [Metric: `process.paging.faults`](#metric-processpagingfaults)

<!-- tocstop -->

## Metric Instruments

### Metric: `process.cpu.time`

<!-- semconv metric.process.cpu.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.cpu.time` | Counter | `s` | Total CPU seconds broken down by different states. |
<!-- endsemconv -->

<<<<<<< HEAD:specification/metrics/semantic_conventions/process-metrics.md
<!-- semconv metric.process.cpu.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `process.cpu.state` | string | The CPU state for this data point. A process SHOULD be characterized _either_ by data points with no `state` labels, _or only_ data points with `state` labels. | `system` | Recommended |
=======
| Name                            | Instrument Type ([\*](/docs/general/metrics.md#instrument-types)) | Unit      | Description                                                                                                                         | Labels                                                                                                                                                                                          |
|---------------------------------|----------------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `process.cpu.time`              | Counter                                            | s         | Total CPU seconds broken down by different states.                                                                                  | `state`, if specified, SHOULD be one of: `system`, `user`, `wait`. A process SHOULD be characterized _either_ by data points with no `state` labels, _or only_ data points with `state` labels. |
| `process.cpu.utilization`       | Gauge                                              | 1         | Difference in process.cpu.time since the last measurement, divided by the elapsed time and number of CPUs available to the process. | `state`, if specified, SHOULD be one of: `system`, `user`, `wait`. A process SHOULD be characterized _either_ by data points with no `state` labels, _or only_ data points with `state` labels. |
| `process.memory.usage`          | UpDownCounter                                      | By        | The amount of physical memory in use.                                                                                               |                                                                                                                                                                                                 |
| `process.memory.virtual`        | UpDownCounter                                      | By        | The amount of committed virtual memory.                                                                                             |                                                                                                                                                                                                 |
| `process.disk.io`               | Counter                                            | By        | Disk bytes transferred.                                                                                                             | `direction` SHOULD be one of: `read`, `write`                                                                                                                                                   |
| `process.network.io`            | Counter                                            | By        | Network bytes transferred.                                                                                                          | `direction` SHOULD be one of: `receive`, `transmit`                                                                                                                                             |
| `process.threads`               | UpDownCounter                                      | {thread} | Process threads count.                                                                                                              |                                                                                                                                                                                                 |
| `process.open_file_descriptors` | UpDownCounter                                      | {count}   | Number of file descriptors in use by the process.                                                                                   |                                                                                                                                                                                                 |
| `process.context_switches`      | Counter                                            | {count}   | Number of times the process has been context switched.                                                                              | `type` SHOULD be one of: `involuntary`, `voluntary`                                                                                                                                             |
| `process.paging.faults`         | Counter                                            | {fault}  | Number of page faults the process has made.                                                                                         | `type`, if specified, SHOULD be one of: `major` (for major, or hard, page faults), `minor` (for minor, or soft, page faults).                                                                   |
>>>>>>> main:docs/system/process-metrics.md

`process.cpu.state` MUST be one of the following:

<<<<<<< HEAD:specification/metrics/semantic_conventions/process-metrics.md
| Value  | Description |
|---|---|
| `system` | system |
| `user` | user |
| `wait` | wait |
<!-- endsemconv -->

### Metric: `process.cpu.utilization`

<!-- semconv metric.process.cpu.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.cpu.utilization` | Gauge | `1` | Difference in process.cpu.time since the last measurement, divided by the elapsed time and number of CPUs available to the process. |
<!-- endsemconv -->

<!-- semconv metric.process.cpu.utilization(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `process.cpu.state` | string | The CPU state for this data point. A process SHOULD be characterized _either_ by data points with no `state` labels, _or only_ data points with `state` labels. | `system` | Recommended |

`process.cpu.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `system` | system |
| `user` | user |
| `wait` | wait |
<!-- endsemconv -->

### Metric: `process.memory.usage`

<!-- semconv metric.process.memory.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.memory.usage` | UpDownCounter | `By` | The amount of physical memory in use. |
<!-- endsemconv -->

<!-- semconv metric.process.memory.usage(full) -->
<!-- endsemconv -->

### Metric: `process.memory.virtual`

<!-- semconv metric.process.memory.virtual(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.memory.virtual` | UpDownCounter | `By` | The amount of committed virtual memory. |
<!-- endsemconv -->

<!-- semconv metric.process.memory.virtual(full) -->
<!-- endsemconv -->

### Metric: `process.disk.io`

<!-- semconv metric.process.disk.io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.disk.io` | Counter | `By` | Disk bytes transferred. |
<!-- endsemconv -->

<!-- semconv metric.process.disk.io(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `process.disk.direction` | string | The direction of the data transfer for this data point. | `read` | Recommended |

`process.disk.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `read` | read |
| `write` | write |
<!-- endsemconv -->

### Metric: `process.network.io`

<!-- semconv metric.process.network.io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.network.io` | Counter | `By` | Network bytes transferred. |
<!-- endsemconv -->

<!-- semconv metric.process.network.io(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `direction` | string | The direction of the data transfer for this data point. | `receive` | Recommended |

`direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `receive` | receive |
| `transmit` | transmit |
<!-- endsemconv -->

### Metric: `process.threads`

<!-- semconv metric.process.threads(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.threads` | UpDownCounter | `{thread}` | Process threads count. |
<!-- endsemconv -->

<!-- semconv metric.process.threads(full) -->
<!-- endsemconv -->

### Metric: `process.threads`

<!-- semconv metric.process.threads(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.threads` | UpDownCounter | `{thread}` | Process threads count. |
<!-- endsemconv -->

<!-- semconv metric.process.threads(full) -->
<!-- endsemconv -->

### Metric: `process.context_switches`

<!-- semconv metric.process.context_switches(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.context_switches` | Counter | `{count}` | Number of times the process has been context switched. |
<!-- endsemconv -->

<!-- semconv metric.process.context_switches(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `process.context_switches.type` | string | Specifies whether the context switches for this data point were voluntary or involuntary. | `voluntary` | Recommended |

`process.context_switches.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `voluntary` | voluntary |
| `involuntary` | involuntary |
<!-- endsemconv -->

### Metric: `process.paging.faults`

<!-- semconv metric.process.paging.faults(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `process.paging.faults` | UpDownCounter | `{fault}` | Number of page faults the process has made. |
<!-- endsemconv -->

<!-- semconv metric.process.paging.faults(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `process.paging.faults.type` | string | The type of page fault for this data point. Type `major` is for major/hard page faults, and `minor` is for minor/soft page faults. | `major` | Recommended |

`process.paging.faults.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `major` | major |
| `minor` | minor |
<!-- endsemconv -->

=======
Process metrics SHOULD be associated with a [`process`](/docs/resource/process.md#process) resource whose attributes provide additional context about the process.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
>>>>>>> main:docs/system/process-metrics.md
