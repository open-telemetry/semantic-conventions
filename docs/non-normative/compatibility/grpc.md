<!--- Hugo front matter used to generate the website version of this page:
linkTitle: gRPC
--->

<!-- disable mdlint requirement for tables to be aligned -->
<!-- markdownlint-disable-file MD060 -->

# Compatibility between OpenTelemetry and gRPC semantic conventions

<!-- toc -->

- [Metrics](#metrics)
- [Spans](#spans)

<!-- tocstop -->

The gRPC project defines conventions for [OpenTelemetry Metrics](https://github.com/grpc/proposal/blob/master/A66-otel-stats.md)
and experimental conventions for [OpenTelemetry Tracing](https://github.com/grpc/proposal/blob/master/A72-open-telemetry-tracing.md).

These conventions differ from the [OpenTelemetry gRPC](/docs/rpc/grpc.md) conventions
hosted in this repository.

This document provides mappings (where applicable) between the OpenTelemetry
conventions hosted in this repository and the native gRPC conventions.

## Metrics

See the [gRPC conventions](https://github.com/grpc/proposal/blob/master/A66-otel-stats.md)
and the [OpenTelemetry conventions](/docs/rpc/rpc-metrics.md) for details.

Metric mapping:

| gRPC metric                                              | OpenTelemetry metric       | Conversion comments                                           |
| :------------------------------------------------------- | :------------------------- | :------------------------------------------------------------ |
| `grpc.client.call.duration`                              | `rpc.client.call.duration` | See the attribute mapping below; metrics are equivalent otherwise |
| `grpc.server.call.duration`                              | `rpc.server.call.duration` | See the attribute mapping below; metrics are equivalent otherwise |
| `grpc.client.attempt.started`                            | no equivalent              |                                                               |
| `grpc.client.attempt.duration`                           | no equivalent              |                                                               |
| `grpc.client.attempt.sent_total_compressed_message_size` | no equivalent              |                                                               |
| `grpc.client.attempt.rcvd_total_compressed_message_size` | no equivalent              |                                                               |
| `grpc.server.call.started`                               | no equivalent              |                                                               |
| `grpc.server.call.sent_total_compressed_message_size`    | no equivalent              |                                                               |
| `grpc.server.call.rcvd_total_compressed_message_size`    | no equivalent              |                                                               |

Attribute mapping:

| gRPC attribute     | OpenTelemetry attribute(s)         | Conversion comments  |
| :----------------- | :--------------------------------- | :------------------- |
| `grpc.method`      | `rpc.method`                       | gRPC -> OTel: when the value is `other`, replace it with `_OTHER`<br>OTel -> gRPC: when the value is `_OTHER`, replace it with `other` |
| `grpc.status`      | `rpc.response.status_code`         | |
| `grpc.target`      | `grpc.target`                      | gRPC -> OTel: preserve `grpc.target` if it contains information that's not captured in `server.address` and `server.port`<br>OTel -> gRPC: preserve `grpc.target` if present; otherwise, set `grpc.target` to `{server.address}:{server.port}` |
|                    | `server.address` and `server.port` | gRPC -> OTel: parse the address and port from `grpc.target` (when applicable)<br>OTel -> gRPC: drop |
|                    | `rpc.system.name`                  | gRPC -> OTel: set to `grpc`<br>OTel -> gRPC: drop |
|                    | `error.type`                       | gRPC -> OTel: set to `rpc.response.status_code` when it indicates an error (see [gRPC OpenTelemetry conventions](/docs/rpc/grpc.md))<br>OTel -> gRPC: drop |

## Spans

See the [gRPC conventions](https://github.com/grpc/proposal/blob/master/A72-open-telemetry-tracing.md)
and the [OpenTelemetry conventions](/docs/rpc/rpc-spans.md) for details.

The gRPC conventions define two types of **client** spans: call and attempt.
The gRPC call span maps to the OpenTelemetry RPC client span. Both span types cover the end-to-end duration
of the client call. OpenTelemetry does not define a per-attempt span.

In the case of **server** spans, both the gRPC and OpenTelemetry conventions define one
per-call server span.

Mapping:

| Property                | gRPC                                                             | OpenTelemetry                                                                | Conversion comments                                      |
| :---------------------- | :--------------------------------------------------------------- | :--------------------------------------------------------------------------- | :-------------------------------------------------------- |
| Span name               | `Sent.{method name}` (client)<br>`Recv.{method name}` (server)<br>Note: The gRPC span name *may be* of high cardinality in edge cases.  | `{rpc.method}`                                                               | gRPC -> OTel: remove the `Sent.` or `Recv.` prefix<br>OTel -> gRPC: add the prefix based on the span kind |
| Span status code        | `ERROR` when the response status code is not `OK`                | `ERROR` for specific error status codes (see the gRPC conventions)           | gRPC -> OTel: parse `rpc.response.status_code` from the status description and set the span status code accordingly (see the [gRPC OpenTelemetry conventions](/docs/rpc/grpc.md)) |
| Span status description | Code and description (e.g., `UNAVAILABLE, unable to resolve host`)| Description only (the error code is recorded separately)                     | |
| Attributes              |                                                                  | `rpc.system.name`                                                            | gRPC -> OTel: set to `grpc`<br>OTel -> gRPC: drop |
|                         |                                                                  | `rpc.method`                                                                 | gRPC -> OTel: parse from the span name<br>OTel -> gRPC: drop |
|                         |                                                                  | `rpc.response.status_code`                                                   | gRPC -> OTel: parse from the status description<br>OTel -> gRPC: drop |

OpenTelemetry defines a few other (non-required) gRPC span attributes listed below. When converting from gRPC spans to OpenTelemetry spans or vice versa, these attributes should not be set:

- `network.peer.address`
- `network.peer.port`
- `server.address`
- `server.port`
- `rpc.request.metadata.<key>` and `rpc.response.metadata.<key>`
- `rpc.method_original`
- (server spans only) `client.address` and `client.port`

gRPC spans may contain additional events that can be recorded as-is when converting to
OpenTelemetry.
