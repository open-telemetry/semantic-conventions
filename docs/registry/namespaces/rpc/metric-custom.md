# RPC

**Summary:** This document defines how to describe remote procedure calls (also called “remote method invocations” / “RMI”) with spans.

> [!IMPORTANT]  Namespace was stablised in v1.20
>
> When migrating from an earlier version of semantic conventions, the migration document should be followed. [Migration Guide](#rpc)

**Description:** The conventions described in this section are RPC specific. When RPC operations occur, measurements about those operations are recorded to instruments. The measurements are aggregated and exported as metrics, which provide insight into those operations. By including RPC properties as attributes on measurements, the metrics can be filtered for finer grain analysis.

---------------------------------

## Metric: RPC Server Duration

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

**Namespace:** [`rpc`](README.md)

**Summary:** Measures the duration of inbound RPC.

**Signal Type:** Metric

**Metric Name:** `rpc.server.duration`

**Instrument Type:** Histogram

**Unit:**  `ms`

**Description:** While streaming RPCs may record this metric as start-of-batch to end-of-batch, it’s hard to interpret in practice.

**Attributes:**

| Key  | Type | Summary  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`rpc.system`](attribute-custom.md) | [rpc.system](type-custom.md) | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc`; `java_rmi`; `dotnet_wcf` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`network.transport`](attribute-custom.md) | string | [OSI transport layer](https://wikipedia.org/wiki/Transport_layer) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). | `tcp`; `udp` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.type`](attribute-custom.md) | string | [OSI network layer](https://wikipedia.org/wiki/Network_layer) or non-OSI equivalent. | `ipv4`; `ipv6` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`rpc.method`](attribute-custom.md) | string | The name of the (logical) method being called, must be equal to the $method part in the span name. | `exampleMethod` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.service`](attribute-custom.md) | string | The full (logical) name of the service being called, including its package name, if applicable. | `myservice.EchoService` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`server.address`](attribute-custom.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [5] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](attribute-custom.md) | int | Server port number. [6] | `80`; `8080`; `443` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**Entity Associations:**

|Entity|Summary|Stability|
|---|---|---|
|[`service`](entity-custom.md)|A service instance.|![Development](https://img.shields.io/badge/-development-blue) |
