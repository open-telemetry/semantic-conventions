<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Container
--->

# Semantic Conventions for Container Metrics

**Status**: [Experimental][DocumentStatus]

## Container Metrics

### Metric: `container.cpu.usage`

This metric is optional.

<!-- semconv metric.container.cpu.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.cpu.usage` | Gauge | `1` | Recent CPU utilization for the container. [1] |

**[1]:** CPU usage percentage normalized by the number of CPU cores. The value range is [0.0,1.0].
<!-- endsemconv -->

<!-- semconv metric.container.cpu.usage(full) -->
<!-- endsemconv -->

### Metric: `container.memory.usage`

This metric is optional.

<!-- semconv metric.container.memory.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.memory.usage` | Gauge | `1` | Recent memory utilization for the container. [1] |

**[1]:** Memory usage percentage. The value range is [0.0,1.0].
<!-- endsemconv -->

<!-- semconv metric.container.memory.usage(full) -->
<!-- endsemconv -->

### Metric: `container.disk.read.bytes`

This metric is optional.

<!-- semconv metric.container.disk.read.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.disk.read.bytes` | Counter | `By` | Disk read bytes for the container. [1] |

**[1]:** The total number of bytes read successfully (aggregated from all disks).
<!-- endsemconv -->

<!-- semconv metric.container.disk.read.bytes(full) -->
<!-- endsemconv -->

### Metric: `container.disk.write.bytes`

This metric is optional.

<!-- semconv metric.container.disk.write.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.disk.write.bytes` | Counter | `By` | Disk write bytes for the container. [1] |

**[1]:** The total number of bytes written successfully (aggregated from all disks).
<!-- endsemconv -->

<!-- semconv metric.container.disk.write.bytes(full) -->
<!-- endsemconv -->

### Metric: `container.network.ingress.bytes`

This metric is optional.

<!-- semconv metric.container.network.ingress.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.network.ingress.bytes` | Counter | `By` | Network ingress bytes for the container. [1] |

**[1]:** The number of bytes received on all network interfaces by the container.
<!-- endsemconv -->

<!-- semconv metric.container.network.ingress.bytes(full) -->
<!-- endsemconv -->

### Metric: `container.network.egress.bytes`

This metric is optional.

<!-- semconv metric.container.network.egress.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.network.egress.bytes` | Counter | `By` | Network egress bytes for the container. [1] |

**[1]:** The number of bytes sent out on all network interfaces by the container.
<!-- endsemconv -->

<!-- semconv metric.container.network.egress.bytes(full) -->
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
