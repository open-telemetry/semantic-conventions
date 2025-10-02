<!--- Hugo front matter used to generate the website version of this page:
linkTitle: RPC
--->

# Semantic conventions for RPC

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for remote procedure calls (RPC)
, also called "remote method invocations" (RMI).

> **Warning**
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

Technology specific semantic conventions are defined for the following RPC systems:

* [Connect](connect-rpc.md): Semantic Conventions for *Connect RPC*.
* [gRPC](grpc.md): Semantic Conventions for *gRPC*.
* [JSON-RPC](json-rpc.md): Semantic Conventions for *JSON-RPC*.

Specifications defined by maintainers of RPC systems:

* [gRPC](https://github.com/grpc/proposal/blob/master/A66-otel-stats.md): Semantic Conventions for *gRPC*.

## RPC Service vs RPC Framework

### What is a RPC Protocol?

A RPC protocol describes the manner in which a message is transported from one service to another.
This protocol may have the same value as the network protocol ie http or it may differ when,
an implementation of the network protocol is used ie gRPC.

These implementation's will usually only expose a subset of functionality of the network protocol
and may only be compatible with newer versions of the network protocol ie grpc will not work over http v1.

Some pre-defined protocols are:

* [gRPC](#)
* [http](#)
* [triple](#)
* [soap](#)
* [Connect RPC](#)

It is expected that these protocols will define protocol specific attributes, for instance gRPC would contain a status attribute.
As such the usage of these attribute/s should be documented via a dedicated protocol page providing complete definitions.

### What is a RPC Framework?

A RPC Framework describes the api's made available to applications wanting to implement RPC Communications
in a protocol agnostic manner. This is why protocol and framework is not a one-to-one relationship but rather one-to-many.

The framework in adddition to providing the api can define properties which are sent along with the message
to provide additional context. For instance a framework might require a message id to be sent with the message.
The framework doesn't care how it is transported across the network.

Some pre-defined frameworks are:

* [Apache Dubbo](#)
* [Dapr](#)
* [Connect RPC](#)
* [JSON-RPC](#)

These frameworks can provide additional attributes for capturing the properties mentioned earlier.
It is expected that these attributes are added where appropriate to the corresponding signals defined for the network protocol,
with a general "if applicable for the rpc framework" condition placed on the requirement level.

A framework may have its own page when the framework defines its own signals which require the inclusion of framework specific
attributes for the signal to have value & meaning.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
