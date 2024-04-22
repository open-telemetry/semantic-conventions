<!--- Hugo front matter used to generate the website version of this page:
--->

# Database

<!-- toc -->

- [Generic Database Attributes](#generic-database-attributes)
- [Cassandra Attributes](#cassandra-attributes)
- [CosmosDB Attributes](#cosmosdb-attributes)
- [Elasticsearch Attributes](#elasticsearch-attributes)
- [MSSQL Attributes](#mssql-attributes)
- [Redis Attributes](#redis-attributes)
- [Deprecated DB Attributes](#deprecated-db-attributes)
- [Deprecated DB Metrics Attributes](#deprecated-db-metrics-attributes)

<!-- tocstop -->

## Generic Database Attributes

<!-- semconv registry.db(omit_requirement_level,tag=db-generic) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `db.client.connections.pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, instrumentation should use a combination of `server.address` and `server.port` attributes formatted as `server.address:server.port`. | `myDataSource` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.client.connections.state` | string | The state of a connection in the pool | `idle` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.collection.name` | string | The name of a collection (table, container) within the database. [1] | `public.users`; `customers` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.instance.id` | string | An identifier (address, unique name, or any other identifier) of the database instance that is executing queries or mutations on the current connection. This is useful in cases where the database is running in a clustered environment and the instrumentation is able to record the node executing the query. The client may obtain this value in databases like MySQL using queries like `select @@hostname`. | `mysql-e26b99z.example.com` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.name` | string | This attribute is used to report the name of the database being accessed. For commands that switch the database, this should be set to the target database (even if the command fails). [2] | `customers`; `main` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.operation.name` | string | The name of the operation or command being executed. | `findAndModify`; `HMSET`; `SELECT` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.query.parameter.<key>` | string | The query parameters used in `db.query.text`, with `<key>` being the parameter name, and the attribute value being the parameter value. [3] | `someval`; `55` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.query.text` | string | The database query being executed. | `SELECT * FROM wuser_table where username = ?`; `SET mykey "WuValue"` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.system` | string | An identifier for the database management system (DBMS) product being used. See below for a list of well-known identifiers. | `other_sql` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.

**[2]:** In some SQL databases, the database name to be used is called "schema name". In case there are multiple layers that could be considered for database name (e.g. Oracle instance name and schema name), the database name to be used is the more specific layer (e.g. Oracle schema name).

**[3]:** Query parameters should only be captured when `db.query.text` is parameterized with placeholders.
If a parameter has no name and instead is referenced only by index, then `<key>` SHOULD be the 0-based index.

`db.client.connections.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `idle` | idle | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | used | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

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

## Cassandra Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-cassandra) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `db.cassandra.consistency_level` | string | The consistency level of the query. Based on consistency values from [CQL](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html). | `all` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.coordinator.dc` | string | The data center of the coordinating node for a query. | `us-west-2` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.coordinator.id` | string | The ID of the coordinating node for a query. | `be13faa2-8574-4d71-926d-27f16cf8a7af` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.idempotence` | boolean | Whether or not the query is idempotent. |  | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.page_size` | int | The fetch size used for paging, i.e. how many rows will be returned at once. | `5000` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.speculative_execution_count` | int | The number of times a query was speculatively executed. Not set or `0` if the query was not executed speculatively. | `0`; `2` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`db.cassandra.consistency_level` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `all` | all | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `each_quorum` | each_quorum | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `quorum` | quorum | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `local_quorum` | local_quorum | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `one` | one | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `two` | two | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `three` | three | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `local_one` | local_one | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `any` | any | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `serial` | serial | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `local_serial` | local_serial | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## CosmosDB Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-cosmosdb) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `db.cosmosdb.client_id` | string | Unique Cosmos client instance id. | `3ba4827d-4422-483f-b59f-85b74211c11d` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.connection_mode` | string | Cosmos client connection mode. | `gateway` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.operation_type` | string | CosmosDB Operation Type. | `Invalid` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.request_charge` | double | RU consumed for that operation | `46.18`; `1.0` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.request_content_length` | int | Request payload size in bytes |  | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.status_code` | int | Cosmos DB status code. | `200`; `201` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.sub_status_code` | int | Cosmos DB sub status code. | `1000`; `1002` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`db.cosmosdb.connection_mode` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `gateway` | Gateway (HTTP) connections mode | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `direct` | Direct connection. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`db.cosmosdb.operation_type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `Invalid` | invalid | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Create` | create | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Patch` | patch | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Read` | read | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ReadFeed` | read_feed | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Delete` | delete | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Replace` | replace | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Execute` | execute | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Query` | query | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Head` | head | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `HeadFeed` | head_feed | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Upsert` | upsert | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Batch` | batch | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `QueryPlan` | query_plan | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ExecuteJavaScript` | execute_javascript | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Elasticsearch Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-elasticsearch) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `db.elasticsearch.cluster.name` | string | Represents the identifier of an Elasticsearch cluster. | `e9106fc68e3044f0b1475b04bf4ffd5f` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.elasticsearch.path_parts.<key>` | string | A dynamic value in the url path. [1] | `db.elasticsearch.path_parts.index=test-index`; `db.elasticsearch.path_parts.doc_id=123` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Many Elasticsearch url paths allow dynamic values. These SHOULD be recorded in span attributes in the format `db.elasticsearch.path_parts.<key>`, where `<key>` is the url path part name. The implementation SHOULD reference the [elasticsearch schema](https://raw.githubusercontent.com/elastic/elasticsearch-specification/main/output/schema/schema.json) in order to map the path part values to their names.
<!-- endsemconv -->

## MSSQL Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-mssql) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `db.mssql.instance_name` | string | The Microsoft SQL Server [instance name](https://docs.microsoft.com/sql/connect/jdbc/building-the-connection-url?view=sql-server-ver15) connecting to. This name is used to determine the port of a named instance. [1] | `MSSQLSERVER` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If setting a `db.mssql.instance_name`, `server.port` is no longer required (but still recommended if non-standard).
<!-- endsemconv -->

## Redis Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-redis) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `db.redis.database_index` | int | The index of the database being accessed as used in the [`SELECT` command](https://redis.io/commands/select), provided as an integer. To be used instead of the generic `db.name` attribute. | `0`; `1`; `15` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Deprecated DB Attributes

<!-- semconv registry.db.deprecated(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `db.cassandra.table` | string | Deprecated, use `db.collection.name` instead. | `mytable` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.collection.name`. |
| `db.connection_string` | string | Deprecated, use `server.address`, `server.port` attributes instead. | `Server=(localdb)\v11.0;Integrated Security=true;` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>"Replaced by `server.address` and `server.port`." |
| `db.cosmosdb.container` | string | Deprecated, use `db.collection.name` instead. | `mytable` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.collection.name`. |
| `db.elasticsearch.node.name` | string | Deprecated, use `db.instance.id` instead. | `instance-0000000001` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.instance.id`. |
| `db.jdbc.driver_classname` | string | Removed, no replacement at this time. | `org.postgresql.Driver`; `com.microsoft.sqlserver.jdbc.SQLServerDriver` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed as not used. |
| `db.mongodb.collection` | string | Deprecated, use `db.collection.name` instead. | `mytable` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.collection.name`. |
| `db.operation` | string | Deprecated, use `db.operation.name` instead. | `findAndModify`; `HMSET`; `SELECT` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.operation.name`. |
| `db.sql.table` | string | Deprecated, use `db.collection.name` instead. | `mytable` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.collection.name`. |
| `db.statement` | string | The database statement being executed. | `SELECT * FROM wuser_table`; `SET mykey "WuValue"` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.query.text`. |
| `db.user` | string | Deprecated, no replacement at this time. | `readonly_user`; `reporting_user` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>No replacement at this time. |
<!-- endsemconv -->

## Deprecated DB Metrics Attributes
<!-- semconv registry.db.metrics.deprecated(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `pool.name` | string | Deprecated, use `db.client.connections.pool.name` instead. | `myDataSource` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.client.connections.pool.name`. |
| `state` | string | Deprecated, use `db.client.connections.state` instead. | `idle` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `db.client.connections.state`. |

`state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `idle` | idle | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `used` | used | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->