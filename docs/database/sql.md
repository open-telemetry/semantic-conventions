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
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.jdbc.driver_classname`](../attributes-registry/db.md) | string | The fully-qualified class name of the [Java Database Connectivity (JDBC)](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) driver used to connect. | `org.postgresql.Driver`; `com.microsoft.sqlserver.jdbc.SQLServerDriver` | Recommended |
| [`db.sql.table`](../attributes-registry/db.md) | string | The name of the primary table that the operation is acting upon, including the database name (if applicable). [1] | `public.users`; `customers` | Recommended |

**[1]:** It is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if it is provided by the library being instrumented. If the operation is acting upon an anonymous table, or more than one table, this value MUST NOT be set.
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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
