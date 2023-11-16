<!--- Hugo front matter used to generate the website version of this page:
linkTitle: HTTP client and server
--->

# Semantic Conventions for HTTP client and server metrics emitted by .NET

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This article defines semantic conventions for HTTP metrics emitted by .NET components and runtime.

<!-- toc -->

- [HTTP client](#http-client)
  * [Metric: `http.client.request.duration`](#metric-httpclientrequestduration)
  * [Metric: `http.client.open_connections`](#metric-httpclientopen_connections)
  * [Metric: `http.client.connection.duration`](#metric-httpclientconnectionduration)
  * [Metric: `http.client.request.time_in_queue`](#metric-httpclientrequesttime_in_queue)
  * [Metric: `http.client.active_requests`](#metric-httpclientactive_requests)
- [HTTP server](#http-server)
  * [Metric: `http.server.request.duration`](#metric-httpserverrequestduration)
  * [Metric: `http.server.active_requests`](#metric-httpserveractive_requests)

<!-- tocstop -->

## HTTP client

All Http client metrics are reported by the `System.Net.Http` meter.

### Metric: `http.client.request.duration`

Client request duration measures the time it takes to receive response headers and doesn't include time to read the response body.

This metric follows the common [http.client.request.duration](../http/http-metrics.md#metric-httpclientrequestduration) definition.

Notes:

- Meter name is `System.Net.Http`
- Metric added in .NET 8.0
- When the `error.type` attribute is reported, it contains one of [HTTP Request errors](https://learn.microsoft.com/dotnet/api/system.net.http.httprequesterror) in snake_case, a full exception type, or a string representation of received status code.

### Metric: `http.client.open_connections`

<!-- semconv metric.dotnet.http.client.open_connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.open_connections` | UpDownCounter | `{connection}` | Number of outbound HTTP connections that are currently active or idle on the client. [1] |

**[1]:** Meter name: `System.Net.Http`; Added in: .NET 8.0
<!-- endsemconv -->

<!-- semconv metric.dotnet.http.client.open_connections(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `http.connection.state` | string | State of the HTTP connection in the HTTP connection pool. | `active`; `idle` | Required |
| [`network.peer.address`](../attributes-registry/network.md) | string | Remote IP address of the socket connection. | `10.1.2.80` | Recommended |
| [`network.protocol.version`](../attributes-registry/network.md) | string | Version of the protocol specified in `network.protocol.name`. [1] | `1.1`; `2` | Recommended |
| [`server.address`](../attributes-registry/server.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) the HTTP request is sent to. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../attributes-registry/server.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) the HTTP request is sent to. [3] | `80`; `8080`; `443` | Conditionally Required: [4] |
| [`url.scheme`](../attributes-registry/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https`; `ftp` | Recommended |

**[1]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[2]:** Determined by using the first of the following that applies:

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) if it's sent in absolute-form.
- Host identifier of the `Host` header.

**[3]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is an absolute URI, `server.port` MUST match the URI port identifier; otherwise, it MUST match the `Host` header port identifier.

**[4]:** If not the default (`80` for `http` scheme, `443` for `https`).

`http.connection.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `active` | active state. |
| `idle` | idle state. |
<!-- endsemconv -->

### Metric: `http.client.connection.duration`

this metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 30, 60, 120, 300 ]`.

<!-- semconv metric.dotnet.http.client.connection.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.connection.duration` | Histogram | `s` | The duration of the successfully established outbound HTTP connections. [1] |

**[1]:** Meter name: `System.Net.Http`; Added in: .NET 8.0
<!-- endsemconv -->

<!-- semconv metric.dotnet.http.client.connection.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`network.protocol.version`](../attributes-registry/network.md) | string | Version of the protocol specified in `network.protocol.name`. [1] | `1.1`; `2` | Recommended |
| [`server.address`](../attributes-registry/server.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) the HTTP request is sent to. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../attributes-registry/server.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) the HTTP request is sent to. [3] | `80`; `8080`; `443` | Conditionally Required: [4] |
| [`url.scheme`](../attributes-registry/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https`; `ftp` | Recommended |

**[1]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[2]:** Determined by using the first of the following that applies:

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) if it's sent in absolute-form.
- Host identifier of the `Host` header.

**[3]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is an absolute URI, `server.port` MUST match the URI port identifier; otherwise, it MUST match the `Host` header port identifier.

**[4]:** If not the default (`80` for `http` scheme, `443` for `https`).
<!-- endsemconv -->

### Metric: `http.client.request.time_in_queue`

this metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.


<!-- semconv metric.dotnet.http.client.request.time_in_queue(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.request.time_in_queue` | Histogram | `s` | The amount of time requests spent on a queue waiting for an available connection. [1] |

**[1]:** Meter name: `System.Net.Http`; Added in: .NET 8.0
<!-- endsemconv -->

<!-- semconv metric.dotnet.http.client.request.time_in_queue(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [1] | `GET`; `POST`; `HEAD` | Recommended |
| [`network.protocol.version`](../attributes-registry/network.md) | string | Version of the protocol specified in `network.protocol.name`. [2] | `1.1`; `2` | Recommended |
| [`server.address`](../attributes-registry/server.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) the HTTP request is sent to. [3] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../attributes-registry/server.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) the HTTP request is sent to. [4] | `80`; `8080`; `443` | Conditionally Required: [5] |
| [`url.scheme`](../attributes-registry/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https`; `ftp` | Recommended |

**[1]:** HTTP request method value is one of the "known" methods listed in [RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-methods) and the PATCH method defined in [RFC5789](https://www.rfc-editor.org/rfc/rfc5789.html).
If the HTTP request method isn't known, it sets the `http.request.method` attribute to `_OTHER`.
It's not possible at the moment to override the list of known HTTP methods.

**[2]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[3]:** Determined by using the first of the following that applies:

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) if it's sent in absolute-form.
- Host identifier of the `Host` header.

**[4]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is an absolute URI, `server.port` MUST match the URI port identifier; otherwise, it MUST match the `Host` header port identifier.

**[5]:** If not the default (`80` for `http` scheme, `443` for `https`).

`http.request.method` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `CONNECT` | CONNECT method. |
| `DELETE` | DELETE method. |
| `GET` | GET method. |
| `HEAD` | HEAD method. |
| `OPTIONS` | OPTIONS method. |
| `PATCH` | PATCH method. |
| `POST` | POST method. |
| `PUT` | PUT method. |
| `TRACE` | TRACE method. |
| `_OTHER` | Any HTTP method that the instrumentation has no prior knowledge of. |
<!-- endsemconv -->

### Metric: `http.client.active_requests`

<!-- semconv metric.dotnet.http.client.active_requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.active_requests` | UpDownCounter | `{request}` | Number of active HTTP requests. [1] |

**[1]:** Meter name: `System.Net.Http`; Added in: .NET 8.0
<!-- endsemconv -->

<!-- semconv metric.dotnet.http.client.active_requests(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [1] | `GET`; `POST`; `HEAD` | Recommended |
| [`server.address`](../attributes-registry/server.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) the HTTP request is sent to. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../attributes-registry/server.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) the HTTP request is sent to. [3] | `80`; `8080`; `443` | Conditionally Required: [4] |
| [`url.scheme`](../attributes-registry/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https`; `ftp` | Recommended |

**[1]:** HTTP request method value is one of the "known" methods listed in [RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-methods) and the PATCH method defined in [RFC5789](https://www.rfc-editor.org/rfc/rfc5789.html).
If the HTTP request method isn't known, it sets the `http.request.method` attribute to `_OTHER`.
It's not possible at the moment to override the list of known HTTP methods.

**[2]:** Determined by using the first of the following that applies:

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) if it's sent in absolute-form.
- Host identifier of the `Host` header.

**[3]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is an absolute URI, `server.port` MUST match the URI port identifier; otherwise, it MUST match the `Host` header port identifier.

**[4]:** If not the default (`80` for `http` scheme, `443` for `https`).

`http.request.method` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `CONNECT` | CONNECT method. |
| `DELETE` | DELETE method. |
| `GET` | GET method. |
| `HEAD` | HEAD method. |
| `OPTIONS` | OPTIONS method. |
| `PATCH` | PATCH method. |
| `POST` | POST method. |
| `PUT` | PUT method. |
| `TRACE` | TRACE method. |
| `_OTHER` | Any HTTP method that the instrumentation has no prior knowledge of. |
<!-- endsemconv -->

## HTTP server

All HTTP server metrics are reported by the `Microsoft.AspNetCore.Hosting` meter.

### Metric: `http.server.request.duration`

Measures time to last byte. This metric follows the common [http.server.request.duration](../http/http-metrics.md#metric-httpserverrequestduration) definition.

Notes:

- Meter name is `Microsoft.AspNetCore.Hosting`
- Metric added in ASP.NET Core 8.0
- Opt-in `server.address` and `server.port` attributes are not reported
- Additional attributes:

  - The `aspnetcore.request.is_unhandled` boolean attribute is reported when the request was **not** handled by the application pipeline. It's skipped otherwise.

### Metric: `http.server.active_requests`

Measures the number of HTTP requests that are currently active on the server. This metric follows the common [http.server.active_requests](../http/http-metrics.md#metric-httpserveractive_requests) definition.

Notes:

- Meter name is `Microsoft.AspNetCore.Hosting`
- Opt-in `server.address` and `server.port` attributes are not reported
- Metric added in ASP.NET Core 8.0

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
