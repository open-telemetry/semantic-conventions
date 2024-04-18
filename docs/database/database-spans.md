<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Client Calls
--->

# Semantic Conventions for Database Client Calls

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Common attributes](#common-attributes)
  - [Notes and well-known identifiers for `db.system`](#notes-and-well-known-identifiers-for-dbsystem)
- [Semantic Conventions for specific database technologies](#semantic-conventions-for-specific-database-technologies)

<!-- tocstop -->

> **Warning**
> Existing database instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-spans.md)
> (or prior) SHOULD NOT change the version of the database conventions that they emit
> until a transition plan to the (future) stable semantic conventions has been published.
> Conventions include, but are not limited to, attributes, metric and span names, and unit of measure.
>
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
> * SHOULD drop the environment variable in the next major version.

**Span kind:** MUST always be `CLIENT`.

The **span name** SHOULD be set to a low cardinality value representing the statement executed on the database.
It MAY be a stored procedure name (without arguments), DB statement without variable arguments, operation name, etc.
Since SQL statements may have very high cardinality even without arguments, SQL spans SHOULD be named the
following way, unless the statement is known to be of low cardinality:

`<db.operation.name> <db.namespace>.<db.collection.name>`, provided that `db.operation.name` and `db.collection.name` are available.
If `db.collection.name` is not available due to its semantics, the span SHOULD be named `<db.operation.name> <db.name>`.

It is not recommended to attempt any client-side parsing of `db.query.text` just to get these properties,
they should only be used if the library being instrumented already provides them.
When it's otherwise impossible to get any meaningful span name, `db.namespace` or the tech-specific database name MAY be used.

Span that describes database call SHOULD cover the duration of the corresponding call as if it was observed by the caller (such as client application).
For example, if a transient issue happened and was retried within this database call, the corresponding span should cover the duration of the logical operation
with all retries.

## Common attributes

These attributes will usually be the same for all operations performed over the same database connection.

<!-- semconv db(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.system`](../attributes-registry/db.md) | string | An identifier for the database management system (DBMS) product being used. See below for a list of well-known identifiers. | `other_sql` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.collection.name`](../attributes-registry/db.md) | string | The name of a collection (table, container) within the database. [1] | `public.users`; `customers` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.namespace`](../attributes-registry/db.md) | string | The name of the database, fully qualified within the server address and port. [3] | `customers`; `test.users` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.operation.name`](../attributes-registry/db.md) | string | The name of the operation or command being executed. | `findAndModify`; `HMSET`; `SELECT` | `Conditionally Required` [4] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [5] | `80`; `8080`; `443` | `Conditionally Required` [6] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`db.instance.id`](../attributes-registry/db.md) | string | An identifier (address, unique name, or any other identifier) of the database instance that is executing queries or mutations on the current connection. This is useful in cases where the database is running in a clustered environment and the instrumentation is able to record the node executing the query. The client may obtain this value in databases like MySQL using queries like `select @@hostname`. | `mysql-e26b99z.example.com` | `Recommended` If different from the `server.address` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.query.text`](../attributes-registry/db.md) | string | The database query being executed. | `SELECT * FROM wuser_table where username = ?`; `SET mykey "WuValue"` | `Recommended` [7] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the database node where the operation was performed. [8] | `10.1.2.80`; `/tmp/my.sock` | `Recommended` If applicable for this database system. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](../attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` if and only if `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.address`](../attributes-registry/server.md) | string | Name of the database host. [9] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`db.query.parameter.<key>`](../attributes-registry/db.md) | string | The query parameters used in `db.query.text`, with `<key>` being the parameter name, and the attribute value being the parameter value. [10] | `someval`; `55` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.collection.name`, then it SHOULD be the first collection name found in the query.

**[3]:** If a database system has multiple namespace components, they SHOULD be concatenated (potentially using database system specific conventions) from most general to most specific namespace component, and more specific namespaces SHOULD NOT be captured without the more general namespaces, to ensure that "startswith" queries for the more general namespaces will be valid.
Semantic conventions for individual database systems SHOULD document what `db.namespace` means in the context of that system.

**[4]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.

**[5]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[6]:** If using a port other than the default port for this DBMS and if `server.address` is set.

**[7]:** SHOULD be collected by default only if there is sanitization that excludes sensitive information.

**[8]:** Semantic conventions for individual database systems SHOULD document whether `network.peer.*` attributes are applicable. Network peer address and port are useful when the application interacts with individual database nodes directly.
If a database operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.

**[9]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[10]:** Query parameters should only be captured when `db.query.text` is parameterized with placeholders.
If a parameter has no name and instead is referenced only by index, then `<key>` SHOULD be the 0-based index.

`db.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `other_sql` | Some other SQL database. Fallback only. See notes. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mssql` | Microsoft SQL Server | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mssqlcompact` | Microsoft SQL Server Compact | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mysql` | MySQL | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `oracle` | Oracle Database | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db2` | IBM Db2 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `postgresql` | PostgreSQL | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `redshift` | Amazon Redshift | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hive` | Apache Hive | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cloudscape` | Cloudscape | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hsqldb` | HyperSQL DataBase | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `progress` | Progress Database | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `maxdb` | SAP MaxDB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hanadb` | SAP HANA | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ingres` | Ingres | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `firstsql` | FirstSQL | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `edb` | EnterpriseDB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cache` | InterSystems Caché | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `adabas` | Adabas (Adaptable Database System) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `firebird` | Firebird | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `derby` | Apache Derby | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `filemaker` | FileMaker | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `informix` | Informix | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `instantdb` | InstantDB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `interbase` | InterBase | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mariadb` | MariaDB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `netezza` | Netezza | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pervasive` | Pervasive PSQL | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pointbase` | PointBase | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `sqlite` | SQLite | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `sybase` | Sybase | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `teradata` | Teradata | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `vertica` | Vertica | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `h2` | H2 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `coldfusion` | ColdFusion IMQ | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cassandra` | Apache Cassandra | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hbase` | Apache HBase | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mongodb` | MongoDB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `redis` | Redis | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `couchbase` | Couchbase | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `couchdb` | CouchDB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cosmosdb` | Microsoft Azure Cosmos DB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `dynamodb` | Amazon DynamoDB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `neo4j` | Neo4j | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `geode` | Apache Geode | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `elasticsearch` | Elasticsearch | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `memcached` | Memcached | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cockroachdb` | CockroachDB | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `opensearch` | OpenSearch | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `clickhouse` | ClickHouse | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `spanner` | Cloud Spanner | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `trino` | Trino | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
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

Back ends could, for example, use the provided identifier to determine the appropriate SQL dialect for parsing the `db.query.text`.

When additional attributes are added that only apply to a specific DBMS, its identifier SHOULD be used as a namespace in the attribute key as for the attributes in the sections below.

## Semantic Conventions for specific database technologies

More specific Semantic Conventions are defined for the following database technologies:

* [AWS DynamoDB](dynamodb.md): Semantic Conventions for *AWS DynamoDB*.
* [Cassandra](cassandra.md): Semantic Conventions for *Cassandra*.
* [Cosmos DB](cosmosdb.md): Semantic Conventions for *Microsoft Cosmos DB*.
* [CouchDB](couchdb.md): Semantic Conventions for *CouchDB*.
* [Elasticsearch](elasticsearch.md): Semantic Conventions for *Elasticsearch*.
* [HBase](hbase.md): Semantic Conventions for *HBase*.
* [MongoDB](mongodb.md): Semantic Conventions for *MongoDB*.
* [MSSQL](mssql.md): Semantic Conventions for *MSSQL*.
* [Redis](redis.md): Semantic Conventions for *Redis*.
* [SQL](sql.md): Semantic Conventions for *SQL* databases.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
