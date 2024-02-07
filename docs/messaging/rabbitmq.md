<!--- Hugo front matter used to generate the website version of this page:
linkTitle: RabbitMQ
--->

# Semantic Conventions for RabbitMQ

**Status**: [Experimental][DocumentStatus]

<!-- toc -->

- [Attributes](#attributes)
- [Metrics](#metrics)
  * [Metric: `messaging.publish.duration`](#metric-messagingpublishduration)
  * [Metric: `messaging.deliver.duration`](#metric-messagingdeliverduration)
  * [Metric: `messaging.receive.duration`](#metric-messagingreceiveduration)

<!-- tocstop -->

The Semantic Conventions for [RabbitMQ](https://www.rabbitmq.com/) extend and override the [Messaging Semantic Conventions](README.md)
that describe common messaging operations attributes in addition to the Semantic Conventions
described on this page.

`messaging.system` MUST be set to `"rabbitmq"`.

## Attributes

In RabbitMQ, the destination is defined by an *exchange* and a *routing key*.
`messaging.destination.name` MUST be set to the name of the exchange. This will be an empty string if the default exchange is used.

<!-- semconv messaging.rabbitmq(full,tag=tech-specific-rabbitmq) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`messaging.rabbitmq.destination.routing_key`](../attributes-registry/messaging.md) | string | RabbitMQ message routing key. | `myKey` | Conditionally Required: If not empty. |
<!-- endsemconv -->

## Metrics

### Metric: `messaging.publish.duration`

Measures time it takes to publish a message or a batch of messages to RabbitMQ including all retries.

This metric is [required][MetricRequired]

This metric follows the common [messaging.publish.duration](./messaging-metrics.md#metric-messagingpublishduration) definition.

**Notes:**

- `messaging.publish.messages` metric is not reported: RabbitMQ doesn't support batch publish, therefore the count of published messages can be derived from `messaging.publish.duration` metric.
- In addition to generic attributes defined for the metric, RabbitMQ instrumentations SHOULD report the following attributes (according to their [requirement levels](#attributes)):
  * `messaging.rabbitmq.destination.routing_key`

### Metric: `messaging.deliver.duration`

Measures duration of delivery callback that consumes a message.

This metric is [required][MetricRequired] when consume API is used.

This metric follows the common [messaging.receive.duration](./messaging-metrics.md#metric-messagingdeliverduration) definition.

**Notes:**

- `messaging.deliver.messages` metric is not reported: RabbitMQ doesn't support batch consumption, therefore the count of delivered messages can be derived from `messaging.deliver.duration` metric.

### Metric: `messaging.receive.duration`

Measures duration of pull call.

This metric is [required][MetricRequired] if pull API is used.

This metric follows the common [messaging.receive.duration](./messaging-metrics.md#metric-messagingdeliverduration) definition.

**Notes:**

- `messaging.receive.messages` metric is not reported: RabbitMQ doesn't support batch receive, therefore the count of received messages can be derived from `messaging.receive.duration` metric.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/metrics/metric-requirement-level.md#required
