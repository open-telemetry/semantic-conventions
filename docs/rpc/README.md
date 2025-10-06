<!--- Hugo front matter used to generate the website version of this page:
linkTitle: RPC
--->

# Semantic conventions for RPC

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for remote procedure calls (RPC)
, sometimes called "remote method invocations" (RMI).

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

The RPC Semantic conventions are designed to cover the logical operation of invoking an operation (function) to run in a remote process.
This remote process call will often travel across the network to reach it's destination.

The details of this invocation can be captured using the following signals:

* [RPC Spans](rpc-spans.md): Semantic Conventions for RPC client and server *spans*.
* [RPC Metrics](rpc-metrics.md): Semantic Conventions for RPC *metrics*.

These generic conventions can be extended based on the protocol/framework being used.
This is described in more detail in the [RPC Transport Protocol vs RPC Framework](#rpc-transport-protocol-vs-rpc-framework) section.

However should the process being invoked be a member of a more specific domain such as those below,
the corresponding conventions should be followed:

* [Database](/docs/database/README.md)
* [Generative AI](/docs/gen-ai/README.md)
* [Messaging](/docs/messaging/README.md)

If your focus is on the network layer calls rather than the logical calls being made,
the RPC documents are not for you but instead what you are after is described via the below conventions:

* Http

## RPC Transport Protocol vs RPC Framework

### What is a RPC Transport Protocol?

A RPC transport protocol describes the manner in which a message is transported from one service to another.
This protocol may have the same value as the network protocol ie http or it may differ when,
an implementation of the network protocol is used e.g. gRPC.

These implementations will usually only expose a subset of functionality of the network protocol
and may only be compatible with newer versions of the network protocol ie grpc will not work over http v1.

Another aspect of how the `network.protocol.*` differs to `rpc.transport.protocol.*` is that,
the transport protocol can implement additional client side functionality such as retry, caching, cancellation etc.

Some pre-defined transport protocols are:

* [gRPC](grpc.md)
* [Http](/docs/http/README.md)
* Triple
* SOAP
* [Connect RPC](connect-rpc.md)

It is expected that these protocols will define protocol specific attributes, for instance gRPC would contain a status attribute.
As such the usage of these attribute/s should be documented via a dedicated protocol page providing complete definitions.

### What is a RPC Framework?

A RPC Framework describes the api's made available to applications wanting to implement RPC Communications
in a protocol agnostic manner. This is why protocol and framework is not a one-to-one relationship but rather one-to-many.

The framework in addition to providing the api can define properties which are sent along with the message
to provide additional context. For instance a framework might require a message id to be sent with the message.
The framework doesn't care how it is transported across the network.

Some pre-defined frameworks are:

* Apache Dubbo
* Dapr
* [Connect RPC](connect-rpc.md)
* [JSON-RPC](json-rpc.md)
* WCF

These frameworks can provide additional attributes for capturing the properties mentioned earlier.
It is expected that these attributes are added where appropriate to the corresponding signals defined for the rpc protocol,
with a general "if applicable for the rpc framework" condition placed on the requirement level.

A framework may have its own page when the framework defines its own signals which require the inclusion of framework specific
attributes for the signal to have value & meaning.

## Supplementary Documents

Specifications defined by maintainers of RPC systems:

* [gRPC](https://github.com/grpc/proposal/blob/master/A66-otel-stats.md): Semantic Conventions for *gRPC*.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
