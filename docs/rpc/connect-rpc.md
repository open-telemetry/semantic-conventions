<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Connect
--->

# Semantic Conventions for Connect RPC

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Connect](http://connect.build) extend and override the [RPC spans](rpc-spans.md) and [RPC metrics](rpc-metrics.md) Semantic Conventions
that describe common RPC operations attributes in addition to the Semantic Conventions
described on this page.

## Connect RPC Attributes

`rpc.system` MUST be set to `"connect_rpc"`.

Below is a table of attributes that SHOULD be included on client and server Connect RPC measurements.

<!-- semconv rpc.connect_rpc(full,tag=connect_rpc-tech-specific) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`rpc.connect_rpc.error_code`](../attributes-registry/rpc.md) | string | The [error codes](https://connect.build/docs/protocol/#error-codes) of the Connect request. Error codes are always string values. | `cancelled` | `Conditionally Required` [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`rpc.connect_rpc.request.metadata.<key>`](../attributes-registry/rpc.md) | string[] | Connect request metadata, `<key>` being the normalized Connect Metadata key (lowercase), the value being the metadata values. [2] | `rpc.request.metadata.my-custom-metadata-attribute=["1.2.3.4", "1.2.3.5"]` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`rpc.connect_rpc.response.metadata.<key>`](../attributes-registry/rpc.md) | string[] | Connect response metadata, `<key>` being the normalized Connect Metadata key (lowercase), the value being the metadata values. [3] | `rpc.response.metadata.my-custom-metadata-attribute=["attribute_value"]` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If response is not successful and if error code available.

**[2]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all request metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

**[3]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all response metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

`rpc.connect_rpc.error_code` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `cancelled` | cancelled | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `unknown` | unknown | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `invalid_argument` | invalid_argument | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `deadline_exceeded` | deadline_exceeded | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `not_found` | not_found | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `already_exists` | already_exists | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `permission_denied` | permission_denied | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `resource_exhausted` | resource_exhausted | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `failed_precondition` | failed_precondition | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aborted` | aborted | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `out_of_range` | out_of_range | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `unimplemented` | unimplemented | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `internal` | internal | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `unavailable` | unavailable | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `data_loss` | data_loss | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `unauthenticated` | unauthenticated | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Connect RPC Status

If `rpc.connect_rpc.error_code` is set, [Span Status](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/trace/api.md#set-status) MUST be set to `Error` and left unset in all other cases.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
