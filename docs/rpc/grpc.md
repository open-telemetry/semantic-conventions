<!--- Hugo front matter used to generate the website version of this page:
linkTitle: gRPC
--->

# Semantic Conventions for gRPC

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [gRPC](https://grpc.io/) extend and override the [RPC spans](rpc-spans.md) and [RPC metrics](rpc-metrics.md) Semantic Conventions
that describe common RPC operations attributes in addition to the Semantic Conventions
described on this page.

## gRPC Attributes

`rpc.system` MUST be set to `"grpc"`.

Below is a table of attributes that SHOULD be included on client and server gRPC measurements.

<!-- semconv rpc.grpc(full,tag=grpc-tech-specific) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`rpc.grpc.status_code`](../attributes-registry/rpc.md) | int | The [numeric status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md) of the gRPC request. | `0` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`rpc.grpc.request.metadata.<key>`](../attributes-registry/rpc.md) | string[] | gRPC request metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. [1] | `rpc.grpc.request.metadata.my-custom-metadata-attribute=["1.2.3.4", "1.2.3.5"]` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`rpc.grpc.response.metadata.<key>`](../attributes-registry/rpc.md) | string[] | gRPC response metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. [2] | `rpc.grpc.response.metadata.my-custom-metadata-attribute=["attribute_value"]` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all request metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

**[2]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all response metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

`rpc.grpc.status_code` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `0` | OK | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `1` | CANCELLED | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `2` | UNKNOWN | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `3` | INVALID_ARGUMENT | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `4` | DEADLINE_EXCEEDED | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `5` | NOT_FOUND | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `6` | ALREADY_EXISTS | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `7` | PERMISSION_DENIED | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `8` | RESOURCE_EXHAUSTED | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `9` | FAILED_PRECONDITION | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `10` | ABORTED | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `11` | OUT_OF_RANGE | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `12` | UNIMPLEMENTED | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `13` | INTERNAL | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `14` | UNAVAILABLE | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `15` | DATA_LOSS | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `16` | UNAUTHENTICATED | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## gRPC Status

The table below describes when
the [Span Status](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/trace/api.md#set-status) MUST be set
to `Error` or remain unset
depending on the [gRPC status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md)
and [Span Kind](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/trace/api.md#spankind).

| gRPC Status Code | `SpanKind.SERVER` Span Status | `SpanKind.CLIENT` Span Status |
|---|---|---|
| OK | unset | unset |
| CANCELLED | unset | `Error` |
| UNKNOWN | `Error` | `Error`  |
| INVALID_ARGUMENT | unset | `Error` |
| DEADLINE_EXCEEDED | `Error` | `Error` |
| NOT_FOUND | unset | `Error` |
| ALREADY_EXISTS | unset | `Error` |
| PERMISSION_DENIED | unset | `Error` |
| RESOURCE_EXHAUSTED | unset| `Error` |
| FAILED_PRECONDITION | unset | `Error` |
| ABORTED | unset | `Error` |
| OUT_OF_RANGE | unset | `Error` |
| UNIMPLEMENTED | `Error` | `Error` |
| INTERNAL | `Error` | `Error` |
| UNAVAILABLE | `Error` | `Error` |
| DATA_LOSS | `Error` | `Error` |
| UNAUTHENTICATED | unset | `Error` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
