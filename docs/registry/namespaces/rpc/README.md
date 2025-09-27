# RPC

**Summary:** This document defines how to describe remote procedure calls (also called “remote method invocations” / “RMI”) with spans.

> [!IMPORTANT]  Namespace was stablised in v1.20
>
> When migrating from an earlier version of semantic conventions, the migration document should be followed. [Migration Guide](#rpc)

**Description:** The conventions described in this section are RPC specific. When RPC operations occur, measurements about those operations are recorded to instruments. The measurements are aggregated and exported as metrics, which provide insight into those operations. By including RPC properties as attributes on measurements, the metrics can be filtered for finer grain analysis.

---------------------------------

**Attributes:**

|Key|Type|Summary|Examples|Stability|
|---|---|---|---|---|
| <a id="rpc-connect-rpc-error-code" href="attribute-custom.md">`rpc.connect_rpc.error_code`</a> | string | The [error codes](https://connectrpc.com//docs/protocol/#error-codes) of the Connect request. Error codes are always string values. | `cancelled`; `unknown`; `invalid_argument` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-connect-rpc-request-metadata" href="attribute-custom.md">`rpc.connect_rpc.request.metadata.<key>`</a> | string[] | Connect request metadata, `<key>` being the normalized Connect Metadata key (lowercase), the value being the metadata values. | `["1.2.3.4", "1.2.3.5"]` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-connect-rpc-response-metadata" href="attribute-custom.md">`rpc.connect_rpc.response.metadata.<key>`</a> | string[] | Connect response metadata, `<key>` being the normalized Connect Metadata key (lowercase), the value being the metadata values. | `["attribute_value"]` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-grpc-request-metadata" href="attribute-custom.md">`rpc.grpc.request.metadata.<key>`</a> | string[] | gRPC request metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. | `["1.2.3.4", "1.2.3.5"]` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-grpc-response-metadata" href="attribute-custom.md">`rpc.grpc.response.metadata.<key>`</a> | string[] | gRPC response metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. | `["attribute_value"]` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-grpc-status-code" href="attribute-custom.md">`rpc.grpc.status_code`</a> | int | The [numeric status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md) of the gRPC request. | `0`; `1`; `2` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-jsonrpc-error-code" href="attribute-custom.md">`rpc.jsonrpc.error_code`</a> | int | `error.code` property of response if it is an error response. | `-32700`; `100` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-jsonrpc-error-message" href="attribute-custom.md">`rpc.jsonrpc.error_message`</a> | string | `error.message` property of response if it is an error response. | `Parse error`; `User already exists` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-jsonrpc-request-id" href="attribute-custom.md">`rpc.jsonrpc.request_id`</a> | string | `id` property of request or response. Since protocol allows id to be int, string, `null` or missing (for notifications), value is expected to be cast to string for simplicity. Use empty string in case of `null` value. Omit entirely if this is a notification. | `10`; `request-7`; `` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-jsonrpc-version" href="attribute-custom.md">`rpc.jsonrpc.version`</a> | string | Protocol version as in `jsonrpc` property of request/response. Since JSON-RPC 1.0 doesn't specify this, the value can be omitted. | `2.0`; `1.0` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-message-compressed-size" href="attribute-custom.md">`rpc.message.compressed_size`</a> | int | Compressed size of the message in bytes. |  | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-message-id" href="attribute-custom.md">`rpc.message.id`</a> | int | MUST be calculated as two different counters starting from `1` one for sent messages and one for received message. |  | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-message-type" href="attribute-custom.md">`rpc.message.type`</a> | string | Whether this is a received or sent message. | `SENT`; `RECEIVED` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-message-uncompressed-size" href="attribute-custom.md">`rpc.message.uncompressed_size`</a> | int | Uncompressed size of the message in bytes. |  | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-method" href="attribute-custom.md">`rpc.method`</a> | string | The name of the (logical) method being called, must be equal to the $method part in the span name. | `exampleMethod` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-service" href="attribute-custom.md">`rpc.service`</a> | string | The full (logical) name of the service being called, including its package name, if applicable. | `myservice.EchoService` | ![Development](https://img.shields.io/badge/-development-blue) |
| <a id="rpc-system" href="attribute-custom.md">`rpc.system`</a> | <a id="rpc-system" href="type-custom.md">`rpc.system`</a> | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc`; `java_rmi`; `dotnet_wcf` | ![Development](https://img.shields.io/badge/-development-blue) |

**Entities:**

None

**Events:**

|Name|Summary|Stability|
|---|---|---|
|[`rpc.message`](event-custom.md)|Describes a message sent or received within the context of an RPC call.|![Development](https://img.shields.io/badge/-development-blue) |

**Metrics:**

|Name|Instrumentation Type|Unit (UCUM)|Summary|Stability|
| -------- | --------------- | ----------- | -------------- | --------- |
| [`rpc.server.duration`](metric-custom.md) | Histogram | `ms` | Measures the duration of inbound RPC. | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.server.request.size`](metric-custom.md) | Histogram | `By` | Measures the size of RPC request messages (uncompressed). | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.server.response.size`](metric-custom.md) | Histogram | `By` | Measures the size of RPC response messages (uncompressed). | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.server.requests_per_rpc`](metric-custom.md) | Histogram | `{count}` | Measures the number of messages received per RPC. | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.server.responses_per_rpc`](metric-custom.md) | Histogram | `{count}` | Measures the number of messages sent per RPC. | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.client.duration`](metric-custom.md) | Histogram | `ms` | Measures the duration of outbound RPC. | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.client.request.size`](metric-custom.md) | Histogram | `By` | Measures the size of RPC request messages (uncompressed). | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.client.response.size`](metric-custom.md) | Histogram | `By` | Measures the size of RPC response messages (uncompressed). | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.client.requests_per_rpc`](metric-custom.md) | Histogram | `{count}` | Measures the number of messages received per RPC. | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.client.responses_per_rpc`](metric-custom.md) | Histogram | `{count}` | Measures the number of messages sent per RPC. | ![Development](https://img.shields.io/badge/-development-blue) |

**Packages:**

|Name|Summary|Stability|
|---|---|---|
|[`rpc.client.command`](package-custom.md)|Client commands are for non streaming scenarios.|![Development](https://img.shields.io/badge/-development-blue)|
|[`rpc.client.streaming`](package-custom.md)|Client streaming are for streaming scenarios.|![Development](https://img.shields.io/badge/-development-blue)|

**Spans:**

|Name|Kind|Summary|Stability|
|---|---|---|---|
|[`rpc.client`](span-custom.md)|Client|This span represents an outgoing Remote Procedure Call (RPC).|![Development](https://img.shields.io/badge/-development-blue)|
|[`rpc.server`](span-custom.md)|Server|This span represents an incoming Remote Procedure Call (RPC).|![Development](https://img.shields.io/badge/-development-blue)|

**Types:**

|Name|Summary|Stability|
|---|---|---|
|[`rpc.system`](type-custom.md)|A string identifying the remoting system. See below for a list of well-known identifiers.| ![Development](https://img.shields.io/badge/-development-blue)|
