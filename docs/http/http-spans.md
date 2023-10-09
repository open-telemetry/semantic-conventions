<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic Conventions for HTTP Spans

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This document defines semantic conventions for HTTP client and server Spans.
They can be used for http and https schemes
and various HTTP versions like 1.1, 2 and SPDY.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Name](#name)
- [Status](#status)
- [Common Attributes](#common-attributes)
- [HTTP client](#http-client)
  * [HTTP client span duration](#http-client-span-duration)
  * [HTTP request retries and redirects](#http-request-retries-and-redirects)
- [HTTP server](#http-server)
  * [HTTP server definitions](#http-server-definitions)
  * [HTTP Server semantic conventions](#http-server-semantic-conventions)
- [Examples](#examples)
  * [HTTP client-server example](#http-client-server-example)
  * [HTTP client retries examples](#http-client-retries-examples)
  * [HTTP client authorization retry examples](#http-client-authorization-retry-examples)
  * [HTTP client redirects examples](#http-client-redirects-examples)
  * [HTTP client call: DNS error](#http-client-call-dns-error)
  * [HTTP client call: Internal Server Error](#http-client-call-internal-server-error)
  * [HTTP server call: connection dropped before response body was sent](#http-server-call-connection-dropped-before-response-body-was-sent)

<!-- tocstop -->

> **Warning**
> Existing HTTP instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md)
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

## Name

HTTP spans MUST follow the overall [guidelines for span names](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/trace/api.md#span).

<!-- markdown-link-check-disable -->
<!-- HTML anchors are not supported https://github.com/tcort/markdown-link-check/issues/225-->
HTTP server span names SHOULD be `{method} {http.route}` if there is a
(low-cardinality) `http.route` available (see below for the exact definition of the [`{method}`](#method-placeholder) placeholder).

If there is no (low-cardinality) `http.route` available, HTTP server span names
SHOULD be [`{method}`](#method-placeholder).

HTTP client spans have no `http.route` attribute since client-side instrumentation
is not generally aware of the "route", and therefore HTTP client spans SHOULD be
[`{method}`](#method-placeholder).
<!-- markdown-link-check-enable -->

The <span id="method-placeholder">`{method}`</span> MUST be `{http.request.method}` if the method represents the original method known to the instrumentation.
In other cases (when `{http.request.method}` is set to `_OTHER`), `{method}` MUST be `HTTP`.

Instrumentation MUST NOT default to using URI
path as span name, but MAY provide hooks to allow custom logic to override the
default span name.

## Status

[Span Status](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/trace/api.md#set-status) MUST be left unset if HTTP status code was in the
1xx, 2xx or 3xx ranges, unless there was another error (e.g., network error receiving
the response body; or 3xx codes with max redirects exceeded), in which case status
MUST be set to `Error`.

For HTTP status codes in the 4xx range span status MUST be left unset in case of `SpanKind.SERVER`
and MUST be set to `Error` in case of `SpanKind.CLIENT`.

For HTTP status codes in the 5xx range, as well as any other code the client
failed to interpret, span status MUST be set to `Error`.

Don't set the span status description if the reason can be inferred from `http.response.status_code`.

HTTP request may fail if it was cancelled or an error occurred preventing
the client or server from sending/receiving the request/response fully.

When instrumentation detects such errors it MUST set span status to `Error`
and MUST set the `error.type` attribute.

## Common Attributes

The common attributes listed in this section apply to both HTTP clients and servers in addition to
the specific attributes listed in the [HTTP client](#http-client) and [HTTP server](#http-server)
sections below.

<!-- semconv trace.http.common(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `name_resolution_error`; `500` | Conditionally Required: If request has ended with an error. |
| [`http.request.body.size`](../attributes-registry/http.md) | int | The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | Recommended |
| [`http.request.header.<key>`](../attributes-registry/http.md) | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase, with `-` characters replaced by `_`), the value being the header values. [2] | `http.request.header.content_type=["application/json"]`; `http.request.header.x_forwarded_for=["1.2.3.4", "1.2.3.5"]` | Opt-In |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [3] | `GET`; `POST`; `HEAD` | Required |
| [`http.request.method_original`](../attributes-registry/http.md) | string | Original HTTP method sent by the client in the request line. | `GeT`; `ACL`; `foo` | Conditionally Required: [4] |
| [`http.response.body.size`](../attributes-registry/http.md) | int | The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | Recommended |
| [`http.response.header.<key>`](../attributes-registry/http.md) | string[] | HTTP response headers, `<key>` being the normalized HTTP Header name (lowercase, with `-` characters replaced by `_`), the value being the header values. [5] | `http.response.header.content_type=["application/json"]`; `http.response.header.my_custom_header=["abc", "def"]` | Opt-In |
| [`http.response.status_code`](../attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: If and only if one was received/sent. |
| [`network.protocol.name`](../general/attributes.md) | string | [OSI application layer](https://osi-model.com/application-layer/) or non-OSI equivalent. [6] | `http`; `spdy` | Recommended: if not default (`http`). |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [7] | `1.0`; `1.1`; `2`; `3` | Recommended |
| [`network.transport`](../general/attributes.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://en.wikipedia.org/wiki/Inter-process_communication). [8] | `tcp`; `udp` | Conditionally Required: [9] |
| [`network.type`](../general/attributes.md) | string | [OSI network layer](https://osi-model.com/network-layer/) or non-OSI equivalent. [10] | `ipv4`; `ipv6` | Recommended |
| `user_agent.original` | string | Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3` | Recommended |

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

**[2]:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all request headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
The `User-Agent` header is already captured in the `user_agent.original` attribute. Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[3]:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[4]:** If and only if it's different than `http.request.method`.

**[5]:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all response headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[6]:** The value SHOULD be normalized to lowercase.

**[7]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[8]:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport, for example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[9]:** If not default (`tcp` for `HTTP/1.1` and `HTTP/2`, `udp` for `HTTP/3`).

**[10]:** The value SHOULD be normalized to lowercase.

Following attributes MUST be provided **at span creation time** (when provided at all), so they can be considered for sampling decisions:

* [`http.request.method`](../attributes-registry/http.md)

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

## HTTP client

This span type represents an outbound HTTP request. There are two ways this can be achieved in an instrumentation:

1. Instrumentations SHOULD create an HTTP span for each attempt to send an HTTP request over the wire.
   In case the request is resent, the resend attempts MUST follow the [HTTP resend spec](#http-request-retries-and-redirects).
   In this case, instrumentations SHOULD NOT (also) emit a logical encompassing HTTP client span.

2. If for some reason it is not possible to emit a span for each send attempt (because e.g. the instrumented library does not expose hooks that would allow this),
   instrumentations MAY create an HTTP span for the top-most operation of the HTTP client.
   In this case, the `url.full` MUST be the absolute URL that was originally requested, before any HTTP-redirects that may happen when executing the request.

For an HTTP client span, `SpanKind` MUST be `Client`.

<!-- semconv trace.http.client(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`http.resend_count`](../attributes-registry/http.md) | int | The ordinal number of request resending attempt (for any reason, including redirects). [1] | `3` | Recommended: if and only if request was retried. |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [2] | `example.com` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [3] | `80`; `8080`; `443` | Conditionally Required: [4] |
| [`server.socket.address`](../general/attributes.md) | string | Server address of the socket connection - IP address or Unix domain socket name. [5] | `10.5.3.2` | Recommended: If different than `server.address`. |
| [`server.socket.domain`](../general/attributes.md) | string | Immediate server peer's domain name if available without reverse DNS lookup [6] | `proxy.example.com` | Recommended: If different than `server.address`. |
| [`server.socket.port`](../general/attributes.md) | int | Server port number of the socket connection. [7] | `16456` | Recommended: If different than `server.port`. |
| [`url.full`](../url/url.md) | string | Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [8] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `//localhost` | Required |

**[1]:** The resend count SHOULD be updated each time an HTTP request gets resent by the client, regardless of what was the cause of the resending (e.g. redirection, authorization failure, 503 Server Unavailable, network issues, or any other).

**[2]:** Determined by using the first of the following that applies

- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form
- Host identifier of the `Host` header

If an HTTP client request is explicitly made to an IP address, e.g. `http://x.x.x.x:8080`, then
`server.address` SHOULD be the IP address `x.x.x.x`. A DNS lookup SHOULD NOT be used.

**[3]:** When [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource) is absolute URI, `server.port` MUST match URI port identifier, otherwise it MUST match `Host` header port identifier.

**[4]:** If not default (`80` for `http` scheme, `443` for `https`).

**[5]:** When observed from the client side, this SHOULD represent the immediate server peer address.
When observed from the server side, this SHOULD represent the physical server address.

**[6]:** Typically observed from the client side, and represents a proxy or other intermediary domain name.

**[7]:** When observed from the client side, this SHOULD represent the immediate server peer port.
When observed from the server side, this SHOULD represent the physical server port.

**[8]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password should be redacted and attribute's value should be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed) and SHOULD NOT be validated or modified except for sanitizing purposes.

Following attributes MUST be provided **at span creation time** (when provided at all), so they can be considered for sampling decisions:

* [`server.address`](../general/attributes.md)
* [`server.port`](../general/attributes.md)
* [`url.full`](../url/url.md)
<!-- endsemconv -->

Note that in some cases host and port identifiers in the `Host` header might be different from the `server.address` and `server.port`, in this case instrumentation MAY populate `Host` header on `http.request.header.host` attribute even if it's not enabled by user.

### HTTP client span duration

There are some minimal constraints that SHOULD be honored:

* HTTP client spans SHOULD start sometime before the first request byte is sent. This may or may not include connection time.
* HTTP client spans SHOULD end sometime after the HTTP response headers are fully read (or when they fail to be read). This may or may not include reading the response body.

If there is any possibility for application code to not fully read the HTTP response
(and for the HTTP client library to then have to clean up the HTTP response asynchronously),
the HTTP client span SHOULD NOT be ended in this cleanup phase,
and instead SHOULD end at some point after the HTTP response headers are fully read (or fail to be read).
This avoids the span being ended asynchronously later on at a time
which is no longer directly associated with the application code which made the HTTP request.

Because of the potential for confusion around this, HTTP client library instrumentations SHOULD document their behavior around ending HTTP client spans.

### HTTP request retries and redirects

Retries and redirects cause more than one physical HTTP request to be sent.
A request is resent when an HTTP client library sends more than one HTTP request to satisfy the same API call.
This may happen due to following redirects, authorization challenges, 503 Server Unavailable, network issues, or any other.

Each time an HTTP request is resent, the `http.resend_count` attribute SHOULD be added to each repeated span and set to the ordinal number of the request resend attempt.

See the examples for more details about:

* [retrying a server error](#http-client-retries-examples),
* [redirects](#http-client-redirects-examples),
* [authorization](#http-client-authorization-retry-examples).

## HTTP server

To understand the attributes defined in this section, it is helpful to read the "Definitions" subsection.

### HTTP server definitions

This section gives a short summary of some concepts
in web server configuration and web app deployment
that are relevant to tracing.

Usually, on a physical host, reachable by one or multiple IP addresses, a single HTTP listener process runs.
If multiple processes are running, they must listen on distinct TCP/UDP ports so that the OS can route incoming TCP/UDP packets to the right one.

Within a single server process, there can be multiple **virtual hosts**.
The [HTTP host header][] (in combination with a port number) is normally used to determine to which of them to route incoming HTTP requests.

The host header value that matches some virtual host is called the virtual hosts's **server name**. If there are multiple aliases for the virtual host, one of them (often the first one listed in the configuration) is called the **primary server name**. See for example, the Apache [`ServerName`][ap-sn] or NGINX [`server_name`][nx-sn] directive or the CGI specification on `SERVER_NAME` ([RFC 3875][rfc-servername]).
In practice the HTTP host header is often ignored when just a single virtual host is configured for the IP.

Within a single virtual host, some servers support the concepts of an **HTTP application**
(for example in Java, the Servlet JSR defines an application as
"a collection of servlets, HTML pages, classes, and other resources that make up a complete application on a Web server"
-- SRV.9 in [JSR 53][];
in a deployment of a Python application to Apache, the application would be the [PEP 3333][] conformant callable that is configured using the
[`WSGIScriptAlias` directive][modwsgisetup] of `mod_wsgi`).

An application can be "mounted" under an **application root**
(also known as a *[context root][]*, *[context prefix][]*, or *[document base][]*)
which is a fixed path prefix of the URL that determines to which application a request is routed
(e.g., the server could be configured to route all requests that go to an URL path starting with `/webshop/`
at a particular virtual host
to the `com.example.webshop` web application).

Some servers allow to bind the same HTTP application to multiple `(virtual host, application root)` pairs.

> TODO: Find way to trace HTTP application and application root ([opentelemetry/opentelementry-specification#335][])

[HTTP host header]: https://tools.ietf.org/html/rfc7230#section-5.4
[PEP 3333]: https://www.python.org/dev/peps/pep-3333/
[modwsgisetup]: https://modwsgi.readthedocs.io/en/develop/user-guides/quick-configuration-guide.html
[context root]: https://docs.jboss.org/jbossas/guides/webguide/r2/en/html/ch06.html
[context prefix]: https://marc.info/?l=apache-cvs&m=130928191414740
[document base]: http://tomcat.apache.org/tomcat-5.5-doc/config/context.html
[rfc-servername]: https://tools.ietf.org/html/rfc3875#section-4.1.14
[ap-sn]: https://httpd.apache.org/docs/2.4/mod/core.html#servername
[nx-sn]: http://nginx.org/en/docs/http/ngx_http_core_module.html#server_name
[JSR 53]: https://jcp.org/aboutJava/communityprocess/maintenance/jsr053/index2.html
[opentelemetry/opentelementry-specification#335]: https://github.com/open-telemetry/opentelemetry-specification/issues/335

### HTTP Server semantic conventions

This span type represents an inbound HTTP request.

For an HTTP server span, `SpanKind` MUST be `Server`.

<!-- semconv trace.http.server(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`client.address`](../general/attributes.md) | string | Client address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `83.164.160.102` | Recommended |
| [`client.port`](../general/attributes.md) | int | The port of the original client behind all proxies, if known (e.g. from [Forwarded](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Forwarded) or a similar header). Otherwise, the immediate client peer port. [2] | `65123` | Recommended |
| [`client.socket.address`](../general/attributes.md) | string | Client address of the socket connection - IP address or Unix domain socket name. [3] | `/tmp/my.sock`; `127.0.0.1` | Recommended: If different than `client.address`. |
| [`client.socket.port`](../general/attributes.md) | int | Client port number of the socket connection. [4] | `35555` | Recommended: If different than `client.port`. |
| [`http.route`](../attributes-registry/http.md) | string | The matched route (path template in the format used by the respective server framework). See note below [5] | `/users/:userID?`; `{controller}/{action}/{id?}` | Conditionally Required: If and only if it's available |
| [`server.address`](../general/attributes.md) | string | Name of the local HTTP server that received the request. [6] | `example.com` | Recommended |
| [`server.port`](../general/attributes.md) | int | Port of the local HTTP server that received the request. [7] | `80`; `8080`; `443` | Recommended: [8] |
| [`server.socket.address`](../general/attributes.md) | string | Local socket address. Useful in case of a multi-IP host. [9] | `10.5.3.2` | Opt-In |
| [`server.socket.port`](../general/attributes.md) | int | Local socket port. Useful in case of a multi-port host. [10] | `16456` | Opt-In |
| [`url.path`](../url/url.md) | string | The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component [11] | `/search` | Required |
| [`url.query`](../url/url.md) | string | The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [12] | `q=OpenTelemetry` | Conditionally Required: If and only if one was received/sent. |
| [`url.scheme`](../url/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https` | Required |

**[1]:** The IP address of the original client behind all proxies, if known (e.g. from [Forwarded](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Forwarded), [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For), or a similar header). Otherwise, the immediate client peer address.

**[2]:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries (e.g. proxies) if it's available.

**[3]:** When observed from the server side, this SHOULD represent the immediate client peer address.
When observed from the client side, this SHOULD represent the physical client address.

**[4]:** When observed from the server side, this SHOULD represent the immediate client peer port.
When observed from the client side, this SHOULD represent the physical client port.

**[5]:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

**[6]:** Determined by using the first of the following that applies

- The [primary server name](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host. MUST only
  include host identifier.
- Host identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Host identifier of the `Host` header

SHOULD NOT be set if only IP address is available and capturing name would require a reverse DNS lookup.

**[7]:** Determined by using the first of the following that applies

- Port identifier of the [primary server host](/docs/http/http-spans.md#http-server-definitions) of the matched virtual host.
- Port identifier of the [request target](https://www.rfc-editor.org/rfc/rfc9110.html#target.resource)
  if it's sent in absolute-form.
- Port identifier of the `Host` header

**[8]:** If not default (`80` for `http` scheme, `443` for `https`).

**[9]:** When observed from the client side, this SHOULD represent the immediate server peer address.
When observed from the server side, this SHOULD represent the physical server address.

**[10]:** When observed from the client side, this SHOULD represent the immediate server peer port.
When observed from the server side, this SHOULD represent the physical server port.

**[11]:** When missing, the value is assumed to be `/`

**[12]:** Sensitive content provided in query string SHOULD be scrubbed when instrumentations can identify it.

Following attributes MUST be provided **at span creation time** (when provided at all), so they can be considered for sampling decisions:

* [`server.address`](../general/attributes.md)
* [`server.port`](../general/attributes.md)
* [`url.path`](../url/url.md)
* [`url.query`](../url/url.md)
* [`url.scheme`](../url/url.md)
<!-- endsemconv -->

`http.route` MUST be provided at span creation time if and only if it's already available. If it becomes available after span starts, instrumentation MUST populate it anytime before span ends.

Note that in some cases host and port identifiers in the `Host` header might be different from the `server.address` and `server.port`, in this case instrumentation MAY populate `Host` header on `http.request.header.host` attribute even if it's not enabled by user.

## Examples

### HTTP client-server example

As an example, if a browser request for `https://example.com:8080/webshop/articles/4?s=1` is invoked from a host with IP 192.0.2.4, we may have the following Span on the client side:

Span name: `GET`

|   Attribute name     |                                       Value             |
| :------------------- | :-------------------------------------------------------|
| `http.request.method`| `"GET"`                                                 |
| `network.protocol.version` | `"1.1"`                                           |
| `url.full`           | `"https://example.com:8080/webshop/articles/4?s=1"`     |
| `server.address`     | `example.com`                                           |
| `server.port`        | 8080                                                    |
| `server.socket.address` | `"192.0.2.5"`                                        |
| `http.response.status_code` | `200`                                            |

The corresponding server Span may look like this:

Span name: `GET /webshop/articles/:article_id`.

|   Attribute name     |                      Value                      |
| :------------------- | :---------------------------------------------- |
| `http.request.method`| `"GET"`                                         |
| `network.protocol.version` | `"1.1"`                                   |
| `url.path`           | `"/webshop/articles/4"`                         |
| `url.query`          | `"?s=1"`                                        |
| `server.address`     | `"example.com"`                                 |
| `server.port`        | `8080`                                          |
| `url.scheme`         | `"https"`                                       |
| `http.route`         | `"/webshop/articles/:article_id"`               |
| `http.response.status_code` | `200`                                    |
| `client.address`     | `"192.0.2.4"`                                   |
| `client.socket.address` | `"192.0.2.5"` (the client goes through a proxy) |
| `user_agent.original` | `"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"` |

### HTTP client retries examples

Example of retries in the presence of a trace started by an inbound request:

```
request (SERVER, trace=t1, span=s1)
  |
  -- GET / - 500 (CLIENT, trace=t1, span=s2)
  |   |
  |   --- server (SERVER, trace=t1, span=s3)
  |
  -- GET / - 500 (CLIENT, trace=t1, span=s4, http.resend_count=1)
  |   |
  |   --- server (SERVER, trace=t1, span=s5)
  |
  -- GET / - 200 (CLIENT, trace=t1, span=s6, http.resend_count=2)
      |
      --- server (SERVER, trace=t1, span=s7)
```

Example of retries with no trace started upfront:

```
GET / - 500 (CLIENT, trace=t1, span=s1)
 |
 --- server (SERVER, trace=t1, span=s2)

GET / - 500 (CLIENT, trace=t2, span=s1, http.resend_count=1)
 |
 --- server (SERVER, trace=t2, span=s2)

GET / - 200 (CLIENT, trace=t3, span=s1, http.resend_count=2)
 |
 --- server (SERVER, trace=t3, span=s1)
```

### HTTP client authorization retry examples

Example of retries in the presence of a trace started by an inbound request:

```
request (SERVER, trace=t1, span=s1)
  |
  -- GET /hello - 401 (CLIENT, trace=t1, span=s2)
  |   |
  |   --- server (SERVER, trace=t1, span=s3)
  |
  -- GET /hello - 200 (CLIENT, trace=t1, span=s4, http.resend_count=1)
      |
      --- server (SERVER, trace=t1, span=s5)
```

Example of retries with no trace started upfront:

```
GET /hello - 401 (CLIENT, trace=t1, span=s1)
 |
 --- server (SERVER, trace=t1, span=s2)

GET /hello - 200 (CLIENT, trace=t2, span=s1, http.resend_count=1)
 |
 --- server (SERVER, trace=t2, span=s2)
```

### HTTP client redirects examples

Example of redirects in the presence of a trace started by an inbound request:

```
request (SERVER, trace=t1, span=s1)
  |
  -- GET / - 302 (CLIENT, trace=t1, span=s2)
  |   |
  |   --- server (SERVER, trace=t1, span=s3)
  |
  -- GET /hello - 200 (CLIENT, trace=t1, span=s4, http.resend_count=1)
      |
      --- server (SERVER, trace=t1, span=s5)
```

Example of redirects with no trace started upfront:

```
GET / - 302 (CLIENT, trace=t1, span=s1)
 |
 --- server (SERVER, trace=t1, span=s2)

GET /hello - 200 (CLIENT, trace=t2, span=s1, http.resend_count=1)
 |
 --- server (SERVER, trace=t2, span=s2)
```

### HTTP client call: DNS error

As an example, if a user requested `https://does-not-exist-123.com`, we may have the following span on the client side:

|   Attribute name     |                                       Value             |
| :------------------- | :-------------------------------------------------------|
| `http.request.method`| `"GET"`                                                 |
| `network.protocol.version` | `"1.1"`                                           |
| `url.full`           | `"https://does-not-exist-123.com"`                      |
| `server.address`     | `"does-not-exist-123.com"`                              |
| `error.type`         | `"java.net.UnknownHostException"`                       |

### HTTP client call: Internal Server Error

As an example, if a user requested `https://example.com` and server returned 500, we may have the following span on the client side:

|   Attribute name     |                                       Value             |
| :------------------- | :-------------------------------------------------------|
| `http.request.method`| `"GET"`                                                 |
| `network.protocol.version` | `"1.1"`                                           |
| `url.full`           | `"https://example.com"`                                 |
| `server.address`     | `"example.com"`                                         |
| `http.response.status_code` | `500`                                            |
| `error.type`         | `"500"`                                                 |

### HTTP server call: connection dropped before response body was sent

As an example, if a user sent a `POST` request with a body to `https://example.com:8080/uploads/4`, we may see the following span on a server side:

Span name: `POST /uploads/:document_id`.

|   Attribute name     |                      Value                      |
| :------------------- | :---------------------------------------------- |
| `http.request.method`| `"GET"`                                         |
| `url.path`           | `"/uploads/4"`                                  |
| `url.scheme`         | `"https"`                                       |
| `http.route`         | `"/uploads/:document_id"`                       |
| `http.response.status_code` | `201`                                    |
| `error.type`         | `WebSocketDisconnect`                           |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
