<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Container
--->

# Semantic Conventions for Container Metrics

**Status**: [Experimental][DocumentStatus]

## Container Metrics

### Metric: `container.cpu.utilization`

This metric is optional.

<!-- semconv metric.container.cpu.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.cpu.time` | Counter | `ns` | Total CPU time consumed [1] |

**[1]:** Total CPU time consumed by the specific container.
<!-- endsemconv -->

<!-- semconv metric.container.cpu.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `container.cpu.state` | string | The state of the CPU | `user`; `kernel` | Opt-In |
| [`container.id`](../attributes-registry/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |

`container.cpu.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `user` | user |
| `system` | system |
| `kernel` | kernel |
<!-- endsemconv -->

### Metric: `container.memory.utilization`

This metric is optional.

<!-- semconv metric.container.memory.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.memory.usage` | Counter | `By` | Memory usage of the container. [1] |

**[1]:** Memory usage of the container.
<!-- endsemconv -->

<!-- semconv metric.container.memory.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../attributes-registry/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
<!-- endsemconv -->

### Metric: `container.disk.io`

This metric is optional.

<!-- semconv metric.container.disk.io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.disk.io` | Counter | `By` | Disk bytes for the container. [1] |

**[1]:** The total number of bytes read/written successfully (aggregated from all disks).
<!-- endsemconv -->

<!-- semconv metric.container.disk.io(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../attributes-registry/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| [`disk.io.direction`](../attributes-registry/disk.md) | string | The disk IO operation direction. | `read` | Recommended |

`disk.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `read` | read |
| `write` | write |
<!-- endsemconv -->

### Metric: `container.network.io`

This metric is optional.

<!-- semconv metric.container.network.io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.network.io` | Counter | `By` | Network bytes for the container. [1] |

**[1]:** The number of bytes sent/received on all network interfaces by the container.
<!-- endsemconv -->

<!-- semconv metric.container.network.io(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../attributes-registry/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| [`network.io.direction`](../attributes-registry/network.md) | string | The network IO operation direction. | `transmit` | Recommended |

`network.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `transmit` | transmit |
| `receive` | receive |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
