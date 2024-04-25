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
| [`db.collection.name`](../attributes-registry/db.md) | string | The name of the SQL table that the operation is acting upon. [1] | `users`; `dbo.products` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.namespace`](../attributes-registry/db.md) | string | The name of the database, fully qualified within the server address and port. [3] | `customers`; `test.users` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.operation.name`](../attributes-registry/db.md) | string | The name of the operation or command being executed. [4] | `SELECT`; `INSERT`; `UPDATE`; `DELETE`; `CREATE`; `mystoredproc` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.collection.name`, then it SHOULD be the first collection name found in the query.

**[3]:** If a database system has multiple namespace components, they SHOULD be concatenated
(potentially using database system specific conventions) from most general to most
specific namespace component, and more specific namespaces SHOULD NOT be captured without
the more general namespaces, to ensure that "startswith" queries for the more general namespaces will be valid.

Unless specified by the system-specific semantic convention, the `db.namespace` attribute matches
the name of the database being accessed.

The database name can usually be obtained with database driver API such as
[JDBC `Connection.getCatalog()`](https://docs.oracle.com/javase/8/docs/api/java/sql/Connection.html#getCatalog--)
or [.NET `SqlConnection.Database`](https://learn.microsoft.com/dotnet/api/system.data.sqlclient.sqlconnection.database).

Some database drivers don't detect when the current database is changed (for example, with SQL `USE database` statement).
Instrumentations that parse SQL statements MAY use the database name provided
in the connection string and keep track of the currently selected database name.

For commands that switch the database, this SHOULD be set to the target database (even if the command fails).

If instrumentation cannot reliably determine the current database name, it SHOULD NOT set `db.namespace`.

**[4]:** This SHOULD be the SQL command such as `SELECT`, `INSERT`, `UPDATE`, `CREATE`, `DROP`.
In the case of `EXEC`, this SHOULD be the stored procedure name that is being executed.

**[5]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.
<!-- endsemconv -->

## Example

This is an example of attributes for a MySQL database span:

| Key                    | Value |
|:-----------------------| :----------------------------------------------------------- |
| Span name              | `"SELECT ShopDb.orders"` |
| `db.collection.name`   | `"orders"` |
| `db.namespace`         | `"ShopDb"` |
| `db.system`            | `"mysql"` |
| `server.address`       | `"shopdb.example.com"` |
| `server.port`          | `3306` |
| `network.peer.address` | `"192.0.2.12"` |
| `network.peer.port`    | `3306` |
| `network.transport`    | `"tcp"` |
| `db.query.text`        | `"SELECT * FROM orders WHERE order_id = 'o4711'"` |
| `db.operation.name`    | `"SELECT"` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
