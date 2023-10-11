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
metrics](/docs/runtime/README.md#metrics).

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
    - [Metric: `process.open_file_descriptors`](#metric-processopen_file_descriptors)
    - [Metric: `process.context_switches`](#metric-processcontext_switches)
    - [Metric: `process.paging.faults`](#metric-processpagingfaults)

<!-- tocstop -->

> **Warning** Existing instrumentations and collector that are using<!-- markdown-link-check-disable-next-line -->
> [v1.21.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.21.0/docs/system/process-metrics.md)
> (or prior):
>
> * SHOULD NOT adopt any breaking changes from document until the system
>   semantic conventions are marked stable. Conventions include, but are not
>   limited to, attributes, metric names, and unit of measure.
> * SHOULD introduce a control mechanism to allow users to opt-in to the new
>   conventions once the migration plan is finalized.

## Metric Instruments

### Metric: `process.cpu.time`

<!-- semconv metric.process.cpu.time(metric_table) -->
| Name               | Instrument Type | Unit (UCUM) | Description                                        |
| ------------------ | --------------- | ----------- | -------------------------------------------------- |
| `process.cpu.time` | Counter         | `s`         | Total CPU seconds broken down by different states. |
<!-- endsemconv -->

<!-- semconv metric.process.cpu.time(full) -->
| Attribute           | Type   | Description                                                                                                                                                     | Examples | Requirement Level |
| ------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------- |
| `process.cpu.state` | string | The CPU state for this data point. A process SHOULD be characterized _either_ by data points with no `state` labels, _or only_ data points with `state` labels. | `system` | Recommended       |

`process.cpu.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value    | Description |
| -------- | ----------- |
| `system` | system      |
| `user`   | user        |
| `wait`   | wait        |
<!-- endsemconv -->

### Metric: `process.cpu.utilization`

<!-- semconv metric.process.cpu.utilization(metric_table) -->
| Name                      | Instrument Type | Unit (UCUM) | Description                                                                                                                         |
| ------------------------- | --------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `process.cpu.utilization` | Gauge           | `1`         | Difference in process.cpu.time since the last measurement, divided by the elapsed time and number of CPUs available to the process. |
<!-- endsemconv -->

<!-- semconv metric.process.cpu.utilization(full) -->
| Attribute           | Type   | Description                                                                                                                                                     | Examples | Requirement Level |
| ------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------- |
| `process.cpu.state` | string | The CPU state for this data point. A process SHOULD be characterized _either_ by data points with no `state` labels, _or only_ data points with `state` labels. | `system` | Recommended       |

`process.cpu.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value    | Description |
| -------- | ----------- |
| `system` | system      |
| `user`   | user        |
| `wait`   | wait        |
<!-- endsemconv -->

### Metric: `process.memory.usage`

<!-- semconv metric.process.memory.usage(metric_table) -->
| Name                   | Instrument Type | Unit (UCUM) | Description                           |
| ---------------------- | --------------- | ----------- | ------------------------------------- |
| `process.memory.usage` | UpDownCounter   | `By`        | The amount of physical memory in use. |
<!-- endsemconv -->

<!-- semconv metric.process.memory.usage(full) -->
<!-- endsemconv -->

### Metric: `process.memory.virtual`

<!-- semconv metric.process.memory.virtual(metric_table) -->
| Name                     | Instrument Type | Unit (UCUM) | Description                             |
| ------------------------ | --------------- | ----------- | --------------------------------------- |
| `process.memory.virtual` | UpDownCounter   | `By`        | The amount of committed virtual memory. |
<!-- endsemconv -->

<!-- semconv metric.process.memory.virtual(full) -->
<!-- endsemconv -->

### Metric: `process.disk.io`

<!-- semconv metric.process.disk.io(metric_table) -->
| Name              | Instrument Type | Unit (UCUM) | Description             |
| ----------------- | --------------- | ----------- | ----------------------- |
| `process.disk.io` | Counter         | `By`        | Disk bytes transferred. |
<!-- endsemconv -->

<!-- semconv metric.process.disk.io(full) -->
| Attribute                                | Type   | Description                                             | Examples | Requirement Level |
| ---------------------------------------- | ------ | ------------------------------------------------------- | -------- | ----------------- |
| `process.disk.process.disk.io.direction` | string | The direction of the data transfer for this data point. | `read`   | Recommended       |

`process.disk.process.disk.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value   | Description |
| ------- | ----------- |
| `read`  | read        |
| `write` | write       |
<!-- endsemconv -->

### Metric: `process.network.io`

<!-- semconv metric.process.network.io(metric_table) -->
| Name                 | Instrument Type | Unit (UCUM) | Description                |
| -------------------- | --------------- | ----------- | -------------------------- |
| `process.network.io` | Counter         | `By`        | Network bytes transferred. |
<!-- endsemconv -->

<!-- semconv metric.process.network.io(full) -->
| Attribute                      | Type   | Description                                             | Examples  | Requirement Level |
| ------------------------------ | ------ | ------------------------------------------------------- | --------- | ----------------- |
| `process.network.io.direction` | string | The direction of the data transfer for this data point. | `receive` | Recommended       |

`process.network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value      | Description |
| ---------- | ----------- |
| `receive`  | receive     |
| `transmit` | transmit    |
<!-- endsemconv -->

### Metric: `process.threads`

<!-- semconv metric.process.threads(metric_table) -->
| Name              | Instrument Type | Unit (UCUM) | Description            |
| ----------------- | --------------- | ----------- | ---------------------- |
| `process.threads` | UpDownCounter   | `{thread}`  | Process threads count. |
<!-- endsemconv -->

<!-- semconv metric.process.threads(full) -->
<!-- endsemconv -->

### Metric: `process.open_file_descriptors`

<!-- semconv metric.process.open_file_descriptors(metric_table) -->
| Name                            | Instrument Type | Unit (UCUM) | Description                                       |
| ------------------------------- | --------------- | ----------- | ------------------------------------------------- |
| `process.open_file_descriptors` | UpDownCounter   | `{count}`   | Number of file descriptors in use by the process. |
<!-- endsemconv -->

<!-- semconv metric.process.open_file_descriptors(full) -->
<!-- endsemconv -->

### Metric: `process.context_switches`

<!-- semconv metric.process.context_switches(metric_table) -->
| Name                       | Instrument Type | Unit (UCUM) | Description                                            |
| -------------------------- | --------------- | ----------- | ------------------------------------------------------ |
| `process.context_switches` | Counter         | `{count}`   | Number of times the process has been context switched. |
<!-- endsemconv -->

<!-- semconv metric.process.context_switches(full) -->
| Attribute                       | Type   | Description                                                                               | Examples    | Requirement Level |
| ------------------------------- | ------ | ----------------------------------------------------------------------------------------- | ----------- | ----------------- |
| `process.context_switches.type` | string | Specifies whether the context switches for this data point were voluntary or involuntary. | `voluntary` | Recommended       |

`process.context_switches.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value         | Description |
| ------------- | ----------- |
| `voluntary`   | voluntary   |
| `involuntary` | involuntary |
<!-- endsemconv -->

### Metric: `process.paging.faults`

<!-- semconv metric.process.paging.faults(metric_table) -->
| Name                    | Instrument Type | Unit (UCUM) | Description                                 |
| ----------------------- | --------------- | ----------- | ------------------------------------------- |
| `process.paging.faults` | Counter         | `{fault}`   | Number of page faults the process has made. |
<!-- endsemconv -->

<!-- semconv metric.process.paging.faults(full) -->
| Attribute                    | Type   | Description                                                                                                                        | Examples | Requirement Level |
| ---------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------- |
| `process.paging.faults.type` | string | The type of page fault for this data point. Type `major` is for major/hard page faults, and `minor` is for minor/soft page faults. | `major`  | Recommended       |

`process.paging.faults.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value   | Description |
| ------- | ----------- |
| `major` | major       |
| `minor` | minor       |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
