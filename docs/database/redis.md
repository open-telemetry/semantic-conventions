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
| [`db.redis.database_index`](../attributes-registry/db.md) | int | The index of the database being accessed as used in the [`SELECT` command](https://redis.io/commands/select), provided as an integer. To be used instead of the generic `db.name` attribute. | `0`; `1`; `15` | `Conditionally Required` If other than the default database (`0`). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.query.text`](../attributes-registry/db.md) | string | The full syntax of the Redis CLI command. [1] | `HMSET myhash field1 'Hello' field2 'World'` | `Recommended` [2] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the database node where the operation was performed. [3] | `10.1.2.80`; `/tmp/my.sock` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](../attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | `Recommended` if and only if `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** For **Redis**, the value provided for `db.query.text` SHOULD correspond to the syntax of the Redis CLI. If, for example, the [`HMSET` command](https://redis.io/commands/hmset) is invoked, `"HMSET myhash field1 'Hello' field2 'World'"` would be a suitable value for `db.query.text`.

**[2]:** Should be collected by default only if there is sanitization that excludes sensitive information.

**[3]:** If a database operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.
<!-- endsemconv -->

## Example

In this example, Redis is connected using a unix domain socket and therefore the connection string is left out.
Furthermore, `db.name` is not specified as there is no database name in Redis and `db.redis.database_index` is set instead.

| Key                       | Value |
|:--------------------------| :-------------------------------------------- |
| Span name                 | `"HMSET myhash"` |
| `db.system`               | `"redis"` |
| `db.user`                 | not set |
| `network.peer.address`    | `"/tmp/redis.sock"` |
| `network.transport`       | `"unix"` |
| `db.name`                 | not set |
| `db.statement`            | `"HMSET myhash field1 'Hello' field2 'World"` |
| `db.operation`            | not set |
| `db.redis.database_index` | `15` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
