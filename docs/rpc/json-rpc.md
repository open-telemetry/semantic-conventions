<!--- Hugo front matter used to generate the website version of this page:
linkTitle: JSON-RPC
--->

# Semantic Conventions for JSON-RPC

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [JSON-RPC](https://www.jsonrpc.org/) extend and override the [RPC spans](rpc-spans.md) and [RPC metrics](rpc-metrics.md) Semantic Conventions
that describe common RPC operations attributes in addition to the Semantic Conventions
described on this page.

## JSON-RPC Attributes

`rpc.system` MUST be set to `"jsonrpc"`.

<!-- semconv rpc.jsonrpc -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `rpc.jsonrpc.error_code` | int | `error.code` property of response if it is an error response. | `-32700`; `100` | Conditionally Required: If response is not successful. |
| `rpc.jsonrpc.error_message` | string | `error.message` property of response if it is an error response. | `Parse error`; `User already exists` | Recommended |
| `rpc.jsonrpc.request_id` | string | `id` property of request or response. Since protocol allows id to be int, string, `null` or missing (for notifications), value is expected to be cast to string for simplicity. Use empty string in case of `null` value. Omit entirely if this is a notification. | `10`; `request-7`; `` | Recommended |
| `rpc.jsonrpc.version` | string | Protocol version as in `jsonrpc` property of request/response. Since JSON-RPC 1.0 doesn't specify this, the value can be omitted. | `2.0`; `1.0` | Conditionally Required: If other than the default version (`1.0`) |
| [`rpc.method`](rpc-spans.md) | string | The name of the (logical) method being called, must be equal to the $method part in the span name. [1] | `exampleMethod` | Required |

**[1]:** This is always required for jsonrpc. See the note in the general RPC conventions for more information.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
