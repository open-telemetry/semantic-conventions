# Service

<!-- semconv service(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `service.name` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Logical name of the service. [1] | `shoppingcart` |
| `service.version` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The version string of the service API or implementation. The format is not defined by these conventions. | `2.0.0`; `a01dbef8a` |

**[1]:** MUST be the same for all instances of horizontally scaled services. If the value was not specified, SDKs MUST fallback to `unknown_service:` concatenated with [`process.executable.name`](process.md#process), e.g. `unknown_service:bash`. If `process.executable.name` is not available, the value MUST be set to `unknown_service`.
<!-- endsemconv -->