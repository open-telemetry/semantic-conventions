<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic Conventions for RPC Spans

**Status**: [Experimental][DocumentStatus]

This document defines how to describe remote procedure calls
(also called "remote method invocations" / "RMI") with spans.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Common remote procedure call conventions](#common-remote-procedure-call-conventions)
  * [Span name](#span-name)
  * [Common attributes](#common-attributes)
    + [Service name](#service-name)
  * [Client attributes](#client-attributes)
  * [Server attributes](#server-attributes)
  * [Events](#events)
  * [Distinction from HTTP spans](#distinction-from-http-spans)
- [Semantic Conventions for specific RPC technologies](#semantic-conventions-for-specific-rpc-technologies)

<!-- tocstop -->

> **Warning**
> Existing RPC instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/rpc.md)
> (or prior):
>
> * SHOULD NOT change the version of the networking conventions that they emit
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
> * SHOULD drop the environment variable in the next major version (stable
>   next major version SHOULD NOT be released prior to October 1, 2023).

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

### Common attributes

<!-- semconv rpc -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `rpc.system` | string | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc` | Required |
| `rpc.service` | string | The full (logical) name of the service being called, including its package name, if applicable. [1] | `myservice.EchoService` | Recommended |
| `rpc.method` | string | The name of the (logical) method being called, must be equal to the $method part in the span name. [2] | `exampleMethod` | Recommended |
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `udp` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended |
| [`server.address`](../general/attributes.md) | string | RPC server [host name](https://grpc.github.io/grpc/core/md_doc_naming.html). [3] | `example.com` | Required |
| [`server.port`](../general/attributes.md) | int | Server port number [4] | `80`; `8080`; `443` | Conditionally Required: See below |
| [`server.socket.address`](../general/attributes.md) | string | Server address of the socket connection - IP address or Unix domain socket name. [5] | `10.5.3.2` | See below |
| [`server.socket.port`](../general/attributes.md) | int | Server port number of the socket connection. [6] | `16456` | Recommended: [7] |

**[1]:** This is the logical name of the service from the RPC interface perspective, which can be different from the name of any implementing class. The `code.namespace` attribute may be used to store the latter (despite the attribute name, it may include a class name; e.g., class with method actually executing the call on the server side, RPC client stub class on the client side).

**[2]:** This is the logical name of the method from the RPC interface perspective, which can be different from the name of any implementing method/function. The `code.function` attribute may be used to store the latter (e.g., method actually executing the call on the server side, RPC client stub method on the client side).

**[3]:** May contain server IP address, DNS name, or local socket name. When host component is an IP address, instrumentations SHOULD NOT do a reverse proxy lookup to obtain DNS name and SHOULD set `server.address` to the IP address provided in the host component.

**[4]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

**[5]:** When observed from the client side, this SHOULD represent the immediate server peer address.
When observed from the server side, this SHOULD represent the physical server address.

**[6]:** When observed from the client side, this SHOULD represent the immediate server peer port.
When observed from the server side, this SHOULD represent the physical server port.

**[7]:** If different than `server.port` and if `server.socket.address` is set.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* [`server.socket.address`](../general/attributes.md)
* [`server.address`](../general/attributes.md)

`rpc.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `grpc` | gRPC |
| `java_rmi` | Java RMI |
| `dotnet_wcf` | .NET WCF |
| `apache_dubbo` | Apache Dubbo |
| `connect_rpc` | Connect RPC |
<!-- endsemconv -->

For client-side spans `server.port` is required if the connection is IP-based and the port is available (it describes the server port they are connecting to).
For server-side spans `client.socket.port` is optional (it describes the port the client is connecting from).

#### Service name

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

<!-- semconv rpc.client -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`server.socket.domain`](../general/attributes.md) | string | Immediate server peer's domain name if available without reverse DNS lookup [1] | `proxy.example.com` | Recommended: [2] |

**[1]:** Typically observed from the client side, and represents a proxy or other intermediary domain name.

**[2]:** If different than `server.address` and if `server.socket.address` is set.
<!-- endsemconv -->

### Server attributes

<!-- semconv rpc.server -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`client.address`](../general/attributes.md) | string | Client address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `/tmp/my.sock`; `10.1.2.80` | Recommended |
| [`client.port`](../general/attributes.md) | int | Client port number. [2] | `65123` | Recommended |
| [`client.socket.address`](../general/attributes.md) | string | Client address of the socket connection - IP address or Unix domain socket name. [3] | `/tmp/my.sock`; `127.0.0.1` | Recommended: If different than `client.address`. |
| [`client.socket.port`](../general/attributes.md) | int | Client port number of the socket connection. [4] | `35555` | Recommended: If different than `client.port`. |
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `udp` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended |

**[1]:** When observed from the server side, and when communicating through an intermediary, `client.address` SHOULD represent the client address behind any intermediaries (e.g. proxies) if it's available.

**[2]:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries (e.g. proxies) if it's available.

**[3]:** When observed from the server side, this SHOULD represent the immediate client peer address.
When observed from the client side, this SHOULD represent the physical client address.

**[4]:** When observed from the server side, this SHOULD represent the immediate client peer port.
When observed from the client side, this SHOULD represent the physical client port.
<!-- endsemconv -->

### Events

In the lifetime of an RPC stream, an event for each message sent/received on
client and server spans SHOULD be created. In case of unary calls only one sent
and one received message will be recorded for both client and server spans.

<!-- semconv rpc.message -->
The event name MUST be `message`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `message.type` | string | Whether this is a received or sent message. | `SENT` | Recommended |
| `message.id` | int | MUST be calculated as two different counters starting from `1` one for sent messages and one for received message. [1] |  | Recommended |
| `message.compressed_size` | int | Compressed size of the message in bytes. |  | Recommended |
| `message.uncompressed_size` | int | Uncompressed size of the message in bytes. |  | Recommended |

**[1]:** This way we guarantee that the values will be consistent between different implementations.

`message.type` MUST be one of the following:

| Value  | Description |
|---|---|
| `SENT` | sent |
| `RECEIVED` | received |
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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
