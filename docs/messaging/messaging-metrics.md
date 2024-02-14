# Semantic Conventions for Messaging Metrics

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Common attributes](#common-attributes)
- [Producer metrics](#producer-metrics)
  * [Metric: `messaging.publish.duration`](#metric-messagingpublishduration)
  * [Metric: `messaging.publish.messages`](#metric-messagingpublishmessages)
- [Consumer metrics](#consumer-metrics)
  * [Metric: `messaging.receive.duration`](#metric-messagingreceiveduration)
  * [Metric: `messaging.receive.messages`](#metric-messagingreceivemessages)
  * [Metric: `messaging.process.duration`](#metric-messagingprocessduration)
  * [Metric: `messaging.process.messages`](#metric-messagingprocessmessages)

<!-- tocstop -->

> **Warning**
> Existing messaging instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/messaging/messaging-metrics.md)
> (or prior) SHOULD NOT change the version of the messaging conventions that they emit
> until a transition plan to the (future) stable semantic conventions has been published.
> Conventions include, but are not limited to, attributes, metric and span names, and unit of measure.

## Common attributes

All messaging metrics share the same set of attributes:

<!-- semconv metric.messaging.attributes(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`error.type`](../attributes-registry/error.md) | string | Describes a class of error the operation ended with. [1] | `amqp:decode-error`; `KAFKA_STORAGE_ERROR`; `channel-error` | Conditionally Required: [2] |
| [`messaging.destination.name`](../attributes-registry/messaging.md) | string | The message destination name [3] | `MyQueue`; `MyTopic` | Conditionally Required: [4] |
| [`messaging.destination.template`](../attributes-registry/messaging.md) | string | Low cardinality representation of the messaging destination name [5] | `/customers/{customerId}` | Conditionally Required: if available. |
| [`messaging.system`](../attributes-registry/messaging.md) | string | An identifier for the messaging system being used. See below for a list of well-known identifiers. | `activemq` | Required |
| [`network.protocol.name`](../attributes-registry/network.md) | string | [OSI application layer](https://osi-model.com/application-layer/) or non-OSI equivalent. [6] | `amqp`; `mqtt` | Conditionally Required: [7] |
| [`network.protocol.version`](../attributes-registry/network.md) | string | Version of the protocol specified in `network.protocol.name`. [8] | `3.1.1` | Recommended |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [9] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Conditionally Required: If available. |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [10] | `80`; `8080`; `443` | Recommended |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low.
Telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

If a specific domain defines its own set of error identifiers (such as HTTP or gRPC status codes),
it's RECOMMENDED to:

* Use a domain-specific attribute
* Set `error.type` to capture all errors, regardless of whether they are defined within the domain-specific set or not.

**[2]:** If and only if the messaging operation has failed.

**[3]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker doesn't have such notion, the destination name SHOULD uniquely identify the broker.

**[4]:** if and only if `messaging.destination.name` is known to have low cardinality. Otherwise, `messaging.destination.template` MAY be populated.

**[5]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[6]:** The value SHOULD be normalized to lowercase.

**[7]:** Only for messaging systems and frameworks that support more than one protocol.

**[8]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[9]:** This should be the IP/hostname of the broker (or other network-level peer) this specific message is sent to/received from.

**[10]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. |

`messaging.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `activemq` | Apache ActiveMQ |
| `aws_sqs` | Amazon Simple Queue Service (SQS) |
| `eventgrid` | Azure Event Grid |
| `eventhubs` | Azure Event Hubs |
| `servicebus` | Azure Service Bus |
| `gcp_pubsub` | Google Cloud Pub/Sub |
| `jms` | Java Message Service |
| `kafka` | Apache Kafka |
| `rabbitmq` | RabbitMQ |
| `rocketmq` | Apache RocketMQ |
<!-- endsemconv -->

## Producer metrics

### Metric: `messaging.publish.duration`

This metric is [required][MetricRequired].

When this metric is reported alongside a messaging publish span, the metric value SHOULD be the same as the corresponding span duration.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advice)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.messaging.publish.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.publish.duration` | Histogram | `s` | Measures the duration of publish operation. |
<!-- endsemconv -->

### Metric: `messaging.publish.messages`

This metric is [required][MetricRequired] when the messaging system supports batch publishing. It's [opt-in][MetricOptIn] when the messaging system does not support batch publishing, since the message count can be derived from the `messaging.publish.duration` histogram.

<!-- semconv metric.messaging.publish.messages(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.publish.messages` | Counter | `{message}` | Measures the number of published messages. |
<!-- endsemconv -->

> The need to report `messaging.publish.messages` depends on the messaging system capabilities and not application scenarios or client library limitations. For example, RabbitMQ does not support batch publishing and corresponding instrumentations don't need to report `messaging.publish.messages`. Kafka supports both, single and batch publishing, and instrumentations MUST report `messaging.publish.messages` counter regardless of application scenarios or APIs available in the client library.

## Consumer metrics

### Metric: `messaging.receive.duration`

This metric is [required][MetricRequired] for operations that are initiated by the application code (pull-based).

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advice)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

When this metric is reported alongside a messaging receive span, the metric value SHOULD be the same as the corresponding span duration.

<!-- semconv metric.messaging.receive.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.receive.duration` | Histogram | `s` | Measures the duration of receive operation. |
<!-- endsemconv -->

### Metric: `messaging.receive.messages`

This metric is [required][MetricRequired] for batch receive operations. It's [opt-in][MetricOptIn] when the messaging system does not support batch receive since the message count can be derived from the `messaging.receive.duration` histogram.

_Note: The need to report `messaging.receive.messages` depends on the messaging system capabilities and not application scenarios or client library limitations._

<!-- semconv metric.messaging.receive.messages(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.receive.messages` | Counter | `{message}` | Measures the number of received messages. |
<!-- endsemconv -->

### Metric: `messaging.process.duration`

This metric is [required][MetricRequired] for operations are not initiated by the application code (push-based deliver), and [recommended][MetricRecommended] for processing operations instrumented for pull-based scenarios.

When this metric is reported alongside a messaging process span, the metric value SHOULD be the same as the corresponding span duration.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advice)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.messaging.process.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.process.duration` | Histogram | `s` | Measures the duration of process operation. |
<!-- endsemconv -->

### Metric: `messaging.process.messages`

This metric is [required][MetricRequired] for batch process operations, and [recommended][MetricRecommended] for batch processing operations instrumented for pull-based scenarios. It's [opt-in][MetricOptIn] when the messaging system does not support batch processing since the message count can be derived from the `messaging.process.duration` histogram.

_Note: The need to report `messaging.process.messages` depends on the messaging system capabilities and not application scenarios or client library limitations._

<!-- semconv metric.messaging.process.messages(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.process.messages` | Counter | `{message}` | Measures the number of processed messages. |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/metrics/metric-requirement-level.md#required
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/metrics/metric-requirement-level.md#recommended
[MetricOptIn]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/metrics/metric-requirement-level.md#opt-in
