<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Recording errors
--->

# Recording errors

**Status**: [Development][DocumentStatus].

This document provides recommendations to semantic convention and instrumentation authors
on how to record errors on spans and metrics.

Individual semantic conventions are encouraged to provide additional guidance.

## What constitutes an error

An operation SHOULD be considered as failed if any of the following is true:

- an exception is thrown by the instrumented method (API, block of code, or another instrumented unit)
- the instrumented method returns an error in another way, for example, via an error code

  Semantic conventions that define domain-specific status codes SHOULD specify
  which status codes should be reported as errors by a general-purpose instrumentation.

> [!NOTE]
>
> The classification of a status code as an error depends on the context.
> For example, an HTTP 404 "Not Found" status code indicates an error if the application
> expected the resource to be available. However, it is not an error when the
> application is simply checking whether the resource exists.
>
> Instrumentations that have additional context about a specific request MAY use
> this context to set the span status more precisely.

Errors that were retried or handled (allowing an operation to complete gracefully) SHOULD NOT
be recorded on spans or metrics that describe this operation.

## How to record errors on spans

[Span Status Code][SpanStatus] MUST be left unset if the instrumented operation has
ended without any errors.

When the operation ends with an error, instrumentation:

- SHOULD set the span status code to `Error`
- SHOULD set the [`error.type`](/docs/attributes-registry/error.md#error-type) attribute
- SHOULD set the span status description when it has additional information
  about the error which is not expected to contain sensitive details and aligns
  with [Span Status Description][SpanStatus] definition.

  It's NOT RECOMMENDED to duplicate status code or `error.type` in span status description.

  When the operation fails with an exception, the span status description SHOULD be set to
  the exception message.

Refer to the [general exception guidance](/docs/exceptions/README.md) on capturing exception
details.

## How to record errors on metrics

Semantic conventions for operations usually define an operation duration histogram
metric. This metric SHOULD include the `error.type` attribute. This enables users to derive
throughput and error rates.

Operations that complete successfully SHOULD NOT include the `error.type` attribute,
allowing users to filter out errors.

Semantic conventions SHOULD include `error.type` on other metrics when it's applicable.
For example, `messaging.client.sent.messages` metric measures message throughput (one
messaging operation may involve sending multiple messages) and includes `error.type`.

It's RECOMMENDED to report one metric that includes successes and failures as opposed
to reporting two (or more) metrics depending on the operation status.

Instrumentation SHOULD ensure `error.type` is applied consistently across spans
and metrics when both are reported. A span and its corresponding metric for a single
operation SHOULD have the same `error.type` value if the operation failed and SHOULD NOT
include it if the operation succeeded.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
[SpanStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.39.0/specification/trace/api.md#set-status
