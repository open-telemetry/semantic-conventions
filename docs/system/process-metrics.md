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

- [Metric Instruments](#metric-instruments)
  * [Process](#process)
- [Attributes](#attributes)

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

### Process

Below is a table of Process metric instruments.

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

## Attributes

Process metrics SHOULD be associated with a [`process`](/docs/resource/process.md#process) resource whose attributes provide additional context about the process.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
