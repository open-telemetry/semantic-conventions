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
| [`db.collection.namespace`](../attributes-registry/db.md) | string | The namespace containing database objects, fully qualified within the server address and port. [3] | `customers`; `test.users` | `Conditionally Required` If applicable. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.operation.name`](../attributes-registry/db.md) | string | The name of the operation or command being executed. [4] | `SELECT`; `INSERT`; `UPDATE`; `DELETE`; `CREATE`; `mystoredproc` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.collection.name`, then it SHOULD be the first collection name found in the query.

**[3]:** Namespace contains different identifiers depending on the database system:
* MySQL - database or schema name. For example, `products.dbo` * PostgreSQL - database and schema name. For example, `products.public` * MS SQL Server - instance name, database and schema name. For example, `test.products.public` * Oracle - instance name and schema name. For example, `test.products`
Current database name can usually be obtained using database driver API such as [JDBC `Connection.getCatalog()`](https://docs.oracle.com/javase/8/docs/api/java/sql/Connection.html#getCatalog--) or [.NET `SqlConnection.Database`](https://learn.microsoft.com/dotnet/api/system.data.sqlclient.sqlconnection.database).
If instrumentation cannot reliably determine the database name (for example, if database can be changed in runtime without instrumentation being aware of it), it SHOULD NOT set `db.collection.namespace`.
Instrumentations that parse SQL statements MAY use database name provided in the connection string and track the currently selected database name as long as current database name is associated with current connection and can't be changed without instrumentation being aware of it.
For commands that switch the database, this should be set to the target database (even if the command fails).
TODO schema.

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
| `db.collection.namespace` | `"ShopDb"` |
| `db.system`            | `"mysql"` |
| `server.address`       | `"shopdb.example.com"` |
| `server.port`          | `3306` |
| `network.peer.address` | `"192.0.2.12"` |
| `network.peer.port`    | `3306` |
| `network.transport`    | `"tcp"` |
| `db.query.text`        | `"SELECT * FROM orders WHERE order_id = 'o4711'"` |
| `db.operation.name`    | `"SELECT"` |
[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
