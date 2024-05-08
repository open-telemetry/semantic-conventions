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

<!-- semconv db.mssql(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.collection.name`](/docs/attributes-registry/db.md) | string | The name of the SQL table that the operation is acting upon. [1] | `users`; `dbo.products` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.namespace`](/docs/attributes-registry/db.md) | string | The name of the database, fully qualified within the server address and port. [3] | `instance1.products`; `customers` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.operation.name`](/docs/attributes-registry/db.md) | string | The name of the operation or command being executed. [4] | `SELECT`; `INSERT`; `UPDATE`; `DELETE`; `CREATE`; `mystoredproc` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [6] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` If and only if the operation failed. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [7] | `80`; `8080`; `443` | `Conditionally Required` [8] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`db.query.text`](/docs/attributes-registry/db.md) | string | The database query being executed. | `SELECT * FROM wuser_table where username = ?`; `SET mykey "WuValue"` | `Recommended` [9] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Name of the database host. [10] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`db.query.parameter.<key>`](/docs/attributes-registry/db.md) | string | The query parameters used in `db.query.text`, with `<key>` being the parameter name, and the attribute value being the parameter value. [11] | `someval`; `55` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.
It is RECOMMENDED to capture the value as provided by the application without attempting to do any case normalization.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.collection.name`, then it SHOULD be the first collection name found in the query.

**[3]:** When connecting to a default instance, `db.namespace` SHOULD be set to the name of the database. When connecting to a [named instance](https://learn.microsoft.com/sql/connect/jdbc/building-the-connection-url#named-and-multiple-sql-server-instances), `db.namespace` SHOULD be set to the combination of instance and database name following the `{instance_name}.{database_name}` pattern.
For commands that switch the database, this SHOULD be set to the target database (even if the command fails).

**[4]:** This SHOULD be the SQL command such as `SELECT`, `INSERT`, `UPDATE`, `CREATE`, `DROP`.
In the case of `EXEC`, this SHOULD be the stored procedure name that is being executed.

**[5]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.

**[6]:** The `error.type` SHOULD match the error code returned by the database or the client library, the canonical name of exception that occurred, or another low-cardinality error identifier. Instrumentations SHOULD document the list of errors they report.

**[7]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[8]:** If using a port other than the default port for this DBMS and if `server.address` is set.

**[9]:** SHOULD be collected by default only if there is sanitization that excludes sensitive information.

**[10]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[11]:** Query parameters should only be captured when `db.query.text` is parameterized with placeholders.
If a parameter has no name and instead is referenced only by index, then `<key>` SHOULD be the 0-based index.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
