# Semantic Conventions for Model Context Protocol (MCP)

## Background

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open protocol for interactions between applications and AI models, supporting structured input and output formats. As MCP adoption grows, there's a need to establish semantic conventions for telemetry to ensure consistent observability across implementations.

## Proposal

This issue proposes semantic conventions for [Model Context Protocol operations](https://github.com/modelcontextprotocol/specification) to standardize how traces, metrics, and logs are reported across MCP client and server implementations.

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
| `mcp.request.method` | string | The MCP operation being performed | `tools.call`, `prompts.get` | Yes |
| `mcp.session.id` | string | Identifier for the MCP session | `c52f5ef3-c7a1-4f7a-a2e3-e38a7a4966d2` | No |
| `mcp.request.id` | string | Identifier for the message | `msg_01234567` | No |
| `mcp.client.name` | string | Name of the MCP client | `mcp-js-client` | No |
| `mcp.client.version` | string | Version of the MCP client | `1.0.0` | No |
| `mcp.server.name` | string | Name of the MCP server | `mcp-cs-server` | No |
| `mcp.server.version` | string | Version of the MCP server | `1.0.0` | No |
| `mcp.request.params.name` | string | Name of the tool or prompt | `GetFileInfo` | No |
| `mcp.request.params.uri` | string | URI of a requested resource | `file://path/to/file` | No |
| `mcp.notification.method` | string | Method for resource change notifications | `notifications/resources/list_changed` | No | 


#### Span creation

For clients:
- Create a span when an MCP request is initiated and end it when the response is received
- Span name: `mcp.<operation>`, e.g., `mcp.tools.call`


For servers:
- Create a span when an MCP request is received and end it when the response is sent
- Span name: `mcp.<operation>`, e.g., `mcp.tools.call`

## Metrics

### MCP Session Duration

| Name | Instrument | Unit | Description |
|---|---|---|---|
| `mcp.session.duration` | Histogram | s | Measures the duration of an MCP session in seconds |

this metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.43.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 30, 60, 120, 300 ]`.

#### MCP Operation Duration

| Name | Instrument | Unit | Description |
|---|---|---|---|
| `mcp.request.duration` | Histogram | s | Measures the duration of an MCP operation in seconds |

this metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.43.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]` to match those for http.

Attributes:
- `mcp.request.method`: The MCP operation being performed
- `mcp.status`: Success or error status of the operation

## Rationale

These conventions align with existing patterns in the OpenTelemetry ecosystem, particularly following similar patterns to HTTP semantic conventions. They provide consistent naming and structure across implementations while capturing the unique aspects of the Model Context Protocol.

## Implementation Status

Initial support for OpenTelemetry has been implemented in the [C# SDK for MCP](https://github.com/modelcontextprotocol/csharp-sdk/pull/183), which includes:
- Activity tracking for message handling
- Metrics for operation duration
- Appropriate naming conventions and attributes

## References

- [Model Context Protocol Specification](https://github.com/modelcontextprotocol/specification)
- [HTTP Semantic Conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/http/http-spans.md)
- [C# SDK OpenTelemetry Implementation](https://github.com/modelcontextprotocol/csharp-sdk/pull/183)
