<!--- Hugo front matter used to generate the website version of this page:
linkTitle: MongoDB
--->

# Semantic Conventions for MongoDB

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [MongoDB](https://www.mongodb.com/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"mongodb"`.

## Attributes

<!-- semconv db.mongodb(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.mongodb.collection`](../attributes-registry/db.md) | string | The MongoDB collection being accessed within the database stated in `db.name`. | `customers`; `products` | Required |
<!-- endsemconv -->

## Example

| Key | Value |
| :---------------------- | :----------------------------------------------------------- |
| Span name               | `"products.findAndModify"` |
| `db.system`             | `"mongodb"` |
| `db.user`               | `"the_user"` |
| `server.address`        | `"mongodb0.example.com"` |
| `server.port`           | `27017` |
| `network.peer.address`  | `"192.0.2.14"` |
| `network.peer.port`     | `27017` |
| `network.transport`     | `"tcp"` |
| `db.name`               | `"shopDb"` |
| `db.statement`          | not set |
| `db.operation`          | `"findAndModify"` |
| `db.mongodb.collection` | `"products"` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
