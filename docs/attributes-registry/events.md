<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
aliases: [docs/specs/semconv/general/events-general]
--->

# Semantic Conventions for Event Attributes

<!-- semconv registry.event -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `event.domain` | string | The domain identifies the business context for the events. [1] | `browser` | Recommended |
| `event.name` | string | The name identifies the event. | `click`; `exception` | Recommended |

**[1]:** Events across different domains may have same `event.name`, yet be unrelated events.

`event.domain` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `browser` | Events from browser apps |
| `device` | Events from mobile apps |
| `k8s` | Events from Kubernetes |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
