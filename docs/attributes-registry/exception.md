<!--- Hugo front matter used to generate the website version of this page:
--->

# Exceptions

## Exception Attributes

<!-- semconv registry.exception(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `exception.escaped` | boolean | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>SHOULD be set to true if the exception event is recorded at a point where it is known that the exception is escaping the scope of the span. [1] |  |
| `exception.message` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The exception message. | `Division by zero`; `Can't convert 'int' object to str implicitly` |
| `exception.stacktrace` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG. | `Exception in thread "main" java.lang.RuntimeException: Test exception\n at com.example.GenerateTrace.methodB(GenerateTrace.java:13)\n at com.example.GenerateTrace.methodA(GenerateTrace.java:9)\n at com.example.GenerateTrace.main(GenerateTrace.java:5)` |
| `exception.type` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The type of the exception (its fully-qualified class name, if applicable). The dynamic type of the exception should be preferred over the static type in languages that support it. | `java.net.ConnectException`; `OSError` |

**[1]:** An exception is considered to have escaped (or left) the scope of a span,
if that span is ended while the exception is still logically "in flight".
This may be actually "in flight" in some languages (e.g. if the exception
is passed to a Context manager's `__exit__` method in Python) but will
usually be caught at the point of recording the exception in most languages.

It is usually not possible to determine at the point where an exception is thrown
whether it will escape the scope of a span.
However, it is trivial to know that an exception
will escape, if one checks for an active exception just before ending the span,
as done in the [example for recording span exceptions](#recording-an-exception).

It follows that an exception may still escape the scope of the span
even if the `exception.escaped` attribute was not set or set to false,
since the event might have been recorded at a time where it was not
clear whether the exception will escape.
<!-- endsemconv -->

### Recording An Exception

The `exception.escaped` attribute has special semantics in the context of
a span. Please read the [details here](../exceptions/exceptions-spans.md#recording-an-exception).
