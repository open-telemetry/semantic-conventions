<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic conventions for database client spans

**Status**: [Release Candidate][DocumentStatus], unless otherwise specified

<!-- toc -->

- [Name](#name)
- [Status](#status)
- [Common attributes](#common-attributes)
  - [Notes and well-known identifiers for `db.system.name`](#notes-and-well-known-identifiers-for-dbsystemname)
- [Sanitization of `db.query.text`](#sanitization-of-dbquerytext)
- [Generating a summary of the query text](#generating-a-summary-of-the-query-text)
- [Semantic Conventions for specific database technologies](#semantic-conventions-for-specific-database-technologies)

<!-- tocstop -->

> **Warning**
>
> Existing database instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-spans.md)
> (or prior):
>
> * SHOULD NOT change the version of the database conventions that they emit by default
>   until the database semantic conventions are marked stable.
>   Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The list of values includes:
>   * `database` - emit the new, stable database conventions,
>     and stop emitting the old experimental database conventions
>     that the instrumentation emitted previously.
>   * `database/dup` - emit both the old and the stable database conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental database conventions
>     the instrumentation was emitting previously.
>   * Note: `database/dup` has higher precedence than `database` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version.

**Span kind:** SHOULD be `CLIENT`. It MAY be set to `INTERNAL` on spans representing
in-memory database calls.
It's RECOMMENDED to use `CLIENT` kind when database system being instrumented usually
runs in a different process than its client or when database calls happen over
instrumented protocol such as HTTP.

Span that describes database call SHOULD cover the duration of the corresponding call as if it was observed by the caller (such as client application).
For example, if a transient issue happened and was retried within this database call, the corresponding span should cover the duration of the logical operation
with all retries.

## Name

Database spans MUST follow the overall [guidelines for span names](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/specification/trace/api.md#span).

The **span name** SHOULD be `{db.query.summary}` if a summary is available.

<!-- markdown-link-check-disable -->
<!-- HTML anchors are not supported https://github.com/tcort/markdown-link-check/issues/225-->
If no summary is available, the span name SHOULD be `{db.operation.name} {target}`
provided that a (low-cardinality) `db.operation.name` is available (see below for
the exact definition of the [`{target}`](#target-placeholder) placeholder).

If a (low-cardinality) `db.operation.name` is not available, database span names
SHOULD default to the [`{target}`](#target-placeholder).
<!-- markdown-link-check-enable -->

If neither `{db.operation.name}` nor `{target}` are available, span name SHOULD be `{db.system}`.

Semantic conventions for individual database systems MAY specify different span name format.

The <span id="target-placeholder">`{target}`</span> SHOULD describe the entity that the operation is performed against
and SHOULD adhere to one of the following values, provided they are accessible:

- `db.collection.name` SHOULD be used for data manipulation operations or operations on a database collection.
- `db.namespace` SHOULD be used for operations on a specific database namespace.
- `server.address:server.port` SHOULD be used for other operations not targeting any specific database(s) or collection(s)

If a corresponding `{target}` value is not available for a specific operation, the instrumentation SHOULD omit the `{target}`.
For example, for an operation describing SQL query on an anonymous table like `SELECT * FROM (SELECT * FROM table) t`, span name should be `SELECT`.

## Status

Refer to the [Recording Errors](/docs/general/recording-errors.md) document for
details on how to record span status.

Semantic conventions for individual systems SHOULD specify which values of `db.response.status_code`
classify as errors.

## Common attributes

These attributes are commonly used across different database systems.

<!-- semconv span.db.client -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.system.name`](/docs/attributes-registry/db.md) | string | The database management system (DBMS) product as identified by the client instrumentation. [1] | `other_sql`; `softwareag.adabas`; `actian.ingres` | `Required` | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| [`db.collection.name`](/docs/attributes-registry/db.md) | string | The name of a collection (table, container) within the database. [2] | `public.users`; `customers` | `Conditionally Required` [3] | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| [`db.namespace`](/docs/attributes-registry/db.md) | string | The name of the database, fully qualified within the server address and port. [4] | `customers`; `test.users` | `Conditionally Required` If available. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| [`db.operation.name`](/docs/attributes-registry/db.md) | string | The name of the operation or command being executed. [5] | `findAndModify`; `HMSET`; `SELECT` | `Conditionally Required` [6] | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| [`db.response.status_code`](/docs/attributes-registry/db.md) | string | Database response status code. [7] | `102`; `ORA-17002`; `08P01`; `404` | `Conditionally Required` [8] | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [9] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` If and only if the operation failed. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [10] | `80`; `8080`; `443` | `Conditionally Required` [11] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`db.operation.batch.size`](/docs/attributes-registry/db.md) | int | The number of queries included in a batch operation. [12] | `2`; `3`; `4` | `Recommended` | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| [`db.query.summary`](/docs/attributes-registry/db.md) | string | Low cardinality representation of a database query text. [13] | `SELECT wuser_table`; `INSERT shipping_details SELECT orders`; `get user by id` | `Recommended` [14] | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| [`db.query.text`](/docs/attributes-registry/db.md) | string | The database query being executed. [15] | `SELECT * FROM wuser_table where username = ?`; `SET mykey ?` | `Recommended` [16] | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| [`db.response.returned_rows`](/docs/attributes-registry/db.md) | int | Number of rows returned by the operation. | `10`; `30`; `1000` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the database node where the operation was performed. [17] | `10.1.2.80`; `/tmp/my.sock` | `Recommended` If applicable for this database system. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` if and only if `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Name of the database host. [18] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`db.operation.parameter.<key>`](/docs/attributes-registry/db.md) | string | A database operation parameter, with `<key>` being the parameter name, and the attribute value being a string representation of the parameter value. [19] | `someval`; `55` | `Opt-In` | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |

**[1] `db.system.name`:** The actual DBMS may differ from the one identified by the client. For example, when using PostgreSQL client libraries to connect to a CockroachDB, the `db.system.name` is set to `postgresql` based on the instrumentation's best knowledge.

**[2] `db.collection.name`:** It is RECOMMENDED to capture the value as provided by the application without attempting to do any case normalization.

The collection name SHOULD NOT be extracted from `db.query.text`,
unless the query format is known to only ever have a single collection name present.

For batch operations, if the individual operations are known to have the same collection name
then that collection name SHOULD be used.

**[3] `db.collection.name`:** If readily available and if a database call is performed on a single collection. The collection name MAY be parsed from the query text, in which case it SHOULD be the single collection name in the query.

**[4] `db.namespace`:** If a database system has multiple namespace components, they SHOULD be concatenated (potentially using database system specific conventions) from most general to most specific namespace component, and more specific namespaces SHOULD NOT be captured without the more general namespaces, to ensure that "startswith" queries for the more general namespaces will be valid.
Semantic conventions for individual database systems SHOULD document what `db.namespace` means in the context of that system.
It is RECOMMENDED to capture the value as provided by the application without attempting to do any case normalization.

**[5] `db.operation.name`:** It is RECOMMENDED to capture the value as provided by the application
without attempting to do any case normalization.

The operation name SHOULD NOT be extracted from `db.query.text`,
unless the query format is known to only ever have a single operation name present.

For batch operations, if the individual operations are known to have the same operation name
then that operation name SHOULD be used prepended by `BATCH `,
otherwise `db.operation.name` SHOULD be `BATCH` or some other database
system specific term if more applicable.

**[6] `db.operation.name`:** If readily available and if there is a single operation name that describes the database call. The operation name MAY be parsed from the query text, in which case it SHOULD be the single operation name found in the query.

**[7] `db.response.status_code`:** The status code returned by the database. Usually it represents an error code, but may also represent partial success, warning, or differentiate between various types of successful outcomes.
Semantic conventions for individual database systems SHOULD document what `db.response.status_code` means in the context of that system.

**[8] `db.response.status_code`:** If the operation failed and status code is available.

**[9] `error.type`:** The `error.type` SHOULD match the `db.response.status_code` returned by the database or the client library, or the canonical name of exception that occurred.
When using canonical exception type name, instrumentation SHOULD do the best effort to report the most relevant type. For example, if the original exception is wrapped into a generic one, the original exception SHOULD be preferred.
Instrumentations SHOULD document how `error.type` is populated.

**[10] `server.port`:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[11] `server.port`:** If using a port other than the default port for this DBMS and if `server.address` is set.

**[12] `db.operation.batch.size`:** Operations are only considered batches when they contain two or more operations, and so `db.operation.batch.size` SHOULD never be `1`.

**[13] `db.query.summary`:** `db.query.summary` provides static summary of the query text. It describes a class of database queries and is useful as a grouping key, especially when analyzing telemetry for database calls involving complex queries.
Summary may be available to the instrumentation through instrumentation hooks or other means. If it is not available, instrumentations that support query parsing SHOULD generate a summary following [Generating query summary](../database/database-spans.md#generating-a-summary-of-the-query-text) section.

**[14] `db.query.summary`:** if readily available or if instrumentation supports query summarization.

**[15] `db.query.text`:** For sanitization see [Sanitization of `db.query.text`](../database/database-spans.md#sanitization-of-dbquerytext).
For batch operations, if the individual operations are known to have the same query text then that query text SHOULD be used, otherwise all of the individual query texts SHOULD be concatenated with separator `; ` or some other database system specific separator if more applicable.
Even though parameterized query text can potentially have sensitive data, by using a parameterized query the user is giving a strong signal that any sensitive data will be passed as parameter values, and the benefit to observability of capturing the static part of the query text by default outweighs the risk.

**[16] `db.query.text`:** Non-parameterized query text SHOULD NOT be collected by default unless there is sanitization that excludes sensitive data, e.g. by redacting all literal values present in the query text. See [Sanitization of `db.query.text`](../database/database-spans.md#sanitization-of-dbquerytext).
Parameterized query text SHOULD be collected by default (the query parameter values themselves are opt-in, see [`db.operation.parameter.<key>`](../attributes-registry/db.md)).

**[17] `network.peer.address`:** Semantic conventions for individual database systems SHOULD document whether `network.peer.*` attributes are applicable. Network peer address and port are useful when the application interacts with individual database nodes directly.
If a database operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.

**[18] `server.address`:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[19] `db.operation.parameter`:** If a parameter has no name and instead is referenced only by index, then `<key>` SHOULD be the 0-based index.
If `db.query.text` is also captured, then `db.operation.parameter.<key>` SHOULD match up with the parameterized placeholders present in `db.query.text`.

The following attributes can be important for making sampling decisions
and SHOULD be provided **at span creation time** (if provided at all):

* [`db.collection.name`](/docs/attributes-registry/db.md)
* [`db.namespace`](/docs/attributes-registry/db.md)
* [`db.operation.name`](/docs/attributes-registry/db.md)
* [`db.query.summary`](/docs/attributes-registry/db.md)
* [`db.query.text`](/docs/attributes-registry/db.md)
* [`db.system.name`](/docs/attributes-registry/db.md)
* [`server.address`](/docs/attributes-registry/server.md)
* [`server.port`](/docs/attributes-registry/server.md)

---

`db.system.name` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `actian.ingres` | [Actian Ingres](https://www.actian.com/databases/ingres/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `aws.dynamodb` | [Amazon DynamoDB](https://aws.amazon.com/pm/dynamodb/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `aws.redshift` | [Amazon Redshift](https://aws.amazon.com/redshift/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `azure.cosmosdb` | [Azure Cosmos DB](https://learn.microsoft.com/azure/cosmos-db) | ![Development](https://img.shields.io/badge/-development-blue) |
| `cassandra` | [Apache Cassandra](https://cassandra.apache.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `clickhouse` | [ClickHouse](https://clickhouse.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `cockroachdb` | [CockroachDB](https://www.cockroachlabs.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `couchbase` | [Couchbase](https://www.couchbase.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `couchdb` | [Apache CouchDB](https://couchdb.apache.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `derby` | [Apache Derby](https://db.apache.org/derby/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `elasticsearch` | [Elasticsearch](https://www.elastic.co/elasticsearch) | ![Development](https://img.shields.io/badge/-development-blue) |
| `firebirdsql` | [Firebird](https://www.firebirdsql.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `gcp.spanner` | [Google Cloud Spanner](https://cloud.google.com/spanner) | ![Development](https://img.shields.io/badge/-development-blue) |
| `geode` | [Apache Geode](https://geode.apache.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `h2database` | [H2 Database](https://h2database.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `hbase` | [Apache HBase](https://hbase.apache.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `hive` | [Apache Hive](https://hive.apache.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `hsqldb` | [HyperSQL Database](https://hsqldb.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `ibm.db2` | [IBM Db2](https://www.ibm.com/db2) | ![Development](https://img.shields.io/badge/-development-blue) |
| `ibm.informix` | [IBM Informix](https://www.ibm.com/products/informix) | ![Development](https://img.shields.io/badge/-development-blue) |
| `ibm.netezza` | [IBM Netezza](https://www.ibm.com/products/netezza) | ![Development](https://img.shields.io/badge/-development-blue) |
| `influxdb` | [InfluxDB](https://www.influxdata.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `instantdb` | [Instant](https://www.instantdb.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `intersystems.cache` | [InterSystems Caché](https://www.intersystems.com/products/cache/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `mariadb` | [MariaDB](https://mariadb.org/) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `memcached` | [Memcached](https://memcached.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `microsoft.sql_server` | [Microsoft SQL Server](https://www.microsoft.com/sql-server) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `mongodb` | [MongoDB](https://www.mongodb.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `mysql` | [MySQL](https://www.mysql.com/) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `neo4j` | [Neo4j](https://neo4j.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `opensearch` | [OpenSearch](https://opensearch.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `oracle.db` | [Oracle Database](https://www.oracle.com/database/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `other_sql` | Some other SQL database. Fallback only. | ![Development](https://img.shields.io/badge/-development-blue) |
| `postgresql` | [PostgreSQL](https://www.postgresql.org/) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `redis` | [Redis](https://redis.io/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `sap.hana` | [SAP HANA](https://www.sap.com/products/technology-platform/hana/what-is-sap-hana.html) | ![Development](https://img.shields.io/badge/-development-blue) |
| `sap.maxdb` | [SAP MaxDB](https://maxdb.sap.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `softwareag.adabas` | [Adabas (Adaptable Database System)](https://documentation.softwareag.com/?pf=adabas) | ![Development](https://img.shields.io/badge/-development-blue) |
| `sqlite` | [SQLite](https://www.sqlite.org/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `teradata` | [Teradata](https://www.teradata.com/) | ![Development](https://img.shields.io/badge/-development-blue) |
| `trino` | [Trino](https://trino.io/) | ![Development](https://img.shields.io/badge/-development-blue) |

---

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Notes and well-known identifiers for `db.system.name`

The list above is a non-exhaustive list of well-known identifiers to be specified for `db.system.name`.

If a value defined in this list applies to the DBMS to which the request is sent, this value MUST be used.
If no value defined in this list is suitable, a custom value MUST be provided.
This custom value MUST be the name of the DBMS in lowercase and without a version number to stay consistent with existing identifiers.

It is encouraged to open a PR towards this specification to add missing values to the list, especially when instrumentations for those missing databases are written.
This allows multiple instrumentations for the same database to be aligned and eases analyzing for backends.

The value `other_sql` is intended as a fallback and MUST only be used if the DBMS is known to be SQL-compliant but the concrete product is not known to the instrumentation.
If the concrete DBMS is known to the instrumentation, its specific identifier MUST be used.

Back ends could, for example, use the provided identifier to determine the appropriate SQL dialect for parsing the `db.query.text`.

When additional attributes are added that only apply to a specific DBMS, its identifier SHOULD be used as a namespace in the attribute key as for the attributes in the sections below.

## Sanitization of `db.query.text`

The `db.query.text` SHOULD be collected by default only if there is sanitization that excludes sensitive information.
Sanitization SHOULD replace all literals with a placeholder value.
Such literals include, but are not limited to, String, Numeric, Date and Time,
Boolean, Interval, Binary, and Hexadecimal literals.
The placeholder value SHOULD be `?`, unless it already has a defined meaning in the given database system,
in which case the instrumentation MAY choose a different placeholder.

Placeholders in a parameterized query SHOULD not be sanitized. E.g. `where id = $1` can be captured as is.

[IN-clauses](https://wikipedia.org/wiki/SQL_syntax#Operators) MAY be collapsed during sanitization,
e.g. from `IN (?, ?, ?, ?)` to `IN (?)`, as this can help with extremely long IN-clauses,
and can help control cardinality for users who choose to (optionally) add `db.query.text` to their metric attributes.

## Generating a summary of the query text

The `db.query.summary` attribute captures a shortened representation of a query text
which SHOULD have low-cardinality and SHOULD NOT contain any dynamic or sensitive data.

> [!NOTE]
>
> The `db.query.text` attribute is intended to identify individual queries. Even though
> it is sanitized if captured by default, it could still have high cardinality and
> might reach hundreds of lines.
>
> The `db.query.summary` is intended to provide a less granular grouping key that
> can be used as a span name or a metric attribute in common cases. It SHOULD
> only contain information that has a significant impact on the query, database,
> or application performance.

Instrumentations that support query parsing SHOULD generate a query summary when
one is not readily available from other sources.

The summary SHOULD preserve the following parts of query in the order they were provided:

- operations such as SQL SELECT, INSERT, UPDATE, DELETE, and other commands
- operation targets such as collections and database names

Instrumentations that support query parsing SHOULD parse the query and extract a
list of operations and targets from the query. It SHOULD set `db.query.summary`
attribute to the value formatted in the following way:

```
{operation1} {target1} {operation2} {target2} {target3} ...
````

Instrumentations SHOULD capture the values of operations and targets as provided
by the application without attempting to do any case normalization. If the operation
and target value is populated on `db.operation.name`, `db.collection.name`,
or other attributes, it SHOULD match the value used in the `db.query.summary`.

**Examples**:

- Query that consist of a single operation:

   ```sql
   SELECT *
   FROM   wuser_table
   WHERE  username = ?
   ```

   the corresponding `db.query.summary` is `SELECT wuser_table`.

- Query that performs multiple operations:

   ```sql
   INSERT INTO shipping_details
               (order_id,
               address)
   SELECT order_id,
          address
   FROM   orders
   WHERE  order_id = ?
   ```

   the corresponding `db.query.summary` is `INSERT shipping_details SELECT orders`.

- Query that performs an operation that's applied to multiple collections:

   ```sql
   SELECT *
   FROM   songs,
          artists
   WHERE  songs.artist_id == artists.id
   ```

   the corresponding `db.query.summary` is `SELECT songs artists`.

- Query that performs an operation on an anonymous table:

   ```sql
   SELECT order_date
   FROM   (SELECT *
           FROM   orders o
                  JOIN customers c
                    ON o.customer_id = c.customer_id)
   ```

   the corresponding `db.query.summary` is `SELECT SELECT orders customers`.

- Query that performs an operation on multiple collections with double-quotes or other punctuation:

    ```sql
    SELECT *
    FROM   "song list",
           'artists'
    ```

    the corresponding `db.query.summary` is `SELECT "songs list" 'artists'`.

Semantic conventions for individual database systems or specialized instrumentations
MAY specify a different `db.query.summary` format as long as produced summary remains
relatively short and its cardinality remains low comparing to the `db.query.text`.

## Semantic Conventions for specific database technologies

More specific Semantic Conventions are defined for the following database technologies:

* [AWS DynamoDB](dynamodb.md): Semantic Conventions for *AWS DynamoDB*.
* [Cassandra](cassandra.md): Semantic Conventions for *Cassandra*.
* [Azure Cosmos DB](cosmosdb.md): Semantic Conventions for *Azure Cosmos DB*.
* [CouchDB](couchdb.md): Semantic Conventions for *CouchDB*.
* [Elasticsearch](elasticsearch.md): Semantic Conventions for *Elasticsearch*.
* [HBase](hbase.md): Semantic Conventions for *HBase*.
* [MongoDB](mongodb.md): Semantic Conventions for *MongoDB*.
* [Microsoft SQL Server](mssql.md): Semantic Conventions for *Microsoft SQL Server*.
* [Redis](redis.md): Semantic Conventions for *Redis*.
* [SQL](sql.md): Semantic Conventions for *SQL* databases.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
