<!--- Hugo front matter used to generate the website version of this page:
linkTitle: MongoDB
--->

# Semantic Conventions for MongoDB

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [MongoDB](https://www.mongodb.com/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"mongodb"`.

## Call-level attributes

<!-- semconv db.mongodb(tag=call-level-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `db.mongodb.collection` | string | The collection being accessed within the database stated in `db.name`. | `customers`; `products` | Required |
<!-- endsemconv -->

## Example

| Key                     | Value |
|:------------------------| :----------------------------------------------------------- |
| Span name               | `"products.findAndModify"` |
| `db.system`             | `"mongodb"` |
| `db.connection_string`  | not set |
| `db.user`               | `"the_user"` |
| `server.address`        | `"mongodb0.example.com"` |
| `server.ip`             | `"192.0.2.14"` |
| `server.port`           | `27017` |
| `network.transport`     | `"IP.TCP"` |
| `db.name`               | `"shopDb"` |
| `db.statement`          | not set |
| `db.operation`          | `"findAndModify"` |
| `db.mongodb.collection` | `"products"` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
