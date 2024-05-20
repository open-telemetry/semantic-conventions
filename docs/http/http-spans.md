<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic Conventions for HTTP Spans

**Status**: [Stable][DocumentStatus], Unless otherwise specified.

This document defines semantic conventions for HTTP client and server Spans.
They can be used for http and https schemes
and various HTTP versions like 1.1, 2 and SPDY.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Name](#name)
- [Status](#status)
- [HTTP client](#http-client)
  - [HTTP client experimental attributes](#http-client-experimental-attributes)
  - [HTTP client span duration](#http-client-span-duration)
  - [HTTP request retries and redirects](#http-request-retries-and-redirects)
- [HTTP server](#http-server)
  - [HTTP server definitions](#http-server-definitions)
    - [Setting `server.address` and `server.port` attributes](#setting-serveraddress-and-serverport-attributes)
    - [Simple client/server example](#simple-clientserver-example)
    - [Client/server example with reverse proxy](#clientserver-example-with-reverse-proxy)
  - [HTTP server semantic conventions](#http-server-semantic-conventions)
  - [HTTP server experimental attributes](#http-server-experimental-attributes)
- [Examples](#examples)
  - [HTTP client-server example](#http-client-server-example)
  - [HTTP client retries examples](#http-client-retries-examples)
  - [HTTP client authorization retry examples](#http-client-authorization-retry-examples)
  - [HTTP client redirects examples](#http-client-redirects-examples)
  - [HTTP client call: DNS error](#http-client-call-dns-error)
  - [HTTP client call: Internal Server Error](#http-client-call-internal-server-error)
  - [HTTP server call: connection dropped before response body was sent](#http-server-call-connection-dropped-before-response-body-was-sent)

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
> * SHOULD drop the environment variable in the next major version.

## Name

HTTP spans MUST follow the overall [guidelines for span names](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.33.0/specification/trace/api.md#span).

HTTP span names SHOULD be `{method} {target}` if there is a (low-cardinality) `target` available. If there is no (low-cardinality) `{target}` available, HTTP span names SHOULD be `{method}`.

<!-- markdown-link-check-disable -->
<!-- HTML anchors are not supported https://github.com/tcort/markdown-link-check/issues/225-->
(see below for the exact definition of the [`{method}`](#method-placeholder) and [`{target}`](#target-placeholder) placeholders).
<!-- markdown-link-check-enable -->

The <span id="method-placeholder">`{method}`</span> MUST be `{http.request.method}` if the method represents the original method known to the instrumentation.
In other cases (when `{http.request.method}` is set to `_OTHER`), `{method}` MUST be `HTTP`.

The <span id="target-placeholder">`{target}`</span> SHOULD be one of the following:

- [`http.route`](/docs/attributes-registry/http.md) for HTTP Server spans
- [`url.template`](/docs/attributes-registry/url.md) for HTTP Client spans if enabled and available (![Experimental](https://img.shields.io/badge/-experimental-blue))
- Other value MAY be provided through custom hooks at span start time or later.

Instrumentation MUST NOT default to using URI path as a `{target}`.

## Status

[Span Status](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.33.0/specification/trace/api.md#set-status) MUST be left unset if HTTP status code was in the
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
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`http.request.method`](/docs/attributes-registry/http.md) | string | HTTP request method. [1] | `GET`; `POST`; `HEAD` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Host identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Port identifier of the ["URI origin"](https://www.rfc-editor.org/rfc/rfc9110.html#name-uri-origin) HTTP request is sent to. [3] | `80`; `8080`; `443` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`url.full`](/docs/attributes-registry/url.md) | string | Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [4] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `//localhost` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [5] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` If request has ended with an error. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.request.method_original`](/docs/attributes-registry/http.md) | string | Original HTTP method sent by the client in the request line. | `GeT`; `ACL`; `foo` | `Conditionally Required` [6] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.response.status_code`](/docs/attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | `Conditionally Required` If and only if one was received/sent. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.protocol.name`](/docs/attributes-registry/network.md) | string | [OSI application layer](https://osi-model.com/application-layer/) or non-OSI equivalent. [7] | `http`; `spdy` | `Conditionally Required` [8] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.request.resend_count`](/docs/attributes-registry/http.md) | int | The ordinal number of request resending attempt (for any reason, including redirects). [9] | `3` | `Recommended` if and only if request was retried. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` If `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.protocol.version`](/docs/attributes-registry/network.md) | string | The actual version of the protocol used for network communication. [10] | `1.0`; `1.1`; `2`; `3` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.request.header.<key>`](/docs/attributes-registry/http.md) | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [11] | `http.request.header.content-type=["application/json"]`; `http.request.header.x-forwarded-for=["1.2.3.4", "1.2.3.5"]` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.response.header.<key>`](/docs/attributes-registry/http.md) | string[] | HTTP response headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [12] | `http.response.header.content-type=["application/json"]`; `http.response.header.my-custom-header=["abc", "def"]` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.transport`](/docs/attributes-registry/network.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [13] | `tcp`; `udp` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`url.scheme`](/docs/attributes-registry/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`user_agent.original`](/docs/attributes-registry/user-agent.md) | string | Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1`; `YourApp/1.0.0 grpc-java-okhttp/1.27.2` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

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

**[2]:** If an HTTP client request is explicitly made to an IP address, e.g. `http://x.x.x.x:8080`, then `server.address` SHOULD be the IP address `x.x.x.x`. A DNS lookup SHOULD NOT be used.

**[3]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[4]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it SHOULD be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password SHOULD be redacted and attribute's value SHOULD be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed). Sensitive content provided in `url.full` SHOULD be scrubbed when instrumentations can identify it.

**[5]:** If the request fails with an error before response status code was sent or received,
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

**[6]:** If and only if it's different than `http.request.method`.

**[7]:** The value SHOULD be normalized to lowercase.

**[8]:** If not `http` and `network.protocol.version` is set.

**[9]:** The resend count SHOULD be updated each time an HTTP request gets resent by the client, regardless of what was the cause of the resending (e.g. redirection, authorization failure, 503 Server Unavailable, network issues, or any other).

**[10]:** If protocol version is subject to negotiation (for example using [ALPN](https://www.rfc-editor.org/rfc/rfc7301.html)), this attribute SHOULD be set to the negotiated version. If the actual protocol version is not known, this attribute SHOULD NOT be set.

**[11]:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all request headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
The `User-Agent` header is already captured in the `user_agent.original` attribute. Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[12]:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all response headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[13]:** Generally `tcp` for `HTTP/1.0`, `HTTP/1.1`, and `HTTP/2`. Generally `udp` for `HTTP/3`. Other obscure implementations are possible.



The following attributes can be important for making sampling decisions
and SHOULD be provided **at span creation time** (if provided at all):

* [`http.request.method`](/docs/attributes-registry/http.md)
* [`server.address`](/docs/attributes-registry/server.md)
* [`server.port`](/docs/attributes-registry/server.md)
* [`url.full`](/docs/attributes-registry/url.md)

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |


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


`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `tcp` | TCP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `pipe` | Named or anonymous pipe. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |



<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### HTTP client experimental attributes

**Status**: [Experimental][DocumentStatus]

Instrumentations MAY allow users to enable additional experimental attributes.

<!-- semconv trace.http.client.experimental(full) -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`http.request.body.size`](/docs/attributes-registry/http.md) | int | The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.request.size`](/docs/attributes-registry/http.md) | int | The total size of the request in bytes. This should be the total number of bytes sent over the wire, including the request line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and request body if any. | `1437` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.response.body.size`](/docs/attributes-registry/http.md) | int | The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.response.size`](/docs/attributes-registry/http.md) | int | The total size of the response in bytes. This should be the total number of bytes sent over the wire, including the status line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and response body and trailers if any. | `1437` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`url.template`](/docs/attributes-registry/url.md) | string | The low-cardinality template of an [absolute path reference](https://www.rfc-editor.org/rfc/rfc3986#section-4.2). [1] | `/users/{id}`; `/users/:id`; `/users?id={id}` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The `url.template` MUST have low cardinality. It is not usually available on HTTP clients, but may be known by the application or specialized HTTP instrumentation.




<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

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

Each time an HTTP request is resent, the `http.request.resend_count` attribute SHOULD be added to each repeated span and set to the ordinal number of the request resend attempt.

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

### HTTP server semantic conventions

This span type represents an inbound HTTP request.

For an HTTP server span, `SpanKind` MUST be `Server`.

<!-- semconv trace.http.server(full) -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`http.request.method`](/docs/attributes-registry/http.md) | string | HTTP request method. [1] | `GET`; `POST`; `HEAD` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`url.path`](/docs/attributes-registry/url.md) | string | The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component [2] | `/search` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`url.scheme`](/docs/attributes-registry/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. [3] | `http`; `https` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [4] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` If request has ended with an error. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.request.method_original`](/docs/attributes-registry/http.md) | string | Original HTTP method sent by the client in the request line. | `GeT`; `ACL`; `foo` | `Conditionally Required` [5] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.response.status_code`](/docs/attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | `Conditionally Required` If and only if one was received/sent. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.route`](/docs/attributes-registry/http.md) | string | The matched route, that is, the path template in the format used by the respective server framework. [6] | `/users/:userID?`; `{controller}/{action}/{id?}` | `Conditionally Required` If and only if it's available | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.protocol.name`](/docs/attributes-registry/network.md) | string | [OSI application layer](https://osi-model.com/application-layer/) or non-OSI equivalent. [7] | `http`; `spdy` | `Conditionally Required` [8] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Port of the local HTTP server that received the request. [9] | `80`; `8080`; `443` | `Conditionally Required` If `server.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`url.query`](/docs/attributes-registry/url.md) | string | The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [10] | `q=OpenTelemetry` | `Conditionally Required` If and only if one was received/sent. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`client.address`](/docs/attributes-registry/client.md) | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [11] | `83.164.160.102` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` If `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.protocol.version`](/docs/attributes-registry/network.md) | string | The actual version of the protocol used for network communication. [12] | `1.0`; `1.1`; `2`; `3` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Name of the local HTTP server that received the request. [13] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`user_agent.original`](/docs/attributes-registry/user-agent.md) | string | Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1`; `YourApp/1.0.0 grpc-java-okhttp/1.27.2` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`client.port`](/docs/attributes-registry/client.md) | int | The port of whichever client was captured in `client.address`. [14] | `65123` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.request.header.<key>`](/docs/attributes-registry/http.md) | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [15] | `http.request.header.content-type=["application/json"]`; `http.request.header.x-forwarded-for=["1.2.3.4", "1.2.3.5"]` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.response.header.<key>`](/docs/attributes-registry/http.md) | string[] | HTTP response headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [16] | `http.response.header.content-type=["application/json"]`; `http.response.header.my-custom-header=["abc", "def"]` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.local.address`](/docs/attributes-registry/network.md) | string | Local socket address. Useful in case of a multi-IP host. | `10.1.2.80`; `/tmp/my.sock` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.local.port`](/docs/attributes-registry/network.md) | int | Local socket port. Useful in case of a multi-port host. | `65123` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.transport`](/docs/attributes-registry/network.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [17] | `tcp`; `udp` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

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

**[2]:** Sensitive content provided in `url.path` SHOULD be scrubbed when instrumentations can identify it.

**[3]:** The scheme of the original client request, if known (e.g. from [Forwarded#proto](https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#proto), [X-Forwarded-Proto](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-Proto), or a similar header). Otherwise, the scheme of the immediate peer request.

**[4]:** If the request fails with an error before response status code was sent or received,
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

**[5]:** If and only if it's different than `http.request.method`.

**[6]:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

**[7]:** The value SHOULD be normalized to lowercase.

**[8]:** If not `http` and `network.protocol.version` is set.

**[9]:** See [Setting `server.address` and `server.port` attributes](/docs/http/http-spans.md#setting-serveraddress-and-serverport-attributes).

**[10]:** Sensitive content provided in `url.query` SHOULD be scrubbed when instrumentations can identify it.

**[11]:** The IP address of the original client behind all proxies, if known (e.g. from [Forwarded#for](https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#for), [X-Forwarded-For](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-For), or a similar header). Otherwise, the immediate client peer address.

**[12]:** If protocol version is subject to negotiation (for example using [ALPN](https://www.rfc-editor.org/rfc/rfc7301.html)), this attribute SHOULD be set to the negotiated version. If the actual protocol version is not known, this attribute SHOULD NOT be set.

**[13]:** See [Setting `server.address` and `server.port` attributes](/docs/http/http-spans.md#setting-serveraddress-and-serverport-attributes).

**[14]:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries,  for example proxies, if it's available.

**[15]:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all request headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
The `User-Agent` header is already captured in the `user_agent.original` attribute. Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[16]:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all response headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[17]:** Generally `tcp` for `HTTP/1.0`, `HTTP/1.1`, and `HTTP/2`. Generally `udp` for `HTTP/3`. Other obscure implementations are possible.



The following attributes can be important for making sampling decisions
and SHOULD be provided **at span creation time** (if provided at all):

* [`client.address`](/docs/attributes-registry/client.md)
* [`http.request.header.<key>`](/docs/attributes-registry/http.md)
* [`http.request.method`](/docs/attributes-registry/http.md)
* [`server.address`](/docs/attributes-registry/server.md)
* [`server.port`](/docs/attributes-registry/server.md)
* [`url.path`](/docs/attributes-registry/url.md)
* [`url.query`](/docs/attributes-registry/url.md)
* [`url.scheme`](/docs/attributes-registry/url.md)
* [`user_agent.original`](/docs/attributes-registry/user-agent.md)

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |


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


`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `tcp` | TCP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `pipe` | Named or anonymous pipe. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |



<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

`http.route` MUST be provided at span creation time if and only if it's already available. If it becomes available after span starts, instrumentation MUST populate it anytime before span ends.

### HTTP server experimental attributes

**Status**: [Experimental][DocumentStatus]

Instrumentations MAY allow users to enable additional experimental attributes.

<!-- semconv trace.http.server.experimental(full) -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`http.request.body.size`](/docs/attributes-registry/http.md) | int | The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.request.size`](/docs/attributes-registry/http.md) | int | The total size of the request in bytes. This should be the total number of bytes sent over the wire, including the request line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and request body if any. | `1437` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.response.body.size`](/docs/attributes-registry/http.md) | int | The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.response.size`](/docs/attributes-registry/http.md) | int | The total size of the response in bytes. This should be the total number of bytes sent over the wire, including the status line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and response body and trailers if any. | `1437` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |


<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Examples

### HTTP client-server example

As an example, if a browser request for `https://example.com:8080/webshop/articles/4?s=1&t=2` is invoked from a host with IP 192.0.2.4, we may have the following Span on the client side:

Span name: `GET`

|   Attribute name     |                                       Value             |
| :------------------- | :-------------------------------------------------------|
| `http.request.method`| `"GET"`                                                 |
| `network.protocol.version` | `"1.1"`                                           |
| `url.full`           | `"https://example.com:8080/webshop/articles/4?s=1&t=2"` |
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
| `url.query`          | `"s=1&t=2"`                                     |
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
  -- GET / - 500 (CLIENT, trace=t1, span=s4, http.request.resend_count=1)
  |   |
  |   --- server (SERVER, trace=t1, span=s5)
  |
  -- GET / - 200 (CLIENT, trace=t1, span=s6, http.request.resend_count=2)
      |
      --- server (SERVER, trace=t1, span=s7)
```

Example of retries with no trace started upfront:

```
GET / - 500 (CLIENT, trace=t1, span=s1)
 |
 --- server (SERVER, trace=t1, span=s2)

GET / - 500 (CLIENT, trace=t2, span=s1, http.request.resend_count=1)
 |
 --- server (SERVER, trace=t2, span=s2)

GET / - 200 (CLIENT, trace=t3, span=s1, http.request.resend_count=2)
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
  -- GET /hello - 200 (CLIENT, trace=t1, span=s4, http.request.resend_count=1)
      |
      --- server (SERVER, trace=t1, span=s5)
```

Example of retries with no trace started upfront:

```
GET /hello - 401 (CLIENT, trace=t1, span=s1)
 |
 --- server (SERVER, trace=t1, span=s2)

GET /hello - 200 (CLIENT, trace=t2, span=s1, http.request.resend_count=1)
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
  -- GET /hello - 200 (CLIENT, trace=t1, span=s4, http.request.resend_count=1)
      |
      --- server (SERVER, trace=t1, span=s5)
```

Example of redirects with no trace started upfront:

```
GET / - 302 (CLIENT, trace=t1, span=s1)
 |
 --- server (SERVER, trace=t1, span=s2)

GET /hello - 200 (CLIENT, trace=t2, span=s1, http.request.resend_count=1)
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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.33.0/specification/document-status.md
[SpanProcessor]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.33.0/specification/trace/sdk.md#span-processor
