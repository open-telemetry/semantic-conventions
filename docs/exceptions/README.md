<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Exceptions
path_base_for_github_subdir:
  from: tmp/semconv/docs/exceptions/_index.md
  to: exceptions/README.md
--->

# Semantic Conventions for Exceptions

**Status**: [Stable][DocumentStatus], Unless otherwise specified.

Semantic conventions for Exceptions are defined for the following signals:

* [Exceptions on spans](exceptions-spans.md): Semantic Conventions for Exceptions associated with *spans*.
* [Exceptions in logs](exceptions-logs.md): Semantic Conventions for Exceptions recorded in *logs*.

## Reporting errors in instrumentation code

**Status**: [Development][DocumentStatus]

When instrumented operation fails with an exception, instrumentation SHOULD record
this exception as a [span event](exceptions-spans.md) or a [log record](exceptions-logs.md).

It's NOT RECOMMENDED to record exceptions that are handled by the instrumented library.

It's RECOMMENDED to use `Span.recordException` API or logging library API that takes exception instance
instead of providing individual attributes. This enables the OpenTelemetry SDK to
control what information is recorded based on user configuration.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
