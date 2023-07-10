# Deployment

**Status**: [Experimental][DocumentStatus]

**type:** `deployment`

**Description:** The software deployment.

<!-- semconv deployment -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `deployment.environment` | string | Name of the [deployment environment](https://en.wikipedia.org/wiki/Deployment_environment) (aka deployment tier). | `staging`; `production` | Recommended |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
