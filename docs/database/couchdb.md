<!--- Hugo front matter used to generate the website version of this page:
linkTitle: CouchDB
--->

# Semantic Conventions for CouchDB

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [CouchDB](https://couchdb.apache.org/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"couchdb"`.

## Attributes

<!-- semconv db.couchdb(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.operation.name`](../attributes-registry/db.md) | string | The HTTP method + the target REST route. [1] | `GET /{db}/{docid}` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** In **CouchDB**, `db.operation.name` should be set to the HTTP method + the target REST route according to the API reference documentation. For example, when retrieving a document, `db.operation.name` would be set to (literally, i.e., without replacing the placeholders with concrete values): [`GET /{db}/{docid}`](https://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid).

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
