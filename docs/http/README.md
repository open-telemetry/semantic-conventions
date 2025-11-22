<!--- Hugo front matter used to generate the website version of this page:
linkTitle: HTTP
--->

# Semantic conventions for HTTP

**Status**: [Mixed][DocumentStatus]

This document defines semantic conventions for HTTP spans, metrics and logs.
They can be used for http and https schemes
and various HTTP versions like 1.1, 2 and SPDY.

> [!IMPORTANT]
> Existing HTTP instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md)
> (or prior):
>
> * SHOULD NOT change the version of the HTTP or networking conventions that they emit by default
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking conventions which are also used
>   in HTTP instrumentations). Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version as a comma-separated list of category-specific values
>   (e.g., http, databases, messaging). The list of values includes:
>   * `http` - emit the new, stable HTTP and networking conventions,
>     and stop emitting the old experimental HTTP and networking conventions
>     that the instrumentation emitted previously.
>   * `http/dup` - emit both the old and the stable HTTP and networking conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental HTTP and networking conventions
>     the instrumentation was emitting previously.
>   * Note: `http/dup` has higher precedence than `http` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version.

Semantic conventions for HTTP are defined for the following signals:

* [HTTP Spans](http-spans.md): Semantic Conventions for HTTP client and server *spans*.
* [HTTP Metrics](http-metrics.md): Semantic Conventions for HTTP client and server *metrics*.

For help migrating from non-stable to stable conventions, see [the migration guide](../non-normative/http-migration.md).

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
