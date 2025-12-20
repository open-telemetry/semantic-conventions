<!--- Hugo front matter used to generate the website version of this page:
linkTitle: gRPC
--->

<!-- disable mdlint requirement for tables to be aligned -->
<!-- markdownlint-disable-file MD060 -->

# Compatibility between OpenTelemetry and gRPC semantic conventions

<!-- toc -->

- [Metrics](#metrics)
  - [`grpc.client.call.duration` (gRPC conventions)](#grpcclientcallduration-grpc-conventions)
  - [`grpc.server.call.duration` (gRPC conventions)](#grpcservercallduration-grpc-conventions)
  - [Other metrics](#other-metrics)
- [Spans](#spans)

<!-- tocstop -->

The gRPC project defines conventions for [OpenTelemetry Metrics](https://github.com/grpc/proposal/blob/master/A66-otel-stats.md)
and experimental conventions for [OpenTelemetry Tracing](https://github.com/grpc/proposal/blob/master/A72-open-telemetry-tracing.md).

These conventions differ from OpenTelemetry [gRPC](/docs/rpc/grpc.md) conventions
hosted in this repository.

This document provides mappings (where applicable) between the official OpenTelemetry
conventions hosted in this repository and native gRPC conventions.

## Metrics

See [gRPC conventions](https://github.com/grpc/proposal/blob/master/A66-otel-stats.md)
and [OpenTelemetry conventions](/docs/rpc/rpc-metrics.md) for details.

Attribute mapping:

| gRPC attribute     | OpenTelemetry attribute(s)         | Conversion comments  |
| :----------------- | :--------------------------------- | :------------------- |
| `grpc.method`      | `rpc.method`                       | gRPC -> OTel: when value is `other`, replace it with `_OTHER`<br>OTel -> gRPC: when value is `_OTHER`, replace it with `other` |
| `grpc.status`      | `rpc.response.status_code`         | |
| `grpc.target`      | `server.address` and `server.port` | gRPC -> OTel: parse address and port from the [gRPC target string](https://grpc.io/docs/guides/custom-name-resolution/) authority or path (depending on the scheme)<br>OTel -> gRPC: set `grpc.target` to `{server.address}:{server.port}` (scheme cannot be determined) |
|                    | `rpc.system.name`                  | gRPC -> OTel: set to `grpc`<br>OTel -> gRPC: drop |
|                    | `error.type`                       | gRPC -> OTel: set to `rpc.response.status_code` when it indicates an error (see [gRPC OpenTelemetry conventions](/docs/rpc/grpc.md))<br>OTel -> gRPC: drop |

OpenTelemetry defines a few other (non-required) gRPC metric attributes listed below. When converting from gRPC to OTel metrics or vice versa, these attributes should not be set:

- `network.protocol.name`
- `network.protocol.version`
- `network.transport`

### `grpc.client.call.duration` (gRPC conventions)

OpenTelemetry equivalent: [`rpc.client.call.duration`](/docs/rpc/rpc-metrics.md#metric-rpcclientcallduration).

Both metrics cover the end-to-end duration of an RPC call from the client perspective and
are recorded as histograms with seconds as the unit.

### `grpc.server.call.duration` (gRPC conventions)

OpenTelemetry equivalent: [`rpc.server.call.duration`](/docs/rpc/rpc-metrics.md#metric-rpcservercallduration).

Both metrics cover the end-to-end duration of an RPC call from the server perspective and
are recorded as histograms with seconds as the unit.

### Other metrics

The following gRPC metrics don't have an OpenTelemetry equivalent:

- Client:
  - `grpc.client.attempt.started`
  - `grpc.client.attempt.duration`
  - `grpc.client.attempt.sent_total_compressed_message_size`
  - `grpc.client.attempt.rcvd_total_compressed_message_size`
- Server:
  - `grpc.server.call.started`
  - `grpc.server.call.sent_total_compressed_message_size`
  - `grpc.server.call.rcvd_total_compressed_message_size`

> [!NOTE]
>
> OpenTelemetry defines [`rpc.client.request.size`](/docs/rpc/rpc-metrics.md#metric-rpcclientrequestsize)
> and [`rpc.client.response.size`](/docs/rpc/rpc-metrics.md#metric-rpcclientresponsesize)
> which are similar to `grpc.client.attempt.sent_total_compressed_message_size`
> and `grpc.client.attempt.rcvd_total_compressed_message_size`, however, OpenTelemetry
> metrics measure uncompressed size and are recorded once per call even if the call involved
> multiple attempts.
>
> OpenTelemetry also defines experimental [`rpc.server.request.size`](/docs/rpc/rpc-metrics.md#metric-rpcserverrequestsize)
> and [`rpc.server.response.size`](/docs/rpc/rpc-metrics.md#metric-rpcserverresponsesize)
> which are similar to `grpc.server.call.sent_total_compressed_message_size`
> and `grpc.server.call.rcvd_total_compressed_message_size`, however, OpenTelemetry
> metrics measure uncompressed size and, for streaming RPCs, record the size of each
> individual message as separate data points.

## Spans

gRPC conventions define two types of **client** spans: call and attempt.
The gRPC call span maps to the OpenTelemetry RPC client span. Both span types cover the end-to-end duration
of the client call. OpenTelemetry does not define a per-attempt span.

In case of **server** span, both gRPC and OpenTelemetry conventions define one
per-call server span.

Mapping:

| Property                | gRPC                                                             | OpenTelemetry                                                                | Conversion comments                                      |
| :---------------------- | :--------------------------------------------------------------- | :--------------------------------------------------------------------------- | :-------------------------------------------------------- |
| Span name               | `Sent.{method name}` (client)<br>`Recv.{method name}` (server)   | `{rpc.method}`                                                               | gRPC -> OTel: remove `Sent.` or `Recv.` prefix<br>OTel -> gRPC: add prefix based on span kind |
| Span status code        | `ERROR` when response status code is not `OK`                    | `ERROR` for specific error status codes (see gRPC conventions)               | gRPC -> OTel: parse `rpc.response.status_code` from status description and set span status code accordingly (see [gRPC OpenTelemetry conventions](/docs/rpc/grpc.md)) |
| Span status description | Code and description, e.g., `UNAVAILABLE, unable to resolve host`| Description only (error code is recorded separately)                         | |
| Attributes              |                                                                  | `rpc.system.name`                                                            | gRPC -> OTel: set to `grpc`<br>OTel -> gRPC: drop |
|                         |                                                                  | `rpc.method`                                                                 | gRPC -> OTel: parse from span name<br>OTel -> gRPC: drop |
|                         |                                                                  | `rpc.response.status_code`                                                   | gRPC -> OTel: parse from status description<br>OTel -> gRPC: drop |

OpenTelemetry defines a few other (non-required) gRPC span attributes listed below. When converting from gRPC spans to OTel spans or vice versa, these attributes should not be set:

- `network.peer.address`
- `network.peer.port`
- `network.protocol.name`
- `network.protocol.version`
- `network.transport`
- `server.address`
- `server.port`
- (server span only) `client.address` and `client.port`

gRPC spans contain additional events that could be recorded as is when converting
OpenTelemetry.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
