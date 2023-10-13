<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Container
--->

# Semantic Conventions for Container Metrics

**Status**: [Experimental][DocumentStatus]

## Container Metrics

### Metric: `container.cpu.utilization`

This metric is optional.

<!-- semconv metric.container.cpu.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.cpu.utilization` | Gauge | `1` | Recent CPU utilization for the container. [1] |

**[1]:** CPU usage percentage normalized by the number of CPU cores. The value range is [0.0,1.0].
<!-- endsemconv -->

<!-- semconv metric.container.cpu.utilization(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../resource/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
<!-- endsemconv -->

### Metric: `container.memory.utilization`

This metric is optional.

<!-- semconv metric.container.memory.utilization(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.memory.utilization` | Gauge | `1` | Recent memory utilization for the container. [1] |

**[1]:** Memory usage percentage. The value range is [0.0,1.0].
<!-- endsemconv -->

<!-- semconv metric.container.memory.utilization(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../resource/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
<!-- endsemconv -->

### Metric: `container.disk.io.bytes`

This metric is optional.

<!-- semconv metric.container.disk.io.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.disk.io.bytes` | Counter | `By` | Disk bytes for the container. [1] |

**[1]:** The total number of bytes read/written successfully (aggregated from all disks).
<!-- endsemconv -->

<!-- semconv metric.container.disk.io.bytes(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `container.disk.io.direction` | string | The disk IO operation's direction | `read`; `write` | Recommended |
| [`container.id`](../resource/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |

`container.disk.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `read` | read |
| `write` | write |
<!-- endsemconv -->

### Metric: `container.network.io.bytes`

This metric is optional.

<!-- semconv metric.container.network.io.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.disk.io.bytes` | Counter | `By` | Network bytes for the container. [1] |

**[1]:** The number of bytes sent/received on all network interfaces by the container.
<!-- endsemconv -->

<!-- semconv metric.container.network.io.bytes(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../resource/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| `container.network.io.direction` | string | The Network IO direction | `ingress`; `egress` | Recommended |

`container.network.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `ingress` | ingress |
| `egress` | egress |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
