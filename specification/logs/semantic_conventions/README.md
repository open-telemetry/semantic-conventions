# Log Attribute Semantic Conventions

**Status**: [Experimental][DocumentStatus]

The following semantic conventions for logs are defined:

* [General](general.md): General semantic attributes that may be used in describing Log Records.
* [Log Media](media.md): Semantic attributes that may be used in describing the source of a log.

The following semantic conventions for events are defined:

* [Events](events.md): Semantic attributes that must be used to represent Events using log data model.

Apart from semantic conventions for logs, [traces](../../trace/semantic_conventions/README.md), and [metrics](../../metrics/semantic_conventions/README.md),
OpenTelemetry also defines the concept of overarching [Resources](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/resource/sdk.md) with their own
[Resource Semantic Conventions](../../resource/semantic_conventions/README.md).

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
