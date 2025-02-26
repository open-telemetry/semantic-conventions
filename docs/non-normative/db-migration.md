<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Database migration
--->

# Database semantic convention stability migration guide

> [!WARNING]
> This document is a work in progress and the database semantic conventions
> have not been marked stable yet and changes are still being made.

Due to the significant number of modifications and the extensive user base
affected by them, existing database instrumentations published by
OpenTelemetry are required to implement a migration plan that will assist users in
transitioning to the stable database semantic conventions.

Specifically, when existing database instrumentations published by OpenTelemetry are
updated to the stable database semantic conventions, they:

- SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN` in
  their existing major version, which accepts:
  - `database` - emit the stable database conventions, and stop emitting
    the old database conventions that the instrumentation emitted previously.
  - `database/dup` - emit both the old and the stable database conventions,
    allowing for a phased rollout of the stable semantic conventions.
  - The default behavior (in the absence of one of these values) is to continue
    emitting whatever version of the old database conventions the
    instrumentation was emitting previously.
- Need to maintain (security patching at a minimum) their existing major version
  for at least six months after it starts emitting both sets of conventions.
- May drop the environment variable in their next major version and emit only
  the stable database conventions.

> [!NOTE]
> `OTEL_SEMCONV_STABILITY_OPT_IN` is only intended to be used when migrating
> from an experimental semantic convention to its initial stable version.

## Summary of changes

This section summarizes the changes made to the HTTP semantic conventions
from
[v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/README.md).
to
[v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/README.md).

### Database client span attributes

<!-- prettier-ignore-start -->
| Change                                              | Comments                                                                                                    |
|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `db.connection_string`                              | Removed                                                                                                     |
| `db.user`                                           | Removed                                                                                                     |
| `network.transport`                                 | Removed                                                                                                     |
| `network.type`                                      | Removed                                                                                                     |
| `db.name`                                           | Removed, integrated into the new `db.namespace`                                                             |
| `db.redis.database_index`                           | Removed, integrated into the new `db.namespace`                                                             |
| `db.mssql.instance_name`                            | Removed, integrated into the new `db.namespace`                                                             |
| `db.instance.id`                                    | Removed, replaced by `server.address` or integrated into `db.namespace` as appropriate                      |
| `db.statement` &rarr; `db.query.text`               | Clarified, SHOULD be collected by default only if there is sanitization that excludes sensitive information |
| `db.operation` &rarr; `db.operation.name`           |                                                                                                             |
| `db.sql.table` &rarr; `db.collection.name`          |                                                                                                             |
| `db.cassandra.table` &rarr; `db.collection.name`    |                                                                                                             |
| `db.mongodb.collection` &rarr; `db.collection.name` |                                                                                                             |
| `db.cosmosdb.container` &rarr; `db.collection.name` |                                                                                                             |
| New: `db.operation.batch.size`                      |                                                                                                             |
| New: `db.response.status_code`                      |                                                                                                             |
| New: `db.operation.parameter.<key>`                 | Opt-In                                                                                                      |
| New: `error.type`                                   |                                                                                                             |
<!-- prettier-ignore-end -->

References:

- [Database client span attributes v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-spans.md)
- [Database client span attributes v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-spans.md)

### Database client span names

The recommended span name has changed to `{db.operation.name} {target}`, where the `{target}` SHOULD describe the entity
that the operation is performed against and SHOULD adhere to one of the following values, provided they are accessible:

- `db.collection.name` SHOULD be used for data manipulation operations or operations on database collections
- `db.namespace` SHOULD be used for operations on a specific database namespace
- `server.address:server.port` SHOULD be used for other operations not targeting any specific database(s) or collection(s)

References:

- [Database client span names v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-spans.md)
- [Database client span names v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-spans.md#name)

### Database client operation duration metric

This is a required metric. There was no similar metric previously.

See [Metric `db.client.operation.duration` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientoperationduration).

### Experimental connection metrics

Database connection metrics are not stable yet, but there have been several changes in the latest release.

#### Database client connection count

Metric changes:

- **Name**: `db.client.connections.usage` &rarr; `db.client.connection.count`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
| `state` &rarr; `db.client.connection.state`         |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.usage` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionsusage)
- [Metric `db.client.connection.count` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectioncount)

#### Database client connection idle max

Metric changes:

- **Name**: `db.client.connections.idle.max` &rarr; `db.client.connection.idle.max`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.idle.max` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionsidlemax)
- [Metric `db.client.connection.idle.max` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectionidlemax)

#### Database client connection idle min

Metric changes:

- **Name**: `db.client.connections.idle.min` &rarr; `db.client.connection.idle.min`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.idle.min` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionsidlemin)
- [Metric `db.client.connection.idle.min` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectionidlemin)

#### Database client connection max

Metric changes:

- **Name**: `db.client.connections.max` &rarr; `db.client.connection.max`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.max` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionsmax)
- [Metric `db.client.connection.max` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectionmax)

#### Database client connection pending requests

Metric changes:

- **Name**: `db.client.connections.pending_requests` &rarr; `db.client.connection.pending_requests`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.pending_requests` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionspending_requests)
- [Metric `db.client.connection.pending_requests` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectionpending_requests)

#### Database client connection timeouts

Metric changes:

- **Name**: `db.client.connections.timeouts` &rarr; `db.client.connection.timeouts`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.timeouts` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionstimeouts)
- [Metric `db.client.connection.timeouts` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectiontimeouts)

#### Database client connection create time

Metric changes:

- **Name**: `db.client.connections.create_time` &rarr; `db.client.connection.create_time`
- **Unit**: `ms` &rarr; `s`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.create_time` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionscreate_time)
- [Metric `db.client.connection.create_time` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectioncreate_time)

#### Database client connection wait time

Metric changes:

- **Name**: `db.client.connections.wait_time` &rarr; `db.client.connection.wait_time`
- **Unit**: `ms` &rarr; `s`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.wait_time` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionswait_time)
- [Metric `db.client.connection.wait_time` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectionwait_time)

#### Database client connection use time

Metric changes:

- **Name**: `db.client.connections.use_time` &rarr; `db.client.connection.use_time`
- **Unit**: `ms` &rarr; `s`
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                                    | Comments |
|-----------------------------------------------------|----------|
| `pool.name` &rarr; `db.client.connection.pool.name` |          |
<!-- prettier-ignore-end -->

References:

- [Metric `db.client.connections.use_time` v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md#metric-dbclientconnectionsuse_time)
- [Metric `db.client.connection.use_time` v1.28.0 (RC)](https://github.com/open-telemetry/semantic-conventions/blob/v1.28.0/docs/database/database-metrics.md#metric-dbclientconnectionuse_time)
