<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Cassandra
--->

# Semantic Conventions for Cassandra

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Cassandra](https://cassandra.apache.org/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"cassandra"`.

## Attributes

<!-- semconv db.cassandra(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`db.cassandra.consistency_level`](../attributes-registry/db.md) | string | The consistency level of the query. Based on consistency values from [CQL](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html). | `all` | Recommended |
| [`db.cassandra.coordinator.dc`](../attributes-registry/db.md) | string | The data center of the coordinating node for a query. | `us-west-2` | Recommended |
| [`db.cassandra.coordinator.id`](../attributes-registry/db.md) | string | The ID of the coordinating node for a query. | `be13faa2-8574-4d71-926d-27f16cf8a7af` | Recommended |
| [`db.cassandra.idempotence`](../attributes-registry/db.md) | boolean | Whether or not the query is idempotent. |  | Recommended |
| [`db.cassandra.page_size`](../attributes-registry/db.md) | int | The fetch size used for paging, i.e. how many rows will be returned at once. | `5000` | Recommended |
| [`db.cassandra.speculative_execution_count`](../attributes-registry/db.md) | int | The number of times a query was speculatively executed. Not set or `0` if the query was not executed speculatively. | `0`; `2` | Recommended |
| [`db.cassandra.table`](../attributes-registry/db.md) | string | The name of the primary Cassandra table that the operation is acting upon, including the keyspace name (if applicable). [1] | `mytable` | Recommended |
| [`db.name`](../attributes-registry/db.md) | string | The keyspace name in Cassandra. [2] | `mykeyspace` | Conditionally Required: If applicable. |
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the database node where the operation was performed. [3] | `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`network.peer.port`](../attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | Recommended: if and only if `network.peer.address` is set. |

**[1]:** This mirrors the db.sql.table attribute but references cassandra rather than sql. It is not recommended to attempt any client-side parsing of `db.statement` just to get this property, but it should be set if it is provided by the library being instrumented. If the operation is acting upon an anonymous table, or more than one table, this value MUST NOT be set.

**[2]:** For Cassandra the `db.name` should be set to the Cassandra keyspace name.

**[3]:** If a database operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.

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
