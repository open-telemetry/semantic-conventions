# Semantic Conventions for MSSQL

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for the [Microsoft SQL Server](https://www.microsoft.com/sql-server) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"mssql"`.

## Connection-level attributes

<!-- semconv db.mssql(tag=connection-level-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.jdbc.driver_classname`](database-spans.md) | string | The fully-qualified class name of the [Java Database Connectivity (JDBC)](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) driver used to connect. | `org.postgresql.Driver`; `com.microsoft.sqlserver.jdbc.SQLServerDriver` | Recommended |
| `db.mssql.instance_name` | string | The Microsoft SQL Server [instance name](https://docs.microsoft.com/en-us/sql/connect/jdbc/building-the-connection-url?view=sql-server-ver15) connecting to. This name is used to determine the port of a named instance. [1] | `MSSQLSERVER` | Recommended |

**[1]:** If setting a `db.mssql.instance_name`, `server.port` is no longer required (but still recommended if non-standard).
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
