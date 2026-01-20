# Recording errors

**Status**: [Development][DocumentStatus].

<!-- toc -->

- [What constitutes an error](#what-constitutes-an-error)
- [Recording errors on spans](#recording-errors-on-spans)
- [Recording errors on metrics](#recording-errors-on-metrics)
- [Recording exceptions](#recording-exceptions)

<!-- tocstop -->

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

## Recording errors on spans

[Span Status Code][SpanStatus] MUST be left unset if the instrumented operation has
ended without any errors.

When the operation ends with an error, instrumentation:

- SHOULD set the span status code to `Error`
- SHOULD set the [`error.type`](/docs/registry/attributes/error.md#error-type) attribute
- SHOULD set the span status description when it has additional information
  about the error which is not expected to contain sensitive details and aligns
  with [Span Status Description][SpanStatus] definition.

  It's NOT RECOMMENDED to duplicate status code or `error.type` in span status description.

  When the operation fails with an exception, the span status description SHOULD be set to
  the exception message.

Refer to the [recording exceptions](#recording-exceptions) on capturing exception
details.

## Recording errors on metrics

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

## Recording exceptions

When an instrumented operation fails with an exception, instrumentation SHOULD record
this exception as a [span event](/docs/exceptions/exceptions-spans.md) or a [log record](/docs/exceptions/exceptions-logs.md).

It's RECOMMENDED to use the `Span.recordException` API or logging library API that takes exception instance
instead of providing individual attributes. This enables the OpenTelemetry SDK to
control what information is recorded based on application configuration.

It's NOT RECOMMENDED to record the same exception more than once.
It's NOT RECOMMENDED to record exceptions that are handled by the instrumented library.

For example, in this code-snippet, `ResourceAlreadyExistsException` is handled and the corresponding
native instrumentation should not record it. Exceptions which are propagated
to the caller should be recorded (or logged) once.

```java
public boolean createIfNotExists(String resourceId) throws IOException {
  Span span = startSpan();
  try {
    create(resourceId);
    return true;
  } catch (ResourceAlreadyExistsException e) {
    // not recording exception and not setting span status to error - exception is handled
    // but we can set attributes that capture additional details
    span.setAttribute(AttributeKey.stringKey("acme.resource.create.status"), "already_exists");
    return false;
  } catch (IOException e) {
    // recording exception here (assuming it was not recorded inside `create` method)
    span.recordException(e);
    // or
    // logger.warn(e);

    span.setAttribute(AttributeKey.stringKey("error.type"), e.getClass().getCanonicalName())
    span.setStatus(StatusCode.ERROR, e.getMessage());
    throw e;
  }
}
```

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
[SpanStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/trace/api.md#set-status
