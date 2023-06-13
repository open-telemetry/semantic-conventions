# Semantic conventions for Elasticsearch

**Status**: [Experimental](../../../document-status.md)

This document defines semantic conventions to apply when creating a span for requests to Elasticsearch.

## Span Name

The **span name** SHOULD be of the format `<endpoint id>`.

The elasticsearch endpoint identifier is used instead of the url path in order to reduce the cardinality of the span 
name, as the path could contain dynamic values. The endpoint id is the `name` field in the
[elasticsearch schema](https://raw.githubusercontent.com/elastic/elasticsearch-specification/main/output/schema/schema.json).
If the endpoint id is not available, the span name SHOULD be `http.request.method`.

## URL path parts

Many Elasticsearch url paths allow dynamic values. These SHOULD be recorded in span attributes in the format
`db.elasticsearch.path_parts.<key>`, where `<key>` is the url path part name. The implementation SHOULD
reference the [elasticsearch schema](https://raw.githubusercontent.com/elastic/elasticsearch-specification/main/output/schema/schema.json)
in order to map the path part values to their names.

| Attribute                           | Type | Description                           | Examples                                                                                 | Requirement Level |
|-------------------------------------|---|---------------------------------------|------------------------------------------------------------------------------------------|---|
| `db.elasticsearch.path_parts.<key>` | string | A dynamic value in the url path.      | `db.elasticsearch.path_parts.index=test-index`; `db.elasticsearch.path_parts.doc_id=123` | Conditionally Required: [1] |

**[1]:** when the url has dynamic values

## Span attributes

<!-- semconv db.elasticsearch -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.operation`](../database.md) | string | The endpoint identifier for the request. [1] | `search`; `ml.close_job`; `cat.aliases` | Required |
| [`db.statement`](../database.md) | string | The request body for a [search-type query](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html), as a json string. [2] | `"{\"name\":\"TestUser\",\"password\":\"REDACTED\"}"` | Recommended: [3] |
| `http.request.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | Required |
| [`server.address`](../span-general.md) | string | Logical server hostname, matches server FQDN if available, and IP or socket address if FQDN is not known. | `example.com` | See below |
| [`server.port`](../span-general.md) | int | Logical server port number | `80`; `8080`; `443` | Recommended |
| `url.full` | string | Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [4] | `https://localhost:9200/index/_search?q=user.id:kimchy` | Required |

**[1]:** When setting this to an SQL keyword, it is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if the operation name is provided by the library being instrumented. If the SQL statement has an ambiguous operation, or performs more than one operation, this value may be omitted.

**[2]:** The value may be sanitized to exclude sensitive information.

**[3]:** Should be collected when a search-type query is executed

**[4]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password should be redacted and attribute's value should be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed) and SHOULD NOT be validated or modified except for sanitizing purposes.
<!-- endsemconv -->
