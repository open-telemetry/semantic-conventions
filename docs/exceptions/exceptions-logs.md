<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Logs
--->

# Semantic Conventions for Exceptions in Logs and Events

**Status**: [Stable][DocumentStatus]

This document defines semantic conventions for recording exceptions on
[logs](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/logs/bridge-api.md#emit-a-logrecord) emitted through the [Logger API](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/logs/bridge-api.md#logger) and [events](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/events.md) emitted through the [Events API](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/logs/event-api.md#emit-event)

<!-- toc -->

- [Recording an Exception in logs](#recording-an-exception-in-logs)
- [Recording an Exception in events](#recording-an-exception-in-events)
- [Attributes](#attributes)
  - [Stacktrace Representation](#stacktrace-representation)
- [Guidelines for Recording Exceptions in Spans, Logs, and Events](#guidelines-for-recording-exceptions-in-spans-logs-and-events)

<!-- tocstop -->

## Recording an Exception in logs

Exceptions SHOULD be recorded as attributes on the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/logs/data-model.md#log-and-event-record-definition) passed to the [Logger](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/logs/bridge-api.md#logger) emit
operations.

To encapsulate proper handling of exceptions API authors MAY provide a
constructor, `RecordException` method/extension, or similar helper mechanism on
the `LogRecord` class/structure or wherever it makes the most sense depending on
the language runtime.

## Recording an Exception in events

Exceptions SHOULD be recorded in Events with the event name `exception` and the exception data in attributes.

## Attributes

The table below indicates which attributes should be added to the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/logs/data-model.md#log-and-event-record-definition) for logs and events and their types.

<!-- semconv log-exception -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`exception.message`](/docs/attributes-registry/exception.md) | string | The exception message. | `Division by zero`; `Can't convert 'int' object to str implicitly` | `Conditionally Required` [1] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`exception.type`](/docs/attributes-registry/exception.md) | string | The type of the exception (its fully-qualified class name, if applicable). The dynamic type of the exception should be preferred over the static type in languages that support it. | `java.net.ConnectException`; `OSError` | `Conditionally Required` [2] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`exception.stacktrace`](/docs/attributes-registry/exception.md) | string | A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG. | `Exception in thread "main" java.lang.RuntimeException: Test exception\n at com.example.GenerateTrace.methodB(GenerateTrace.java:13)\n at com.example.GenerateTrace.methodA(GenerateTrace.java:9)\n at com.example.GenerateTrace.main(GenerateTrace.java:5)` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** Required if `exception.type` is not set, recommended otherwise.

**[2]:** Required if `exception.message` is not set, recommended otherwise.
<!-- endsemconv -->

### Stacktrace Representation

Same as [Trace Semantic Conventions for Exceptions - Stacktrace
Representation](exceptions-spans.md#stacktrace-representation).

## Guidelines for Recording Exceptions in Spans, Logs, and Events

When it comes to recording exceptions, it's crucial to distinguish between Spans, Logs, and Events:

* Spans and Events: Exception recording in Spans and Events follows a similar pattern. Both utilize the event name `exception`. Exceptions MAY be recorded within Span Events if they occur during the span's lifecycle.
* Logs: Exceptions SHOULD be recorded in logs when utilizing the log bridge API to map application logs to OpenTelemetry logs.

Note that in all cases the exception data is stored in attributes.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
