# Semantic Conventions for Model Context Protocol (MCP)

## Background

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open protocol for interactions between applications and AI models, supporting structured input and output formats. As MCP adoption grows, there's a need to establish semantic conventions for telemetry to ensure consistent observability across implementations.

## Proposal

This issue proposes semantic conventions for [Model Context Protocol operations](https://github.com/modelcontextprotocol/specification) to standardize how traces, metrics, and logs are reported across MCP client and server implementations.

The conventions are based on the [`2025-3-26`](https://github.com/modelcontextprotocol/specification/tree/main/docs/specification/2025-03-26) version of the MCP specification.

While MCP is intended as primarily for extending gen_ai LLM tool calling, its not strictly tied to being used in gen_ai scenarios. For that reason, the MCP attributes being proposed user their own independent namespace.
MCP uses JSON-RPC for it's calling implementation. The MCP attributes cover the higher-level MCP semantics irrespective of the transport and RPC details. It is recommended that implementations use separate spans for JSON-RPC and MCP, but they can be overlaid if necessary as the attributes have been designed not to conflict.

These conventions do not document how the trace context needs to be propagated from the client to the server. Changes to the MCP protocol will be needed to enable that proagation. Proposals are being made to the MCP specification.

## Spans

### MCP Session

An MCP session represents the lifecycle of a connection between a client and server.

| Attribute | Type | Description | Examples | Required |
|---|---|---|---|---|
| `mcp.session.id` | string | Identifier for the MCP session | `c52f5ef3-c7a1-4f7a-a2e3-e38a7a4966d2` | Yes |
| `mcp.transport` | string | Transport mechanism used | `streamable-http`, `stdio` | No |

#### Span creation

- Create a span when an MCP session is established and end it when the session is terminated
- Span name: `mcp.session`

### MCP Operation

An MCP operation represents a complete client-server interaction for methods such as tool calls, prompt retrieval, and other protocol-defined operations.

| Attribute | Type | Description | Examples | Required |
|---|---|---|---|---|
| `mcp.session.id` | string | Identifier for the MCP session | `c52f5ef3-c7a1-4f7a-a2e3-e38a7a4966d2` | No |
| `mcp.request.type` | string | The MCP operation being performed | `tools.call`, `prompts.get` | Yes |
| `mcp.request.name` | string | Name of the tool or prompt, or URI template for resource | `GetFileInfo`, `file://path/to/file` | No |
| `mcp.request.parameter.<key>` | string | parameter values for tool calls, prompts or substitutions in URI templates | `New York` | No |
| `mcp.request.id` | string | Identifier for the message | `msg_01234567` | No |
| `mcp.client.name` | string | Name of the MCP client | `mcp-js-client` | No |
| `mcp.client.version` | string | Version of the MCP client | `1.0.0` | No |
| `mcp.server.name` | string | Name of the MCP server | `mcp-cs-server` | No |
| `mcp.server.version` | string | Version of the MCP server | `1.0.0` | No |
| `mcp.notification.method` | string | Method for resource change notifications | `notifications/resources/list_changed` | No | 

The schema for MCP attributes does not change according to the type of MCP call that is being made. The attribute pair of `mcp.request.type` and `mcp.request.name` will provide the type and target of the mcp call.
For resource calls, the name should be the URI template for the request, without any value substitutions.

`mcp.request.parameter.<key>` can be used to log parameters for MCP tool calls and prompts, and for URI template substitutions for resources. As the parameter values are the most likely to contain sensitive or PII information, emitting these values should be guarded behind a flag or other implementation specific control mechanism to only emit the data when safe to do so, for example when running under a debugger.

#### Span creation

For clients:
- Create a span when an MCP request is initiated and end it when the response is received
- Span name: `mcp.<request.type>/<name>`, e.g., `mcp.tools.call/GetFileInfo`

For servers:
- Create a span when an MCP request is received and end it when the response is sent
- Span name: `mcp.<request.type>/<name>`, e.g., `mcp.tools.call/GetFileInfo`

## Metrics

### MCP Session Duration

| Name | Instrument | Unit | Description |
|---|---|---|---|
| `mcp.session.duration` | Histogram | s | Measures the duration of an MCP session in seconds |

this metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.43.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 30, 60, 120, 300]`.

#### MCP Operation Duration

| Name | Instrument | Unit | Description |
|---|---|---|---|
| `mcp.request.duration` | Histogram | s | Measures the duration of an MCP operation in seconds |

this metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.43.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

> Note: These durations are different from those for http, as the http semantic conventions changed their units to seconds, but have not updated the histogram buckets to match.

Attributes:
| Attribute | Type | Description | Examples | Required |
|---|---|---|---|---|
| `mcp.request.type` | string | The MCP operation being performed | `tools.call`, `prompts.get` | Yes |
| `mcp.request.name` | string | Name of the tool or prompt, or URI template for resource | `GetFileInfo`, `file://path/to/file` | No |

## Rationale

These conventions align with existing patterns in the OpenTelemetry ecosystem, particularly following similar patterns to HTTP semantic conventions and those for JSON-RPC. They provide consistent naming and structure across implementations while capturing the unique aspects of the Model Context Protocol.

## Implementation Status

Initial support for OpenTelemetry has been implemented in the [C# SDK for MCP](https://github.com/modelcontextprotocol/csharp-sdk/pull/183), which includes:
- Activity tracking for message handling
- Metrics for operation duration
- Appropriate naming conventions and attributes

## References

- [Model Context Protocol Specification](https://github.com/modelcontextprotocol/specification)
- [HTTP Semantic Conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-spans.md)
- [C# SDK OpenTelemetry Implementation](https://github.com/modelcontextprotocol/csharp-sdk/pull/183)
