<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic conventions for HTTP spans

**Status**: [Stable][DocumentStatus], Unless otherwise specified.

This document defines semantic conventions for HTTP client and server Spans.
They can be used for http and https schemes
and various HTTP versions like 1.1, 2 and SPDY.

<!-- toc -->

- [Name](#name)
- [Status](#status)
- [HTTP client span](#http-client-span)
  - [HTTP client span duration](#http-client-span-duration)
  - [HTTP request retries and redirects](#http-request-retries-and-redirects)
- [HTTP server](#http-server)
  - [HTTP server definitions](#http-server-definitions)
    - [Setting `server.address` and `server.port` attributes](#setting-serveraddress-and-serverport-attributes)
    - [Simple client/server example](#simple-clientserver-example)
    - [Client/server example with reverse proxy](#clientserver-example-with-reverse-proxy)
  - [HTTP server span](#http-server-span)
- [Examples](#examples)
  - [HTTP client-server example](#http-client-server-example)
  - [HTTP client retries examples](#http-client-retries-examples)
  - [HTTP client authorization retry examples](#http-client-authorization-retry-examples)
  - [HTTP client redirects examples](#http-client-redirects-examples)
  - [HTTP client call: DNS error](#http-client-call-dns-error)
  - [HTTP client call: Internal Server Error](#http-client-call-internal-server-error)
  - [HTTP server call: connection dropped before response body was sent](#http-server-call-connection-dropped-before-response-body-was-sent)

<!-- tocstop -->

> [!IMPORTANT]
> Existing HTTP instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md)
> (or prior):
>
> * SHOULD NOT change the version of the HTTP or networking conventions that they emit by default
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking conventions which are also used
>   in HTTP instrumentations). Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version as a comma-separated list of category-specific values
>   (e.g., http, databases, messaging). The list of values includes:
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

HTTP spans MUST follow the overall [guidelines for span names](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/trace/api.md#span).

HTTP span names SHOULD be `{method} {target}` if there is a (low-cardinality) `target` available. If there is no (low-cardinality) `{target}` available, HTTP span names SHOULD be `{method}`.

(see below for the exact definition of the [`{method}`](#method-placeholder) and [`{target}`](#target-placeholder) placeholders).

The <span id="method-placeholder">`{method}`</span> MUST be `{http.request.method}` if the method represents the original method known to the instrumentation.
In other cases (when `{http.request.method}` is set to `_OTHER`), `{method}` MUST be `HTTP`.

The <span id="target-placeholder">`{target}`</span> SHOULD be one of the following:

- [`http.route`](/docs/registry/attributes/http.md) for HTTP Server spans
- [`url.template`](/docs/registry/attributes/url.md) for HTTP Client spans if enabled and available (![Development](https://img.shields.io/badge/-development-blue))
- Other value MAY be provided through custom hooks at span start time or later.

Instrumentation MUST NOT default to using URI path as a `{target}`.

## Status

[Span Status](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/trace/api.md#set-status) MUST be left unset if HTTP status code was in the
1xx, 2xx or 3xx ranges, unless there was another error (e.g., network error receiving
the response body; or 3xx codes with max redirects exceeded), in which case status
MUST be set to `Error`.

> [!NOTE]
>
> The classification of an HTTP status code as an error depends on the context.
> For example, a 404 "Not Found" status code indicates an error if the application
> expected the resource to be available. However, it is not an error when the
> application is simply checking whether the resource exists.
>
> Instrumentations that have additional context about a specific request MAY use
> this context to set the span status more precisely.
> Instrumentations that don't have any additional context MUST follow the
> guidelines in this section.

For HTTP status codes in the 4xx range span status MUST be left unset in case of `SpanKind.SERVER`
and SHOULD be set to `Error` in case of `SpanKind.CLIENT`.

For HTTP status codes in the 5xx range, as well as any other code the client
failed to interpret, span status SHOULD be set to `Error`.

Don't set the span status description if the reason can be inferred from `http.response.status_code`.

HTTP request may fail if it was cancelled or an error occurred preventing
the client or server from sending/receiving the request/response fully.

When instrumentation detects such errors it SHOULD set span status to `Error`
and SHOULD set the `error.type` attribute.

**Status**: [Development][DocumentStatus] - Refer to the [Recording Errors](/docs/general/recording-errors.md) document for
general considerations on how to record span status.

## HTTP client span

<!-- semconv span.http.client -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Stable](https://img.shields.io/badge/-stable-lightgreen)

This span represents an outbound HTTP request.

There are two ways HTTP client spans can be implemented in an instrumentation:

1. Instrumentations SHOULD create an HTTP span for each attempt to send an HTTP request over the wire.
   In case the request is resent, the resend attempts MUST follow the [HTTP resend spec](#http-request-retries-and-redirects).
   In this case, instrumentations SHOULD NOT (also) emit a logical encompassing HTTP client span.

2. If for some reason it is not possible to emit a span for each send attempt (because e.g. the instrumented library does not expose hooks that would allow this),
   instrumentations MAY create an HTTP span for the top-most operation of the HTTP client.
   In this case, the `url.full` MUST be the absolute URL that was originally requested, before any HTTP-redirects that may happen when executing the request.

**Span name:** refer to the [Span Name](/docs/http/http-spans.md#name) section.

**Span kind** MUST be `CLIENT`.

**Span status:** refer to the [Span Status](/docs/http/http-spans.md#status) section.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`http.request.method`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Required` | string | HTTP request method. [1] | `GET`; `POST`; `HEAD` |
| [`server.address`](/docs/registry/attributes/server.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Required` | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [2] | `example.com`; `10.1.2.80`; `/tmp/my.sock` |
| [`server.port`](/docs/registry/attributes/server.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Required` | int | Server port number. [3] | `80`; `8080`; `443` |
| [`url.full`](/docs/registry/attributes/url.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Required` | string | Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [4] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `//localhost` |
| [`error.type`](/docs/registry/attributes/error.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If request has ended with an error. | string | Describes a class of error the operation ended with. [5] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` |
| [`http.request.method_original`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [6] | string | Original HTTP method sent by the client in the request line. | `GeT`; `ACL`; `foo` |
| [`http.response.status_code`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If and only if one was received/sent. | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` |
| [`network.protocol.name`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [7] | string | [OSI application layer](https://wikipedia.org/wiki/Application_layer) or non-OSI equivalent. [8] | `http`; `spdy` |
| [`http.request.resend_count`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` if and only if request was retried. | int | The ordinal number of request resending attempt (for any reason, including redirects). [9] | `3` |
| [`network.peer.address`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` |
| [`network.peer.port`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` If `network.peer.address` is set. | int | Peer port number of the network connection. | `65123` |
| [`network.protocol.version`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | The actual version of the protocol used for network communication. [10] | `1.0`; `1.1`; `2`; `3` |
| [`http.request.body.size`](/docs/registry/attributes/http.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | int | The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` |
| [`http.request.header.<key>`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [11] | `["application/json"]`; `["1.2.3.4", "1.2.3.5"]` |
| [`http.request.size`](/docs/registry/attributes/http.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | int | The total size of the request in bytes. This should be the total number of bytes sent over the wire, including the request line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and request body if any. | `1437` |
| [`http.response.body.size`](/docs/registry/attributes/http.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | int | The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` |
| [`http.response.header.<key>`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string[] | HTTP response headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [12] | `["application/json"]`; `["abc", "def"]` |
| [`http.response.size`](/docs/registry/attributes/http.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | int | The total size of the response in bytes. This should be the total number of bytes sent over the wire, including the status line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and response body and trailers if any. | `1437` |
| [`network.transport`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string | [OSI transport layer](https://wikipedia.org/wiki/Transport_layer) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [13] | `tcp`; `udp` |
| [`url.scheme`](/docs/registry/attributes/url.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `http`; `https` |
| [`url.template`](/docs/registry/attributes/url.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | string | The low-cardinality template of an [absolute path reference](https://www.rfc-editor.org/rfc/rfc3986#section-4.2). [14] | `/users/{id}`; `/users/:id`; `/users?id={id}` |
| [`user_agent.original`](/docs/registry/attributes/user-agent.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string | Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1`; `YourApp/1.0.0 grpc-java-okhttp/1.27.2` |
| [`user_agent.synthetic.type`](/docs/registry/attributes/user-agent.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | string | Specifies the category of synthetic traffic, such as tests or bots. [15] | `bot`; `test` |

**[1] `http.request.method`:** HTTP request method value SHOULD be "known" to the instrumentation.
By default, this convention defines "known" methods as the ones listed in [RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-methods),
the PATCH method defined in [RFC5789](https://www.rfc-editor.org/rfc/rfc5789.html)
and the QUERY method defined in [httpbis-safe-method-w-body](https://datatracker.ietf.org/doc/draft-ietf-httpbis-safe-method-w-body/?include_text=1).

If the HTTP request method is not known to instrumentation, it MUST set the `http.request.method` attribute to `_OTHER`.

If the HTTP instrumentation could end up converting valid HTTP request methods to `_OTHER`, then it MUST provide a way to override
the list of known HTTP methods. If this override is done via environment variable, then the environment variable MUST be named
OTEL_INSTRUMENTATION_HTTP_KNOWN_METHODS and support a comma-separated list of case-sensitive known HTTP methods
(this list MUST be a full override of the default known method, it is not a list of known methods in addition to the defaults).

HTTP method names are case-sensitive and `http.request.method` attribute value MUST match a known HTTP method name exactly.
Instrumentations for specific web frameworks that consider HTTP methods to be case insensitive, SHOULD populate a canonical equivalent.
Tracing instrumentations that do so, MUST also set `http.request.method_original` to the original value.

**[2] `server.address`:** In HTTP/1.1, when the [request target](https://www.rfc-editor.org/rfc/rfc9112.html#name-request-target)
is passed in its [absolute-form](https://www.rfc-editor.org/rfc/rfc9112.html#section-3.2.2),
the `server.address` SHOULD match the host component of the request target.

In all other cases, `server.address` SHOULD match the host component of the
`Host` header in HTTP/1.1 or the `:authority` pseudo-header in HTTP/2 and HTTP/3.

**[3] `server.port`:** In the case of HTTP/1.1, when the [request target](https://www.rfc-editor.org/rfc/rfc9112.html#name-request-target)
is passed in its [absolute-form](https://www.rfc-editor.org/rfc/rfc9112.html#section-3.2.2),
the `server.port` SHOULD match the port component of the request target.

In all other cases, `server.port` SHOULD match the port component of the
`Host` header in HTTP/1.1 or the `:authority` pseudo-header in HTTP/2 and HTTP/3.

**[4] `url.full`:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment
is not transmitted over HTTP, but if it is known, it SHOULD be included nevertheless.

`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`.
In such case username and password SHOULD be redacted and attribute's value SHOULD be `https://REDACTED:REDACTED@www.example.com/`.

`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed).

Sensitive content provided in `url.full` SHOULD be scrubbed when instrumentations can identify it.

![Development](https://img.shields.io/badge/-development-blue)
Query string values for the following keys SHOULD be redacted by default and replaced by the
value `REDACTED`:

* [`AWSAccessKeyId`](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RESTAuthentication.html#RESTAuthenticationQueryStringAuth)
* [`Signature`](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RESTAuthentication.html#RESTAuthenticationQueryStringAuth)
* [`sig`](https://learn.microsoft.com/azure/storage/common/storage-sas-overview#sas-token)
* [`X-Goog-Signature`](https://cloud.google.com/storage/docs/access-control/signed-urls)

This list is subject to change over time.

When a query string value is redacted, the query string key SHOULD still be preserved, e.g.
`https://www.example.com/path?color=blue&sig=REDACTED`.

**[5] `error.type`:** If the request fails with an error before response status code was sent or received,
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

**[6] `http.request.method_original`:** If and only if it's different than `http.request.method`.

**[7] `network.protocol.name`:** If not `http` and `network.protocol.version` is set.

**[8] `network.protocol.name`:** The value SHOULD be normalized to lowercase.

**[9] `http.request.resend_count`:** The resend count SHOULD be updated each time an HTTP request gets resent by the client, regardless of what was the cause of the resending (e.g. redirection, authorization failure, 503 Server Unavailable, network issues, or any other).

**[10] `network.protocol.version`:** If protocol version is subject to negotiation (for example using [ALPN](https://www.rfc-editor.org/rfc/rfc7301.html)), this attribute SHOULD be set to the negotiated version. If the actual protocol version is not known, this attribute SHOULD NOT be set.

**[11] `http.request.header.<key>`:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured.
Including all request headers can be a security risk - explicit configuration helps avoid leaking sensitive information.

The `User-Agent` header is already captured in the `user_agent.original` attribute.
Users MAY explicitly configure instrumentations to capture them even though it is not recommended.

The attribute value MUST consist of either multiple header values as an array of strings
or a single-item array containing a possibly comma-concatenated string, depending on the way
the HTTP library provides access to headers.

Examples:

- A header `Content-Type: application/json` SHOULD be recorded as the `http.request.header.content-type`
  attribute with value `["application/json"]`.
- A header `X-Forwarded-For: 1.2.3.4, 1.2.3.5` SHOULD be recorded as the `http.request.header.x-forwarded-for`
  attribute with value `["1.2.3.4", "1.2.3.5"]` or `["1.2.3.4, 1.2.3.5"]` depending on the HTTP library.

**[12] `http.response.header.<key>`:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured.
Including all response headers can be a security risk - explicit configuration helps avoid leaking sensitive information.

Users MAY explicitly configure instrumentations to capture them even though it is not recommended.

The attribute value MUST consist of either multiple header values as an array of strings
or a single-item array containing a possibly comma-concatenated string, depending on the way
the HTTP library provides access to headers.

Examples:

- A header `Content-Type: application/json` header SHOULD be recorded as the `http.request.response.content-type`
  attribute with value `["application/json"]`.
- A header `My-custom-header: abc, def` header SHOULD be recorded as the `http.response.header.my-custom-header`
  attribute with value `["abc", "def"]` or `["abc, def"]` depending on the HTTP library.

**[13] `network.transport`:** Generally `tcp` for `HTTP/1.0`, `HTTP/1.1`, and `HTTP/2`. Generally `udp` for `HTTP/3`. Other obscure implementations are possible.

**[14] `url.template`:** The `url.template` MUST have low cardinality. It is not usually available on HTTP clients, but may be known by the application or specialized HTTP instrumentation.

**[15] `user_agent.synthetic.type`:** This attribute MAY be derived from the contents of the `user_agent.original` attribute. Components that populate the attribute are responsible for determining what they consider to be synthetic bot or test traffic. This attribute can either be set for self-identification purposes, or on telemetry detected to be generated as a result of a synthetic request. This attribute is useful for distinguishing between genuine client traffic and synthetic traffic generated by bots or tests.

The following attributes can be important for making sampling decisions
and SHOULD be provided **at span creation time** (if provided at all):

* [`http.request.method`](/docs/registry/attributes/http.md)
* [`server.address`](/docs/registry/attributes/server.md)
* [`server.port`](/docs/registry/attributes/server.md)
* [`url.full`](/docs/registry/attributes/url.md)

---

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`http.request.method` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `_OTHER` | Any HTTP method that the instrumentation has no prior knowledge of. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `CONNECT` | CONNECT method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `DELETE` | DELETE method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `GET` | GET method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `HEAD` | HEAD method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `OPTIONS` | OPTIONS method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `PATCH` | PATCH method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `POST` | POST method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `PUT` | PUT method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `QUERY` | QUERY method. | ![Development](https://img.shields.io/badge/-development-blue) |
| `TRACE` | TRACE method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `pipe` | Named or anonymous pipe. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `quic` | QUIC | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `tcp` | TCP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`user_agent.synthetic.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `bot` | Bot source. | ![Development](https://img.shields.io/badge/-development-blue) |
| `test` | Synthetic test source. | ![Development](https://img.shields.io/badge/-development-blue) |

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

> [!NOTE]
> The `Host` and `:authority` headers contain host and port number of the server. The same applies to the `host` identifier of `Forwarded` header or the `X-Forwarded-Host` header. Instrumentations SHOULD populate both `server.address` and `server.port` attributes by parsing the value of corresponding header.

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

### HTTP server span

<!-- semconv span.http.server -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Stable](https://img.shields.io/badge/-stable-lightgreen)

This span represents an inbound HTTP request.

**Span name:** refer to the [Span Name](/docs/http/http-spans.md#name) section.

**Span kind** MUST be `SERVER`.

**Span status:** refer to the [Span Status](/docs/http/http-spans.md#status) section.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`http.request.method`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Required` | string | HTTP request method. [1] | `GET`; `POST`; `HEAD` |
| [`url.path`](/docs/registry/attributes/url.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Required` | string | The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component [2] | `/search` |
| [`url.scheme`](/docs/registry/attributes/url.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Required` | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. [3] | `http`; `https` |
| [`error.type`](/docs/registry/attributes/error.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If request has ended with an error. | string | Describes a class of error the operation ended with. [4] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` |
| [`http.request.method_original`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [5] | string | Original HTTP method sent by the client in the request line. | `GeT`; `ACL`; `foo` |
| [`http.response.status_code`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If and only if one was received/sent. | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` |
| [`http.route`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If and only if it's available | string | The matched route template for the request. This MUST be low-cardinality and include all static path segments, with dynamic path segments represented with placeholders. [6] | `/users/:userID?`; `my-controller/my-action/{id?}` |
| [`network.protocol.name`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [7] | string | [OSI application layer](https://wikipedia.org/wiki/Application_layer) or non-OSI equivalent. [8] | `http`; `spdy` |
| [`server.port`](/docs/registry/attributes/server.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If available and `server.address` is set. | int | Port of the local HTTP server that received the request. [9] | `80`; `8080`; `443` |
| [`url.query`](/docs/registry/attributes/url.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If and only if one was received/sent. | string | The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [10] | `q=OpenTelemetry` |
| [`client.address`](/docs/registry/attributes/client.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [11] | `83.164.160.102` |
| [`network.peer.address`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` |
| [`network.peer.port`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` If `network.peer.address` is set. | int | Peer port number of the network connection. | `65123` |
| [`network.protocol.version`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | The actual version of the protocol used for network communication. [12] | `1.0`; `1.1`; `2`; `3` |
| [`server.address`](/docs/registry/attributes/server.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Name of the local HTTP server that received the request. [13] | `example.com`; `10.1.2.80`; `/tmp/my.sock` |
| [`user_agent.original`](/docs/registry/attributes/user-agent.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1`; `YourApp/1.0.0 grpc-java-okhttp/1.27.2` |
| [`client.port`](/docs/registry/attributes/client.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | int | The port of whichever client was captured in `client.address`. [14] | `65123` |
| [`http.request.body.size`](/docs/registry/attributes/http.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | int | The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` |
| [`http.request.header.<key>`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [15] | `["application/json"]`; `["1.2.3.4", "1.2.3.5"]` |
| [`http.request.size`](/docs/registry/attributes/http.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | int | The total size of the request in bytes. This should be the total number of bytes sent over the wire, including the request line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and request body if any. | `1437` |
| [`http.response.body.size`](/docs/registry/attributes/http.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | int | The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` |
| [`http.response.header.<key>`](/docs/registry/attributes/http.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string[] | HTTP response headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [16] | `["application/json"]`; `["abc", "def"]` |
| [`http.response.size`](/docs/registry/attributes/http.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | int | The total size of the response in bytes. This should be the total number of bytes sent over the wire, including the status line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and response body and trailers if any. | `1437` |
| [`network.local.address`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string | Local socket address. Useful in case of a multi-IP host. | `10.1.2.80`; `/tmp/my.sock` |
| [`network.local.port`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | int | Local socket port. Useful in case of a multi-port host. | `65123` |
| [`network.transport`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Opt-In` | string | [OSI transport layer](https://wikipedia.org/wiki/Transport_layer) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [17] | `tcp`; `udp` |
| [`user_agent.synthetic.type`](/docs/registry/attributes/user-agent.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Opt-In` | string | Specifies the category of synthetic traffic, such as tests or bots. [18] | `bot`; `test` |

**[1] `http.request.method`:** HTTP request method value SHOULD be "known" to the instrumentation.
By default, this convention defines "known" methods as the ones listed in [RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-methods),
the PATCH method defined in [RFC5789](https://www.rfc-editor.org/rfc/rfc5789.html)
and the QUERY method defined in [httpbis-safe-method-w-body](https://datatracker.ietf.org/doc/draft-ietf-httpbis-safe-method-w-body/?include_text=1).

If the HTTP request method is not known to instrumentation, it MUST set the `http.request.method` attribute to `_OTHER`.

If the HTTP instrumentation could end up converting valid HTTP request methods to `_OTHER`, then it MUST provide a way to override
the list of known HTTP methods. If this override is done via environment variable, then the environment variable MUST be named
OTEL_INSTRUMENTATION_HTTP_KNOWN_METHODS and support a comma-separated list of case-sensitive known HTTP methods
(this list MUST be a full override of the default known method, it is not a list of known methods in addition to the defaults).

HTTP method names are case-sensitive and `http.request.method` attribute value MUST match a known HTTP method name exactly.
Instrumentations for specific web frameworks that consider HTTP methods to be case insensitive, SHOULD populate a canonical equivalent.
Tracing instrumentations that do so, MUST also set `http.request.method_original` to the original value.

**[2] `url.path`:** Sensitive content provided in `url.path` SHOULD be scrubbed when instrumentations can identify it.

**[3] `url.scheme`:** The scheme of the original client request, if known (e.g. from [Forwarded#proto](https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#proto), [X-Forwarded-Proto](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-Proto), or a similar header). Otherwise, the scheme of the immediate peer request.

**[4] `error.type`:** If the request fails with an error before response status code was sent or received,
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

**[5] `http.request.method_original`:** If and only if it's different than `http.request.method`.

**[6] `http.route`:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

A static path segment is a part of the route template with a fixed, low-cardinality value. This includes literal strings like `/users/` and placeholders that
are constrained to a finite, predefined set of values, e.g. `{controller}` or `{action}`.

A dynamic path segment is a placeholder for a value that can have high cardinality and is not constrained to a predefined list like static path segments.

Instrumentations SHOULD use routing information provided by the corresponding web framework. They SHOULD pick the most precise source of routing information and MAY
support custom route formatting. Instrumentations SHOULD document the format and the API used to obtain the route string.

**[7] `network.protocol.name`:** If not `http` and `network.protocol.version` is set.

**[8] `network.protocol.name`:** The value SHOULD be normalized to lowercase.

**[9] `server.port`:** See [Setting `server.address` and `server.port` attributes](/docs/http/http-spans.md#setting-serveraddress-and-serverport-attributes).

**[10] `url.query`:** Sensitive content provided in `url.query` SHOULD be scrubbed when instrumentations can identify it.

![Development](https://img.shields.io/badge/-development-blue)
Query string values for the following keys SHOULD be redacted by default and replaced by the value `REDACTED`:

* [`AWSAccessKeyId`](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RESTAuthentication.html#RESTAuthenticationQueryStringAuth)
* [`Signature`](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RESTAuthentication.html#RESTAuthenticationQueryStringAuth)
* [`sig`](https://learn.microsoft.com/azure/storage/common/storage-sas-overview#sas-token)
* [`X-Goog-Signature`](https://cloud.google.com/storage/docs/access-control/signed-urls)

This list is subject to change over time.

When a query string value is redacted, the query string key SHOULD still be preserved, e.g.
`q=OpenTelemetry&sig=REDACTED`.

**[11] `client.address`:** The IP address of the original client behind all proxies, if known (e.g. from [Forwarded#for](https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#for), [X-Forwarded-For](https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-For), or a similar header). Otherwise, the immediate client peer address.

**[12] `network.protocol.version`:** If protocol version is subject to negotiation (for example using [ALPN](https://www.rfc-editor.org/rfc/rfc7301.html)), this attribute SHOULD be set to the negotiated version. If the actual protocol version is not known, this attribute SHOULD NOT be set.

**[13] `server.address`:** See [Setting `server.address` and `server.port` attributes](/docs/http/http-spans.md#setting-serveraddress-and-serverport-attributes).

**[14] `client.port`:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries,  for example proxies, if it's available.

**[15] `http.request.header.<key>`:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured.
Including all request headers can be a security risk - explicit configuration helps avoid leaking sensitive information.

The `User-Agent` header is already captured in the `user_agent.original` attribute.
Users MAY explicitly configure instrumentations to capture them even though it is not recommended.

The attribute value MUST consist of either multiple header values as an array of strings
or a single-item array containing a possibly comma-concatenated string, depending on the way
the HTTP library provides access to headers.

Examples:

- A header `Content-Type: application/json` SHOULD be recorded as the `http.request.header.content-type`
  attribute with value `["application/json"]`.
- A header `X-Forwarded-For: 1.2.3.4, 1.2.3.5` SHOULD be recorded as the `http.request.header.x-forwarded-for`
  attribute with value `["1.2.3.4", "1.2.3.5"]` or `["1.2.3.4, 1.2.3.5"]` depending on the HTTP library.

**[16] `http.response.header.<key>`:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured.
Including all response headers can be a security risk - explicit configuration helps avoid leaking sensitive information.

Users MAY explicitly configure instrumentations to capture them even though it is not recommended.

The attribute value MUST consist of either multiple header values as an array of strings
or a single-item array containing a possibly comma-concatenated string, depending on the way
the HTTP library provides access to headers.

Examples:

- A header `Content-Type: application/json` header SHOULD be recorded as the `http.request.response.content-type`
  attribute with value `["application/json"]`.
- A header `My-custom-header: abc, def` header SHOULD be recorded as the `http.response.header.my-custom-header`
  attribute with value `["abc", "def"]` or `["abc, def"]` depending on the HTTP library.

**[17] `network.transport`:** Generally `tcp` for `HTTP/1.0`, `HTTP/1.1`, and `HTTP/2`. Generally `udp` for `HTTP/3`. Other obscure implementations are possible.

**[18] `user_agent.synthetic.type`:** This attribute MAY be derived from the contents of the `user_agent.original` attribute. Components that populate the attribute are responsible for determining what they consider to be synthetic bot or test traffic. This attribute can either be set for self-identification purposes, or on telemetry detected to be generated as a result of a synthetic request. This attribute is useful for distinguishing between genuine client traffic and synthetic traffic generated by bots or tests.

The following attributes can be important for making sampling decisions
and SHOULD be provided **at span creation time** (if provided at all):

* [`client.address`](/docs/registry/attributes/client.md)
* [`http.request.header.<key>`](/docs/registry/attributes/http.md)
* [`http.request.method`](/docs/registry/attributes/http.md)
* [`server.address`](/docs/registry/attributes/server.md)
* [`server.port`](/docs/registry/attributes/server.md)
* [`url.path`](/docs/registry/attributes/url.md)
* [`url.query`](/docs/registry/attributes/url.md)
* [`url.scheme`](/docs/registry/attributes/url.md)
* [`user_agent.original`](/docs/registry/attributes/user-agent.md)

---

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`http.request.method` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `_OTHER` | Any HTTP method that the instrumentation has no prior knowledge of. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `CONNECT` | CONNECT method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `DELETE` | DELETE method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `GET` | GET method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `HEAD` | HEAD method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `OPTIONS` | OPTIONS method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `PATCH` | PATCH method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `POST` | POST method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `PUT` | PUT method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `QUERY` | QUERY method. | ![Development](https://img.shields.io/badge/-development-blue) |
| `TRACE` | TRACE method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `pipe` | Named or anonymous pipe. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `quic` | QUIC | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `tcp` | TCP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`user_agent.synthetic.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `bot` | Bot source. | ![Development](https://img.shields.io/badge/-development-blue) |
| `test` | Synthetic test source. | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

`http.route` MUST be provided at span creation time if and only if it's already available. If it becomes available after span starts, instrumentation MUST populate it anytime before span ends.

## Examples

### HTTP client-server example

As an example, if a browser request for `https://example.com:8080/webshop/articles/4?s=1&t=2` is invoked from a host with IP 192.0.2.4, we may have the following Span on the client side:

Span name: `GET`

| Attribute name              | Value                                                   |
| :-------------------------- | :------------------------------------------------------ |
| `http.request.method`       | `"GET"`                                                 |
| `network.protocol.version`  | `"1.1"`                                                 |
| `url.full`                  | `"https://example.com:8080/webshop/articles/4?s=1&t=2"` |
| `server.address`            | `example.com`                                           |
| `server.port`               | `8080`                                                  |
| `network.peer.address`      | `"192.0.2.5"`                                           |
| `network.peer.port`         | `8080`                                                  |
| `http.response.status_code` | `200`                                                   |

The corresponding server Span may look like this:

Span name: `GET /webshop/articles/:article_id`.

| Attribute name              | Value                                                                              |
| :-------------------------- | :--------------------------------------------------------------------------------- |
| `http.request.method`       | `"GET"`                                                                            |
| `network.protocol.version`  | `"1.1"`                                                                            |
| `url.path`                  | `"/webshop/articles/4"`                                                            |
| `url.query`                 | `"s=1&t=2"`                                                                        |
| `server.address`            | `"example.com"`                                                                    |
| `server.port`               | `8080`                                                                             |
| `url.scheme`                | `"https"`                                                                          |
| `http.route`                | `"/webshop/articles/:article_id"`                                                  |
| `http.response.status_code` | `200`                                                                              |
| `client.address`            | `"192.0.2.4"`                                                                      |
| `network.peer.address`      | `"192.0.2.5"` (the client goes through a proxy)                                    |
| `user_agent.original`       | `"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"` |

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

| Attribute name             | Value                              |
| :------------------------- | :--------------------------------- |
| `http.request.method`      | `"GET"`                            |
| `network.protocol.version` | `"1.1"`                            |
| `url.full`                 | `"https://does-not-exist-123.com"` |
| `server.address`           | `"does-not-exist-123.com"`         |
| `error.type`               | `"java.net.UnknownHostException"`  |

### HTTP client call: Internal Server Error

As an example, if a user requested `https://example.com` and server returned 500, we may have the following span on the client side:

| Attribute name              | Value                   |
| :-------------------------- | :---------------------- |
| `http.request.method`       | `"GET"`                 |
| `network.protocol.version`  | `"1.1"`                 |
| `url.full`                  | `"https://example.com"` |
| `server.address`            | `"example.com"`         |
| `http.response.status_code` | `500`                   |
| `error.type`                | `"500"`                 |

### HTTP server call: connection dropped before response body was sent

As an example, if a user sent a `POST` request with a body to `https://example.com:8080/uploads/4`, we may see the following span on a server side:

Span name: `POST /uploads/:document_id`.

| Attribute name              | Value                     |
| :-------------------------- | :------------------------ |
| `http.request.method`       | `"POST"`                  |
| `url.path`                  | `"/uploads/4"`            |
| `url.scheme`                | `"https"`                 |
| `http.route`                | `"/uploads/:document_id"` |
| `http.response.status_code` | `201`                     |
| `error.type`                | `WebSocketDisconnect`     |

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
[SpanProcessor]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/trace/sdk.md#span-processor
