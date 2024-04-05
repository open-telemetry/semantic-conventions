# Deployment

## Deployment Attributes
<!-- semconv registry.deployment(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `deployment.environment` | string | Name of the [deployment environment](https://wikipedia.org/wiki/Deployment_environment) (aka deployment tier). [1] | `staging`; `production` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** `deployment.environment` does not affect the uniqueness constraints defined through
the `service.namespace`, `service.name` and `service.instance.id` resource attributes.
This implies that resources carrying the following attribute combinations MUST be
considered to be identifying the same service:

* `service.name=frontend`, `deployment.environment=production`
* `service.name=frontend`, `deployment.environment=staging`.
<!-- endsemconv -->
