# Semantic Conventions for IBM CICS Transaction Server for z/OS Spans

This documents defines for spans of IBM CICS Transaction Server for z/OS.

## Semantic Conventions for CICS HTTP Server Spans

<!-- semconv span.tps.cics.http.server -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`http.request.method`](/docs/attributes-registry/http.md) | string | HTTP request method. [1] | `GET`; `POST`; `HEAD` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`tps.system`](/docs/attributes-registry/tps.md) | string | Type of Transaction Processing System | `cics` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.transaction.id`](/docs/attributes-registry/tps.md) | string | Identifier of the transaction initiated by a user or system request | `TRX1` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`url.path`](/docs/attributes-registry/url.md) | string | The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component [2] | `/search` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`url.scheme`](/docs/attributes-registry/url.md) | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. [3] | `http`; `https` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [4] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` If request has ended with an error. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.request.method_original`](/docs/attributes-registry/http.md) | string | Original HTTP method sent by the client in the request line. | `GeT`; `ACL`; `foo` | `Conditionally Required` [5] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.response.status_code`](/docs/attributes-registry/http.md) | int | [HTTP response status code](https://tools.ietf.org/html/rfc7231#section-6). | `200` | `Conditionally Required` If and only if one was received/sent. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.route`](/docs/attributes-registry/http.md) | string | The matched route, that is, the path template in the format used by the respective server framework. [6] | `/users/:userID?`; `{controller}/{action}/{id?}` | `Conditionally Required` If and only if it's available | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.protocol.name`](/docs/attributes-registry/network.md) | string | [OSI application layer](https://wikipedia.org/wiki/Application_layer) or non-OSI equivalent. [7] | `http`; `spdy` | `Conditionally Required` [8] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Port of the local HTTP server that received the request. [9] | `80`; `8080`; `443` | `Conditionally Required` If available and `server.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`url.query`](/docs/attributes-registry/url.md) | string | The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [10] | `q=OpenTelemetry` | `Conditionally Required` If and only if one was received/sent. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`client.address`](/docs/attributes-registry/client.md) | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [11] | `83.164.160.102` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` If `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.protocol.version`](/docs/attributes-registry/network.md) | string | The actual version of the protocol used for network communication. [12] | `1.0`; `1.1`; `2`; `3` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Name of the local HTTP server that received the request. [13] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`tps.program.name`](/docs/attributes-registry/tps.md) | string | Program name executed by the task | `PROG123` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.region.id`](/docs/attributes-registry/tps.md) | string | Runtime environment within the Transaction Processing System | `PRD1` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.task.id`](/docs/attributes-registry/tps.md) | string | Identifier of the task created to run the transaction | `1554` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.transaction.owner`](/docs/attributes-registry/tps.md) | string | Identifier of the user owning the transaction | `USER` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.unit_of_work.id`](/docs/attributes-registry/tps.md) | string | Unit of work executed by the program | `DF308CBF385A3C05` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`user_agent.original`](/docs/attributes-registry/user-agent.md) | string | Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1`; `YourApp/1.0.0 grpc-java-okhttp/1.27.2` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`client.port`](/docs/attributes-registry/client.md) | int | The port of whichever client was captured in `client.address`. [14] | `65123` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.request.body.size`](/docs/attributes-registry/http.md) | int | The size of the request payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.request.header.<key>`](/docs/attributes-registry/http.md) | string[] | HTTP request headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [15] | `http.request.header.content-type=["application/json"]`; `http.request.header.x-forwarded-for=["1.2.3.4", "1.2.3.5"]` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.request.size`](/docs/attributes-registry/http.md) | int | The total size of the request in bytes. This should be the total number of bytes sent over the wire, including the request line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and request body if any. | `1437` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.response.body.size`](/docs/attributes-registry/http.md) | int | The size of the response payload body in bytes. This is the number of bytes transferred excluding headers and is often, but not always, present as the [Content-Length](https://www.rfc-editor.org/rfc/rfc9110.html#field.content-length) header. For requests using transport encoding, this should be the compressed size. | `3495` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`http.response.header.<key>`](/docs/attributes-registry/http.md) | string[] | HTTP response headers, `<key>` being the normalized HTTP Header name (lowercase), the value being the header values. [16] | `http.response.header.content-type=["application/json"]`; `http.response.header.my-custom-header=["abc", "def"]` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`http.response.size`](/docs/attributes-registry/http.md) | int | The total size of the response in bytes. This should be the total number of bytes sent over the wire, including the status line (HTTP/1.1), framing (HTTP/2 and HTTP/3), headers, and response body and trailers if any. | `1437` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`network.local.address`](/docs/attributes-registry/network.md) | string | Local socket address. Useful in case of a multi-IP host. | `10.1.2.80`; `/tmp/my.sock` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.local.port`](/docs/attributes-registry/network.md) | int | Local socket port. Useful in case of a multi-port host. | `65123` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.transport`](/docs/attributes-registry/network.md) | string | [OSI transport layer](https://wikipedia.org/wiki/Transport_layer) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [17] | `tcp`; `udp` | `Opt-In` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`user_agent.synthetic.type`](/docs/attributes-registry/user-agent.md) | string | Specifies the category of synthetic traffic, such as tests or bots. [18] | `bot`; `test` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1] `http.request.method`:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[7] `network.protocol.name`:** The value SHOULD be normalized to lowercase.

**[8] `network.protocol.name`:** If not `http` and `network.protocol.version` is set.

**[9] `server.port`:** See [Setting `server.address` and `server.port` attributes](/docs/http/http-spans.md#setting-serveraddress-and-serverport-attributes).

**[10] `url.query`:** Sensitive content provided in `url.query` SHOULD be scrubbed when instrumentations can identify it.

![Experimental](https://img.shields.io/badge/-experimental-blue)
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

**[15] `http.request.header`:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all request headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
The `User-Agent` header is already captured in the `user_agent.original` attribute. Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[16] `http.response.header`:** Instrumentations SHOULD require an explicit configuration of which headers are to be captured. Including all response headers can be a security risk - explicit configuration helps avoid leaking sensitive information.
Users MAY explicitly configure instrumentations to capture them even though it is not recommended.
The attribute value MUST consist of either multiple header values as an array of strings or a single-item array containing a possibly comma-concatenated string, depending on the way the HTTP library provides access to headers.

**[17] `network.transport`:** Generally `tcp` for `HTTP/1.0`, `HTTP/1.1`, and `HTTP/2`. Generally `udp` for `HTTP/3`. Other obscure implementations are possible.

**[18] `user_agent.synthetic.type`:** This attribute MAY be derived from the contents of the `user_agent.original` attribute. Components that populate the attribute are responsible for determining what they consider to be synthetic bot or test traffic. This attribute can either be set for self-identification purposes, or on telemetry detected to be generated as a result of a synthetic request. This attribute is useful for distinguishing between genuine client traffic and synthetic traffic generated by bots or tests.

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

---

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`http.request.method` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | Any HTTP method that the instrumentation has no prior knowledge of. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `CONNECT` | CONNECT method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `DELETE` | DELETE method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `GET` | GET method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `HEAD` | HEAD method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `OPTIONS` | OPTIONS method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `PATCH` | PATCH method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `POST` | POST method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `PUT` | PUT method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `TRACE` | TRACE method. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `pipe` | Named or anonymous pipe. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `quic` | QUIC | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tcp` | TCP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`user_agent.synthetic.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `bot` | Bot source. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `test` | Synthetic test source. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Semantic Conventions for CICS RPC Server Spans

<!-- semconv span.tps.cics.rpc.server -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`rpc.system`](/docs/attributes-registry/rpc.md) | string | A string identifying the remoting system. See below for a list of well-known identifiers. | `dpl`; `rmi` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | RPC server [host name](https://grpc.github.io/grpc/core/md_doc_naming.html). [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`tps.system`](/docs/attributes-registry/tps.md) | string | Type of Transaction Processing System | `cics` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.transaction.id`](/docs/attributes-registry/tps.md) | string | Identifier of the transaction initiated by a user or system request | `TRX1` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [2] | `80`; `8080`; `443` | `Conditionally Required` [3] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`client.address`](/docs/attributes-registry/client.md) | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [4] | `client.example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`client.port`](/docs/attributes-registry/client.md) | int | Client port number. [5] | `65123` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` If `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.protocol.name`](/docs/attributes-registry/network.md) | string | [OSI application layer](https://wikipedia.org/wiki/Application_layer) or non-OSI equivalent. [6] | `ipic`; `mro` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.transport`](/docs/attributes-registry/network.md) | string | [OSI transport layer](https://wikipedia.org/wiki/Transport_layer) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [7] | `tcp`; `udp` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.type`](/docs/attributes-registry/network.md) | string | [OSI network layer](https://wikipedia.org/wiki/Network_layer) or non-OSI equivalent. [8] | `ipv4`; `ipv6` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`rpc.method`](/docs/attributes-registry/rpc.md) | string | The name of the (logical) method being called, must be equal to the $method part in the span name. [9] | `exampleMethod` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`rpc.service`](/docs/attributes-registry/rpc.md) | string | The full (logical) name of the service being called, including its package name, if applicable. [10] | `myservice.EchoService` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.program.name`](/docs/attributes-registry/tps.md) | string | Program name executed by the task | `PROG123` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.region.id`](/docs/attributes-registry/tps.md) | string | Runtime environment within the Transaction Processing System | `PRD1` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.task.id`](/docs/attributes-registry/tps.md) | string | Identifier of the task created to run the transaction | `1554` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.transaction.owner`](/docs/attributes-registry/tps.md) | string | Identifier of the user owning the transaction | `USER` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`tps.unit_of_work.id`](/docs/attributes-registry/tps.md) | string | Unit of work executed by the program | `DF308CBF385A3C05` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1] `server.address`:** May contain server IP address, DNS name, or local socket name. When host component is an IP address, instrumentations SHOULD NOT do a reverse proxy lookup to obtain DNS name and SHOULD set `server.address` to the IP address provided in the host component.

**[2] `server.port`:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[3] `server.port`:** if the port is supported by the network transport used for communication.

**[4] `client.address`:** When observed from the server side, and when communicating through an intermediary, `client.address` SHOULD represent the client address behind any intermediaries,  for example proxies, if it's available.

**[5] `client.port`:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries,  for example proxies, if it's available.

**[6] `network.protocol.name`:** The value SHOULD be normalized to lowercase.

**[7] `network.transport`:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[8] `network.type`:** The value SHOULD be normalized to lowercase.

**[9] `rpc.method`:** This is the logical name of the method from the RPC interface perspective, which can be different from the name of any implementing method/function. The `code.function` attribute may be used to store the latter (e.g., method actually executing the call on the server side, RPC client stub method on the client side).

**[10] `rpc.service`:** This is the logical name of the service from the RPC interface perspective, which can be different from the name of any implementing class. The `code.namespace` attribute may be used to store the latter (despite the attribute name, it may include a class name; e.g., class with method actually executing the call on the server side, RPC client stub class on the client side).

---

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `pipe` | Named or anonymous pipe. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `quic` | QUIC | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tcp` | TCP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `ipv4` | IPv4 | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `ipv6` | IPv6 | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

---

`rpc.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `apache_dubbo` | Apache Dubbo | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `connect_rpc` | Connect RPC | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `dotnet_wcf` | .NET WCF | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `grpc` | gRPC | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `java_rmi` | Java RMI | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->