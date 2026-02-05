<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
--->

# Semantic Conventions for DHCP Metrics

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for DHCP metrics, covering client,
server, and relay agent instrumentation.

<!-- toc -->

- [Client Metrics](#client-metrics)
  - [Metric: `dhcp.client.request.duration`](#metric-dhcpclientrequestduration)
  - [Metric: `dhcp.client.lease.duration`](#metric-dhcpclientleaseduration)
- [Server Metrics](#server-metrics)
  - [Metric: `dhcp.server.request.duration`](#metric-dhcpserverrequestduration)
  - [Metric: `dhcp.server.pool.usage`](#metric-dhcpserverpoolusage)
  - [Metric: `dhcp.server.pool.limit`](#metric-dhcpserverpoollimit)
  - [Metric: `dhcp.server.pool.utilization`](#metric-dhcpserverpoolutilization)
  - [Metric: `dhcp.server.leases.active`](#metric-dhcpserverleasesactive)
- [Relay Metrics](#relay-metrics)
  - [Metric: `dhcp.relay.request.duration`](#metric-dhcprelayrequestduration)

<!-- tocstop -->

## Client Metrics

### Metric: `dhcp.client.request.duration`

This metric measures the duration of DHCP client requests.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.dhcp.client.request.duration -->
<!-- endsemconv -->

### Metric: `dhcp.client.lease.duration`

This metric tracks the time remaining on the current lease.

<!-- semconv metric.dhcp.client.lease.duration -->
<!-- endsemconv -->

## Server Metrics

### Metric: `dhcp.server.request.duration`

This metric measures server-side request processing duration.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.dhcp.server.request.duration -->
<!-- endsemconv -->

### Metric: `dhcp.server.pool.usage`

This metric tracks address pool utilization (number of addresses currently leased).

<!-- semconv metric.dhcp.server.pool.usage -->
<!-- endsemconv -->

### Metric: `dhcp.server.pool.limit`

This metric reports the total capacity of an address pool.

<!-- semconv metric.dhcp.server.pool.limit -->
<!-- endsemconv -->

### Metric: `dhcp.server.pool.utilization`

This metric reports pool utilization as a ratio (0.0-1.0).

<!-- semconv metric.dhcp.server.pool.utilization -->
<!-- endsemconv -->

### Metric: `dhcp.server.leases.active`

This metric tracks the number of active leases.

<!-- semconv metric.dhcp.server.leases.active -->
<!-- endsemconv -->

## Relay Metrics

### Metric: `dhcp.relay.request.duration`

This metric measures relay processing latency.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.dhcp.relay.request.duration -->
<!-- endsemconv -->

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
