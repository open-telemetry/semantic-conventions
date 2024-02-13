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

- [Database call](#database-call)
  * [Metric: `db.client.call.duration`](#metric-dbclientcallduration)
- [Connection pools](#connection-pools)
  * [Metric: `db.client.connections.usage`](#metric-dbclientconnectionsusage)
  * [Metric: `db.client.connections.idle.max`](#metric-dbclientconnectionsidlemax)
  * [Metric: `db.client.connections.idle.min`](#metric-dbclientconnectionsidlemin)
  * [Metric: `db.client.connections.max`](#metric-dbclientconnectionsmax)
  * [Metric: `db.client.connections.pending_requests`](#metric-dbclientconnectionspending_requests)
  * [Metric: `db.client.connections.timeouts`](#metric-dbclientconnectionstimeouts)
  * [Metric: `db.client.connections.create_time`](#metric-dbclientconnectionscreate_time)
  * [Metric: `db.client.connections.wait_time`](#metric-dbclientconnectionswait_time)
  * [Metric: `db.client.connections.use_time`](#metric-dbclientconnectionsuse_time)

<!-- tocstop -->

> **Warning**
> Existing database instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md)
> (or prior) SHOULD NOT change the version of the database conventions that they emit
> until a transition plan to the (future) stable semantic conventions has been published.
> Conventions include, but are not limited to, attributes, metric and span names, and unit of measure.

## Database call

### Metric: `db.client.call.duration`

**Status**: [Experimental][DocumentStatus]

This metric is [required][MetricRequired].

When this metric is reported alongside a database operation span, the metric value SHOULD be the same as the database operation span duration.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.db.client.call.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.call.duration` | Histogram | `s` | Duration of database client calls. |
<!-- endsemconv -->

<!-- semconv metric.db.client.call.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.connection_string`](../attributes-registry/db.md) | string | The connection string used to connect to the database. It is recommended to remove embedded credentials. | `Server=(localdb)\v11.0;Integrated Security=true;` | Recommended |
| [`db.instance.id`](../attributes-registry/db.md) | string | An identifier (address, unique name, or any other identifier) of the database instance that is executing queries or mutations on the current connection. This is useful in cases where the database is running in a clustered environment and the instrumentation is able to record the node executing the query. The client may obtain this value in databases like MySQL using queries like `select @@hostname`. | `mysql-e26b99z.example.com` | Recommended: If different from the `server.address` |
| [`db.name`](../attributes-registry/db.md) | string | This attribute is used to report the name of the database being accessed. For commands that switch the database, this should be set to the target database (even if the command fails). [1] | `customers`; `main` | Conditionally Required: If applicable. |
| [`db.operation`](../attributes-registry/db.md) | string | The name of the operation being executed, e.g. the [MongoDB command name](https://docs.mongodb.com/manual/reference/command/#database-operations) such as `findAndModify`, or the SQL keyword. [2] | `findAndModify`; `HMSET`; `SELECT` | Conditionally Required: If available. |
| [`db.system`](../attributes-registry/db.md) | string | An identifier for the database management system (DBMS) product being used. See below for a list of well-known identifiers. | `other_sql` | Required |
| [`db.user`](../attributes-registry/db.md) | string | Username for accessing the database. | `readonly_user`; `reporting_user` | Recommended |
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`network.peer.port`](../attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | Recommended: If `network.peer.address` is set. |
| [`network.transport`](../attributes-registry/network.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [3] | `tcp`; `udp` | Recommended |
| [`network.type`](../attributes-registry/network.md) | string | [OSI network layer](https://osi-model.com/network-layer/) or non-OSI equivalent. [4] | `ipv4`; `ipv6` | Recommended |
| [`server.address`](../attributes-registry/server.md) | string | Name of the database host. [5] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [6] | `80`; `8080`; `443` | Conditionally Required: [7] |

**[1]:** In some SQL databases, the database name to be used is called "schema name". In case there are multiple layers that could be considered for database name (e.g. Oracle instance name and schema name), the database name to be used is the more specific layer (e.g. Oracle schema name).

**[2]:** When setting this to an SQL keyword, it is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if the operation name is provided by the library being instrumented. If the SQL statement has an ambiguous operation, or performs more than one operation, this value may be omitted.

**[3]:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[4]:** The value SHOULD be normalized to lowercase.

**[5]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[6]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

**[7]:** If using a port other than the default port for this DBMS and if `server.address` is set.

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

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |
<!-- endsemconv -->

## Connection pools

The following metric instruments describe database client connection pool operations.

### Metric: `db.client.connections.usage`

This metric is [required][MetricRequired].

<!-- semconv metric.db.client.connections.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.usage` | UpDownCounter | `{connection}` | The number of connections that are currently in state described by the `state` attribute |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
| `state` | string | The state of a connection in the pool | `idle` | Required |

`state` MUST be one of the following:

| Value  | Description |
|---|---|
| `idle` | idle |
| `used` | used |
<!-- endsemconv -->
### Metric: `db.client.connections.idle.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.idle.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.idle.max` | UpDownCounter | `{connection}` | The maximum number of idle open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.idle.max(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.idle.min`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.idle.min(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.idle.min` | UpDownCounter | `{connection}` | The minimum number of idle open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.idle.min(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.max` | UpDownCounter | `{connection}` | The maximum number of open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.max(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.pending_requests`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.pending_requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.pending_requests` | UpDownCounter | `{request}` | The number of pending requests for an open connection, cumulative for the entire pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.pending_requests(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.timeouts`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.timeouts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.timeouts` | Counter | `{timeout}` | The number of connection timeouts that have occurred trying to obtain a connection from the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.timeouts(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.create_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.create_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.create_time` | Histogram | `ms` | The time it took to create a new connection |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.create_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.wait_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.wait_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.wait_time` | Histogram | `ms` | The time it took to obtain an open connection from the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.wait_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.use_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.use_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.use_time` | Histogram | `ms` | The time between borrowing a connection and returning it to the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.use_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/metric-requirement-level.md#required
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/metric-requirement-level.md#recommended
