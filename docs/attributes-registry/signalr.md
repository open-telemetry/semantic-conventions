# ASP.NET Core

<!-- toc -->

- [SignalR Attributes](#signalr-attributes)

<!-- tocstop -->

## SignalR Attributes

<!-- semconv registry.signalr(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `signalr.connection.status` | string | SignalR HTTP connection closure status. | `app_shutdown`; `timeout` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `signalr.transport` | string | [SignalR transport type](https://github.com/dotnet/aspnetcore/blob/main/src/SignalR/docs/specs/TransportProtocols.md) | `web_sockets`; `long_polling` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`signalr.connection.status` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `normal_closure` | The connection was closed normally. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `timeout` | The connection was closed due to a timeout. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `app_shutdown` | The connection was closed because the app is shutting down. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`signalr.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `server_sent_events` | ServerSentEvents protocol | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `long_polling` | LongPolling protocol | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `web_sockets` | WebSockets protocol | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->