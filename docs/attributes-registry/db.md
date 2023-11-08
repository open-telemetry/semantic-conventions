<!--- Hugo front matter used to generate the website version of this page:
--->

# Database

<!-- toc -->

- [Generic Database Attributes](#generic-database-attributes)
- [Cassandra Attributes](#cassandra-attributes)
- [CosmosDB Attributes](#cosmosdb-attributes)
- [Elasticsearch Attributes](#elasticsearch-attributes)
- [JDBC Attributes](#jdbc-attributes)
- [MongoDB Attributes](#mongodb-attributes)
- [MSSQL Attributes](#mssql-attributes)
- [Redis Attributes](#redis-attributes)
- [SQL Attributes](#sql-attributes)

<!-- tocstop -->

## Generic Database Attributes

<!-- semconv registry.db(omit_requirement_level,tag=db-generic) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.name` | string | This attribute is used to report the name of the database being accessed. For commands that switch the database, this should be set to the target database (even if the command fails). [1] | `customers`; `main` |
| `db.operation` | string | The name of the operation being executed, e.g. the [MongoDB command name](https://docs.mongodb.com/manual/reference/command/#database-operations) such as `findAndModify`, or the SQL keyword. [2] | `findAndModify`; `HMSET`; `SELECT` |
| `db.statement` | string | The database statement being executed. | `SELECT * FROM wuser_table`; `SET mykey "WuValue"` |
| `db.system` | string | An identifier for the database management system (DBMS) product being used. See below for a list of well-known identifiers. | `other_sql` |
| `db.user` | string | Username for accessing the database. | `readonly_user`; `reporting_user` |

**[1]:** In some SQL databases, the database name to be used is called "schema name". In case there are multiple layers that could be considered for database name (e.g. Oracle instance name and schema name), the database name to be used is the more specific layer (e.g. Oracle schema name).

**[2]:** When setting this to an SQL keyword, it is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if the operation name is provided by the library being instrumented. If the SQL statement has an ambiguous operation, or performs more than one operation, this value may be omitted.

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

## Cassandra Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-cassandra) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.cassandra.consistency_level` | string | The consistency level of the query. Based on consistency values from [CQL](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html). | `all` |
| `db.cassandra.coordinator.dc` | string | The data center of the coordinating node for a query. | `us-west-2` |
| `db.cassandra.coordinator.id` | string | The ID of the coordinating node for a query. | `be13faa2-8574-4d71-926d-27f16cf8a7af` |
| `db.cassandra.idempotence` | boolean | Whether or not the query is idempotent. |  |
| `db.cassandra.page_size` | int | The fetch size used for paging, i.e. how many rows will be returned at once. | `5000` |
| `db.cassandra.speculative_execution_count` | int | The number of times a query was speculatively executed. Not set or `0` if the query was not executed speculatively. | `0`; `2` |
| `db.cassandra.table` | string | The name of the primary Cassandra table that the operation is acting upon, including the keyspace name (if applicable). [1] | `mytable` |

**[1]:** This mirrors the db.sql.table attribute but references cassandra rather than sql. It is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if it is provided by the library being instrumented. If the operation is acting upon an anonymous table, or more than one table, this value MUST NOT be set.

`db.cassandra.consistency_level` MUST be one of the following:

| Value  | Description |
|---|---|
| `all` | all |
| `each_quorum` | each_quorum |
| `quorum` | quorum |
| `local_quorum` | local_quorum |
| `one` | one |
| `two` | two |
| `three` | three |
| `local_one` | local_one |
| `any` | any |
| `serial` | serial |
| `local_serial` | local_serial |
<!-- endsemconv -->

## CosmosDB Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-cosmosdb) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.cosmosdb.client_id` | string | Unique Cosmos client instance id. | `3ba4827d-4422-483f-b59f-85b74211c11d` |
| `db.cosmosdb.connection_mode` | string | Cosmos client connection mode. | `gateway` |
| `db.cosmosdb.container` | string | Cosmos DB container name. | `anystring` |
| `db.cosmosdb.operation_type` | string | CosmosDB Operation Type. | `Invalid` |
| `db.cosmosdb.request_charge` | double | RU consumed for that operation | `46.18`; `1.0` |
| `db.cosmosdb.request_content_length` | int | Request payload size in bytes |  |
| `db.cosmosdb.status_code` | int | Cosmos DB status code. | `200`; `201` |
| `db.cosmosdb.sub_status_code` | int | Cosmos DB sub status code. | `1000`; `1002` |

`db.cosmosdb.connection_mode` MUST be one of the following:

| Value  | Description |
|---|---|
| `gateway` | Gateway (HTTP) connections mode |
| `direct` | Direct connection. |

`db.cosmosdb.operation_type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `Invalid` | invalid |
| `Create` | create |
| `Patch` | patch |
| `Read` | read |
| `ReadFeed` | read_feed |
| `Delete` | delete |
| `Replace` | replace |
| `Execute` | execute |
| `Query` | query |
| `Head` | head |
| `HeadFeed` | head_feed |
| `Upsert` | upsert |
| `Batch` | batch |
| `QueryPlan` | query_plan |
| `ExecuteJavaScript` | execute_javascript |
<!-- endsemconv -->

## Elasticsearch Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-elasticsearch) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.elasticsearch.cluster.name` | string | Represents the identifier of an Elasticsearch cluster. | `e9106fc68e3044f0b1475b04bf4ffd5f` |
| `db.elasticsearch.node.name` | string | Represents the human-readable identifier of the node/instance to which a request was routed. | `instance-0000000001` |
| `db.elasticsearch.path_parts.<key>` | string | A dynamic value in the url path. [1] | `db.elasticsearch.path_parts.index=test-index`; `db.elasticsearch.path_parts.doc_id=123` |

**[1]:** Many Elasticsearch url paths allow dynamic values. These SHOULD be recorded in span attributes in the format `db.elasticsearch.path_parts.<key>`, where `<key>` is the url path part name. The implementation SHOULD reference the [elasticsearch schema](https://raw.githubusercontent.com/elastic/elasticsearch-specification/main/output/schema/schema.json) in order to map the path part values to their names.
<!-- endsemconv -->

## JDBC Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-jdbc) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.jdbc.driver_classname` | string | The fully-qualified class name of the [Java Database Connectivity (JDBC)](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/) driver used to connect. | `org.postgresql.Driver`; `com.microsoft.sqlserver.jdbc.SQLServerDriver` |
<!-- endsemconv -->

## MongoDB Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-mongodb) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.mongodb.collection` | string | The MongoDB collection being accessed within the database stated in `db.name`. | `customers`; `products` |
<!-- endsemconv -->

## MSSQL Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-mssql) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.mssql.instance_name` | string | The Microsoft SQL Server [instance name](https://docs.microsoft.com/sql/connect/jdbc/building-the-connection-url?view=sql-server-ver15) connecting to. This name is used to determine the port of a named instance. [1] | `MSSQLSERVER` |

**[1]:** If setting a `db.mssql.instance_name`, `server.port` is no longer required (but still recommended if non-standard).
<!-- endsemconv -->

## Redis Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-redis) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.redis.database_index` | int | The index of the database being accessed as used in the [`SELECT` command](https://redis.io/commands/select), provided as an integer. To be used instead of the generic `db.name` attribute. | `0`; `1`; `15` |
<!-- endsemconv -->


## SQL Attributes

<!-- semconv registry.db(omit_requirement_level,tag=tech-specific-sql) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `db.sql.table` | string | The name of the primary table that the operation is acting upon, including the database name (if applicable). [1] | `public.users`; `customers` |

**[1]:** It is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if it is provided by the library being instrumented. If the operation is acting upon an anonymous table, or more than one table, this value MUST NOT be set.
<!-- endsemconv -->
