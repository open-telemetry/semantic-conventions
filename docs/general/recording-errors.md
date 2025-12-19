# Recording errors

**Status**: [Development][DocumentStatus].

<!-- toc -->

- [What constitutes an error](#what-constitutes-an-error)
- [What constitutes a failed operation](#what-constitutes-a-failed-operation)
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

## What constitutes a failed operation

An operation SHOULD be considered as failed when it ends with an error.

Errors that were retried or handled (allowing an operation to complete gracefully)
SHOULD NOT be recorded on spans or metrics that describe this operation.

## Recording errors

Instrumentation SHOULD ensure that, for a given error, the same value is
used as the [`error.type`][ErrorType] attribute on spans and metrics, and as
[`EventName`][EventName] on logs.

## Recording errors on spans

When the instrumented operation failed, the instrumentation:

- SHOULD set the span status code to `Error`,
- SHOULD set the [`error.type`][ErrorType] attribute,
- SHOULD set the span status description when it has additional information
  about the error that aligns with [Span Status Description][SpanStatus]
  definition, for example, an exception message.

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

When recording an error using logs:

- MUST set [`EventName`][EventName] with a value that would normally be
  used for an [`error.type`][ErrorType] attribute.
- SHOULD set [`error.message`][ErrorMessage] attribute to add additional
  information about the error, for example, an exception message.

When an error is retried or handled and the overall operation completes successfully,
it SHOULD still be recorded as an event record for diagnostic purposes.
In such scenario, [`SeverityNumber`][SeverityNumber] MUST be below 17 (ERROR).

When an error occurs outside the context of any span
and it causes an operation to fail,
the instrumentation SHOULD record it as an event record.
In such scenario, [`SeverityNumber`][SeverityNumber] MUST be greater than
or equal to 17 (ERROR).

When an error occurs inside the context of a span
and it causes an operation to fail,
the instrumentation SHOULD NOT additionally record it as an event record.

> [!NOTE]
>
> Applications that also want error event records corresponding to spans
> that already record errors can use a span processor (or equivalent component)
> that emits error logs for such spans. This is an optional, user-configured
> mechanism and is not required by these conventions.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
[SpanStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/trace/api.md#set-status
[RecordException]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/trace/api.md#record-exception
[ErrorType]: /docs/registry/attributes/error.md#error-type
[ErrorMessage]: /docs/registry/attributes/error.md#error-message
[EventName]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/logs/data-model.md#field-eventname
[SeverityNumber]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.52.0/specification/logs/data-model.md#field-severitynumber
