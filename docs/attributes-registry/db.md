<!--- Hugo front matter used to generate the website version of this page:
--->

# DB

- [db](#db)
- [db deprecated](#db deprecated)

## db Attributes

| Attribute                                  | Type    | Description                                                                                                                                                                                                                                                                                                                                                                                                        | Examples                                                                                 | Stability                                                        |
| ------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `db.cassandra.consistency_level`           | string  | The consistency level of the query. Based on consistency values from [CQL](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html).                                                                                                                                                                                                                                                | `all`                                                                                    | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.coordinator.dc`              | string  | The data center of the coordinating node for a query.                                                                                                                                                                                                                                                                                                                                                              | `us-west-2`                                                                              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.coordinator.id`              | string  | The ID of the coordinating node for a query.                                                                                                                                                                                                                                                                                                                                                                       | `be13faa2-8574-4d71-926d-27f16cf8a7af`                                                   | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.idempotence`                 | boolean | Whether or not the query is idempotent.                                                                                                                                                                                                                                                                                                                                                                            |                                                                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.page_size`                   | int     | The fetch size used for paging, i.e. how many rows will be returned at once.                                                                                                                                                                                                                                                                                                                                       | `5000`                                                                                   | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cassandra.speculative_execution_count` | int     | The number of times a query was speculatively executed. Not set or `0` if the query was not executed speculatively.                                                                                                                                                                                                                                                                                                | `0`; `2`                                                                                 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.collection.name`                       | string  | The name of a collection (table, container) within the database. [1]                                                                                                                                                                                                                                                                                                                                               | `public.users`; `customers`                                                              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.client_id`                    | string  | Unique Cosmos client instance id.                                                                                                                                                                                                                                                                                                                                                                                  | `3ba4827d-4422-483f-b59f-85b74211c11d`                                                   | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.connection_mode`              | string  | Cosmos client connection mode.                                                                                                                                                                                                                                                                                                                                                                                     | `gateway`                                                                                | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.operation_type`               | string  | CosmosDB Operation Type.                                                                                                                                                                                                                                                                                                                                                                                           | `Invalid`                                                                                | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.request_charge`               | double  | RU consumed for that operation                                                                                                                                                                                                                                                                                                                                                                                     | `46.18`; `1.0`                                                                           | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.request_content_length`       | int     | Request payload size in bytes                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.status_code`                  | int     | Cosmos DB status code.                                                                                                                                                                                                                                                                                                                                                                                             | `200`; `201`                                                                             | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.cosmosdb.sub_status_code`              | int     | Cosmos DB sub status code.                                                                                                                                                                                                                                                                                                                                                                                         | `1000`; `1002`                                                                           | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.elasticsearch.cluster.name`            | string  | Represents the identifier of an Elasticsearch cluster.                                                                                                                                                                                                                                                                                                                                                             | `e9106fc68e3044f0b1475b04bf4ffd5f`                                                       | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.elasticsearch.path_parts.<key>`        | string  | A dynamic value in the url path. [2]                                                                                                                                                                                                                                                                                                                                                                               | `db.elasticsearch.path_parts.index=test-index`; `db.elasticsearch.path_parts.doc_id=123` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.instance.id`                           | string  | An identifier (address, unique name, or any other identifier) of the database instance that is executing queries or mutations on the current connection. This is useful in cases where the database is running in a clustered environment and the instrumentation is able to record the node executing the query. The client may obtain this value in databases like MySQL using queries like `select @@hostname`. | `mysql-e26b99z.example.com`                                                              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.mssql.instance_name`                   | string  | The Microsoft SQL Server [instance name](https://docs.microsoft.com/sql/connect/jdbc/building-the-connection-url?view=sql-server-ver15) connecting to. This name is used to determine the port of a named instance. [3]                                                                                                                                                                                            | `MSSQLSERVER`                                                                            | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.name`                                  | string  | This attribute is used to report the name of the database being accessed. For commands that switch the database, this should be set to the target database (even if the command fails). [4]                                                                                                                                                                                                                        | `customers`; `main`                                                                      | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.operation.name`                        | string  | The name of the operation or command being executed.                                                                                                                                                                                                                                                                                                                                                               | `findAndModify`; `HMSET`; `SELECT`                                                       | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.query.parameter.<key>`                 | string  | The query parameters used in `db.query.text`, with `<key>` being the parameter name, and the attribute value being the parameter value. [5]                                                                                                                                                                                                                                                                        | `someval`; `55`                                                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.query.text`                            | string  | The database query being executed.                                                                                                                                                                                                                                                                                                                                                                                 | `SELECT * FROM wuser_table where username = ?`; `SET mykey "WuValue"`                    | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.redis.database_index`                  | int     | The index of the database being accessed as used in the [`SELECT` command](https://redis.io/commands/select), provided as an integer. To be used instead of the generic `db.name` attribute.                                                                                                                                                                                                                       | `0`; `1`; `15`                                                                           | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db.system`                                | string  | An identifier for the database management system (DBMS) product being used. See below for a list of well-known identifiers.                                                                                                                                                                                                                                                                                        | `other_sql`                                                                              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.

**[2]:** Many Elasticsearch url paths allow dynamic values. These SHOULD be recorded in span attributes in the format `db.elasticsearch.path_parts.<key>`, where `<key>` is the url path part name. The implementation SHOULD reference the [elasticsearch schema](https://raw.githubusercontent.com/elastic/elasticsearch-specification/main/output/schema/schema.json) in order to map the path part values to their names.

**[3]:** If setting a `db.mssql.instance_name`, `server.port` is no longer required (but still recommended if non-standard).

**[4]:** In some SQL databases, the database name to be used is called "schema name". In case there are multiple layers that could be considered for database name (e.g. Oracle instance name and schema name), the database name to be used is the more specific layer (e.g. Oracle schema name).

**[5]:** Query parameters should only be captured when `db.query.text` is parameterized with placeholders.
If a parameter has no name and instead is referenced only by index, then `<key>` SHOULD be the 0-based index.

`db.cassandra.consistency_level` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value          | Description | Stability                                                        |
| -------------- | ----------- | ---------------------------------------------------------------- |
| `all`          | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `each_quorum`  | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `quorum`       | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `local_quorum` | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `one`          | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `two`          | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `three`        | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `local_one`    | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `any`          | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `serial`       | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `local_serial` | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`db.cosmosdb.connection_mode` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value     | Description                     | Stability                                                        |
| --------- | ------------------------------- | ---------------------------------------------------------------- |
| `gateway` | Gateway (HTTP) connections mode | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `direct`  | Direct connection.              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`db.cosmosdb.operation_type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value               | Description | Stability                                                        |
| ------------------- | ----------- | ---------------------------------------------------------------- |
| `Invalid`           | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Create`            | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Patch`             | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Read`              | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ReadFeed`          | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Delete`            | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Replace`           | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Execute`           | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Query`             | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Head`              | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `HeadFeed`          | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Upsert`            | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `Batch`             | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `QueryPlan`         | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ExecuteJavaScript` | none        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`db.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value           | Description                                        | Stability                                                        |
| --------------- | -------------------------------------------------- | ---------------------------------------------------------------- |
| `other_sql`     | Some other SQL database. Fallback only. See notes. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mssql`         | Microsoft SQL Server                               | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mssqlcompact`  | Microsoft SQL Server Compact                       | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mysql`         | MySQL                                              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `oracle`        | Oracle Database                                    | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `db2`           | IBM Db2                                            | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `postgresql`    | PostgreSQL                                         | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `redshift`      | Amazon Redshift                                    | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hive`          | Apache Hive                                        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cloudscape`    | Cloudscape                                         | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hsqldb`        | HyperSQL DataBase                                  | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `progress`      | Progress Database                                  | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `maxdb`         | SAP MaxDB                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hanadb`        | SAP HANA                                           | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ingres`        | Ingres                                             | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `firstsql`      | FirstSQL                                           | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `edb`           | EnterpriseDB                                       | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cache`         | InterSystems Caché                                 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `adabas`        | Adabas (Adaptable Database System)                 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `firebird`      | Firebird                                           | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `derby`         | Apache Derby                                       | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `filemaker`     | FileMaker                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `informix`      | Informix                                           | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `instantdb`     | InstantDB                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `interbase`     | InterBase                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mariadb`       | MariaDB                                            | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `netezza`       | Netezza                                            | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pervasive`     | Pervasive PSQL                                     | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pointbase`     | PointBase                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `sqlite`        | SQLite                                             | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `sybase`        | Sybase                                             | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `teradata`      | Teradata                                           | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `vertica`       | Vertica                                            | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `h2`            | H2                                                 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `coldfusion`    | ColdFusion IMQ                                     | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cassandra`     | Apache Cassandra                                   | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hbase`         | Apache HBase                                       | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mongodb`       | MongoDB                                            | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `redis`         | Redis                                              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `couchbase`     | Couchbase                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `couchdb`       | CouchDB                                            | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cosmosdb`      | Microsoft Azure Cosmos DB                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `dynamodb`      | Amazon DynamoDB                                    | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `neo4j`         | Neo4j                                              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `geode`         | Apache Geode                                       | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `elasticsearch` | Elasticsearch                                      | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `memcached`     | Memcached                                          | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cockroachdb`   | CockroachDB                                        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `opensearch`    | OpenSearch                                         | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `clickhouse`    | ClickHouse                                         | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `spanner`       | Cloud Spanner                                      | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `trino`         | Trino                                              | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

## db deprecated Attributes

| Attribute                    | Type   | Description                                                             | Examples                                                                | Stability                                                   |
| ---------------------------- | ------ | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------- |
| `db.cassandra.table`         | string | Deprecated, use `db.collection.name` instead. [6]                       | `mytable`                                                               | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.connection_string`       | string | Deprecated, use `server.address`, `server.port` attributes instead. [7] | `Server=(localdb)\v11.0;Integrated Security=true;`                      | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.cosmosdb.container`      | string | Deprecated, use `db.collection.name` instead. [8]                       | `mytable`                                                               | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.elasticsearch.node.name` | string | Deprecated, use `db.instance.id` instead. [9]                           | `instance-0000000001`                                                   | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.jdbc.driver_classname`   | string | Removed, no replacement at this time. [10]                              | `org.postgresql.Driver`; `com.microsoft.sqlserver.jdbc.SQLServerDriver` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.mongodb.collection`      | string | Deprecated, use `db.collection.name` instead. [11]                      | `mytable`                                                               | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.operation`               | string | Deprecated, use `db.operation.name` instead. [12]                       | `findAndModify`; `HMSET`; `SELECT`                                      | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.sql.table`               | string | Deprecated, use `db.collection.name` instead. [13]                      | `mytable`                                                               | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.statement`               | string | The database statement being executed. [14]                             | `SELECT * FROM wuser_table`; `SET mykey "WuValue"`                      | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `db.user`                    | string | Deprecated, no replacement at this time. [15]                           | `readonly_user`; `reporting_user`                                       | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |

**[6]:** Replaced by `db.collection.name`.
**[7]:** "Replaced by `server.address` and `server.port`."

**[8]:** Replaced by `db.collection.name`.
**[9]:** Replaced by `db.instance.id`.
**[10]:** Removed as not used.
**[11]:** Replaced by `db.collection.name`.
**[12]:** Replaced by `db.operation.name`.
**[13]:** Replaced by `db.collection.name`.
**[14]:** Replaced by `db.query.text`.
**[15]:** No replacement at this time.
