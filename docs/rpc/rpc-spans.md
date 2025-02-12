<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic conventions for RPC spans

**Status**: [Development][DocumentStatus]

This document defines how to describe remote procedure calls
(also called "remote method invocations" / "RMI") with spans.

<!-- toc -->

- [Common remote procedure call conventions](#common-remote-procedure-call-conventions)
  - [Span name](#span-name)
  - [Span status](#span-status)
  - [Service name](#service-name)
  - [Client attributes](#client-attributes)
  - [Server attributes](#server-attributes)
  - [Events](#events)
    - [Message event](#message-event)
  - [Distinction from HTTP spans](#distinction-from-http-spans)
- [Semantic Conventions for specific RPC technologies](#semantic-conventions-for-specific-rpc-technologies)

<!-- tocstop -->

> **Warning**
> Existing RPC instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/rpc.md)
> (or prior):
>
> * SHOULD NOT change the version of the networking conventions that they emit by default
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking conventions which are also used
>   in RPC instrumentations). Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The only values defined so far are:
>   * `http` - emit the new, stable networking conventions,
>     and stop emitting the old experimental networking conventions
>     that the instrumentation emitted previously.
>   * `http/dup` - emit both the old and the stable networking conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental networking conventions
>     the instrumentation was emitting previously.
>   * Note: `http/dup` has higher precedence than `http` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version.

## Common remote procedure call conventions

A remote procedure calls is described by two separate spans, one on the client-side and one on the server-side.

For outgoing requests, the `SpanKind` MUST be set to `CLIENT` and for incoming requests to `SERVER`.

Remote procedure calls can only be represented with these semantic conventions, when the names of the called service and method are known and available.

### Span name

The *span name* MUST be the full RPC method name formatted as:

```
$package.$service/$method
```

(where $service MUST NOT contain dots and $method MUST NOT contain slashes)

If there is no package name or if it is unknown, the `$package.` part (including the period) is omitted.

Examples of span names:

- `grpc.test.EchoService/Echo`
- `com.example.ExampleRmiService/exampleMethod`
- `MyCalcService.Calculator/Add` reported by the server and
  `MyServiceReference.ICalculator/Add` reported by the client for .NET WCF calls
- `MyServiceWithNoPackage/theMethod`

### Span status

Refer to the [Recording Errors](/docs/general/recording-errors.md) document for
details on how to record span status.

### Service name

On the server process receiving and handling the remote procedure call, the service name provided in `rpc.service` does not necessarily have to match the [`service.name`][] resource attribute.
One process can expose multiple RPC endpoints and thus have multiple RPC service names. From a deployment perspective, as expressed by the `service.*` resource attributes, it will be treated as one deployed service with one `service.name`.
Likewise, on clients sending RPC requests to a server, the service name provided in `rpc.service` does not have to match the [`peer.service`][] span attribute.

As an example, given a process deployed as `QuoteService`, this would be the name that goes into the `service.name` resource attribute which applies to the entire process.
This process could expose two RPC endpoints, one called `CurrencyQuotes` (= `rpc.service`) with a method called `getMeanRate` (= `rpc.method`) and the other endpoint called `StockQuotes`  (= `rpc.service`) with two methods `getCurrentBid` and `getLastClose` (= `rpc.method`).
In this example, spans representing client request should have their `peer.service` attribute set to `QuoteService` as well to match the server's `service.name` resource attribute.
Generally, a user SHOULD NOT set `peer.service` to a fully qualified RPC service name.

[`service.name`]: /docs/resource/README.md#service
[`peer.service`]: /docs/general/attributes.md#general-remote-service-attributes

### Client attributes

<!-- semconv span.rpc.client -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`rpc.system`](/docs/attributes-registry/rpc.md) | string | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc`; `java_rmi`; `dotnet_wcf` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | RPC server [host name](https://grpc.github.io/grpc/core/md_doc_naming.html). [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [2] | `80`; `8080`; `443` | `Conditionally Required` [3] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` If `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.transport`](/docs/attributes-registry/network.md) | string | [OSI transport layer](https://wikipedia.org/wiki/Transport_layer) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [4] | `tcp`; `udp` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.type`](/docs/attributes-registry/network.md) | string | [OSI network layer](https://wikipedia.org/wiki/Network_layer) or non-OSI equivalent. [5] | `ipv4`; `ipv6` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`rpc.method`](/docs/attributes-registry/rpc.md) | string | The name of the (logical) method being called, must be equal to the $method part in the span name. [6] | `exampleMethod` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.service`](/docs/attributes-registry/rpc.md) | string | The full (logical) name of the service being called, including its package name, if applicable. [7] | `myservice.EchoService` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

**[1] `server.address`:** May contain server IP address, DNS name, or local socket name. When host component is an IP address, instrumentations SHOULD NOT do a reverse proxy lookup to obtain DNS name and SHOULD set `server.address` to the IP address provided in the host component.

**[2] `server.port`:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[3] `server.port`:** if the port is supported by the network transport used for communication.

**[4] `network.transport`:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[5] `network.type`:** The value SHOULD be normalized to lowercase.

**[6] `rpc.method`:** This is the logical name of the method from the RPC interface perspective, which can be different from the name of any implementing method/function. The `code.function.name` attribute may be used to store the latter (e.g., method actually executing the call on the server side, RPC client stub method on the client side).

**[7] `rpc.service`:** This is the logical name of the service from the RPC interface perspective, which can be different from the name of any implementing class. The `code.namespace` attribute may be used to store the latter (despite the attribute name, it may include a class name; e.g., class with method actually executing the call on the server side, RPC client stub class on the client side).

---

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `pipe` | Named or anonymous pipe. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `quic` | QUIC | ![Development](https://img.shields.io/badge/-development-blue) |
| `tcp` | TCP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `ipv4` | IPv4 | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `ipv6` | IPv6 | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`rpc.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `apache_dubbo` | Apache Dubbo | ![Development](https://img.shields.io/badge/-development-blue) |
| `connect_rpc` | Connect RPC | ![Development](https://img.shields.io/badge/-development-blue) |
| `dotnet_wcf` | .NET WCF | ![Development](https://img.shields.io/badge/-development-blue) |
| `grpc` | gRPC | ![Development](https://img.shields.io/badge/-development-blue) |
| `java_rmi` | Java RMI | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Server attributes

<!-- semconv span.rpc.server -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`rpc.system`](/docs/attributes-registry/rpc.md) | string | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc`; `java_rmi`; `dotnet_wcf` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | RPC server [host name](https://grpc.github.io/grpc/core/md_doc_naming.html). [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [2] | `80`; `8080`; `443` | `Conditionally Required` [3] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`client.address`](/docs/attributes-registry/client.md) | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [4] | `client.example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`client.port`](/docs/attributes-registry/client.md) | int | Client port number. [5] | `65123` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` If `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.transport`](/docs/attributes-registry/network.md) | string | [OSI transport layer](https://wikipedia.org/wiki/Transport_layer) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [6] | `tcp`; `udp` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.type`](/docs/attributes-registry/network.md) | string | [OSI network layer](https://wikipedia.org/wiki/Network_layer) or non-OSI equivalent. [7] | `ipv4`; `ipv6` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`rpc.method`](/docs/attributes-registry/rpc.md) | string | The name of the (logical) method being called, must be equal to the $method part in the span name. [8] | `exampleMethod` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.service`](/docs/attributes-registry/rpc.md) | string | The full (logical) name of the service being called, including its package name, if applicable. [9] | `myservice.EchoService` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

**[1] `server.address`:** May contain server IP address, DNS name, or local socket name. When host component is an IP address, instrumentations SHOULD NOT do a reverse proxy lookup to obtain DNS name and SHOULD set `server.address` to the IP address provided in the host component.

**[2] `server.port`:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[3] `server.port`:** if the port is supported by the network transport used for communication.

**[4] `client.address`:** When observed from the server side, and when communicating through an intermediary, `client.address` SHOULD represent the client address behind any intermediaries,  for example proxies, if it's available.

**[5] `client.port`:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries,  for example proxies, if it's available.

**[6] `network.transport`:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[7] `network.type`:** The value SHOULD be normalized to lowercase.

**[8] `rpc.method`:** This is the logical name of the method from the RPC interface perspective, which can be different from the name of any implementing method/function. The `code.function.name` attribute may be used to store the latter (e.g., method actually executing the call on the server side, RPC client stub method on the client side).

**[9] `rpc.service`:** This is the logical name of the service from the RPC interface perspective, which can be different from the name of any implementing class. The `code.namespace` attribute may be used to store the latter (despite the attribute name, it may include a class name; e.g., class with method actually executing the call on the server side, RPC client stub class on the client side).

---

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `pipe` | Named or anonymous pipe. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `quic` | QUIC | ![Development](https://img.shields.io/badge/-development-blue) |
| `tcp` | TCP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `ipv4` | IPv4 | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `ipv6` | IPv6 | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`rpc.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `apache_dubbo` | Apache Dubbo | ![Development](https://img.shields.io/badge/-development-blue) |
| `connect_rpc` | Connect RPC | ![Development](https://img.shields.io/badge/-development-blue) |
| `dotnet_wcf` | .NET WCF | ![Development](https://img.shields.io/badge/-development-blue) |
| `grpc` | gRPC | ![Development](https://img.shields.io/badge/-development-blue) |
| `java_rmi` | Java RMI | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Events

#### Message event

<!-- semconv event.rpc.message -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

The event name MUST be `rpc.message`.

Describes a message sent or received within the context of an RPC call.

In the lifetime of an RPC stream, an event for each message sent/received on client and server spans SHOULD be created. In case of unary calls only one sent and one received message will be recorded for both client and server spans.

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`rpc.message.compressed_size`](/docs/attributes-registry/rpc.md) | int | Compressed size of the message in bytes. |  | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.message.id`](/docs/attributes-registry/rpc.md) | int | MUST be calculated as two different counters starting from `1` one for sent messages and one for received message. [1] |  | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.message.type`](/docs/attributes-registry/rpc.md) | string | Whether this is a received or sent message. | `SENT`; `RECEIVED` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.message.uncompressed_size`](/docs/attributes-registry/rpc.md) | int | Uncompressed size of the message in bytes. |  | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

**[1] `rpc.message.id`:** This way we guarantee that the values will be consistent between different implementations.

---

`rpc.message.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `RECEIVED` | received | ![Development](https://img.shields.io/badge/-development-blue) |
| `SENT` | sent | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Distinction from HTTP spans

HTTP calls can generally be represented using just [HTTP spans](/docs/http/http-spans.md).
If they address a particular remote service and method known to the caller, i.e., when it is a remote procedure call transported over HTTP, the `rpc.*` attributes might be added additionally on that span, or in a separate RPC span that is a parent of the transporting HTTP call.
Note that *method* in this context is about the called remote procedure and *not* the HTTP verb (GET, POST, etc.).

## Semantic Conventions for specific RPC technologies

More specific Semantic Conventions are defined for the following RPC technologies:

* [Connect](connect-rpc.md): Semantic Conventions for *Connect RPC*.
* [gRPC](grpc.md): Semantic Conventions for *gRPC*.
* [JSON-RPC](json-rpc.md): Semantic Conventions for *JSON-RPC*.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
