<!--- Hugo front matter used to generate the website version of this page:
linkTitle: MSSQL
--->

# Semantic Conventions for MSSQL

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for the *Microsoft SQL Server* extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"mssql"`.

## Attributes

<!-- semconv db.mssql(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.collection.name`](../attributes-registry/db.md) | string | The name of the SQL table that the operation is acting upon. [1] | `users`; `dbo.products` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.namespace`](../attributes-registry/db.md) | string | The name of the database, fully qualified within the server address and port. [3] | `instance1.products`; `customers` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.operation.name`](../attributes-registry/db.md) | string | The name of the operation or command being executed. [4] | `SELECT`; `INSERT`; `UPDATE`; `DELETE`; `CREATE`; `mystoredproc` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.collection.name`, then it SHOULD be the first collection name found in the query.

**[3]:** When connecting to a default instance, `db.namespace` SHOULD be set to the name of the database. When connecting to a [named instance](https://learn.microsoft.com/sql/connect/jdbc/building-the-connection-url#named-and-multiple-sql-server-instances), `db.namespace` SHOULD be set to the combination of instance and database name following the `{instance_name}.{database_name}` pattern.
For commands that switch the database, this SHOULD be set to the target database (even if the command fails).

**[4]:** This SHOULD be the SQL command such as `SELECT`, `INSERT`, `UPDATE`, `CREATE`, `DROP`.
In the case of `EXEC`, this SHOULD be the stored procedure name that is being executed.

**[5]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
