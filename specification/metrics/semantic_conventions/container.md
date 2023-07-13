<!--- Hugo front matter used to generate the website version of this page:
linkTitle: HTTP
--->

# Semantic Conventions for Container Metrics

**Status**: [Experimental][DocumentStatus]

## HTTP Server

### Metric: `metric.container.cpu.usage`

This metric is optional.

<!-- semconv metric.container.cpu.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.cpu.usage` | Gauge | `1` | Recent CPU utilization for the container. |
<!-- endsemconv -->

<!-- semconv metric.container.cpu.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../../resource/semantic_conventions/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| [`container.image.name`](../../resource/semantic_conventions/container.md) | string | Name of the image the container was built on. | `gcr.io/opentelemetry/operator` | Recommended |
| [`container.image.tag`](../../resource/semantic_conventions/container.md) | string | Container image tag. | `0.1` | Recommended |
| [`container.name`](../../resource/semantic_conventions/container.md) | string | Container name used by container runtime. | `opentelemetry-autoconf` | Recommended |
| [`container.runtime`](../../resource/semantic_conventions/container.md) | string | The container runtime managing this container. | `docker`; `containerd`; `rkt` | Recommended |
<!-- endsemconv -->

### Metric: `metric.container.memory.usage`

This metric is optional.

<!-- semconv metric.container.memory.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.memory.usage` | Gauge | `1` | Recent memory utilization for the container. |
<!-- endsemconv -->

<!-- semconv metric.container.memory.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../../resource/semantic_conventions/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| [`container.image.name`](../../resource/semantic_conventions/container.md) | string | Name of the image the container was built on. | `gcr.io/opentelemetry/operator` | Recommended |
| [`container.image.tag`](../../resource/semantic_conventions/container.md) | string | Container image tag. | `0.1` | Recommended |
| [`container.name`](../../resource/semantic_conventions/container.md) | string | Container name used by container runtime. | `opentelemetry-autoconf` | Recommended |
| [`container.runtime`](../../resource/semantic_conventions/container.md) | string | The container runtime managing this container. | `docker`; `containerd`; `rkt` | Recommended |
<!-- endsemconv -->

### Metric: `metric.container.disk.read.bytes`

This metric is optional.

<!-- semconv metric.container.disk.read.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.disk.read.bytes` | Gauge | `By` | Disk read bytes for the container. |
<!-- endsemconv -->

<!-- semconv metric.container.disk.read.bytes(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../../resource/semantic_conventions/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| [`container.image.name`](../../resource/semantic_conventions/container.md) | string | Name of the image the container was built on. | `gcr.io/opentelemetry/operator` | Recommended |
| [`container.image.tag`](../../resource/semantic_conventions/container.md) | string | Container image tag. | `0.1` | Recommended |
| [`container.name`](../../resource/semantic_conventions/container.md) | string | Container name used by container runtime. | `opentelemetry-autoconf` | Recommended |
| [`container.runtime`](../../resource/semantic_conventions/container.md) | string | The container runtime managing this container. | `docker`; `containerd`; `rkt` | Recommended |
<!-- endsemconv -->

### Metric: `metric.container.disk.write.bytes`

This metric is optional.

<!-- semconv metric.container.disk.write.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.disk.write.bytes` | Gauge | `By` | Disk write bytes for the container. |
<!-- endsemconv -->

<!-- semconv metric.container.disk.write.bytes(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../../resource/semantic_conventions/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| [`container.image.name`](../../resource/semantic_conventions/container.md) | string | Name of the image the container was built on. | `gcr.io/opentelemetry/operator` | Recommended |
| [`container.image.tag`](../../resource/semantic_conventions/container.md) | string | Container image tag. | `0.1` | Recommended |
| [`container.name`](../../resource/semantic_conventions/container.md) | string | Container name used by container runtime. | `opentelemetry-autoconf` | Recommended |
| [`container.runtime`](../../resource/semantic_conventions/container.md) | string | The container runtime managing this container. | `docker`; `containerd`; `rkt` | Recommended |
<!-- endsemconv -->

### Metric: `metric.container.network.ingress.bytes`

This metric is optional.

<!-- semconv metric.container.network.ingress.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.network.ingress.bytes` | Gauge | `By` | Network ingress bytes for the container. |
<!-- endsemconv -->

<!-- semconv metric.container.network.ingress.bytes(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../../resource/semantic_conventions/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| [`container.image.name`](../../resource/semantic_conventions/container.md) | string | Name of the image the container was built on. | `gcr.io/opentelemetry/operator` | Recommended |
| [`container.image.tag`](../../resource/semantic_conventions/container.md) | string | Container image tag. | `0.1` | Recommended |
| [`container.name`](../../resource/semantic_conventions/container.md) | string | Container name used by container runtime. | `opentelemetry-autoconf` | Recommended |
| [`container.runtime`](../../resource/semantic_conventions/container.md) | string | The container runtime managing this container. | `docker`; `containerd`; `rkt` | Recommended |
<!-- endsemconv -->

### Metric: `metric.container.network.egress.bytes`

This metric is optional.

<!-- semconv metric.container.network.egress.bytes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `container.network.egress.bytes` | Gauge | `By` | Network egress bytes for the container. |
<!-- endsemconv -->

<!-- semconv metric.container.network.egress.bytes(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`container.id`](../../resource/semantic_conventions/container.md) | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| [`container.image.name`](../../resource/semantic_conventions/container.md) | string | Name of the image the container was built on. | `gcr.io/opentelemetry/operator` | Recommended |
| [`container.image.tag`](../../resource/semantic_conventions/container.md) | string | Container image tag. | `0.1` | Recommended |
| [`container.name`](../../resource/semantic_conventions/container.md) | string | Container name used by container runtime. | `opentelemetry-autoconf` | Recommended |
| [`container.runtime`](../../resource/semantic_conventions/container.md) | string | The container runtime managing this container. | `docker`; `containerd`; `rkt` | Recommended |
<!-- endsemconv -->