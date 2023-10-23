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

<!-- semconv rpc.grpc -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `rpc.grpc.request.metadata.<key>` | string[] | gRPC request metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. [1] | `rpc.grpc.request.metadata.my-custom-metadata-attribute=["1.2.3.4", "1.2.3.5"]` | Opt-In |
| `rpc.grpc.response.metadata.<key>` | string[] | gRPC response metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. [2] | `rpc.grpc.response.metadata.my-custom-metadata-attribute=["attribute_value"]` | Opt-In |
| `rpc.grpc.status_code` | int | The [numeric status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md) of the gRPC request. | `0` | Required |

**[1]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all request metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

**[2]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all response metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

`rpc.grpc.status_code` MUST be one of the following:

| Value  | Description |
|---|---|
| `0` | OK |
| `1` | CANCELLED |
| `2` | UNKNOWN |
| `3` | INVALID_ARGUMENT |
| `4` | DEADLINE_EXCEEDED |
| `5` | NOT_FOUND |
| `6` | ALREADY_EXISTS |
| `7` | PERMISSION_DENIED |
| `8` | RESOURCE_EXHAUSTED |
| `9` | FAILED_PRECONDITION |
| `10` | ABORTED |
| `11` | OUT_OF_RANGE |
| `12` | UNIMPLEMENTED |
| `13` | INTERNAL |
| `14` | UNAVAILABLE |
| `15` | DATA_LOSS |
| `16` | UNAUTHENTICATED |
<!-- endsemconv -->

## gRPC Status

The table below describes when
the [Span Status](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/trace/api.md#set-status) MUST be set
to `Error` or remain unset
depending on the [gRPC status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md)
and [Span Kind](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/trace/api.md#spankind).

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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
