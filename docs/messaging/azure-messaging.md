<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Azure Messaging Systems
--->

# Semantic Conventions for Azure Messaging Systems

**Status**: [Experimental][DocumentStatus]

<!-- toc -->

- [Azure Service Bus](#azure-service-bus)
  * [Service Bus Attributes](#service-bus-attributes)
  * [Service Bus Metrics](#service-bus-metrics)
    + [Metric: `messaging.publish.duration`](#metric-messagingpublishduration)
    + [Metric: `messaging.publish.messages`](#metric-messagingpublishmessages)
    + [Metric: `messaging.deliver.duration`](#metric-messagingdeliverduration)
    + [Metric: `messaging.receive.duration`](#metric-messagingreceiveduration)
    + [Metric: `messaging.receive.messages`](#metric-messagingreceivemessages)
- [Azure Event Hubs](#azure-event-hubs)
  * [Event Hubs Attributes](#event-hubs-attributes)
  * [Event Hubs Metrics](#event-hubs-metrics)
    + [Metric: `messaging.publish.duration`](#metric-messagingpublishduration-1)
    + [Metric: `messaging.publish.messages`](#metric-messagingpublishmessages-1)
    + [Metric: `messaging.deliver.duration`](#metric-messagingdeliverduration-1)
    + [Metric: `messaging.deliver.messages`](#metric-messagingdelivermessages)
    + [Metric: `messaging.receive.duration`](#metric-messagingreceiveduration-1)
    + [Metric: `messaging.receive.messages`](#metric-messagingreceivemessages-1)

<!-- tocstop -->

The Semantic Conventions for [Azure Service Bus](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) and [Azure Event Hubs](https://learn.microsoft.com/azure/event-hubs/event-hubs-about) extend and override the [Messaging Semantic Conventions](README.md) that describe common messaging operations attributes in addition to the Semantic Conventions described on this page.

## Azure Service Bus

`messaging.system` MUST be set to `"servicebus"`.

### Service Bus Attributes

The following attributes are defined or reused:
<!-- semconv messaging.servicebus -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`error.type`](../attributes-registry/error.md) | string | Describes a class of error the operation ended with. [1] | `amqp:resource-limit-exceeded`; `com.microsoft:message-lock-lost`; `503`; `System.OperationCanceledException` | Conditionally Required: [2] |
| [`messaging.batch.message_count`](../attributes-registry/messaging.md) | int | The number of messages sent, received, or processed in the scope of the batching operation. [3] | `0`; `1`; `2` | Conditionally Required: [4] |
| [`messaging.destination.name`](../attributes-registry/messaging.md) | string | The message destination name [5] | `MyQueue`; `MyTopic` | Conditionally Required: [6] |
| [`messaging.message.conversation_id`](../attributes-registry/messaging.md) | string | Service Bus [Session Id](https://learn.microsoft.com/azure/service-bus-messaging/message-sessions) | `MyConversationId` | Recommended |
| [`messaging.message.id`](../attributes-registry/messaging.md) | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` | Recommended |
| [`messaging.operation`](../attributes-registry/messaging.md) | string | A string identifying the kind of messaging operation. [7] | `publish` | Required |
| [`messaging.servicebus.destination.subscription_name`](../attributes-registry/messaging.md) | string | The name of the subscription in the topic messages are received from. | `mySubscription` | Conditionally Required: If messages are received from the subscription. |
| [`messaging.servicebus.message.delivery_count`](../attributes-registry/messaging.md) | int | Number of deliveries that have been attempted for this message. | `2` | Conditionally Required: [8] |
| [`messaging.servicebus.message.enqueued_time`](../attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | Recommended |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [9] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Conditionally Required: If available. |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [10] | `5672` | Conditionally Required: If not default (`5672`). |

**[1]:** When available, SHOULD match [AMQP error condition](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-transport-v1.0-os.html#type-error) or string representation of a [management response status code](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-amqp-request-response). Otherwise SHOULD match full name of the exception type.

**[2]:** If and only if the messaging operation has failed.

**[3]:** Instrumentations SHOULD NOT set `messaging.batch.message_count` on spans that operate with a single message. When a messaging client library supports both batch and single-message API for the same operation, instrumentations SHOULD use `messaging.batch.message_count` for batching APIs and SHOULD NOT use it for single-message APIs.

**[4]:** If the span describes an operation on a batch of messages.

**[5]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker doesn't have such notion, the destination name SHOULD uniquely identify the broker.

**[6]:** If span describes operation on a single message or if the value applies to all messages in the batch.

**[7]:** If a custom value is used, it MUST be of low cardinality.

**[8]:** If delivery count is available and is bigger than 0.

**[9]:** This should be the IP/hostname of the broker (or other network-level peer) this specific message is sent to/received from.

**[10]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.
<!-- endsemconv -->

### Service Bus Metrics

#### Metric: `messaging.publish.duration`

Measures time it takes to publish message or a batch of messages to Azure Service Bus including all retries.

This metric is [required][MetricRequired]

This metric follows the common [messaging.publish.duration](./messaging-metrics.md#metric-messagingpublishduration) definition.

#### Metric: `messaging.publish.messages`

Measures the number of published messages.

This metric is [required][MetricRequired]

This metric follows the common [messaging.publish.messages](./messaging-metrics.md#metric-messagingpublishmessages) definition.

#### Metric: `messaging.deliver.duration`

Measures duration of processor client callback that processes a message.

This metric is [required][MetricRequired] when processor client is used by the application.

This metric follows the common [messaging.deliver.duration](./messaging-metrics.md#metric-messagingdeliverduration) definition.

**Notes:**

- Azure Service Bus client libraries don't support batch processing, therefore the count of processed messages can be derived from the `messaging.deliver.duration` metric and is not reported.
- The following attributes (with corresponding [requirement levels](#service-bus-attributes)) are defined in addition to generic attributes for this metric:
  * `messaging.servicebus.destination.subscription_name`

#### Metric: `messaging.receive.duration`

Measures duration of receiver client call that receives (or awaits) messages.

This metric is [required][MetricRequired] when receiver client is used by the application directly and when receive method is called to get a message/batch of messages.
When receiver client is called once to get unbounded stream of messages (for example when using [ServiceBusReceiverAsyncClient](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/servicebus/azure-messaging-servicebus/src/samples/java/com/azure/messaging/servicebus/ReceiveMessageAsyncSample.java)), this metric MUST NOT be reported.

This metric follows the common [messaging.receive.duration](./messaging-metrics.md#metric-messagingdeliverduration) definition.

**Notes:**

- The following attributes (with corresponding [requirement levels](#service-bus-attributes)) are defined in addition to generic attributes for this metric:
  * `messaging.servicebus.destination.subscription_name`

#### Metric: `messaging.receive.messages`

Measures the number of received messages.

This metric is [required][MetricRequired] when receiver client is used by the application directly.

This metric follows the common [messaging.receive.messages](./messaging-metrics.md#metric-messagingreceivemessages) definition.

**Notes:**

- The following attributes (with corresponding [requirement levels](#service-bus-attributes)) are defined in addition to generic attributes for this metric:
  * `messaging.servicebus.destination.subscription_name`

## Azure Event Hubs

`messaging.system` MUST be set to `"eventhubs"`.

### Event Hubs Attributes

The following attributes are defined or overridden:
<!-- semconv messaging.eventhubs -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`error.type`](../attributes-registry/error.md) | string | Describes a class of error the operation ended with. [1] | `amqp:resource-limit-exceeded`; `com.microsoft:server-busy`; `503`; `System.OperationCanceledException` | Conditionally Required: [2] |
| [`messaging.batch.message_count`](../attributes-registry/messaging.md) | int | The number of messages sent, received, or processed in the scope of the batching operation. [3] | `0`; `1`; `2` | Conditionally Required: [4] |
| [`messaging.destination.name`](../attributes-registry/messaging.md) | string | The message destination name [5] | `MyQueue`; `MyTopic` | Conditionally Required: [6] |
| [`messaging.eventhubs.consumer.group`](../attributes-registry/messaging.md) | string | The name of the consumer group the event consumer is associated with. | `indexer` | Conditionally Required: If not default ("$Default"). |
| [`messaging.eventhubs.destination.partition.id`](../attributes-registry/messaging.md) | string | The identifier of the partition messages are sent to or received from, unique to the Event Hub which contains it. | `1` | Conditionally Required: If available. |
| [`messaging.eventhubs.message.enqueued_time`](../attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | Recommended |
| [`messaging.message.id`](../attributes-registry/messaging.md) | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` | Recommended |
| [`messaging.operation`](../attributes-registry/messaging.md) | string | A string identifying the kind of messaging operation. [7] | `publish` | Required |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [8] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Conditionally Required: If available. |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [9] | `5672` | Conditionally Required: If not default (`5672`). |

**[1]:** When available, SHOULD match [AMQP error condition](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-transport-v1.0-os.html#type-error) or string representation of a [management response status code](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-amqp-request-response). Otherwise SHOULD match full name of the exception type.

**[2]:** If and only if the messaging operation has failed.

**[3]:** Instrumentations SHOULD NOT set `messaging.batch.message_count` on spans that operate with a single message. When a messaging client library supports both batch and single-message API for the same operation, instrumentations SHOULD use `messaging.batch.message_count` for batching APIs and SHOULD NOT use it for single-message APIs.

**[4]:** If the span describes an operation on a batch of messages.

**[5]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker doesn't have such notion, the destination name SHOULD uniquely identify the broker.

**[6]:** If span describes operation on a single message or if the value applies to all messages in the batch.

**[7]:** If a custom value is used, it MUST be of low cardinality.

**[8]:** This should be the IP/hostname of the broker (or other network-level peer) this specific message is sent to/received from.

**[9]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.
<!-- endsemconv -->

### Event Hubs Metrics

#### Metric: `messaging.publish.duration`

Measures time it takes to publish event or a batch of events to Azure Event Hubs including all retries.

This metric is [required][MetricRequired]

This metric follows the common [messaging.publish.duration](./messaging-metrics.md#metric-messagingpublishduration) definition.

#### Metric: `messaging.publish.messages`

Measures the number of published events.

This metric is [required][MetricRequired]

This metric follows the common [messaging.publish.messages](./messaging-metrics.md#metric-messagingpublishmessages) definition.

**Notes:**

- The following attributes (with corresponding [requirement levels](#event-hubs-attributes)) are defined in addition to generic attributes for this metric:
  * `messaging.eventhubs.destination.partition.id`

#### Metric: `messaging.deliver.duration`

Measures duration of processor client callback that processes an event or a batch of events.

This metric is [required][MetricRequired] when processor client is used by the application.

This metric follows the common [messaging.deliver.duration](./messaging-metrics.md#metric-messagingdeliverduration) definition.

**Notes:**

- The following attributes (with corresponding [requirement levels](#event-hubs-attributes)) are defined in addition to generic attributes for this metric:
  * `messaging.eventhubs.destination.partition.id`
  * `messaging.eventhubs.consumer.group`

#### Metric: `messaging.deliver.messages`

This metric is [required][MetricRequired] when processor client is used by the application.

This metric follows the common [messaging.deliver.messages](./messaging-metrics.md#metric-messagingdelivermessages) definition.

**Notes:**

- The following attributes (with corresponding [requirement levels](#event-hubs-attributes)) are defined in addition to generic attributes for this metric:
  * `messaging.eventhubs.destination.partition.id`
  * `messaging.eventhubs.consumer.group`

#### Metric: `messaging.receive.duration`

Measures duration of consumer client call that receives (or awaits) events.

This metric is [required][MetricRequired] when consumer client is used by the application directly and when receive method is called to get an event/batch of event.
When consumer client is called once to get unbounded stream of events (for example when using [EventHubConsumerAsyncClient](https://github.com/Azure/azure-sdk-for-java/blob/4587bbec4ceab1e669842155baa8546680134d61/sdk/eventhubs/azure-messaging-eventhubs/README.md#consume-events-with-eventhubconsumerasyncclient)), this metric MUST NOT be reported.

This metric follows the common [messaging.receive.duration](./messaging-metrics.md#metric-messagingdeliverduration) definition.

**Notes:**

- The following attributes (with corresponding [requirement levels](#event-hubs-attributes)) are defined in addition to generic attributes for this metric:
  * `messaging.eventhubs.destination.partition.id`
  * `messaging.eventhubs.consumer.group`

#### Metric: `messaging.receive.messages`

Measures the number of received events.

This metric is [required][MetricRequired] when receiver client is used by the application directly.

This metric follows the common [messaging.receive.messages](./messaging-metrics.md#metric-messagingreceivemessages) definition.

**Notes:**

- The following attributes (with corresponding [requirement levels](#event-hubs-attributes)) are defined in addition to generic attributes for this metric:
  * `messaging.eventhubs.destination.partition.id`
  * `messaging.eventhubs.consumer.group`

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/metrics/metric-requirement-level.md#required
