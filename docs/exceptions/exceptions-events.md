<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
--->

# Semantic Conventions for Exceptions in Logs

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for recording exceptions on
[events](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/logs/event-api.md#emit-event)
emitted through the [EventLogger](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/event-api.md#eventlogger) API.


<!-- toc -->

- [Recording an Exception](#recording-an-exception)
- [Attributes](#attributes)
  - [Stacktrace Representation](#stacktrace-representation)

<!-- tocstop -->

## Recording an Exception Event

Exception events MUST be recorded using the event name `exception`. 


## Attributes

The table below indicates which attributes should be added to the event and their types.

<!-- semconv log-exception -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`exception.message`](../attributes-registry/exception.md) | string | The exception message. | `Division by zero`; `Can't convert 'int' object to str implicitly` | `Conditionally Required` [1] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`exception.type`](../attributes-registry/exception.md) | string | The type of the exception (its fully-qualified class name, if applicable). The dynamic type of the exception should be preferred over the static type in languages that support it. | `java.net.ConnectException`; `OSError` | `Conditionally Required` [2] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`exception.stacktrace`](../attributes-registry/exception.md) | string | A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG. | `Exception in thread "main" java.lang.RuntimeException: Test exception\n at com.example.GenerateTrace.methodB(GenerateTrace.java:13)\n at com.example.GenerateTrace.methodA(GenerateTrace.java:9)\n at com.example.GenerateTrace.main(GenerateTrace.java:5)` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** Required if `exception.type` is not set, recommended otherwise.

**[2]:** Required if `exception.message` is not set, recommended otherwise.
<!-- endsemconv -->

### Stacktrace Representation

Same as [Trace Semantic Conventions for Exceptions - Stacktrace
Representation](exceptions-spans.md#stacktrace-representation).

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
