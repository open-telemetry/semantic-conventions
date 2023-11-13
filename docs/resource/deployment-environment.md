# Deployment

**Status**: [Experimental][DocumentStatus]

**type:** `deployment`

**Description:** The software deployment.

<!-- semconv deployment -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `deployment.environment` | string | Name of the [deployment environment](https://wikipedia.org/wiki/Deployment_environment) (aka deployment tier). [1] | `staging`; `production` | Recommended |

**[1]:** `deployment.environment` does not affect the uniqueness constraints defined through
the `service.namespace`, `service.name` and `service.instance.id` resource attributes.
This implies that resources carrying the following attribute combinations MUST be
considered to be identifying the same service:

* `service.name=frontend`, `deployment.environment=production`
* `service.name=frontend`, `deployment.environment=staging`.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
