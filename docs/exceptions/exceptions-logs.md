<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Logs
--->

# Semantic conventions for exceptions in logs

**Status**: [Stable, except where otherwise specified][DocumentStatus]

This document defines semantic conventions for recording exceptions on
[logs](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.55.0/specification/logs/api.md#emit-a-logrecord)
emitted through the [Logger API](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.55.0/specification/logs/api.md#logger).

<!-- toc -->

- [Recording an exception](#recording-an-exception)
  - [When not to record exceptions](#when-not-to-record-exceptions)
  - [Event name](#event-name)
  - [Severity](#severity)
    - [FATAL severity](#fatal-severity)
    - [ERROR severity](#error-severity)
    - [WARN severity](#warn-severity)
    - [INFO severity](#info-severity)
    - [DEBUG severity](#debug-severity)
    - [TRACE severity](#trace-severity)
  - [Attributes](#attributes)
  - [Stacktrace representation](#stacktrace-representation)

<!-- tocstop -->

> [!IMPORTANT]
>
> Existing instrumentations that record exceptions as span events:
>
> * SHOULD introduce an environment variable `OTEL_SEMCONV_EXCEPTION_SIGNAL_OPT_IN`
>   supporting the following values:
>   * `logs` - emit exceptions as logs only.
>   * `logs/dup` - emit both span events and logs, allowing for a phased rollout.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting exceptions as span events (existing behavior).
> * SHOULD maintain (security patching at a minimum) their existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * MAY drop the environment variable in their next major version and emit exceptions
>   as logs only.
>
> Even after instrumentations start emitting exceptions only as logs, users will
> still have the option to route those to span events at the SDK layer.

## Recording an exception

> [!NOTE]
> This document describes how exception events should be recorded and when to avoid
> recording them. Guidance on when to record exceptions is left to specific
> semantic conventions authors.

OpenTelemetry Semantic Conventions authors SHOULD define exception events according
to this document.
This guidance is also recommended for application developers and instrumentations
not hosted in OpenTelemetry.
This document does not apply to logging bridges.

Exceptions SHOULD be recorded as attributes on the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.55.0/specification/logs/data-model.md#log-and-event-record-definition) passed to the [Logger](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.55.0/specification/logs/api.md#logger) emit
operations.

Exception events emitted by instrumentations that also record spans for the same
operation MUST be associated with the corresponding span context.

When language implementations support passing exception instances to the
[Emit a LogRecord](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.55.0/specification/logs/api.md#emit-a-logrecord) API, instrumentations SHOULD provide the exception instance
rather than manually setting individual exception attributes.

![Development](https://img.shields.io/badge/-development-blue) Instrumentations
SHOULD record exceptions as events.

### When not to record exceptions

**Status**: [Development][DocumentStatus]

Some libraries, frameworks, or runtimes generate artificial exceptions for
operations that end with an unsuccessful error code. When possible,
instrumentations SHOULD NOT record these artificial exceptions.

For example, FastAPI in Python recommends raising [`HTTPException`](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception)
instead of returning a response with an unsuccessful status
code. Similarly, Spring in Java provides [`ResponseStatusException`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/server/ResponseStatusException.html).

### Event name

**Status**: [Development][DocumentStatus]

It is RECOMMENDED to provide an [event name](/docs/general/events.md) that
describes the instrumented operation with a `.exception` suffix.

For example, [`http.client.request.exception`](/docs/http/http-exceptions.md#http-client-request-exception)
represents exceptions that occur during an HTTP client request.

Instrumentations that are not specific to a particular operation or domain, such as
global unhandled exception handlers, SHOULD use the `exception` event name.

### Severity

**Status**: [Development][DocumentStatus]

The severity reflects the expected impact of the exception, not just its presence.

[Severity Number](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.55.0/specification/logs/data-model.md#field-severitynumber)
SHOULD be provided on all exception events and SHOULD be set based on the context
in which the exception occurs, following the guidance below.

#### FATAL severity

Exceptions that usually result in application shutdown SHOULD be recorded with
severity `FATAL` (severity number 21).

Examples:

- The application detects an invalid configuration at startup and shuts down.
- The application encounters an out-of-memory condition.

> [!NOTE]
> Instrumentation SHOULD do the best effort to record such errors, but
> OpenTelemetry SDK and exporters might not have a chance to actually export them.

#### ERROR severity

Exceptions that are unhandled by application code and don't result in application
shutdown SHOULD be recorded with severity `ERROR` (severity number 17).

Semantic conventions that define `SERVER` or `CONSUMER` spans SHOULD also define
a corresponding exception event and recommend using `ERROR` severity.

Examples:

- A messaging consumer terminates message processing with an exception.
- An HTTP server framework error handler catches an exception not handled by the
  application code.

#### WARN severity

Exceptions that are expected to be handled by application code SHOULD be
reported with severity `WARN` (severity number 13).

Semantic conventions that define `CLIENT` or `PRODUCER` spans SHOULD also define
a corresponding exception event and recommend using `WARN` severity.

Examples:

- A connection attempt to a remote service times out.
- Writing data to a file results in an I/O exception.
- A client library call fails after exhausting retries because the underlying
  service is unavailable. The client library instrumentation records a single
  WARN log; logging of individual retry attempts is left to the lower-level
  instrumentation.

#### INFO severity

Application developers may use `INFO` severity (number 9) to record exceptions.

#### DEBUG severity

Exceptions that don't indicate an actual issue SHOULD be recorded with severity
`DEBUG` (severity number 5).

For example, an exception indicating that a request was cancelled on the client
side is thrown on the server and detected by the server instrumentation.

#### TRACE severity

Application developers may use `TRACE` severity (number 1) to record exceptions.
Semantic conventions authors SHOULD NOT define exception events with `TRACE`
severity.

### Attributes

The table below indicates which attributes should be added to the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.55.0/specification/logs/data-model.md#log-and-event-record-definition).

![Development](https://img.shields.io/badge/-development-blue) Instrumentations MAY
provide additional attributes to describe the context in which the exception occurred.
Instrumentations that also record spans for the same operation MAY provide a
configuration option to populate exception events with attributes captured on
the corresponding span.

<!-- semconv log-exception -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`exception.message`](/docs/registry/attributes/exception.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [1] | string | The exception message. [2] | `Division by zero`; `Can't convert 'int' object to str implicitly` |
| [`exception.type`](/docs/registry/attributes/exception.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [3] | string | The type of the exception (its fully-qualified class name, if applicable). The dynamic type of the exception should be preferred over the static type in languages that support it. [4] | `java.net.ConnectException`; `OSError` |
| [`exception.stacktrace`](/docs/registry/attributes/exception.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG. | `Exception in thread "main" java.lang.RuntimeException: Test exception\n at com.example.GenerateTrace.methodB(GenerateTrace.java:13)\n at com.example.GenerateTrace.methodA(GenerateTrace.java:9)\n at com.example.GenerateTrace.main(GenerateTrace.java:5)` |

**[1] `exception.message`:** Required if `exception.type` is not set, recommended otherwise.

**[2] `exception.message`:**

> [!WARNING]
>
> This attribute may contain sensitive information.

**[3] `exception.type`:** Required if `exception.message` is not set, recommended otherwise.

**[4] `exception.type`:** If the recorded exception type is a wrapper that is not meaningful for
failure classification, instrumentation MAY use the type of the inner
exception instead. For example, in Go, errors created with `fmt.Errorf`
using `%w` MAY be unwrapped when the wrapper type does not help
classify the failure.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Stacktrace representation

Same as [Trace Semantic Conventions for Exceptions - Stacktrace
Representation](exceptions-spans.md#stacktrace-representation).

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
