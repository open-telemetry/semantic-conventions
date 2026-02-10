<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Logs
--->

# Semantic conventions for exceptions in logs

**Status**: [Stable, except where otherwise specified][DocumentStatus]

This document defines semantic conventions for recording exceptions on
[logs](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/api.md#emit-a-logrecord)
emitted through the [Logger API](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/api.md#logger).

<!-- toc -->

- [Recording an exception](#recording-an-exception)
  - [Event name considerations](#event-name-considerations)
  - [Severity considerations](#severity-considerations)
    - [Fatal severity](#fatal-severity)
    - [Error severity](#error-severity)
    - [Warn and below severity](#warn-and-below-severity)
  - [Attributes](#attributes)
  - [Stacktrace representation](#stacktrace-representation)

<!-- tocstop -->

## Recording an exception

Exceptions SHOULD be recorded as attributes on the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/data-model.md#log-and-event-record-definition) passed to the [Logger](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/api.md#logger) emit
operations. Exceptions MAY be recorded on "logs" or "events" depending on the
context.

To encapsulate proper handling of exceptions API authors MAY provide a
constructor, `RecordException` method/extension, or similar helper mechanism on
the `LogRecord` class/structure or wherever it makes the most sense depending on
the language runtime.

![Development](https://img.shields.io/badge/-development-blue) Instrumentations SHOULD record exception information along with relevant context.
If no context beyond the exception instance is available to the instrumentation,
it's RECOMMENDED to record exception details on the log record (without providing an event name).

![Development](https://img.shields.io/badge/-development-blue) OpenTelemetry instrumentations
that emit events SHOULD document them including the event name and any additional
attributes that provide the context in which the exception has happened.

### Event name considerations

**Status**: [Development][DocumentStatus]

Events contain a unique [name](/docs/general/events.md) that describes
that specific class of events.

It is RECOMMENDED to use a specific event name that identifies the error category,
and NOT RECOMMENDED to use a generic name such as `exception`.

For example, when recording an exception that occurs during an HTTP client request
and prevents the request from completing successfully, use the `http.client.exception`
event name instead of a generic exception or error, or leaving the event name
unspecified.

### Severity considerations

**Status**: [Development][DocumentStatus]

[Severity Number](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/data-model.md#field-severitynumber)
SHOULD be provided on all exception log records (including events) and SHOULD be
set depending on the available context.

#### Fatal severity

Exceptions that usually result in application shutdown SHOULD be recorded with severity `Fatal`.

Examples:

- The application detects an invalid configuration at startup and shuts down.
- The application encounters a (presumably) terminal error, such as an out-of-memory condition.

#### Error severity

Unhandled (by the application code) exceptions that don't result in application
shutdown SHOULD be recorded with severity `Error`.

These exceptions are not expected and may indicate a bug in the application code
or a gap in the error handling logic.

Examples:

- A background job terminates with an exception.
- An HTTP framework error handler catches an exception not handled by the application
  code.

  Note: Some frameworks use exceptions as a communication mechanism when a request fails. For example,
  Spring users can throw a [ResponseStatusException](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/server/ResponseStatusException.html)
  exception to return an unsuccessful status code. Such exceptions represent errors
  already handled by the application code.
  Instrumentations for such components, when they can reliably detect
  that the exception was handled, SHOULD use `Warn` or lower severity (if they emit logs
  for this exception at all).

#### Warn and below severity

Exceptions that don't qualify for [`Fatal`](#fatal-severity) or [`Error`](#error-severity)
severity SHOULD be reported at `Warn` severity or below.

Errors that are expected to be retried or handled by the caller or another
layer of the component SHOULD be recorded with severity not higher than `Warn`.

Such errors represent transient failures that are common and expected in
distributed applications. They typically increase the latency of individual
operations and have a minor impact on overall application availability.

Examples:

- An attempt to connect to the required remote dependency times out.
- A remote dependency returns a 401 "Unauthorized" response code.
- Writing data to a file results in an IO exception.
- A remote dependency returned a 503 "Service Unavailable" response for 5 consecutive times;
  retry attempts are exhausted, and the corresponding operation has failed.

Errors that don't indicate actual issues SHOULD be recorded with
severity not higher than `Info`.

Such errors can be used to control application logic and have a minor impact, if any,
on application functionality, availability, or performance (beyond the performance hit introduced
if an exception is used to control application logic).

Examples:

- An error is returned when checking for an optional dependency or resource existence.
- An exception is thrown on the server when the client disconnects before reading
  the full response from the server.

### Attributes

The table below indicates which attributes should be added to the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/data-model.md#log-and-event-record-definition).

![Development](https://img.shields.io/badge/-development-blue) When recording exceptions, instrumentations are encouraged to add more attributes
to describe the context in which the exception occurred.

<!-- semconv log-exception -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`exception.message`](/docs/registry/attributes/exception.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [1] | string | The exception message. | `Division by zero`; `Can't convert 'int' object to str implicitly` |
| [`exception.type`](/docs/registry/attributes/exception.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [2] | string | The type of the exception (its fully-qualified class name, if applicable). The dynamic type of the exception should be preferred over the static type in languages that support it. | `java.net.ConnectException`; `OSError` |
| [`exception.stacktrace`](/docs/registry/attributes/exception.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG. | `Exception in thread "main" java.lang.RuntimeException: Test exception\n at com.example.GenerateTrace.methodB(GenerateTrace.java:13)\n at com.example.GenerateTrace.methodA(GenerateTrace.java:9)\n at com.example.GenerateTrace.main(GenerateTrace.java:5)` |

**[1] `exception.message`:** Required if `exception.type` is not set, recommended otherwise.

**[2] `exception.type`:** Required if `exception.message` is not set, recommended otherwise.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Stacktrace representation

Same as [Trace Semantic Conventions for Exceptions - Stacktrace
Representation](exceptions-spans.md#stacktrace-representation).

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
