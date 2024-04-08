<!--- Hugo front matter used to generate the website version of this page:
linkTitle: SQL
--->

# Semantic Conventions for SQL Databases

**Status**: [Experimental][DocumentStatus]

The SQL databases Semantic Conventions extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

## Attributes

<!-- semconv db.sql(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.operation.name`](../attributes-registry/db.md) | string | The name of the operation or command being executed. [1] | `SELECT`; `INSERT`; `UPDATE`; `DELETE`; `CREATE`; `mystoredproc` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.sql.table`](../attributes-registry/db.md) | string | The name of the primary table that the operation is acting upon, including the database name (if applicable). [3] | `public.users`; `customers` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** This SHOULD be the SQL command such as `SELECT`, `INSERT`, `UPDATE`, `CREATE`, `DROP`.
In the case of `EXEC`, this SHOULD be the stored procedure name that is being executed.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.statement` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.

**[3]:** It is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if it is provided by the library being instrumented. If the operation is acting upon an anonymous table, or more than one table, this value MUST NOT be set.
<!-- endsemconv -->

## Example

This is an example of attributes for a MySQL database span:

| Key                     | Value |
|:------------------------| :----------------------------------------------------------- |
| Span name               | `"SELECT ShopDb.orders"` |
| `db.system`             | `"mysql"` |
| `db.user`               | `"billing_user"` |
| `server.address`        | `"shopdb.example.com"` |
| `server.port`           | `3306` |
| `network.peer.address`  | `"192.0.2.12"` |
| `network.peer.port`     | `3306` |
| `network.transport`     | `"tcp"` |
| `db.name`               | `"ShopDb"` |
| `db.statement`          | `"SELECT * FROM orders WHERE order_id = 'o4711'"` |
| `db.operation`          | `"SELECT"` |
| `db.sql.table`          | `"orders"` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
