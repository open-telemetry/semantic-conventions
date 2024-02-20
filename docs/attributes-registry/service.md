# Service

<!-- semconv registry.service(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `service.instance.id` | string | The string ID of the service instance. [1] | `my-k8s-pod-deployment-1`; `627cc493-f310-47de-96bd-71410b7dec09` |
| `service.name` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Logical name of the service. [2] | `shoppingcart` |
| `service.namespace` | string | A namespace for `service.name`. [3] | `Shop` |
| `service.version` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The version string of the service API or implementation. The format is not defined by these conventions. | `2.0.0`; `a01dbef8a` |

**[1]:** MUST be unique for each instance of the same `service.namespace,service.name` pair (in other words `service.namespace,service.name,service.instance.id` triplet MUST be globally unique). The ID helps to distinguish instances of the same service that exist at the same time (e.g. instances of a horizontally scaled service). It is preferable for the ID to be persistent and stay the same for the lifetime of the service instance, however it is acceptable that the ID is ephemeral and changes during important lifetime events for the service (e.g. service restarts). If the service has no inherent unique ID that can be used as the value of this attribute it is recommended to generate a random Version 1 or Version 4 RFC 4122 UUID (services aiming for reproducible UUIDs may also use Version 5, see RFC 4122 for more recommendations).

**[2]:** MUST be the same for all instances of horizontally scaled services. If the value was not specified, SDKs MUST fallback to `unknown_service:` concatenated with [`process.executable.name`](process.md#process), e.g. `unknown_service:bash`. If `process.executable.name` is not available, the value MUST be set to `unknown_service`.

**[3]:** A string value having a meaning that helps to distinguish a group of services, for example the team name that owns a group of services. `service.name` is expected to be unique within the same namespace. If `service.namespace` is not specified in the Resource then `service.name` is expected to be unique for all services that have no explicit namespace defined (so the empty/unspecified namespace is simply one more valid namespace). Zero-length namespace string is assumed equal to unspecified namespace.
<!-- endsemconv -->