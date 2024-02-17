<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Connection Metrics
--->

# Semantic Conventions for Connection Metrics

This document defines semantic conventions to apply when instrumenting client side of socket connections with metrics.

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Common attributes](#common-attributes)
- [Metric: `connection.client.connect_duration`](#metric-connectionclientconnect_duration)
- [Metric: `connection.client.duration`](#metric-connectionclientduration)
- [Metric: `connection.client.open_connections`](#metric-connectionclientopen_connections)

<!-- tocstop -->

## Common attributes

All connection metrics share the same set of attributes:

<!-- semconv metric_attributes.connection.client(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`error.type`](../attributes-registry/error.md) | string | Describes a class of error the operation ended with. [1] | `econnreset`; `econnrefused`; `address_family_not_supported`; `java.net.SocketException` | Conditionally Required: [2] |
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. [3] | `10.1.2.80`; `/tmp/my.sock` | Recommended: see the note below |
| [`network.peer.port`](../attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | Recommended: if `network.peer.address` is set.` |
| [`network.transport`](../attributes-registry/network.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [4] | `tcp`; `udp` | Recommended |
| [`network.type`](../attributes-registry/network.md) | string | [OSI network layer](https://osi-model.com/network-layer/) or non-OSI equivalent. [5] | `ipv4`; `ipv6` | Recommended |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [6] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Conditionally Required: if available without reverse DNS lookup |

**[1]:** It's REQUIRED to document error types instrumentation produces. It's RECOMMENDED to use a connection error code if it's provided by the socket library, runtime, or the OS (such as `connect` method error code on [Linux or other POSIX systems](https://man7.org/linux/man-pages/man2/connect.2.html#ERRORS) / [Windows](https://docs.microsoft.com/windows/win32/api/winsock2/nf-winsock2-connect#return-value)).

**[2]:** If and only if a connection (attempt) ended with an error.

**[3]:** The `network.peer.address` could be of a high cardinality. In practice, however, its cardinality is limited to the number of distinct IP addresses for the given domain name, which is small when destination service is behind a load balancer or NAT.
Connection instrumentations MAY set `network.peer.address` by default, or let users opt into collecting it. If instrumentation collects `network.peer.address` by default, it MUST allow users to opt-out of `network.peer.address` collection or disable collection of all connection metrics that set the attribute.

**[4]:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[5]:** The value SHOULD be normalized to lowercase.

**[6]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. |

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Metric: `connection.client.connect_duration`

This metric is [recommended][MetricRequirementLevel].

<!-- semconv metric.connection.client.connect_duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `connection.client.connect_duration` | Histogram | `s` | The duration of the attempt to establish connection. |
<!-- endsemconv -->

## Metric: `connection.client.duration`

This metric is [recommended][MetricRequirementLevel].

<!-- semconv metric.connection.client.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `connection.client.duration` | Histogram | `s` | The duration of the successfully established outbound connection. |
<!-- endsemconv -->

## Metric: `connection.client.open_connections`

This metric is [recommended][MetricRequirementLevel].

<!-- semconv metric.connection.client.open_connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `connection.client.open_connections` | UpDownCounter | `{connection}` | Number of outbound connections that are currently open (active or idle) on the client. |
<!-- endsemconv -->

[MetricRequirementLevel]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/metrics/metric-requirement-level.md
[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
