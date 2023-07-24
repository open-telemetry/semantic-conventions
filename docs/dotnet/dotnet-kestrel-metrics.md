# Semantic Conventions for Kestrel web server metrics emitted by .NET

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This document defines semantic conventions for Kestrel web server.

<!-- toc -->

- [Kestrel endpoint](#kestrel-endpoint)
- [Metric: `kestrel.active_connections`](#metric-kestrelactive_connections)
- [Metric: `kestrel.connection.duration`](#metric-kestrelconnectionduration)
- [Metric: `kestrel.rejected_connections`](#metric-kestrelrejected_connections)
- [Metric: `kestrel.queued_connections`](#metric-kestrelqueued_connections)
- [Metric: `kestrel.queued_requests`](#metric-kestrelqueued_requests)
- [Metric: `kestrel.upgraded_connections`](#metric-kestrelupgraded_connections)
- [Metric: `kestrel.tls_handshake.duration`](#metric-kestreltls_handshakeduration)
- [Metric: `kestrel.active_tls_handshakes`](#metric-kestrelactive_tls_handshakes)

<!-- tocstop -->

## Kestrel endpoint

Kestrel endpoint is represented with [`System.Net.EndPoint`](https://learn.microsoft.com/en-us/dotnet/api/system.net.endpoint) class,
which does not always provide information about server address or port.

Instrumentation supports `IPEndPoint`, `UnixDomainSocketEndPoint`, and `NamedPipeEndPoint` and sets `server.address`, `server.port` (for IP endpoint), `network.type`, and `network.transport` attributes from corresponding endpoint on Kestrel metrics.

In case instrumentation does not recognize `EndPoint` implementation, it sets `server.address` attribute to `endpoint.ToString()` value
and `network.transport` value to corresponding `endpoint.AddressFamily` property.

## Metric: `kestrel.active_connections`

<!-- semconv metric.kestrel.active_connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `kestrel.active_connections` | UpDownCounter | `{connection}` | Number of connections that are currently active on the server. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Server.Kestrel`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.kestrel.active_connections(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `unix` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended: if the transport is `tcp` or `udp` |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Server port number [2] | `80`; `8080`; `443` | Recommended |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. See note below. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Metric: `kestrel.connection.duration`

<!-- semconv metric.kestrel.connection.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `kestrel.connection.duration` | Histogram | `s` | The duration of connections on the server. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Server.Kestrel`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.kestrel.connection.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `exception.type` | string | The full name of exception type. | `System.OperationCanceledException`; `Contoso.MyException` | Conditionally Required: if and only if an exception was thrown. |
| [`network.protocol.name`](../general/attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `http`; `web_sockets` | Recommended |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the application layer protocol used. See note below. [1] | `1.1`; `2` | Recommended |
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `unix` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended: if the transport is `tcp` or `udp` |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Server port number [3] | `80`; `8080`; `443` | Recommended |
| `tls.protocol.version` | string | TLS protocol version. | `1.2`; `1.3` | Conditionally Required: if the connection is secured with TLS. |

**[1]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[3]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. See note below. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Metric: `kestrel.rejected_connections`

<!-- semconv metric.kestrel.rejected_connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `kestrel.rejected_connections` | Counter | `{connection}` | Number of connections rejected by the server. [1] |

**[1]:** Connections are rejected when the currently active count exceeds the value configured with MaxConcurrentConnections.
Meter name: `Microsoft.AspNetCore.Server.Kestrel`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.kestrel.rejected_connections(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `unix` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended: if the transport is `tcp` or `udp` |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Server port number [2] | `80`; `8080`; `443` | Recommended |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. See note below. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Metric: `kestrel.queued_connections`

<!-- semconv metric.kestrel.queued_connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `kestrel.queued_connections` | UpDownCounter | `{connection}` | Number of connections that are currently queued and are waiting to start. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Server.Kestrel`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.kestrel.queued_connections(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `unix` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended: if the transport is `tcp` or `udp` |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Server port number [2] | `80`; `8080`; `443` | Recommended |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. See note below. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Metric: `kestrel.queued_requests`

<!-- semconv metric.kestrel.queued_requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `kestrel.queued_requests` | UpDownCounter | `{request}` | Number of HTTP requests on multiplexed connections (HTTP/2 and HTTP/3) that are currently queued and are waiting to start. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Server.Kestrel`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.kestrel.queued_requests(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.protocol.name`](../general/attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `http`; `web_sockets` | Recommended |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the application layer protocol used. See note below. [1] | `1.1`; `2` | Recommended |
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `unix` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended: if the transport is `tcp` or `udp` |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Server port number [3] | `80`; `8080`; `443` | Recommended |

**[1]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[3]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. See note below. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Metric: `kestrel.upgraded_connections`

<!-- semconv metric.kestrel.upgraded_connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `kestrel.upgraded_connections` | UpDownCounter | `{connection}` | Number of connections that are currently upgraded (WebSockets). . [1] |

**[1]:** The counter only tracks HTTP/1.1 connections.

Meter name: `Microsoft.AspNetCore.Server.Kestrel`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.kestrel.upgraded_connections(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `unix` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended: if the transport is `tcp` or `udp` |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Server port number [2] | `80`; `8080`; `443` | Recommended |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. See note below. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Metric: `kestrel.tls_handshake.duration`

<!-- semconv metric.kestrel.tls_handshake.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `kestrel.tls_handshake.duration` | Histogram | `s` | The duration of TLS handshakes on the server. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Server.Kestrel`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.kestrel.tls_handshake.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `exception.type` | string | The full name of exception type. | `System.OperationCanceledException`; `Contoso.MyException` | Conditionally Required: if and only if an exception was thrown. |
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `unix` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended: if the transport is `tcp` or `udp` |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Server port number [2] | `80`; `8080`; `443` | Recommended |
| `tls.protocol.version` | string | TLS protocol version. | `1.2`; `1.3` | Conditionally Required: if the connection is secured with TLS. |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. See note below. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Metric: `kestrel.active_tls_handshakes`

<!-- semconv metric.kestrel.active_tls_handshakes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `kestrel.active_tls_handshakes` | UpDownCounter | `{handshake}` | Number of TLS handshakes that are currently in progress on the server. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Server.Kestrel`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.kestrel.active_tls_handshakes(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. Consider always setting the transport when setting a port number, since a port number is ambiguous without knowing the transport, for example different processes could be listening on TCP port 12345 and UDP port 12345. | `tcp`; `unix` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended: if the transport is `tcp` or `udp` |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Server port number [2] | `80`; `8080`; `443` | Recommended |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. See note below. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
