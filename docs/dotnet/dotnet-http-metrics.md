# Semantic Conventions for HTTP-relevant metrics emitted by .NET

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This document defines semantic conventions for HTTP metrics emitted by .NET components and runtime.

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

All Http client metrics are reported by `System.Net.Http` meter.

### Metric: `http.client.request.duration`

Client request duration measures time it takes to receive response headers and does not include time to read response body.

This metric follows common [http.client.request.duration](../http/http-metrics.md#metric-httpclientrequestduration) definition.

Notes:

- Meter name is `System.Net.Http`
- Metric added in .NET 8.0
- When `error.type` attribute is reported, it contains one of [HTTP Request errors](https://github.com/dotnet/runtime/blob/main/src/libraries/System.Net.Http/src/System/Net/Http/HttpRequestError.cs), a full exception type, or a string representation of received status code.

### Metric: `http.client.open_connections`

<!-- semconv metric.dotnet.http.client.open_connections(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.open_connections` | UpDownCounter | `{connection}` | Number of outbound HTTP connections that are currently active or idle on the client [1] |

**[1]:** Meter name: `System.Net.Http`; Added in: .NET 8.0
<!-- endsemconv -->

<!-- semconv metric.dotnet.http.client.open_connections(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `http.connection.state` | string | State of HTTP connection in the HTTP connection pool. | `active`; `idle` | Required |
| [`network.peer.address`](../general/attributes.md) | string | Remote IP address of the socket connection. | `10.1.2.80` | Recommended |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [1] | `1.1`; `2` | Recommended |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [3] | `80`; `8080`; `443` | Conditionally Required: [4] |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https`; `ftp` | Recommended |

**[1]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[2]:** Determined by using the first of the following that applies

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form
- Host identifier of the `Host` header

**[3]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is absolute URI, `server.port` MUST match URI port identifier, otherwise it MUST match `Host` header port identifier.

**[4]:** If not default (`80` for `http` scheme, `443` for `https`).

`http.connection.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `active` | active state. |
| `idle` | idle state. |
<!-- endsemconv -->

### Metric: `http.client.connection.duration`

<!-- semconv metric.dotnet.http.client.connection.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.connection.duration` | Histogram | `s` | The duration of successfully established outbound HTTP connections. [1] |

**[1]:** Meter name: `System.Net.Http`; Added in: .NET 8.0
<!-- endsemconv -->

<!-- semconv metric.dotnet.http.client.connection.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.peer.address`](../general/attributes.md) | string | Remote IP address of the socket connection. | `10.1.2.80` | Recommended |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [1] | `1.1`; `2` | Recommended |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [3] | `80`; `8080`; `443` | Conditionally Required: [4] |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https`; `ftp` | Recommended |

**[1]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[2]:** Determined by using the first of the following that applies

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form
- Host identifier of the `Host` header

**[3]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is absolute URI, `server.port` MUST match URI port identifier, otherwise it MUST match `Host` header port identifier.

**[4]:** If not default (`80` for `http` scheme, `443` for `https`).
<!-- endsemconv -->

### Metric: `http.client.request.time_in_queue`

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
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [2] | `1.1`; `2` | Recommended |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [3] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [4] | `80`; `8080`; `443` | Conditionally Required: [5] |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https`; `ftp` | Recommended |

**[1]:** HTTP request method value SHOULD be "known" to the instrumentation.
By default, this convention defines "known" methods as the ones listed in [RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-methods)
and the PATCH method defined in [RFC5789](https://www.rfc-editor.org/rfc/rfc5789.html).

If the HTTP request method is not known to instrumentation, it MUST set the `http.request.method` attribute to `_OTHER`.

If the HTTP instrumentation could end up converting valid HTTP request methods to `_OTHER`, then it MUST provide a way to override
the list of known HTTP methods. If this override is done via environment variable, then the environment variable MUST be named
OTEL_INSTRUMENTATION_HTTP_KNOWN_METHODS and support a comma-separated list of case-sensitive known HTTP methods
(this list MUST be a full override of the default known method, it is not a list of known methods in addition to the defaults).

HTTP method names are case-sensitive and `http.request.method` attribute value MUST match a known HTTP method name exactly.
Instrumentations for specific web frameworks that consider HTTP methods to be case insensitive, SHOULD populate a canonical equivalent.
Tracing instrumentations that do so, MUST also set `http.request.method_original` to the original value.

**[2]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[3]:** Determined by using the first of the following that applies

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form
- Host identifier of the `Host` header

**[4]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is absolute URI, `server.port` MUST match URI port identifier, otherwise it MUST match `Host` header port identifier.

**[5]:** If not default (`80` for `http` scheme, `443` for `https`).

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
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [2] | `1.1`; `2` | Recommended |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [3] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [4] | `80`; `8080`; `443` | Conditionally Required: [5] |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https`; `ftp` | Recommended |

**[1]:** HTTP request method value is one of the "known" methods listed in [RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-methods)
and the PATCH method defined in [RFC5789](https://www.rfc-editor.org/rfc/rfc5789.html).

If the HTTP request method is not known, it sets the `http.request.method` attribute to `_OTHER`.

It is not possible at the moment to override the list of known HTTP methods.

**[2]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[3]:** Determined by using the first of the following that applies

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form
- Host identifier of the `Host` header

**[4]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is absolute URI, `server.port` MUST match URI port identifier, otherwise it MUST match `Host` header port identifier.

**[5]:** If not default (`80` for `http` scheme, `443` for `https`).

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

All HTTP server metrics are reported by `Microsoft.AspNetCore.Hosting` meter.

### Metric: `http.server.request.duration`

Measures time to last byte. This metric follows common [http.server.request.duration](../http/http-metrics.md#metric-httpserverrequestduration) definition.

Notes:

- Meter name is `Microsoft.AspNetCore.Hosting`
- Metric added in ASP.NET Core 8.0
- Opt-in `server.address` and `server.port` attributes are not reported
- Additional attributes:

  - The `aspnetcore.request.is_unhandled` boolean attribute is reported when the request was **not** handled by the application pipeline. It's skipped otherwise.

### Metric: `http.server.active_requests`

Measures the number of HTTP requests that are currently active on the server. This metric follows common [http.server.active_requests](../http/http-metrics.md#metric-httpserveractive_requests) definition.

Notes:

- Meter name is `Microsoft.AspNetCore.Hosting`
- Opt-in `server.address` and `server.port` attributes are not reported
- Metric added in ASP.NET Core 8.0

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
