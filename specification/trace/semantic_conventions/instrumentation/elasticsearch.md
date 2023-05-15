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
<!-- endsemconv -->
