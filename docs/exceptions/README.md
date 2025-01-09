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

## Reporting exceptions in instrumentation code

**Status**: [Development][DocumentStatus]

When instrumented operation fails with an exception, instrumentation SHOULD record
this exception as a [span event](exceptions-spans.md) or a [log record](exceptions-logs.md).

Recording exceptions on spans SHOULD be accompanied by
- setting span status to `ERROR`
- setting [`error.type`](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/attributes-registry/error.md#error-type)

Refer to the [Recording errors](/docs/general/recording-errors.md) document for additional
details on how to record errors across different signals.

It's RECOMMENDED to use `Span.recordException` API or logging library API that takes exception instance
instead of providing individual attributes. This enables the OpenTelemetry SDK to
control what information is recorded based on application configuration.

It's NOT RECOMMENDED to record the same exception more than once.
It's NOT RECOMMENDED to record exceptions that are handled by the instrumented library.

For example, in this code-snippet, `ResourceNotFoundException` is handled and corresponding
native instrumentation should not record it. Other exceptions, that are propagated
to the caller, should be recorded (or logged) once.

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
