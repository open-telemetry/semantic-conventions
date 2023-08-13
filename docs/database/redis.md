<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Redis
--->

# Semantic Conventions for Redis

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Redis](https://redis.com/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"redis"`.

## Call-level attributes

<!-- semconv db.redis(tag=call-level-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `db.redis.database_index` | int | The index of the database being accessed as used in the [`SELECT` command](https://redis.io/commands/select), provided as an integer. To be used instead of the generic `db.name` attribute. | `0`; `1`; `15` | Conditionally Required: If other than the default database (`0`). |
| [`db.statement`](database-spans.md) | string | The full syntax of the Redis CLI command. [1] | `HMSET myhash field1 'Hello' field2 'World'` | Recommended: [2] |

**[1]:** For **Redis**, the value provided for `db.statement` SHOULD correspond to the syntax of the Redis CLI. If, for example, the [`HMSET` command](https://redis.io/commands/hmset) is invoked, `"HMSET myhash field1 'Hello' field2 'World'"` would be a suitable value for `db.statement`.

**[2]:** Should be collected by default only if there is sanitization that excludes sensitive information.
<!-- endsemconv -->

## Example

In this example, Redis is connected using a unix domain socket and therefore the connection string and `server.address` are left out.
Furthermore, `db.name` is not specified as there is no database name in Redis and `db.redis.database_index` is set instead.

| Key                       | Value |
|:--------------------------| :-------------------------------------------- |
| Span name                 | `"HMSET myhash"` |
| `db.system`               | `"redis"` |
| `db.connection_string`    | not set |
| `db.user`                 | not set |
| `server.socket.address`   | `"/tmp/redis.sock"` |
| `network.transport`       | `"Unix"` |
| `db.name`                 | not set |
| `db.statement`            | `"HMSET myhash field1 'Hello' field2 'World"` |
| `db.operation`            | not set |
| `db.redis.database_index` | `15` |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
