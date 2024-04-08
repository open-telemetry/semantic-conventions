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
| [`db.operation.name`](../attributes-registry/db.md) | string | The name of the operation or command being executed. [1] | `SELECT`; `INSERT`; `UPDATE`; `DELETE`; `CREATE`; `mystoredproc` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.mssql.instance_name`](../attributes-registry/db.md) | string | The Microsoft SQL Server [instance name](https://docs.microsoft.com/sql/connect/jdbc/building-the-connection-url?view=sql-server-ver15) connecting to. This name is used to determine the port of a named instance. [3] | `MSSQLSERVER` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.sql.table`](../attributes-registry/db.md) | string | The name of the primary table that the operation is acting upon, including the database name (if applicable). [4] | `public.users`; `customers` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** This SHOULD be the SQL command such as `SELECT`, `INSERT`, `UPDATE`, `CREATE`, `DROP`.
In the case of `EXEC`, this SHOULD be the stored procedure name that is being executed.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.statement` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.

**[3]:** If setting a `db.mssql.instance_name`, `server.port` is no longer required (but still recommended if non-standard).

**[4]:** It is not recommended to attempt any client-side parsing of `db.query.text` just to get this property, but it should be set if it is provided by the library being instrumented. If the operation is acting upon an anonymous table, or more than one table, this value MUST NOT be set.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
