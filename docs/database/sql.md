<!--- Hugo front matter used to generate the website version of this page:
linkTitle: SQL
--->

# Semantic Conventions for SQL Databases

**Status**: [Experimental][DocumentStatus]

The SQL databases Semantic Conventions extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

## Span name

SQL spans SHOULD be named the following way:
- `{db.name} {db.statement}` if `db.statement` without variable arguments is available and know to be of a low cardinality.
- `{db.name}.{db.sql.table} {db.operation}`, provided that `db.operation` and `db.sql.table` are available.
  - If `db.sql.table` is not available due to its semantics, the span SHOULD be named `{db.name} {db.operation}`
  - If `db.operation` is not available, the span SHOULD be named `{db.name}`
  - If no information is available, the span SHOULD be named `{db.system}`

## Call-level attributes

<!-- semconv db.sql(full,tag=call-level-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.sql.table`](../attributes-registry/db.md) | string | The name of the primary table that the operation is acting upon, including the database name (if applicable). [1] | `public.users`; `customers` | Recommended |

**[1]:** It is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if it is provided by the library being instrumented. If the operation is acting upon an anonymous table, or more than one table, this value MUST NOT be set.
<!-- endsemconv -->

## Example

This is an example of attributes for a MySQL database span when `db.statement` contains variable arguments:

| Key                     | Value |
|:------------------------| :----------------------------------------------------------- |
| Span name               | `"ShopDb.orders SELECT"` |
| `db.system`             | `"mysql"` |
| `db.connection_string`  | `"Server=shopdb.example.com;Database=ShopDb;Uid=billing_user;TableCache=true;UseCompression=True;MinimumPoolSize=10;MaximumPoolSize=50;"` |
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

This is an example of attributes for a MySQL database span when `db.statement` is available without variable arguments:

| Key                     | Value |
|:------------------------| :----------------------------------------------------------- |
| Span name               | `"ShopDb SELECT * FROM orders WHERE order_id = ?"` |
| `db.system`             | `"mysql"` |
| `db.connection_string`  | `"Server=shopdb.example.com;Database=ShopDb;Uid=billing_user;TableCache=true;UseCompression=True;MinimumPoolSize=10;MaximumPoolSize=50;"` |
| `db.user`               | `"billing_user"` |
| `server.address`        | `"shopdb.example.com"` |
| `server.port`           | `3306` |
| `network.peer.address`  | `"192.0.2.12"` |
| `network.peer.port`     | `3306` |
| `network.transport`     | `"tcp"` |
| `db.name`               | `"ShopDb"` |
| `db.statement`          | `"SELECT * FROM orders WHERE order_id = ?"` |
| `db.operation`          | `"SELECT"` |
| `db.sql.table`          | `"orders"` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
