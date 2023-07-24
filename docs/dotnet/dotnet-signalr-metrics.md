# Semantic Conventions for SignalR metrics emitted by ASP.NET Core 8.0

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This document defines semantic conventions for SignalR metrics emitted by .NET components and runtime.

<!-- toc -->

- [Metric: `signalr.server.connection.duration`](#metric-signalrserverconnectionduration)
- [Metric: `signalr.server.active_connections`](#metric-signalrserveractive_connections)

<!-- tocstop -->

## Metric: `signalr.server.connection.duration`

<!-- semconv metric.signalr.server.connection.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `signalr.server.connection.duration` | Histogram | `s` | The duration of connections on the server. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Http.Connections`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.signalr.server.connection.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `signalr.connection.status` | string | SignalR HTTP connection closure status. | `app_shutdown`; `timeout` | Recommended |
| `signalr.transport` | string | [SignalR transport type](https://github.com/dotnet/aspnetcore/blob/main/src/SignalR/docs/specs/TransportProtocols.md) | `web_sockets`; `long_polling` | Recommended |

`signalr.connection.status` MUST be one of the following:

| Value  | Description |
|---|---|
| `normal_closure` | The connection was closed normally. |
| `timeout` | The connection was closed due to a timeout. |
| `app_shutdown` | The connection was closed because the app is shutting down. |

`signalr.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `server_sent_events` | ServerSentEvents protocol |
| `long_polling` | LongPolling protocol |
| `web_sockets` | WebSockets protocol |
<!-- endsemconv -->

## Metric: `signalr.server.active_connections`

<!-- semconv metric.signalr.server.active_connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `signalr.server.active_connections` | UpDownCounter | `{connection}` | Number of connections that are currently active on the server. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Http.Connections`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.signalr.server.active_connections(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `signalr.connection.status` | string | SignalR HTTP connection closure status. | `app_shutdown`; `timeout` | Recommended |
| `signalr.transport` | string | [SignalR transport type](https://github.com/dotnet/aspnetcore/blob/main/src/SignalR/docs/specs/TransportProtocols.md) | `web_sockets`; `long_polling` | Recommended |

`signalr.connection.status` MUST be one of the following:

| Value  | Description |
|---|---|
| `normal_closure` | The connection was closed normally. |
| `timeout` | The connection was closed due to a timeout. |
| `app_shutdown` | The connection was closed because the app is shutting down. |

`signalr.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `server_sent_events` | ServerSentEvents protocol |
| `long_polling` | LongPolling protocol |
| `web_sockets` | WebSockets protocol |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
