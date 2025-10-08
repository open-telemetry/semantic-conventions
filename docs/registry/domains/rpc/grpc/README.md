<!--To eventually be auto-generated based upon implementations with data grouped based on scope-->
# gRPC

**Summary:** This document defines how to describe remote procedure calls (also called “remote method invocations” / “RMI”) with spans.

> [!IMPORTANT]  Namespace was stablised in v1.20
>
> When migrating from an earlier version of semantic conventions, the migration document should be followed. [Migration Guide](#grpc)

**Description:** The conventions described in this section are RPC specific. When RPC operations occur, measurements about those operations are recorded to instruments. The measurements are aggregated and exported as metrics, which provide insight into those operations. By including RPC properties as attributes on measurements, the metrics can be filtered for finer grain analysis.

## Scope

**Summary:** The gRPC scope is for all instrumentation which communicates via rpc in particular when using grpc.

**Name:** `rpc.grpc`

**Description:**  This is a description.

**Attributes:**

|Key|Type|Summary|Value|
|---|---|---|---|
|[`rpc.system`](../../../namespaces/rpc/attribute-custom.md)|[`rpc.system`](../../../namespaces/rpc/type-custom.md)|A string identifying the remoting system. See below for a list of well-known identifiers.| `grpc` |

The above attributes should be set at the instrumentation scope level if possible, otherwise can be specified as measurement attributes.

**Packages:**

| Name | Summary|
| --- | --- |
| [`rpc.client`](#grpc-client) | Telemetry describing grpc interactions from the client side. |
| [`rpc.server`](#grpc-server) | Telemetry describing grpc interactions from the server side. |

## gRPC Client

**Summary:** Telemetry describing grpc interactions from the client side.

**Base Definition:** [`rpc.client`](../../../namespaces/rpc/package-custom.md)

**Description:** This is a description.

### Span: [`rpc.client`](span-custom.md)

**Summary:** This span represents an outgoing Remote Procedure Call (RPC).

**Requirement Level:** `Required`

**Span kind:** `CLIENT`.

**Description:** Remote procedure calls can only be represented with these semantic conventions when the names of the called service and method are known and available.

**Attributes:**

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`server.address`](../../../namespaces/rpc/attribute-custom.md) | string | RPC server [host name](https://grpc.github.io/grpc/core/md_doc_naming.html). | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](../../../namespaces/rpc/attribute-custom.md) | int | Server port number. | `80`; `8080`; `443` | `Conditionally Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`rpc.grpc.status_code`](../../../namespaces/rpc/attribute-custom.md) | int | The [numeric status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md) of the gRPC request. | `0`; `1`; `2` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.grpc.request.metadata.<key>`](../../../namespaces/rpc/attribute-custom.md) | string[] | gRPC request metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. | `["1.2.3.4", "1.2.3.5"]` | `Opt-In` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.grpc.response.metadata.<key>`](../../../namespaces/rpc/attribute-custom.md) | string[] | gRPC response metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values.| `["attribute_value"]` | `Opt-In` | ![Development](https://img.shields.io/badge/-development-blue) |

The full definition is available via [span definition](span-custom.md).

---------------------------------

### Event: [`rpc.message`](event-custom.md)

**Summary:** Describes a message sent or received within the context of an RPC call.

**Requirement Level:** `Opt-in`

**Description:** In the lifetime of an RPC stream, an event for each message sent/received on client and server spans SHOULD be created. In case of unary calls only one sent and one received message will be recorded for both client and server spans.

**Attributes:**

|Key|Type|Summary|Value|
|---|---|---|---|
| [`rpc.grpc.status_code`](../../../namespaces/rpc/attribute-custom.md) | int | The [numeric status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md) of the gRPC request. | `0`; `1`; `2` |
| [`rpc.grpc.request.metadata.<key>`](../../../namespaces/rpc/attribute-custom.md) | string[] | gRPC request metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. | `["1.2.3.4", "1.2.3.5"]` |
| [`rpc.grpc.response.metadata.<key>`](../../../namespaces/rpc/attribute-custom.md) | string[] | gRPC response metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values.| `["attribute_value"]` |

The full definition is available via [event definition](event-custom.md).

---------------------------------

### Metric: [`rpc.client.duration`](metric-custom.md)

**Summary:** Measures the duration of outbound RPC.

**Requirement Level:** `Recommended`

**Instrument Type:** Histogram

**Description:** While streaming RPCs may record this metric as start-of-batch
to end-of-batch, it's hard to interpret in practice.

The full definition is available via [metric definition](metric-custom.md).

---------------------------------

### Metric: [`rpc.client.request.size`](metric-custom.md)

**Summary:** Measures the size of RPC request messages (uncompressed).

**Requirement Level:** `Recommended`

**Instrument Type:** Histogram

**Description:** This is a description.

The full definition is available via [metric definition](metric-custom.md).

---------------------------------

### Metric: [`rpc.client.response.size`](metric-custom.md)

**Summary:** Measures the size of RPC response messages (uncompressed).

**Requirement Level:** `Recommended`

**Instrument Type:** Histogram

**Description:** This is a description.

The full definition is available via [metric definition](metric-custom.md).

---------------------------------

### Metric: [`rpc.client.requests_per_rpc`](metric-custom.md)

**Summary:** Measures the number of messages received per RPC.

**Requirement Level:** `Recommended`

**Instrument Type:** Histogram

**Description:** This is a description.

The full definition is available via [metric definition](metric-custom.md).

---------------------------------

### Metric: [`rpc.client.responses_per_rpc`](metric-custom.md)

**Summary:** Measures the number of messages sent per RPC.

**Requirement Level:** `Recommended`

**Instrument Type:** Histogram

**Description:** This is a description.

The full definition is available via [metric definition](metric-custom.md).

## gRPC Server

**Summary:** Telemetry describing grpc interactions from the client side.

**Base Definition:** [`rpc.server`](../../../namespaces/rpc/package-custom.md)

**Description:** This is a description.

{{Repeat of what is done for client}}
