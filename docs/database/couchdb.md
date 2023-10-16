<!--- Hugo front matter used to generate the website version of this page:
linkTitle: CouchDB
--->

# Semantic Conventions for CouchDB

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [CouchDB](https://couchdb.apache.org/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"couchdb"`.

## Call-level attributes

<!-- semconv db.couchdb(tag=call-level-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.operation`](database-spans.md) | string | The HTTP method + the target REST route. [1] | `GET /{db}/{docid}` | Conditionally Required: If `db.statement` is not applicable. |

**[1]:** In **CouchDB**, `db.operation` should be set to the HTTP method + the target REST route according to the API reference documentation. For example, when retrieving a document, `db.operation` would be set to (literally, i.e., without replacing the placeholders with concrete values): [`GET /{db}/{docid}`](http://docs.couchdb.org/stable/api/document/common.html#get--db-docid).
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
