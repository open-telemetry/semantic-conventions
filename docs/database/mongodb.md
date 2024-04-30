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
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.collection.name`](../attributes-registry/db.md) | string | The MongoDB collection being accessed within the database stated in `db.namespace`. [1] | `public.users`; `customers` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.namespace`](../attributes-registry/db.md) | string | The MongoDB database name. [2] | `customers`; `test.users` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.operation.name`](../attributes-registry/db.md) | string | The name of the command being executed. [3] | `findAndModify`; `getMore`; `update` | `Conditionally Required` [4] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.

**[2]:** <!-- TODO: overriding the base note, workaround for https://github.com/open-telemetry/build-tools/issues/299 -->

**[3]:** See [MongoDB database commands](https://www.mongodb.com/docs/manual/reference/command/).

**[4]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.
<!-- endsemconv -->

## Example

| Key                     | Value |
|:------------------------| :----------------------------------------------------------- |
| Span name               | `"products.findAndModify"` |
| `db.system`             | `"mongodb"` |
| `server.address`        | `"mongodb0.example.com"` |
| `server.port`           | `27017` |
| `network.peer.address`  | `"192.0.2.14"` |
| `network.peer.port`     | `27017` |
| `network.transport`     | `"tcp"` |
| `db.collection.name`    | `"products"` |
| `db.namespace`          | `"shopDb"` |
| `db.query.text`         | not set |
| `db.operation.name`     | `"findAndModify"` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
