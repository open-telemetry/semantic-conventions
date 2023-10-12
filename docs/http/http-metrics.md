<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
--->

# Semantic Conventions for HTTP Metrics

**Status**: [Experimental, partial feature-freeze][DocumentStatus]

The conventions described in this section are HTTP specific. When HTTP operations occur,
metric events about those operations will be generated and reported to provide insight into the
operations. By adding HTTP attributes to metric events it allows for finely tuned filtering.

**Disclaimer:** These are initial HTTP metric instruments and attributes but more may be added in the future.

<!-- toc -->

- [HTTP Server](#http-server)
  * [Metric: `http.server.request.duration`](#metric-httpserverrequestduration)
  * [Metric: `http.server.active_requests`](#metric-httpserveractive_requests)
  * [Metric: `http.server.request.body.size`](#metric-httpserverrequestbodysize)
  * [Metric: `http.server.response.body.size`](#metric-httpserverresponsebodysize)
- [HTTP Client](#http-client)
  * [Metric: `http.client.request.duration`](#metric-httpclientrequestduration)
  * [Metric: `http.client.request.body.size`](#metric-httpclientrequestbodysize)
  * [Metric: `http.client.response.body.size`](#metric-httpclientresponsebodysize)

<!-- tocstop -->

> **Warning**
> Existing HTTP instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/metrics/semantic_conventions/http-metrics.md)
> (or prior):
>
> * SHOULD NOT change the version of the HTTP or networking conventions that they emit
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking conventions which are also used
>   in HTTP instrumentations). Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The only values defined so far are:
>   * `http` - emit the new, stable HTTP and networking conventions,
>     and stop emitting the old experimental HTTP and networking conventions
>     that the instrumentation emitted previously.
>   * `http/dup` - emit both the old and the stable HTTP and networking conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental HTTP and networking conventions
>     the instrumentation was emitting previously.
>   * Note: `http/dup` has higher precedence than `http` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version (stable
>   next major version SHOULD NOT be released prior to October 1, 2023).

## HTTP Server

### Metric: `http.server.request.duration`

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This metric is required.

When this metric is reported alongside an HTTP server span, the metric value SHOULD be the same as the HTTP server span duration.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advice)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.http.server.request.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.server.request.duration` | Histogram | `s` | Duration of HTTP server requests. |
<!-- endsemconv -->

<!-- semconv metric.http.server.request.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `name_resolution_error`; `500` | Conditionally Required: If request has ended with an error. |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [2] | `GET`; `POST`; `HEAD` | Required |
| [`http.response.status_code`](../attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: If and only if one was received/sent. |
| [`http.route`](../attributes-registry/http.md) | string | The matched route (path template in the format used by the respective server framework). See note below [3] | `/users/:userID?`; `{controller}/{action}/{id?}` | Conditionally Required: If and only if it's available |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [4] | `1.0`; `1.1`; `2`; `3` | Recommended |
| [`server.address`](../general/attributes.md) | string | Name of the local HTTP server that received the request. [5] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Opt-In |
| [`server.port`](../general/attributes.md) | int | Port of the local HTTP server that received the request. [6] | `80`; `8080`; `443` | Opt-In |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https` | Required |

**[1]:** If the request fails with an error before response status code was sent or received,
`error.type` SHOULD be set to exception type or a component-specific low cardinality error code.

If response status code was sent or received and status indicates an error according to [HTTP span status definition](/docs/http/http-spans.md),
`error.type` SHOULD be set to the status code number (represented as a string), an exception type (if thrown) or a component-specific error code.

The `error.type` value SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the request has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[3]:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[5]:** Determined by using the first of the following that applies

- The [primary server name](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host. MUST only
  include host identifier.
- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Host identifier of the `Host` header

SHOULD NOT be set if only IP address is available and capturing name would require a reverse DNS lookup.

**[6]:** Determined by using the first of the following that applies

- Port identifier of the [primary server host](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host.
- Port identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Port identifier of the `Host` header

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |

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

### Metric: `http.server.active_requests`

**Status**: [Experimental][DocumentStatus]

This metric is optional.

<!-- semconv metric.http.server.active_requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.server.active_requests` | UpDownCounter | `{request}` | Number of active HTTP server requests. |
<!-- endsemconv -->

<!-- semconv metric.http.server.active_requests(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [1] | `GET`; `POST`; `HEAD` | Required |
| [`server.address`](../general/attributes.md) | string | Name of the local HTTP server that received the request. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Opt-In |
| [`server.port`](../general/attributes.md) | int | Port of the local HTTP server that received the request. [3] | `80`; `8080`; `443` | Opt-In |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https` | Required |

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

**[2]:** Determined by using the first of the following that applies

- The [primary server name](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host. MUST only
  include host identifier.
- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Host identifier of the `Host` header

SHOULD NOT be set if only IP address is available and capturing name would require a reverse DNS lookup.

**[3]:** Determined by using the first of the following that applies

- Port identifier of the [primary server host](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host.
- Port identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Port identifier of the `Host` header

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

### Metric: `http.server.request.body.size`

**Status**: [Experimental][DocumentStatus]

This metric is optional.

<!-- semconv metric.http.server.request.body.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.server.request.body.size` | Histogram | `By` | Size of HTTP server request bodies. [1] |

**[1]:** The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size.
<!-- endsemconv -->

<!-- semconv metric.http.server.request.body.size(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `name_resolution_error`; `500` | Conditionally Required: If request has ended with an error. |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [2] | `GET`; `POST`; `HEAD` | Required |
| [`http.response.status_code`](../attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: If and only if one was received/sent. |
| [`http.route`](../attributes-registry/http.md) | string | The matched route (path template in the format used by the respective server framework). See note below [3] | `/users/:userID?`; `{controller}/{action}/{id?}` | Conditionally Required: If and only if it's available |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [4] | `1.0`; `1.1`; `2`; `3` | Recommended |
| [`server.address`](../general/attributes.md) | string | Name of the local HTTP server that received the request. [5] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Opt-In |
| [`server.port`](../general/attributes.md) | int | Port of the local HTTP server that received the request. [6] | `80`; `8080`; `443` | Opt-In |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https` | Required |

**[1]:** If the request fails with an error before response status code was sent or received,
`error.type` SHOULD be set to exception type or a component-specific low cardinality error code.

If response status code was sent or received and status indicates an error according to [HTTP span status definition](/docs/http/http-spans.md),
`error.type` SHOULD be set to the status code number (represented as a string), an exception type (if thrown) or a component-specific error code.

The `error.type` value SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the request has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[3]:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[5]:** Determined by using the first of the following that applies

- The [primary server name](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host. MUST only
  include host identifier.
- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Host identifier of the `Host` header

SHOULD NOT be set if only IP address is available and capturing name would require a reverse DNS lookup.

**[6]:** Determined by using the first of the following that applies

- Port identifier of the [primary server host](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host.
- Port identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Port identifier of the `Host` header

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |

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

### Metric: `http.server.response.body.size`

**Status**: [Experimental][DocumentStatus]

This metric is optional.

<!-- semconv metric.http.server.response.body.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.server.response.body.size` | Histogram | `By` | Size of HTTP server response bodies. [1] |

**[1]:** The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size.
<!-- endsemconv -->

<!-- semconv metric.http.server.response.body.size(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `name_resolution_error`; `500` | Conditionally Required: If request has ended with an error. |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [2] | `GET`; `POST`; `HEAD` | Required |
| [`http.response.status_code`](../attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: If and only if one was received/sent. |
| [`http.route`](../attributes-registry/http.md) | string | The matched route (path template in the format used by the respective server framework). See note below [3] | `/users/:userID?`; `{controller}/{action}/{id?}` | Conditionally Required: If and only if it's available |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [4] | `1.0`; `1.1`; `2`; `3` | Recommended |
| [`server.address`](../general/attributes.md) | string | Name of the local HTTP server that received the request. [5] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Opt-In |
| [`server.port`](../general/attributes.md) | int | Port of the local HTTP server that received the request. [6] | `80`; `8080`; `443` | Opt-In |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https` | Required |

**[1]:** If the request fails with an error before response status code was sent or received,
`error.type` SHOULD be set to exception type or a component-specific low cardinality error code.

If response status code was sent or received and status indicates an error according to [HTTP span status definition](/docs/http/http-spans.md),
`error.type` SHOULD be set to the status code number (represented as a string), an exception type (if thrown) or a component-specific error code.

The `error.type` value SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the request has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[3]:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[5]:** Determined by using the first of the following that applies

- The [primary server name](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host. MUST only
  include host identifier.
- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Host identifier of the `Host` header

SHOULD NOT be set if only IP address is available and capturing name would require a reverse DNS lookup.

**[6]:** Determined by using the first of the following that applies

- Port identifier of the [primary server host](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host.
- Port identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Port identifier of the `Host` header

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |

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

## HTTP Client

### Metric: `http.client.request.duration`

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This metric is required.

When this metric is reported alongside an HTTP client span, the metric value SHOULD be the same as the HTTP client span duration.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advice)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.http.client.request.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.request.duration` | Histogram | `s` | Duration of HTTP client requests. |
<!-- endsemconv -->

<!-- semconv metric.http.client.request.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `name_resolution_error`; `500` | Conditionally Required: If request has ended with an error. |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [2] | `GET`; `POST`; `HEAD` | Required |
| [`http.response.status_code`](../attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: If and only if one was received/sent. |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [3] | `1.0`; `1.1`; `2`; `3` | Recommended |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [4] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [5] | `80`; `8080`; `443` | Conditionally Required: [6] |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `https`; `ftp`; `telnet` | Required |

**[1]:** If the request fails with an error before response status code was sent or received,
`error.type` SHOULD be set to exception type or a component-specific low cardinality error code.

If response status code was sent or received and status indicates an error according to [HTTP span status definition](/docs/http/http-spans.md),
`error.type` SHOULD be set to the status code number (represented as a string), an exception type (if thrown) or a component-specific error code.

The `error.type` value SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the request has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[3]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[4]:** Determined by using the first of the following that applies

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form
- Host identifier of the `Host` header

If an HTTP client request is explicitly made to an IP address, e.g. `http://x.x.x.x:8080`, then
`server.address` SHOULD be the IP address `x.x.x.x`. A DNS lookup SHOULD NOT be used.

**[5]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is absolute URI, `server.port` MUST match URI port identifier, otherwise it MUST match `Host` header port identifier.

**[6]:** If not default (`80` for `http` scheme, `443` for `https`).

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |

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

### Metric: `http.client.request.body.size`

**Status**: [Experimental][DocumentStatus]

This metric is optional.

<!-- semconv metric.http.client.request.body.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.request.body.size` | Histogram | `By` | Size of HTTP client request bodies. [1] |

**[1]:** The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size.
<!-- endsemconv -->

<!-- semconv metric.http.client.request.body.size(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `name_resolution_error`; `500` | Conditionally Required: If request has ended with an error. |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [2] | `GET`; `POST`; `HEAD` | Required |
| [`http.response.status_code`](../attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: If and only if one was received/sent. |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [3] | `1.0`; `1.1`; `2`; `3` | Recommended |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [4] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [5] | `80`; `8080`; `443` | Conditionally Required: [6] |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `https`; `ftp`; `telnet` | Required |

**[1]:** If the request fails with an error before response status code was sent or received,
`error.type` SHOULD be set to exception type or a component-specific low cardinality error code.

If response status code was sent or received and status indicates an error according to [HTTP span status definition](/docs/http/http-spans.md),
`error.type` SHOULD be set to the status code number (represented as a string), an exception type (if thrown) or a component-specific error code.

The `error.type` value SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the request has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[3]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[4]:** Determined by using the first of the following that applies

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form
- Host identifier of the `Host` header

If an HTTP client request is explicitly made to an IP address, e.g. `http://x.x.x.x:8080`, then
`server.address` SHOULD be the IP address `x.x.x.x`. A DNS lookup SHOULD NOT be used.

**[5]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is absolute URI, `server.port` MUST match URI port identifier, otherwise it MUST match `Host` header port identifier.

**[6]:** If not default (`80` for `http` scheme, `443` for `https`).

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |

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

### Metric: `http.client.response.body.size`

**Status**: [Experimental][DocumentStatus]

This metric is optional.

<!-- semconv metric.http.client.response.body.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `http.client.response.body.size` | Histogram | `By` | Size of HTTP client response bodies. [1] |

**[1]:** The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size.
<!-- endsemconv -->

<!-- semconv metric.http.client.response.body.size(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `name_resolution_error`; `500` | Conditionally Required: If request has ended with an error. |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [2] | `GET`; `POST`; `HEAD` | Required |
| [`http.response.status_code`](../attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: If and only if one was received/sent. |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [3] | `1.0`; `1.1`; `2`; `3` | Recommended |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [4] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [5] | `80`; `8080`; `443` | Conditionally Required: [6] |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `https`; `ftp`; `telnet` | Required |

**[1]:** If the request fails with an error before response status code was sent or received,
`error.type` SHOULD be set to exception type or a component-specific low cardinality error code.

If response status code was sent or received and status indicates an error according to [HTTP span status definition](/docs/http/http-spans.md),
`error.type` SHOULD be set to the status code number (represented as a string), an exception type (if thrown) or a component-specific error code.

The `error.type` value SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the request has completed successfully, instrumentations SHOULD NOT set `error.type`.

**[2]:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[3]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[4]:** Determined by using the first of the following that applies

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form
- Host identifier of the `Host` header

If an HTTP client request is explicitly made to an IP address, e.g. `http://x.x.x.x:8080`, then
`server.address` SHOULD be the IP address `x.x.x.x`. A DNS lookup SHOULD NOT be used.

**[5]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is absolute URI, `server.port` MUST match URI port identifier, otherwise it MUST match `Host` header port identifier.

**[6]:** If not default (`80` for `http` scheme, `443` for `https`).

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |

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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
