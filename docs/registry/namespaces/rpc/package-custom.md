# RPC

**Summary:** This document defines how to describe remote procedure calls (also called “remote method invocations” / “RMI”) with spans.

> [!IMPORTANT]  Namespace was stablised in v1.20
>
> When migrating from an earlier version of semantic conventions, the migration document should be followed. [Migration Guide](#rpc)

**Description:** The conventions described in this section are RPC specific. When RPC operations occur, measurements about those operations are recorded to instruments. The measurements are aggregated and exported as metrics, which provide insight into those operations. By including RPC properties as attributes on measurements, the metrics can be filtered for finer grain analysis.

---------------------------------

## RPC Client Command

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

**Summary:** Client commands are for non streaming scenarios

**Description:** This is..

**Signals:**

|Name|Signal Type|Summary|[Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) |Stability|
|---|---|---|---|---|
|[`rpc.message`](event-custom.md)|Event|Describes a message sent or received within the context of an RPC call.|`Opt-in`|![Development](https://img.shields.io/badge/-development-blue) |
|[`rpc.server.duration`](metric-custom.md)|Metric|Measures the duration of inbound RPC.|`Recommended`|![Development](https://img.shields.io/badge/-development-blue) |
|[`rpc.client`](span-custom.md)|Span|This span represents an outgoing Remote Procedure Call (RPC).|`Required`|![Development](https://img.shields.io/badge/-development-blue) |
