<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Trace
aliases: [trace-general]
--->

# Trace semantic conventions

**Status**: [Mixed][DocumentStatus]

In OpenTelemetry spans can be created freely and it’s up to the implementer to
annotate them with attributes specific to the represented operation. Spans
represent specific operations in and between systems. Some of these operations
represent calls that use well-known protocols like HTTP or database calls.
Depending on the protocol and the type of operation, additional information
is needed to represent and analyze a span correctly in monitoring systems. It is
also important to unify how this attribution is made in different languages.
This way, the operator will not need to learn specifics of a language and
telemetry collected from polyglot (multi-language) micro-service environments
can still be easily correlated and cross-analyzed.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
