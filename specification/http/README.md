# Semantic conventions for HTTP

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This document defines semantic conventions for HTTP spans, metrics and logs.
They can be used for http and https schemes
and various HTTP versions like 1.1, 2 and SPDY.

> **Warning**
> Existing HTTP instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/http/http-spans.md)
> (or prior):
>
> * SHOULD NOT change the version of the HTTP or networking attributes that they emit
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking attributes which are also used
>   in HTTP instrumentations).
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The only values defined so far are:
>   * `http` - emit the new, stable HTTP and networking attributes,
>     and stop emitting the old experimental HTTP and networking attributes
>     that the instrumentation emitted previously.
>   * `http/dup` - emit both the old and the stable HTTP and networking attributes,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental HTTP and networking attributes
>     the instrumentation was emitting previously.
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of attributes.
> * SHOULD drop the environment variable in the next major version (stable
>   next major version SHOULD NOT be released prior to October 1, 2023).

Semantic conventions for HTTP are defined for the following signals:

* [HTTP Spans](http-spans.md): Semantic Conventions for HTTP client and server *spans*.
* [HTTP Metrics](http-metrics.md): Semantic Conventions for HTTP client and server *metrics*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
