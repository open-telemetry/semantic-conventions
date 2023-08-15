<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
--->

# Semantic Conventions for Database Metrics

**Status**: [Experimental][DocumentStatus]

The conventions described in this section are specific to SQL and NoSQL clients.

**Disclaimer:** These are initial database client metric instruments
and attributes but more may be added in the future.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Connection pools](#connection-pools)
  * [Metric: `db.client.connection.usage`](#metric-dbclientconnectionusage)
  * [Metric: `db.client.connection.idle.max`](#metric-dbclientconnectionidlemax)
  * [Metric: `db.client.connection.idle.min`](#metric-dbclientconnectionidlemin)
  * [Metric: `db.client.connection.max`](#metric-dbclientconnectionmax)
  * [Metric: `db.client.connection.pending_requests`](#metric-dbclientconnectionpending_requests)
  * [Metric: `db.client.connection.timeouts`](#metric-dbclientconnectiontimeouts)
  * [Metric: `db.client.connection.create_time`](#metric-dbclientconnectioncreate_time)
  * [Metric: `db.client.connection.wait_time`](#metric-dbclientconnectionwait_time)
  * [Metric: `db.client.connection.use_time`](#metric-dbclientconnectionuse_time)

<!-- tocstop -->

## Connection pools

The following metric instruments describe database client connection pool operations.

### Metric: `db.client.connection.usage`

This metric is [required][MetricRequired].

<!-- semconv metric.db.client.connection.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.usage` | UpDownCounter | `{connection}` | The number of connections that are currently in state described by the `state` attribute |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
| `state` | string | The state of a connection in the pool | `idle` | Required |

`state` MUST be one of the following:

| Value  | Description |
|---|---|
| `idle` | idle |
| `used` | used |
<!-- endsemconv -->
### Metric: `db.client.connection.idle.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.idle.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.idle.max` | UpDownCounter | `{connection}` | The maximum number of idle open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.idle.max(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connection.idle.min`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.idle.min(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.idle.min` | UpDownCounter | `{connection}` | The minimum number of idle open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.idle.min(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connection.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.max` | UpDownCounter | `{connection}` | The maximum number of open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.max(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connection.pending_requests`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.pending_requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.pending_requests` | UpDownCounter | `{request}` | The number of pending requests for an open connection, cumulative for the entire pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.pending_requests(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connection.timeouts`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.timeouts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.timeouts` | Counter | `{timeout}` | The number of connection timeouts that have occurred trying to obtain a connection from the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.timeouts(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connection.create_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.create_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.create_time` | Histogram | `ms` | The time it took to create a new connection |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.create_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connection.wait_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.wait_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.wait_time` | Histogram | `ms` | The time it took to obtain an open connection from the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.wait_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connection.use_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connection.use_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connection.use_time` | Histogram | `ms` | The time between borrowing a connection and returning it to the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connection.use_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation does not provide a name, then the [db.connection_string](/docs/database/database-spans.md#connection-level-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/metric-requirement-level.md#required
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/metric-requirement-level.md#recommended
