<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Redis
--->

# Semantic Conventions for Redis

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Redis](https://redis.com/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"redis"`.

## Attributes

<!-- semconv db.redis(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.collection.namespace`](../attributes-registry/db.md) | string | The index of the database being accessed as used in the [`SELECT` command](https://redis.io/commands/select). [1] | `0`; `1`; `15` | `Conditionally Required` If and only if it can be captured reliably. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.query.text`](../attributes-registry/db.md) | string | The full syntax of the Redis CLI command. [2] | `HMSET myhash field1 'Hello' field2 'World'` | `Recommended` [3] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the database node where the operation was performed. [4] | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](../attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` if and only if `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** The database index for current connection can be changed by the application dynamically. Instrumentations MAY track the currently selected database and set `db.collection.namespace` accordingly.
Instrumentations SHOULD NOT set this attribute if capturing it would require additional network calls to Redis.
For commands that switch the database, this should be set to the target database (even if the command fails).

**[2]:** For **Redis**, the value provided for `db.query.text` SHOULD correspond to the syntax of the Redis CLI. If, for example, the [`HMSET` command](https://redis.io/commands/hmset) is invoked, `"HMSET myhash field1 'Hello' field2 'World'"` would be a suitable value for `db.query.text`.

**[3]:** SHOULD be collected by default only if there is sanitization that excludes sensitive information.

**[4]:** If a database operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.
<!-- endsemconv -->

## Example

In this example, Redis is connected using a unix domain socket and therefore the connection string is left out.

| Key                       | Value |
|:--------------------------| :-------------------------------------------- |
| Span name                 | `"HMSET myhash"` |
| `db.system`               | `"redis"` |
| `network.peer.address`    | `"/tmp/redis.sock"` |
| `network.transport`       | `"unix"` |
| `db.collection.namespace` | `"15"` |
| `db.query.text`           | `"HMSET myhash field1 'Hello' field2 'World"` |
| `db.operation.name`       | not set |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
