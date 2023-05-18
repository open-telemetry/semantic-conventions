# Container

**Status**: [Experimental][DocumentStatus]

**type:** `container`

**Description:** A container instance.

<!-- semconv container -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `container.name` | string | Container name used by container runtime. | `opentelemetry-autoconf` | Recommended |
| `container.id` | string | Container ID. Usually a UUID, as for example used to [identify Docker containers](https://docs.docker.com/engine/reference/run/#container-identification). The UUID might be abbreviated. | `a3bf90e006b2` | Recommended |
| `container.runtime` | string | The container runtime managing this container. | `docker`; `containerd`; `rkt` | Recommended |
| `container.image.name` | string | Name of the image the container was built on. | `gcr.io/opentelemetry/operator` | Recommended |
| `container.image.tag` | string | Container image tag. | `0.1` | Recommended |
| `container.image.id` | string | The ID of the container image. Usually a hash algorithm followed by a UUID. The UUID might be abbreviated. | `sha256:f90d814248a0` | Recommended |
| `container.command` | string | The command used to run the container (i.e. the command name). | `otelcontribcol` | Recommended |
| `container.command_line` | string | The full command run by the container as a single string representing the full command. It is recommended to remove embedded credentials or sensitive data to prevent potential leakage. | `otelcontribcol --config config.yaml` | Recommended |
| `container.command_args` | string[] | All the command arguments (including the command/executable itself) run by the container. It is recommended to remove embedded credentials or sensitive data to prevent potential leakage. | `[otelcontribcol, --config, config.yaml]` | Recommended |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
