<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Client Calls
--->

# Semantic Conventions for Database Client Calls

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Connection-level attributes](#connection-level-attributes)
  * [Notes and well-known identifiers for `db.system`](#notes-and-well-known-identifiers-for-dbsystem)
- [Call-level attributes](#call-level-attributes)
- [Semantic Conventions for specific database technologies](#semantic-conventions-for-specific-database-technologies)

<!-- tocstop -->

> **Warning**
> Existing Database instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/database.md)
> (or prior):
>
> * SHOULD NOT change the version of the networking conventions that they emit
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking conventions which are also used
>   in Database instrumentations). Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The only values defined so far are:
>   * `http` - emit the new, stable networking conventions,
>     and stop emitting the old experimental networking conventions
>     that the instrumentation emitted previously.
>   * `http/dup` - emit both the old and the stable networking conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental networking conventions
>     the instrumentation was emitting previously.
>   * Note: `http/dup` has higher precedence than `http` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version (stable
>   next major version SHOULD NOT be released prior to October 1, 2023).

**Span kind:** MUST always be `CLIENT`.

The **span name** SHOULD be set to a low cardinality value representing the statement executed on the database.
It MAY be a stored procedure name (without arguments), DB statement without variable arguments, operation name, etc.
Since SQL statements may have very high cardinality even without arguments, SQL spans SHOULD be named the
following way, unless the statement is known to be of low cardinality:
`<db.operation> <db.name>.<db.sql.table>`, provided that `db.operation` and `db.sql.table` are available.
If `db.sql.table` is not available due to its semantics, the span SHOULD be named `<db.operation> <db.name>`.
It is not recommended to attempt any client-side parsing of `db.statement` just to get these properties,
they should only be used if the library being instrumented already provides them.
When it's otherwise impossible to get any meaningful span name, `db.name` or the tech-specific database name MAY be used.

## Connection-level attributes

These attributes will usually be the same for all operations performed over the same database connection.
Some database systems may allow a connection to switch to a different `db.user`, for example, and other database systems may not even have the concept of a connection at all.

<!-- semconv db(tag=connection-level) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `db.system` | string | An identifier for the database management system (DBMS) product being used. See below for a list of well-known identifiers. | `other_sql` | Required |
| `db.connection_string` | string | The connection string used to connect to the database. It is recommended to remove embedded credentials. | `Server=(localdb)\v11.0;Integrated Security=true;` | Recommended |
| `db.user` | string | Username for accessing the database. | `readonly_user`; `reporting_user` | Recommended |
| [`network.server.address`](../general/attributes.md) | string | Server address of the (physical) network connection - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock`; `proxy.example.com` | Recommended: If different than `server.address`. |
| [`network.server.ip`](../general/attributes.md) | string | Server IP address of the (physical) network connection. | `10.1.2.80` | Recommended: If different than `network.server.address`. |
| [`network.server.port`](../general/attributes.md) | int | Server port number of the (physical) network connection. | `65123` | Recommended: [2] |
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. | `tcp`; `udp` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended |
| [`server.address`](../general/attributes.md) | string | Name of the database host. [3] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Conditionally Required: See alternative attributes below. |
| [`server.port`](../general/attributes.md) | int | Server port number. [4] | `80`; `8080`; `443` | Conditionally Required: [5] |

**[1]:** Typically an IP address or Unix domain socket name, but can be domain name if available without reverse DNS lookup.

**[2]:** If different than `server.port` and if `network.server.address` is set.

**[3]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

**[4]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries (e.g. proxies) if it's available.

**[5]:** If using a port other than the default port for this DBMS and if `server.address` is set.

`db.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `other_sql` | Some other SQL database. Fallback only. See notes. |
| `mssql` | Microsoft SQL Server |
| `mssqlcompact` | Microsoft SQL Server Compact |
| `mysql` | MySQL |
| `oracle` | Oracle Database |
| `db2` | IBM Db2 |
| `postgresql` | PostgreSQL |
| `redshift` | Amazon Redshift |
| `hive` | Apache Hive |
| `cloudscape` | Cloudscape |
| `hsqldb` | HyperSQL DataBase |
| `progress` | Progress Database |
| `maxdb` | SAP MaxDB |
| `hanadb` | SAP HANA |
| `ingres` | Ingres |
| `firstsql` | FirstSQL |
| `edb` | EnterpriseDB |
| `cache` | InterSystems Caché |
| `adabas` | Adabas (Adaptable Database System) |
| `firebird` | Firebird |
| `derby` | Apache Derby |
| `filemaker` | FileMaker |
| `informix` | Informix |
| `instantdb` | InstantDB |
| `interbase` | InterBase |
| `mariadb` | MariaDB |
| `netezza` | Netezza |
| `pervasive` | Pervasive PSQL |
| `pointbase` | PointBase |
| `sqlite` | SQLite |
| `sybase` | Sybase |
| `teradata` | Teradata |
| `vertica` | Vertica |
| `h2` | H2 |
| `coldfusion` | ColdFusion IMQ |
| `cassandra` | Apache Cassandra |
| `hbase` | Apache HBase |
| `mongodb` | MongoDB |
| `redis` | Redis |
| `couchbase` | Couchbase |
| `couchdb` | CouchDB |
| `cosmosdb` | Microsoft Azure Cosmos DB |
| `dynamodb` | Amazon DynamoDB |
| `neo4j` | Neo4j |
| `geode` | Apache Geode |
| `elasticsearch` | Elasticsearch |
| `memcached` | Memcached |
| `cockroachdb` | CockroachDB |
| `opensearch` | OpenSearch |
| `clickhouse` | ClickHouse |
| `spanner` | Cloud Spanner |
| `trino` | Trino |
<!-- endsemconv -->

### Notes and well-known identifiers for `db.system`

The list above is a non-exhaustive list of well-known identifiers to be specified for `db.system`.

If a value defined in this list applies to the DBMS to which the request is sent, this value MUST be used.
If no value defined in this list is suitable, a custom value MUST be provided.
This custom value MUST be the name of the DBMS in lowercase and without a version number to stay consistent with existing identifiers.

It is encouraged to open a PR towards this specification to add missing values to the list, especially when instrumentations for those missing databases are written.
This allows multiple instrumentations for the same database to be aligned and eases analyzing for backends.

The value `other_sql` is intended as a fallback and MUST only be used if the DBMS is known to be SQL-compliant but the concrete product is not known to the instrumentation.
If the concrete DBMS is known to the instrumentation, its specific identifier MUST be used.

Back ends could, for example, use the provided identifier to determine the appropriate SQL dialect for parsing the `db.statement`.

When additional attributes are added that only apply to a specific DBMS, its identifier SHOULD be used as a namespace in the attribute key as for the attributes in the sections below.

## Call-level attributes

These attributes may be different for each operation performed, even if the same connection is used for multiple operations.
Usually only one `db.name` will be used per connection though.

<!-- semconv db(tag=call-level,remove_constraints) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `db.name` | string | This attribute is used to report the name of the database being accessed. For commands that switch the database, this should be set to the target database (even if the command fails). [1] | `customers`; `main` | Conditionally Required: If applicable. |
| `db.statement` | string | The database statement being executed. | `SELECT * FROM wuser_table`; `SET mykey "WuValue"` | Recommended: [2] |
| `db.operation` | string | The name of the operation being executed, e.g. the [MongoDB command name](https://docs.mongodb.com/manual/reference/command/#database-operations) such as `findAndModify`, or the SQL keyword. [3] | `findAndModify`; `HMSET`; `SELECT` | Conditionally Required: If `db.statement` is not applicable. |

**[1]:** In some SQL databases, the database name to be used is called "schema name". In case there are multiple layers that could be considered for database name (e.g. Oracle instance name and schema name), the database name to be used is the more specific layer (e.g. Oracle schema name).

**[2]:** Should be collected by default only if there is sanitization that excludes sensitive information.

**[3]:** When setting this to an SQL keyword, it is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if the operation name is provided by the library being instrumented. If the SQL statement has an ambiguous operation, or performs more than one operation, this value may be omitted.
<!-- endsemconv -->

## Semantic Conventions for specific database technologies

More specific Semantic Conventions are defined for the following database technologies:

* [AWS DynamoDB](dynamodb.md): Semantic Conventions for *AWS DynamoDB*.
* [Cassandra](cassandra.md): Semantic Conventions for *Cassandra*.
* [Cosmos DB](cosmosdb.md): Semantic Conventions for *Microsoft Cosmos DB*.
* [CouchDB](couchdb.md): Semantic Conventions for *CouchDB*.
* [Elasticsearch](elasticsearch.md): Semantic Conventions for *Elasticsearch*.
* [GraphQL](graphql.md): Semantic Conventions for *GraphQL Server*.
* [HBase](hbase.md): Semantic Conventions for *HBase*.
* [MongoDB](mongodb.md): Semantic Conventions for *MongoDB*.
* [MSSQL](mssql.md): Semantic Conventions for *MSSQL*.
* [Redis](redis.md): Semantic Conventions for *Redis*.
* [SQL](sql.md): Semantic Conventions for *SQL* databases.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
