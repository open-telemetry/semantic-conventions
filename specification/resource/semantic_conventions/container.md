# Container

**Status**: [Experimental](../../document-status.md)

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
| `container.image.id` | string | Runtime specific image identifier. Usually a hash algorithm followed by a UUID. [1] | `sha256:19c92d0a00d1b66d897bceaa7319bee0dd38a10a851c60bcec9474aa3f01e50f` | Recommended |
| `container.command` | string | The command used to run the container (i.e. the command name). | `otelcontribcol` | Conditionally Required: [2] |
| `container.command_line` | string | The full command run by the container as a single string representing the full command. | `otelcontribcol --config config.yaml` | Conditionally Required: [2] |
| `container.command_args` | string[] | All the command arguments (including the command/executable itself) run by the container. | `[otelcontribcol, --config, config.yaml]` | Conditionally Required: [2] |

**[1]:** On docker, `image.id` corresponds to the `Image` field from the Docker container inspect [API](https://docs.docker.com/engine/api/v1.43/#tag/Container/operation/ContainerInspect) endpoint.

**[2]:** If using embedded credentials or sensitive data, it is recommended to remove them to prevent potential leakage.
<!-- endsemconv -->
