# RPC

**Summary:** This document defines how to describe remote procedure calls (also called “remote method invocations” / “RMI”) with spans.

> [!IMPORTANT]  Namespace was stablised in v1.20
>
> When migrating from an earlier version of semantic conventions, the migration document should be followed. [Migration Guide](#rpc)

**Description:** The conventions described in this section are RPC specific. When RPC operations occur, measurements about those operations are recorded to instruments. The measurements are aggregated and exported as metrics, which provide insight into those operations. By including RPC properties as attributes on measurements, the metrics can be filtered for finer grain analysis.

---------------------------------

## Event: RPC Message

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

**Namespace:** [`rpc`](README.md)

**Summary:** Describes a message sent or received within the context of an RPC call.

**Signal Type:** Event

**Event Name:** `rpc.message`

**Description:** In the lifetime of an RPC stream, an event for each message sent/received on client and server spans SHOULD be created. In case of unary calls only one sent and one received message will be recorded for both client and server spans.

**Attributes:**

|Key|Type|Summary|Examples|Requirement|Stability|
|---|---|---|---|---|--|
| [`rpc.system`](attribute-custom.md) | [rpc.system](type-custom.md) | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc`; `java_rmi`; `dotnet_wcf` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.message.compressed_size`](attribute-custom.md) | int | Compressed size of the message in bytes. |  | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.message.id`](attribute-custom.md) | int | MUST be calculated as two different counters starting from `1` one for sent messages and one for received message. |  | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.message.type`](attribute-custom.md) | string | Whether this is a received or sent message. | `SENT`; `RECEIVED` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`rpc.message.uncompressed_size`](attribute-custom.md) | int | Uncompressed size of the message in bytes. |  | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

**Body:**

|Body Field|Type|Summary|Examples|Requirement|Stability|
|---|---|---|---|---|---|
| `content` | undefined | The contents of the tool message. | `The weather in Paris is rainy and overcast, with temperatures around 57°F` | `Opt-In` | ![Development](https://img.shields.io/badge/-development-blue) |

**Entity Associations:**

|Entity|Summary|Stability|
|---|---|---|
|[`service`](entity-custom.md)|A service instance.|![Development](https://img.shields.io/badge/-development-blue) |
