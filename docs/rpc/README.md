<!--- Hugo front matter used to generate the website version of this page:
linkTitle: RPC
--->

# Semantic conventions for RPC

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for remote procedure calls (RPC)
, also called "remote method invocations" (RMI).

> [!IMPORTANT]
> Existing RPC instrumentations that are using
> [v1.37.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/README.md)
> (or prior):
>
> * SHOULD NOT change the version of the RPC conventions that they emit by
>   default in their existing major version. Conventions include (but are not
>   limited to) attributes, metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in their existing major version as a comma-separated list of category-specific values
>   (e.g., http, databases, rpc). The list of values includes:
>   * `rpc` - emit the stable RPC conventions, and stop emitting
>     the experimental RPC conventions that the instrumentation emitted
>     previously.
>   * `rpc/dup` - emit both the experimental and stable RPC conventions,
>     allowing for a phased rollout of the stable semantic conventions.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental RPC conventions
>     the instrumentation was emitting previously.
>   * Note: `rpc/dup` has higher precedence than `rpc` in case both values are present
> * SHOULD maintain (security patching at a minimum) their existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * MAY drop the environment variable in their next major version and emit only
>   the stable RPC conventions.

Semantic conventions for RPC are defined for the following signals:

* [RPC Spans](rpc-spans.md): Semantic Conventions for RPC client and server *spans*.
* [RPC Metrics](rpc-metrics.md): Semantic Conventions for RPC *metrics*.
* [RPC Events](rpc-events.md): Semantic Conventions for RPC *events*.

Technology specific semantic conventions are defined for the following RPC systems:

* [Connect](connect-rpc.md): Semantic Conventions for *Connect RPC*.
* [gRPC](grpc.md): Semantic Conventions for *gRPC*.
* [JSON-RPC](json-rpc.md): Semantic Conventions for *JSON-RPC*.

Specifications defined by maintainers of RPC systems:

* [gRPC](https://github.com/grpc/proposal/blob/master/A66-otel-stats.md): Semantic Conventions for *gRPC*.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
