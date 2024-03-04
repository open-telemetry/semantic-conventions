<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Elasticsearch
--->

# Semantic Conventions for Elasticsearch

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Elasticsearch](https://www.elastic.co/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"elasticsearch"`.

## Span Name

The **span name** SHOULD be of the format `<endpoint id>`.

The elasticsearch endpoint identifier is used instead of the url path in order to reduce the cardinality of the span
name, as the path could contain dynamic values. The endpoint id is the `name` field in the
[elasticsearch schema](https://raw.githubusercontent.com/elastic/elasticsearch-specification/main/output/schema/schema.json).
If the endpoint id is not available, the span name SHOULD be the `http.request.method`.

## Attributes

<!-- semconv db.elasticsearch(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.elasticsearch.cluster.name`](../attributes-registry/db.md) | string | Represents the identifier of an Elasticsearch cluster. | `e9106fc68e3044f0b1475b04bf4ffd5f` | Recommended: [1] |
| [`db.elasticsearch.node.name`](../attributes-registry/db.md) | string | Represents the human-readable identifier of the node/instance to which a request was routed. | `instance-0000000001` | Recommended: [2] |
| [`db.elasticsearch.path_parts.<key>`](../attributes-registry/db.md) | string | A dynamic value in the url path. [3] | `db.elasticsearch.path_parts.index=test-index`; `db.elasticsearch.path_parts.doc_id=123` | Conditionally Required: when the url has dynamic values |
| [`db.operation`](../attributes-registry/db.md) | string | The endpoint identifier for the request. [4] | `search`; `ml.close_job`; `cat.aliases` | Required |
| [`db.statement`](../attributes-registry/db.md) | string | The request body for a [search-type query](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html), as a json string. | `"{\"query\":{\"term\":{\"user.id\":\"kimchy\"}}}"` | Recommended: [5] |
| [`http.request.method`](../attributes-registry/http.md) | string | HTTP request method. [6] | `GET`; `POST`; `HEAD` | Required |
| [`server.address`](../attributes-registry/server.md) | string | Name of the database host. [7] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [8] | `80`; `8080`; `443` | Conditionally Required: [9] |
| [`url.full`](../attributes-registry/url.md) | string | Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [10] | `https://localhost:9200/index/_search?q=user.id:kimchy` | Required |

**[1]:** When communicating with an Elastic Cloud deployment, this should be collected from the "X-Found-Handling-Cluster" HTTP response header.

**[2]:** When communicating with an Elastic Cloud deployment, this should be collected from the "X-Found-Handling-Instance" HTTP response header.

**[3]:** Many Elasticsearch url paths allow dynamic values. These SHOULD be recorded in span attributes in the format `db.elasticsearch.path_parts.<key>`, where `<key>` is the url path part name. The implementation SHOULD reference the [elasticsearch schema](https://raw.githubusercontent.com/elastic/elasticsearch-specification/main/output/schema/schema.json) in order to map the path part values to their names.

**[4]:** When setting this to an SQL keyword, it is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if the operation name is provided by the library being instrumented. If the SQL statement has an ambiguous operation, or performs more than one operation, this value may be omitted.

**[5]:** Should be collected by default for search-type queries and only if there is sanitization that excludes sensitive information.

**[6]:** HTTP request method value SHOULD be "known" to the instrumentation.
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

**[7]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[8]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[9]:** If using a port other than the default port for this DBMS and if `server.address` is set.

**[10]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it SHOULD be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password SHOULD be redacted and attribute's value SHOULD be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed). Sensitive content provided in `url.full` SHOULD be scrubbed when instrumentations can identify it.

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

## Example

| Key                                 | Value                                                                                                                               |
|:------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|
| Span name                           | `"search"`                                                                                                                          |
| `db.system`                         | `"elasticsearch"`                                                                                                                   |
| `server.address`                    | `"elasticsearch.mydomain.com"`                                                                                                      |
| `server.port`                       | `9200`                                                                                                                              |
| `http.request.method`               | `"GET"`                                                                                                                             |
| `db.statement`                      | `"{\"query\":{\"term\":{\"user.id\":\"kimchy\"}}}"`                                                                                 |
| `db.operation`                      | `"search"`                                                                                                                          |
| `url.full`                          | `"https://elasticsearch.mydomain.com:9200/my-index-000001/_search?from=40&size=20"`                                                 |
| `db.elasticsearch.path_parts.index` | `"my-index-000001"`                                                                                                                 |
| `db.elasticsearch.cluster.name`     | `"e9106fc68e3044f0b1475b04bf4ffd5f"`                                                                                                |
| `db.elasticsearch.node.name` | `"instance-0000000001"`                                                                                                             |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
