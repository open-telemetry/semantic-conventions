<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Cassandra
--->

# Semantic Conventions for Cassandra

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Cassandra](https://cassandra.apache.org/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"cassandra"`.

## Call-level attributes

<!-- semconv db.cassandra(tag=call-level-tech-specific-cassandra) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `db.cassandra.consistency_level` | string | The consistency level of the query. Based on consistency values from [CQL](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html). | `all` | Recommended |
| `db.cassandra.coordinator.dc` | string | The data center of the coordinating node for a query. | `us-west-2` | Recommended |
| `db.cassandra.coordinator.id` | string | The ID of the coordinating node for a query. | `be13faa2-8574-4d71-926d-27f16cf8a7af` | Recommended |
| `db.cassandra.idempotence` | boolean | Whether or not the query is idempotent. |  | Recommended |
| `db.cassandra.page_size` | int | The fetch size used for paging, i.e. how many rows will be returned at once. | `5000` | Recommended |
| `db.cassandra.speculative_execution_count` | int | The number of times a query was speculatively executed. Not set or `0` if the query was not executed speculatively. | `0`; `2` | Recommended |
| `db.cassandra.table` | string | The name of the primary table that the operation is acting upon, including the keyspace name (if applicable). [1] | `mytable` | Recommended |
| [`db.name`](database-spans.md) | string | The keyspace name in Cassandra. [2] | `mykeyspace` | Conditionally Required: If applicable. |

**[1]:** This mirrors the db.sql.table attribute but references cassandra rather than sql. It is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if it is provided by the library being instrumented. If the operation is acting upon an anonymous table, or more than one table, this value MUST NOT be set.

**[2]:** For Cassandra the `db.name` should be set to the Cassandra keyspace name.

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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
