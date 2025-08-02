<!--To eventually be auto-generated based upon implementations with data grouped based on namespace of scope-->
# RPC

**Summary:** This document defines how to describe remote procedure calls (also called “remote method invocations” / “RMI”) with spans.

> [!IMPORTANT]  Namespace was stablised in v1.20
>
> When migrating from an earlier version of semantic conventions, the migration document should be followed. [Migration Guide](#rpc)

**Description:** The conventions described in this section are RPC specific. When RPC operations occur, measurements about those operations are recorded to instruments. The measurements are aggregated and exported as metrics, which provide insight into those operations. By including RPC properties as attributes on measurements, the metrics can be filtered for finer grain analysis.

## Instrumentation: [`rpc.grpc`](grpc/README.md)

**Summary:** The gRPC scope is for all instrumentation which communicates via rpc using `grpc` technology.

**Description:** This is a description.

The definition of the measurements are available via [grpc definitions](grpc/README.md).

## Instrumentation: [`rpc.connect`](grpc/README.md)

**Summary:** The connect scope is for all instrumentation which communicates via rpc using `connect` technology.

**Description:** This is a description.

The definition of the measurements are available via [Connect definitions](grpc/README.md).

## Instrumentation: [`rpc.json_rpc`](grpc/README.md)

**Summary:** The connect scope is for all instrumentation which communicates via rpc using `json_rpc` technology.

**Description:** This is a description.

The definition of the measurements are available via [JSON RPC definitions](grpc/README.md).
