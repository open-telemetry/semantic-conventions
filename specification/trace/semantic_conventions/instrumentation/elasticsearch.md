# Semantic conventions for Elasticsearch

**Status**: [Experimental](../../../document-status.md)

This document defines semantic conventions to apply when instrumenting requests to Elasticsearch. They map Elasticsearch
requests to attributes on a Span.

## Span Name

The **span name** SHOULD be of the format `<http.method> <db.elasticsearch.url *with placeholders*>`.

The elasticsearch url is modified with placeholders in order to reduce the cardinality of the span name. When the url
contains a document id, it SHOULD be replaced by the identifier `{id}`. When the url contains a target data stream or
index, it SHOULD be replaced by `{target}`.
For example, a request to `/test-index/_doc/123` should have the span name `GET /{target}/_doc/{id}`.
When there is no target or document id, the span name will contain the exact url, as in `POST /_search`.

### Span attributes

<!-- semconv db.elasticsearch -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `db.elasticsearch.doc_id` | string | The document that the request targets. | `123`; `456` | Conditionally Required: [1] |
| `db.elasticsearch.target` | string | The name of the data stream or index that is targeted. | `users` | Conditionally Required: [2] |
| [`db.statement`](../database.md) | string | The request body, as a json string. [3] | `"{\"name\":\"TestUser\",\"password\":\"top_secret\"}"` | Conditionally Required: when there is a request body |
| `http.request.method` | string | HTTP request method. | `GET`; `POST`; `HEAD` | Required |
| `url.path` | string | The path of the request, including the target and exact document id. [4] | `/test-index/_search`; `/test-index/_doc/123` | Required |
| `url.query` | string | The query params of the request, as a json string. [5] | `"{\"q\":\"test\"}", "{\"refresh\":true}"` | Conditionally Required: [6] |

**[1]:** when the request targets a specific document by id

**[2]:** when a specific index or data stream is targeted by the request

**[3]:** The value may be sanitized to exclude sensitive information.

**[4]:** When missing, the value is assumed to be `/`

**[5]:** Sensitive content provided in query string SHOULD be scrubbed when instrumentations can identify it.

**[6]:** when query params are provided as part of the request
<!-- endsemconv -->
