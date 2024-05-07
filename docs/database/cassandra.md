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
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.collection.name`](/docs/attributes-registry/db.md) | string | The name of the Cassandra table that the operation is acting upon. [1] | `public.users`; `customers` | `Conditionally Required` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.namespace`](/docs/attributes-registry/db.md) | string | The Cassandra keyspace name. [3] | `mykeyspace` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.cassandra.consistency_level`](/docs/attributes-registry/db.md) | string | The consistency level of the query. Based on consistency values from [CQL](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html). | `all`; `each_quorum`; `quorum` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.cassandra.coordinator.dc`](/docs/attributes-registry/db.md) | string | The data center of the coordinating node for a query. | `us-west-2` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.cassandra.coordinator.id`](/docs/attributes-registry/db.md) | string | The ID of the coordinating node for a query. | `be13faa2-8574-4d71-926d-27f16cf8a7af` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.cassandra.idempotence`](/docs/attributes-registry/db.md) | boolean | Whether or not the query is idempotent. |  | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.cassandra.page_size`](/docs/attributes-registry/db.md) | int | The fetch size used for paging, i.e. how many rows will be returned at once. | `5000` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.cassandra.speculative_execution_count`](/docs/attributes-registry/db.md) | int | The number of times a query was speculatively executed. Not set or `0` if the query was not executed speculatively. | `0`; `2` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the database node where the operation was performed. [4] | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` if and only if `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** If the collection name is parsed from the query, it SHOULD match the value provided in the query and may be qualified with the schema and database name.
It is RECOMMENDED to capture the value as provided by the application without attempting to do any case normalization.

**[2]:** If readily available. Otherwise, if the instrumentation library parses `db.query.text` to capture `db.collection.name`, then it SHOULD be the first collection name found in the query.

**[3]:** For commands that switch the keyspace, this SHOULD be set to the target keyspace (even if the command fails).

**[4]:** If a database operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.

`db.cassandra.consistency_level` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
