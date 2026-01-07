# Recording errors

**Status**: [Development][DocumentStatus].

<!-- toc -->

- [What constitutes an error](#what-constitutes-an-error)
- [Recording errors](#recording-errors)
- [Recording errors on spans](#recording-errors-on-spans)
- [Recording errors on metrics](#recording-errors-on-metrics)
- [Recording errors on logs](#recording-errors-on-logs)

<!-- tocstop -->

This document provides recommendations to semantic convention
and instrumentation authors on how to record errors on spans, metrics, and logs.

Individual semantic conventions are encouraged to provide additional guidance.

## What constitutes an error

In the scope of this document, an error occurs when:

- an exception is thrown by an instrumented operation,
- the instrumented operation returns an error in another way,
  for example, via an error object or status code.

> [!NOTE]
>
> The classification of a status code as an error depends on the context.
> For example, an HTTP 404 "Not Found" status code indicates an error if the application
> expected the resource to be available. However, it is not an error when the
> application is simply checking whether the resource exists.
>
> Instrumentations that have additional context about a specific request SHOULD
> use this context to classify whether the status code is an error.

## Recording errors

Instrumentation SHOULD ensure that, for a given error,
the same [`error.type`][ErrorType] attribute value is used across all signals.

## Recording errors on spans

When the instrumented operation ends with an error, the instrumentation:

- SHOULD set the span status code to `Error` if this is an operation error
  according to semantics, for example, see
  [Semantic conventions for HTTP spans: Status](../http/http-spans.md#status),
- SHOULD set the [`error.type`][ErrorType] attribute,
- SHOULD set [`error.message`][ErrorMessage] attribute to add additional
  information about the error, for example, an exception message,
- SHOULD set the `error.stacktrace` attribute.

Note that [Span Status Code][SpanStatus] MUST be left unset if the instrumented
operation has ended without any errors.

It is NOT RECOMMENDED to record the error via a span event,
for example, by using [`Span.RecordException`][RecordException].

## Recording errors on metrics

Semantic conventions for operations usually define an operation duration histogram
metric. This metric SHOULD include the [`error.type`][ErrorType] attribute.
This enables users to derive throughput and error rates.

Operations that complete successfully SHOULD NOT include the `error.type` attribute,
allowing users to filter out errors.

Semantic conventions SHOULD include `error.type` on other metrics when it's applicable.
For example, `messaging.client.sent.messages` metric measures message throughput (one
messaging operation may involve sending multiple messages) and includes `error.type`.

It's RECOMMENDED to report one metric that includes successes and failures as opposed
to reporting two (or more) metrics depending on the operation status.

## Recording errors on logs

When recording an error using logs ([event records][EventRecord]):

- SHOULD set [`EventName`][EventName] with a value that help indicating
  what operation failed, e.g. `socket.connection_failed`,
- SHOULD set [`SeverityNumber`][SeverityNumber],
  but not necessarily at the ERROR severity level.
  Errors that were retried or handled (allowing an operation to complete gracefully)
  SHOULD NOT be recorded with the ERROR severity level (or higher).
  For example, an error on an operation may be a DEBUG event if the operation is
  retried, and if the failure is not generally relevant to the application owner.
- SHOULD set the [`error.type`][ErrorType] attribute,
- SHOULD set [`error.message`][ErrorMessage] attribute to add additional
  information about the error, for example, an exception message,
- SHOULD set the `error.stacktrace` attribute.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
[SpanStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/trace/api.md#set-status
[RecordException]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/trace/api.md#record-exception
[ErrorType]: /docs/registry/attributes/error.md#error-type
[ErrorMessage]: /docs/registry/attributes/error.md#error-message
[EventRecord]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/logs/data-model.md#log-and-event-record-definition
[EventName]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/logs/data-model.md#field-eventname
[SeverityNumber]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/logs/data-model.md#field-severitynumber
