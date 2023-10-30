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
    + [Setting `server.address` and `server.port` attributes](#setting-serveraddress-and-serverport-attributes)
    + [Simple client/server example](#simple-clientserver-example)
    + [Client/server example with reverse proxy](#clientserver-example-with-reverse-proxy)
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

HTTP spans MUST follow the overall [guidelines for span names](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/trace/api.md#span).

<!-- markdown-link-check-disable -->
<!-- HTML anchors are not supported https://github.com/tcort/markdown-link-check/issues/225-->
HTTP server span names SHOULD be `{method} {http.route}` if there is a
(low-cardinality) `http.route` available (see below for the exact definition of the [`{method}`](#method-placeholder) placeholder).

If there is no (low-cardinality) `http.route` available, HTTP server span names
SHOULD be [`{method}`](#method-placeholder).

HTTP client spans have no `http.route` attribute since client-side instrumentation
is not generally aware of the "route", and therefore HTTP client span names SHOULD be
[`{method}`](#method-placeholder).
<!-- markdown-link-check-enable -->

The <span id="method-placeholder">`{method}`</span> MUST be `{http.request.method}` if the method represents the original method known to the instrumentation.
In other cases (when `{http.request.method}` is set to `_OTHER`), `{method}` MUST be `HTTP`.

Instrumentation MUST NOT default to using URI
path as span name, but MAY provide hooks to allow custom logic to override the
default span name.

## Status

[Span Status](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/trace/api.md#set-status) MUST be left unset if HTTP status code was in the
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
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Conditionally Required: If request has ended with an error. |
| [`http.request.header.<key>`](../attributes-registry/http.md) | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [2] | `http.request.header.content-type=["application/json"]`; `http.request.header.x-forwarded-for=["1.2.3.4", "1.2.3.5"]` | Opt-In |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [3] | `GET`; `POST`; `HEAD` | Required |
| [`http.request.method_original`](../attributes-registry/http.md) | string | Original HTTP method sent by the client in the request line. | `GeT`; `ACL`; `foo` | Conditionally Required: [4] |
| [`http.response.header.<key>`](../attributes-registry/http.md) | string[] | HTTP response headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [5] | `http.response.header.content-type=["application/json"]`; `http.response.header.my-custom-header=["abc", "def"]` | Opt-In |
| [`http.response.status_code`](../attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | Conditionally Required: If and only if one was received/sent. |
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`network.peer.port`](../attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | Recommended: If `network.peer.address` is set. |
| [`network.protocol.name`](../attributes-registry/network.md) | string | [OSI application layer](https://osi-model.com/application-layer/) or non-OSI equivalent. [6] | `http`; `spdy` | Opt-In |
| [`network.protocol.version`](../attributes-registry/network.md) | string | Version of the protocol specified in `network.protocol.name`. [7] | `1.0`; `1.1`; `2`; `3` | Recommended |
| [`network.transport`](../attributes-registry/network.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [8] | `tcp`; `udp` | Opt-In |

**[1]:** If the request fails with an error before response status code was sent or received,
`error.type` SHOULD be set to exception type (its fully-qualified class name, if applicable)
or a component-specific low cardinality error identifier.

If response status code was sent or received and status indicates an error according to [HTTP span status definition](/docs/http/http-spans.md),
`error.type` SHOULD be set to the status code number (represented as a string), an exception type (if thrown) or a component-specific error identifier.

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

**[7]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[8]:** Generally `tcp` for `HTTP/1.0`, `HTTP/1.1`, and `HTTP/2`. Generally `udp` for `HTTP/3`. Other obscure implementations are possible.

Following attributes MUST be provided **at span creation time** (when provided at all), so they can be considered for sampling decisions:

* [`http.request.method`](../attributes-registry/http.md)

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. |

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
| `pipe` | Named or anonymous pipe. |
| `unix` | Unix domain socket |
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

<!-- semconv trace.http.client -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`http.request.resend_count`](../attributes-registry/http.md) | int | The ordinal number of request resending attempt (for any reason, including redirects). [1] | `3` | Recommended: if and only if request was retried. |
| [`server.address`](../general/attributes.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Required |
| [`server.port`](../general/attributes.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [3] | `80`; `8080`; `443` | Conditionally Required: [4] |
| [`url.full`](../attributes-registry/url.md) | string | Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [5] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `//localhost` | Required |
| [`user_agent.original`](../attributes-registry/user-agent.md) | string | Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1` | Opt-In |

**[1]:** The resend count SHOULD be updated each time an HTTP request gets resent by the client, regardless of what was the cause of the resending (e.g. redirection, authorization failure, 503 Server Unavailable, network issues, or any other).

**[2]:** If an HTTP client request is explicitly made to an IP address, e.g. `http://x.x.x.x:8080`, then `server.address` SHOULD be the IP address `x.x.x.x`. A DNS lookup SHOULD NOT be used.

**[3]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[4]:** If not default (`80` for `http` scheme, `443` for `https`).

**[5]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it SHOULD be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password SHOULD be redacted and attribute's value SHOULD be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed) and SHOULD NOT be validated or modified except for sanitizing purposes.

Following attributes MUST be provided **at span creation time** (when provided at all), so they can be considered for sampling decisions:

* [`server.address`](../general/attributes.md)
* [`server.port`](../general/attributes.md)
* [`url.full`](../attributes-registry/url.md)
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

Read the following section to understand how HTTP server instrumentations are suggested to capture server information.

### HTTP server definitions

An HTTP request can be routed to a specific HTTP application via intermediaries such as reverse proxies.
HTTP requests sent to the same domain name may be handled by multiple applications depending on the port, path, headers, or other parameters.

For example, different versions of the same web-application can run side-by-side as independent applications behind the reverse proxy which routes request to one or another based on the request path.

Instances of different HTTP server applications may run on the same physical host and share the same IP address, but listen to different TCP/UDP ports.
In order to route the request to a specific application, reverse proxies usually modify the [HTTP Host header][Host and authority] replacing the original value provided by the client with an actual proxied server name. This behavior depends on the reverse proxy configuration. In some cases, the `Host` header is not used when routing request to a specific application, making it prone to having bogus content.

HTTP server frameworks and their instrumentations have limited knowledge about the HTTP infrastructure and intermediaries that requests go through. In a general case, they can only use HTTP request properties such as request target or headers to populate `server.*` attributes.

#### Setting `server.address` and `server.port` attributes

In the context of HTTP server, `server.address` and `server.port` attributes capture the original host name and port. They are intended, whenever possible, to be the same on the client and server sides.

HTTP server instrumentations SHOULD do the best effort when populating `server.address` and `server.port` attributes and SHOULD determine them by using the first of the following that applies:

* The original host which may be passed by the reverse proxy in the [`Forwarded#host`][Forwarded#host], [`X-Forwarded-Host`][X-Forwarded-Host], or a similar header.
* The [`:authority`][HTTP/2 authority] pseudo-header in case of HTTP/2 or HTTP/3
* The [`Host`][Host header] header.

> **Note**: The `Host` and `:authority` headers contain host and port number of the server. The same applies to the `host` identifier of `Forwarded` header or the `X-Forwarded-Host` header. Instrumentations SHOULD populate both `server.address` and `server.port` attributes by parsing the value of corresponding header.

Application developers MAY overwrite potentially inaccurate values of `server.*` attributes using a [SpanProcessor][SpanProcessor] and MAY capture private host information using applicable [resource attributes](/docs/resource/README.md).

#### Simple client/server example

![simple-http-server.png](simple-http-server.png)

#### Client/server example with reverse proxy

![reverse-proxy-http-server.png](reverse-proxy-http-server.png)

[Host and authority]: https://tools.ietf.org/html/rfc9110#section-7.2
[Host header]: https://tools.ietf.org/html/rfc7230#section-5.4
[HTTP/2 authority]: https://tools.ietf.org/html/rfc9113#section-8.3.1
[Forwarded#host]: https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#host
[X-Forwarded-Host]: https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-Host

### HTTP Server semantic conventions

This span type represents an inbound HTTP request.

For an HTTP server span, `SpanKind` MUST be `Server`.

<!-- semconv trace.http.server -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`client.address`](../general/attributes.md) | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `83.164.160.102` | Recommended |
| [`client.port`](../general/attributes.md) | int | The port of whichever client was captured in `client.address`. [2] | `65123` | Opt-In |
| [`http.route`](../attributes-registry/http.md) | string | The matched route, that is, the path template in the format used by the respective server framework. [3] | `/users/:userID?`; `{controller}/{action}/{id?}` | Conditionally Required: If and only if it's available |
| [`network.local.address`](../attributes-registry/network.md) | string | Local socket address. Useful in case of a multi-IP host. | `10.1.2.80`; `/tmp/my.sock` | Opt-In |
| [`network.local.port`](../attributes-registry/network.md) | int | Local socket port. Useful in case of a multi-port host. | `65123` | Opt-In |
| [`server.address`](../general/attributes.md) | string | Name of the local HTTP server that received the request. [4] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`server.port`](../general/attributes.md) | int | Port of the local HTTP server that received the request. [5] | `80`; `8080`; `443` | Conditionally Required: [6] |
| [`url.path`](../attributes-registry/url.md) | string | The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component | `/search` | Required |
| [`url.query`](../attributes-registry/url.md) | string | The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [7] | `q=OpenTelemetry` | Conditionally Required: If and only if one was received/sent. |
| [`url.scheme`](../attributes-registry/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. [8] | `http`; `https` | Required |
| [`user_agent.original`](../attributes-registry/user-agent.md) | string | Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1` | Recommended |

**[1]:** The IP address of the original client behind all proxies, if known (e.g. from [Forwarded#for](https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#for), [X-Forwarded-For](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-For), or a similar header). Otherwise, the immediate client peer address.

**[2]:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries,  for example proxies, if it's available.

**[3]:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

**[4]:** See [Setting `server.address` and `server.port` attributes](/docs/http/http-spans.md#setting-serveraddress-and-serverport-attributes).

**[5]:** See [Setting `server.address` and `server.port` attributes](/docs/http/http-spans.md#setting-serveraddress-and-serverport-attributes).

**[6]:** If `server.address` is set and the port is not default (`80` for `http` scheme, `443` for `https`).

**[7]:** Sensitive content provided in query string SHOULD be scrubbed when instrumentations can identify it.

**[8]:** The scheme of the original client request, if known (e.g. from [Forwarded#proto](https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#proto), [X-Forwarded-Proto](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-Proto), or a similar header). Otherwise, the scheme of the immediate peer request.

Following attributes MUST be provided **at span creation time** (when provided at all), so they can be considered for sampling decisions:

* [`server.address`](../general/attributes.md)
* [`server.port`](../general/attributes.md)
* [`url.path`](../attributes-registry/url.md)
* [`url.query`](../attributes-registry/url.md)
* [`url.scheme`](../attributes-registry/url.md)
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
| `server.port`        | `8080`                                                  |
| `network.peer.address` | `"192.0.2.5"`                                         |
| `network.peer.port`    | `8080`                                                |
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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[SpanProcessor]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/trace/sdk.md#span-processor
