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

<!-- semconv rpc.connect_rpc -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `rpc.connect_rpc.error_code` | string | The [error codes](https://connect.build/docs/protocol/#error-codes) of the Connect request. Error codes are always string values. | `cancelled` | Conditionally Required: [1] |

**[1]:** If response is not successful and if error code available.

`rpc.connect_rpc.error_code` MUST be one of the following:

| Value  | Description |
|---|---|
| `cancelled` | cancelled |
| `unknown` | unknown |
| `invalid_argument` | invalid_argument |
| `deadline_exceeded` | deadline_exceeded |
| `not_found` | not_found |
| `already_exists` | already_exists |
| `permission_denied` | permission_denied |
| `resource_exhausted` | resource_exhausted |
| `failed_precondition` | failed_precondition |
| `aborted` | aborted |
| `out_of_range` | out_of_range |
| `unimplemented` | unimplemented |
| `internal` | internal |
| `unavailable` | unavailable |
| `data_loss` | data_loss |
| `unauthenticated` | unauthenticated |
<!-- endsemconv -->

## Connect RPC Status

If `rpc.connect_rpc.error_code` is set, [Span Status](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/trace/api.md#set-status) MUST be set to `Error` and left unset in all other cases.

## Connect RPC Request and Response Metadata

| Attribute                                 | Type     | Description                                                                                                                                                             | Examples                                                                   | Requirement Level |
|-------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|-------------------|
| `rpc.connect_rpc.request.metadata.<key>`  | string[] | Connect request metadata, `<key>` being the normalized Connect Metadata key (lowercase, with `-` characters replaced by `_`), the value being the metadata values. [1]  | `rpc.request.metadata.my_custom_metadata_attribute=["1.2.3.4", "1.2.3.5"]` | Optional          |
| `rpc.connect_rpc.response.metadata.<key>` | string[] | Connect response metadata, `<key>` being the normalized Connect Metadata key (lowercase, with `-` characters replaced by `_`), the value being the metadata values. [1] | `rpc.response.metadata.my_custom_metadata_attribute=["attribute_value"]`   | Optional          |

**[1]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured.
Including all request/response metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
