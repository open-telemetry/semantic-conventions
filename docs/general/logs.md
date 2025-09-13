<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Logs
aliases: [logs-general]
--->

# General logs attributes

**Status**: [Development][DocumentStatus]

The attributes described in this section are rather generic.
They may be used in any Log Record they apply to.

The following semantic conventions for logs are defined:

* [Exceptions](/docs/exceptions/exceptions-logs.md): Semantic attributes that may be used in describing exceptions in logs.
* [Feature Flags](/docs/feature-flags/feature-flags-logs.md): Semantic attributes that may be used in describing feature flag evaluations in logs.

Apart from semantic conventions for logs, [events](events.md), [traces](trace.md), and [metrics](metrics.md),
OpenTelemetry also defines the concept of overarching [Resources](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.48.0/specification/resource/sdk.md) with their own
[Resource Semantic Conventions](/docs/resource/README.md).

## Useful Additional Attribute Namespaces

There are some attribute namespaces which can be used to provide additional context and
are not specific to a particular domain. Such as:

* [Code](/docs/registry/attributes/code.md)
* [Feature Flag](/docs/registry/attributes/feature-flag.md)
* [Log](/docs/registry/attributes/log.md)
* [Peer](/docs/registry/attributes/peer.md)
* [Thread](/docs/registry/attributes/thread.md)

These attributes can be used anywhere they would be useful and apply, with the log namespace particularly useful for describing the transmission of the log messages.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
