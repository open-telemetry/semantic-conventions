<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Google Cloud Pub/Sub
--->

# Semantic Conventions for Azure Messaging systems

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Azure Service Bus](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) and [Azure Event Hubs](https://learn.microsoft.com/azure/event-hubs/event-hubs-about) extend and override the [Messaging Semantic Conventions](README.md) that describe common messaging operations attributes in addition to the Semantic Conventions described on this page.

## Azure Service Bus

`messaging.system` MUST be set to `"servicebus"`.

### Span attributes

The following additional attributes are defined:
<!-- semconv messaging.servicebus -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`messaging.servicebus.destination.subscription_name`](../attributes-registry/messaging.md) | string | The name of the subscription in the topic messages are received from. | `mySubscription` | `Conditionally Required` If messages are received from the subscription. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.disposition_status`](../attributes-registry/messaging.md) | string | Describes the [settlement type](https://learn.microsoft.com/azure/service-bus-messaging/message-transfers-locks-settlement#peeklock). | `complete` | `Conditionally Required` if and only if `messaging.operation` is `settle`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.message.delivery_count`](../attributes-registry/messaging.md) | int | Number of deliveries that have been attempted for this message. | `2` | `Conditionally Required` [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.message.enqueued_time`](../attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If delivery count is available and is bigger than 0.
<!-- endsemconv -->

## Azure Event Hubs

`messaging.system` MUST be set to `"eventhubs"`.

### Span attributes

The following additional attributes are defined:
<!-- semconv messaging.eventhubs -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`messaging.destination.partition.id`](../attributes-registry/messaging.md) | string | String representation of the partition id messages are sent to or received from, unique within the Event Hub. | `1` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.eventhubs.consumer.group`](../attributes-registry/messaging.md) | string | The name of the consumer group the event consumer is associated with. | `indexer` | `Conditionally Required` If not default ("$Default"). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.eventhubs.message.enqueued_time`](../attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
