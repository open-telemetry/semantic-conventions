<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
--->

# Semantic Conventions for Database Metrics

**Status**: [Experimental][DocumentStatus]

The conventions described in this section are specific to SQL and NoSQL clients.

**Disclaimer:** These are initial database client metric instruments
and attributes but more may be added in the future.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Database operation](#database-operation)
  - [Metric: `db.client.operation.duration`](#metric-dbclientoperationduration)
- [Connection pools](#connection-pools)
  - [Metric: `db.client.connection.count`](#metric-dbclientconnectioncount)
  - [Metric: `db.client.connection.idle.max`](#metric-dbclientconnectionidlemax)
  - [Metric: `db.client.connection.idle.min`](#metric-dbclientconnectionidlemin)
  - [Metric: `db.client.connection.max`](#metric-dbclientconnectionmax)
  - [Metric: `db.client.connection.pending_requests`](#metric-dbclientconnectionpending_requests)
  - [Metric: `db.client.connection.timeouts`](#metric-dbclientconnectiontimeouts)
  - [Metric: `db.client.connection.create_time`](#metric-dbclientconnectioncreate_time)
  - [Metric: `db.client.connection.wait_time`](#metric-dbclientconnectionwait_time)
  - [Metric: `db.client.connection.use_time`](#metric-dbclientconnectionuse_time)

<!-- tocstop -->

> **Warning**
>
> Existing database instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-spans.md)
> (or prior):
>
> * SHOULD NOT change the version of the database conventions that they emit
>   until the database semantic conventions are marked stable.
>   Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   If the list of values includes:
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

## Database operation

### Metric: `db.client.operation.duration`

**Status**: [Experimental][DocumentStatus]

This metric is [required][MetricRequired].

When this metric is reported alongside a database operation span, the metric value SHOULD be the same as the database operation span duration.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10 ]`.

<!-- semconv metric.db.client.operation.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.operation.duration` | Histogram | `s` | Duration of database client operations. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.operation.duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.system`](/docs/attributes-registry/db.md) | string | An identifier for the database management system (DBMS) product being used. See below for a list of well-known identifiers. | `other_sql`; `mssql`; `mssqlcompact` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.collection.name`](/docs/attributes-registry/db.md) | string | The name of a collection (table, container) within the database. [1] | `public.users`; `customers` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.namespace`](/docs/attributes-registry/db.md) | string | The name of the database, fully qualified within the server address and port. [3] | `customers`; `test.users` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.operation.name`](/docs/attributes-registry/db.md) | string | The name of the operation or command being executed. [4] | `findAndModify`; `HMSET`; `SELECT` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [6] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | `Conditionally Required` If and only if the operation failed. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [7] | `80`; `8080`; `443` | `Conditionally Required` [8] | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the database node where the operation was performed. [9] | `10.1.2.80`; `/tmp/my.sock` | `Recommended` If applicable for this database system. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` If and only if `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Name of the database host. [10] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.
It is RECOMMENDED to capture the value as provided by the application without attempting to do any case normalization.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.collection.name`, then it SHOULD be the first collection name found in the query.

**[3]:** If a database system has multiple namespace components, they SHOULD be concatenated (potentially using database system specific conventions) from most general to most specific namespace component, and more specific namespaces SHOULD NOT be captured without the more general namespaces, to ensure that "startswith" queries for the more general namespaces will be valid.
Semantic conventions for individual database systems SHOULD document what `db.namespace` means in the context of that system.
It is RECOMMENDED to capture the value as provided by the application without attempting to do any case normalization.

**[4]:** It is RECOMMENDED to capture the value as provided by the application without attempting to do any case normalization.

**[5]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.operation.name`, then it SHOULD be the first operation name found in the query.

**[6]:** The `error.type` SHOULD match the error code returned by the database or the client library, the canonical name of exception that occurred, or another low-cardinality error identifier. Instrumentations SHOULD document the list of errors they report.

**[7]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[8]:** If using a port other than the default port for this DBMS and if `server.address` is set.

**[9]:** Semantic conventions for individual database systems SHOULD document whether `network.peer.*` attributes are applicable. Network peer address and port are useful when the application interacts with individual database nodes directly.
If a database operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.

**[10]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

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

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

## Connection pools

The following metric instruments describe database client connection pool operations.

### Metric: `db.client.connection.count`

This metric is [required][MetricRequired].

<!-- semconv metric.db.client.connection.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.count` | UpDownCounter | `{connection}` | The number of connections that are currently in state described by the `state` attribute | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.count(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.client.connections.state`](/docs/attributes-registry/db.md) | string | The state of a connection in the pool | `idle` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`db.client.connections.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `idle` | idle | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | used | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->
### Metric: `db.client.connection.idle.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.idle.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.idle.max` | UpDownCounter | `{connection}` | The maximum number of idle open connections allowed | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.idle.max(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `db.client.connection.idle.min`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.idle.min(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.idle.min` | UpDownCounter | `{connection}` | The minimum number of idle open connections allowed | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.idle.min(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `db.client.connection.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.max` | UpDownCounter | `{connection}` | The maximum number of open connections allowed | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.max(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `db.client.connection.pending_requests`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.pending_requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.pending_requests` | UpDownCounter | `{request}` | The number of pending requests for an open connection, cumulative for the entire pool | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.pending_requests(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `db.client.connection.timeouts`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.timeouts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.timeouts` | Counter | `{timeout}` | The number of connection timeouts that have occurred trying to obtain a connection from the pool | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.timeouts(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `db.client.connection.create_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.create_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.create_time` | Histogram | `s` | The time it took to create a new connection | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.create_time(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `db.client.connection.wait_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.wait_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.wait_time` | Histogram | `s` | The time it took to obtain an open connection from the pool | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.wait_time(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `db.client.connection.use_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.use_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `db.client.connection.use_time` | Histogram | `s` | The time between borrowing a connection and returning it to the pool | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.use_time(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.client.connections.pool.name`](/docs/attributes-registry/db.md) | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRequired]: /docs/general/metric-requirement-level.md#required
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
