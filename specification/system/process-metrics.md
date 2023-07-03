<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Process
--->

# Semantic Conventions for OS Process Metrics

**Status**: [Experimental][DocumentStatus]

This document describes instruments and attributes for common OS process level
metrics in OpenTelemetry. Also consider the [general metric semantic
conventions](/specification/general/metrics-general.md#general-metric-semantic-conventions) when creating
instruments not explicitly defined in this document. OS process metrics are
not related to the runtime environment of the program, and should take
measurements from the operating system. For runtime environment metrics see
[semantic conventions for runtime environment
metrics](runtime-environment-metrics.md).

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Metric Instruments](#metric-instruments)
  * [Process](#process)
- [Attributes](#attributes)

<!-- tocstop -->

## Metric Instruments

### Process

Below is a table of Process metric instruments.

| Name                            | Instrument Type ([\*](/specification/general/metrics-general.md#instrument-types)) | Unit      | Description                                                                                                                         | Labels                                                                                                                                                                                          |
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

Process metrics SHOULD be associated with a [`process`](/specification/resource/semantic_conventions/process.md#process) resource whose attributes provide additional context about the process.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
