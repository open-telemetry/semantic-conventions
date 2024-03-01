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
  * [Metric: `db.client.connections.usage`](#metric-dbclientconnectionsusage)
  * [Metric: `db.client.connections.idle.max`](#metric-dbclientconnectionsidlemax)
  * [Metric: `db.client.connections.idle.min`](#metric-dbclientconnectionsidlemin)
  * [Metric: `db.client.connections.max`](#metric-dbclientconnectionsmax)
  * [Metric: `db.client.connections.pending_requests`](#metric-dbclientconnectionspending_requests)
  * [Metric: `db.client.connections.timeouts`](#metric-dbclientconnectionstimeouts)
  * [Metric: `db.client.connections.create_time`](#metric-dbclientconnectionscreate_time)
  * [Metric: `db.client.connections.wait_time`](#metric-dbclientconnectionswait_time)
  * [Metric: `db.client.connections.use_time`](#metric-dbclientconnectionsuse_time)

<!-- tocstop -->

> **Warning**
> Existing database instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-metrics.md)
> (or prior) SHOULD NOT change the version of the database conventions that they emit
> until a transition plan to the (future) stable semantic conventions has been published.
> Conventions include, but are not limited to, attributes, metric and span names, and unit of measure.

## Connection pools

The following metric instruments describe database client connection pool operations.

### Metric: `db.client.connections.usage`

This metric is [required][MetricRequired].

<!-- semconv metric.db.client.connections.usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.usage` | UpDownCounter | `{connection}` | The number of connections that are currently in state described by the `state` attribute |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
| `state` | string | The state of a connection in the pool | `idle` | Required |

`state` MUST be one of the following:

| Value  | Description |
|---|---|
| `idle` | idle |
| `used` | used |
<!-- endsemconv -->
### Metric: `db.client.connections.idle.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.idle.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.idle.max` | UpDownCounter | `{connection}` | The maximum number of idle open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.idle.max(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.idle.min`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.idle.min(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.idle.min` | UpDownCounter | `{connection}` | The minimum number of idle open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.idle.min(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.max(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.max` | UpDownCounter | `{connection}` | The maximum number of open connections allowed |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.max(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.pending_requests`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.pending_requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.pending_requests` | UpDownCounter | `{request}` | The number of pending requests for an open connection, cumulative for the entire pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.pending_requests(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.timeouts`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.timeouts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.timeouts` | Counter | `{timeout}` | The number of connection timeouts that have occurred trying to obtain a connection from the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.timeouts(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.create_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.create_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.create_time` | Histogram | `ms` | The time it took to create a new connection |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.create_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.wait_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.wait_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.wait_time` | Histogram | `ms` | The time it took to obtain an open connection from the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.wait_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

### Metric: `db.client.connections.use_time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.db.client.connections.use_time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `db.client.connections.use_time` | Histogram | `ms` | The time between borrowing a connection and returning it to the pool |
<!-- endsemconv -->

<!-- semconv metric.db.client.connections.use_time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `pool.name` | string | The name of the connection pool; unique within the instrumented application. In case the connection pool implementation doesn't provide a name, then the [db.connection_string](/docs/database/database-spans.md#common-attributes) should be used | `myDataSource` | Required |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/metric-requirement-level.md#required
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/metric-requirement-level.md#recommended
