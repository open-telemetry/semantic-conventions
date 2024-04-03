<!--- Hugo front matter used to generate the website version of this page:
--->

# HTTP

## HTTP Attributes

<!-- semconv registry.http(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `http.connection.state` | string | State of the HTTP connection in the HTTP connection pool. | `active`; `idle` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http.request.body.size` | int | The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http.request.header.<key>` | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [1] | `http.request.header.content-type=["application/json"]`; `http.request.header.x-forwarded-for=["1.2.3.4", "1.2.3.5"]` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `http.request.method` | string | HTTP request method. [2] | `GET`; `POST`; `HEAD` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `http.request.method_original` | string | Original HTTP method sent by the client in the request line. | `GeT`; `ACL`; `foo` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `http.request.resend_count` | int | The ordinal number of request resending attempt (for any reason, including redirects). [3] | `3` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `http.request.size` | int | The total size of the request in bytes. This should be the total number of bytes sent over the wire, including the request line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and request body if any. | `1437` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http.response.body.size` | int | The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http.response.header.<key>` | string[] | HTTP response headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [4] | `http.response.header.content-type=["application/json"]`; `http.response.header.my-custom-header=["abc", "def"]` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `http.response.size` | int | The total size of the response in bytes. This should be the total number of bytes sent over the wire, including the status line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and response body and trailers if any. | `1437` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http.response.status_code` | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `http.route` | string | The matched route, that is, the path template in the format used by the respective server framework. [5] | `/users/:userID?`; `{controller}/{action}/{id?}` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all request headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
The `User-Agent` header is already captured in the `user_agent.original` attribute. Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

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

**[3]:** The resend count SHOULD be updated each time an HTTP request gets resent by the client, regardless of what was the cause of the resending (e.g. redirection, authorization failure, 503 Server Unavailable, network issues, or any other).

**[4]:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all response headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[5]:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

`http.connection.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `active` | active state. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `idle` | idle state. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`http.request.method` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `CONNECT` | CONNECT method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `DELETE` | DELETE method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `GET` | GET method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `HEAD` | HEAD method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `OPTIONS` | OPTIONS method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `PATCH` | PATCH method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `POST` | POST method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `PUT` | PUT method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `TRACE` | TRACE method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `_OTHER` | Any HTTP method that the instrumentation has no prior knowledge of. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

## Deprecated HTTP Attributes

<!-- semconv attributes.http.deprecated(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `http.flavor` | string | Deprecated, use `network.protocol.name` instead. | `1.0` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `network.protocol.name`. |
| `http.method` | string | Deprecated, use `http.request.method` instead. | `GET`; `POST`; `HEAD` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `http.request.method`. |
| `http.request_content_length` | int | Deprecated, use `http.request.header.content-length` instead. | `3495` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `http.request.header.content-length`. |
| `http.response_content_length` | int | Deprecated, use `http.response.header.content-length` instead. | `3495` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `http.response.header.content-length`. |
| `http.scheme` | string | Deprecated, use `url.scheme` instead. | `http`; `https` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `url.scheme` instead. |
| `http.status_code` | int | Deprecated, use `http.response.status_code` instead. | `200` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `http.response.status_code`. |
| `http.target` | string | Deprecated, use `url.path` and `url.query` instead. | `/search?q=OpenTelemetry#SemConv` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Split to `url.path` and `url.query. |
| `http.url` | string | Deprecated, use `url.full` instead. | `https://www.foo.bar/search?q=OpenTelemetry#SemConv` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `url.full`. |
| `http.user_agent` | string | Deprecated, use `user_agent.original` instead. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `user_agent.original`. |

`http.flavor` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `1.0` | HTTP/1.0 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `1.1` | HTTP/1.1 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `2.0` | HTTP/2 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `3.0` | HTTP/3 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `SPDY` | SPDY protocol. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `QUIC` | QUIC protocol. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->
