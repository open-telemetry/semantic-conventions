<!--- Hugo front matter used to generate the website version of this page:
linkTitle: URL
--->

# Semantic conventions for URL

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for url.

* [Attributes](../registry/attributes/url.md)

## Sensitive information

Capturing URL and its components MAY impose security risk. User and password information, when they are provided in [User Information](https://datatracker.ietf.org/doc/html/rfc3986#section-3.2.1) subcomponent, MUST NOT be recorded.

Instrumentations that are aware of specific sensitive query string parameters MUST scrub their values before capturing `url.query` attribute. For example, native instrumentation of a client library that passes credentials or user location in URL, must scrub corresponding properties.

_Note: Applications and telemetry consumers should scrub sensitive information from URL attributes on collected telemetry. In systems unable to identify sensitive information, certain attribute values may be redacted entirely._

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
