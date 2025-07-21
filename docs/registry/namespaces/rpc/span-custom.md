# RPC

**Summary:** This document defines how to describe remote procedure calls (also called “remote method invocations” / “RMI”) with spans.

> [!IMPORTANT]  Namespace was stablised in v1.20
>
> When migrating from an earlier version of semantic conventions, the migration document should be followed. [Migration Guide](#rpc)

**Description:** The conventions described in this section are RPC specific. When RPC operations occur, measurements about those operations are recorded to instruments. The measurements are aggregated and exported as metrics, which provide insight into those operations. By including RPC properties as attributes on measurements, the metrics can be filtered for finer grain analysis.

---------------------------------

## Span: RPC Client

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

**Namespace:** [`rpc`](README.md)

**Summary:** This span represents an outgoing Remote Procedure Call (RPC).

**Signal Type:** Span

**Span name:** refer to the Span Name section.

**Span kind:** `CLIENT`.

**Span status** SHOULD follow the [Recording Errors](/docs/general/recording-errors.md) document.

**Description:** Remote procedure calls can only be represented with these semantic conventions when the names of the called service and method are known and available.

**Attributes:**

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`rpc.system`](attribute-custom.md) | [rpc.system](type-custom.md) | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc`; `java_rmi`; `dotnet_wcf` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`server.address`](attribute-custom.md) | string | RPC server [host name](https://grpc.github.io/grpc/core/md_doc_naming.html). | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](attribute-custom.md) | int | Server port number. | `80`; `8080`; `443` | `Conditionally Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.address`](attribute-custom.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](attribute-custom.md) | int | Peer port number of the network connection. | `65123` | `Recommended` If `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.transport`](attribute-custom.md) | string | [OSI transport layer](https://wikipedia.org/wiki/Transport_layer) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). | `tcp`; `udp` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.type`](attribute-custom.md) | string | [OSI network layer](https://wikipedia.org/wiki/Network_layer) or non-OSI equivalent. | `ipv4`; `ipv6` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`rpc.method`](attribute-custom.md) | string | The name of the (logical) method being called, must be equal to the $method part in the span name. | `exampleMethod` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.service`](attribute-custom.md) | string | The full (logical) name of the service being called, including its package name, if applicable. | `myservice.EchoService` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

**Entity Associations:**

|Entity|Summary|Stability|
|---|---|---|
|[`service`](entity-custom.md)|A service instance.|![Development](https://img.shields.io/badge/-development-blue) |
