<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Google Cloud Pub/Sub
--->

# Semantic Conventions for Azure Messaging systems

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Azure Service Bus](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) and [Azure Event Hubs](https://learn.microsoft.com/azure/event-hubs/event-hubs-about) extend and override the [Messaging Semantic Conventions](README.md) that describe common messaging operations attributes in addition to the Semantic Conventions described on this page.

## Azure Service Bus

`messaging.system` MUST be set to `"servicebus"`.

### Span names

The span name SHOULD follow [general messaging span name pattern](../messaging/azure-messaging.md): it SHOULD start with the messaging destination name (Event Hubs queue or topic name) and
contain a low-cardinality name of an operation span describes:

- Spans for `deliver` operation SHOULD follow `<destination name> process` pattern (matching terminology used in Azure client libraries)
- Spans for `settle` operation SHOULD follow `<destination name> <disposition status>` pattern. Disposition status MUST match the value of `messaging.servicebus.disposition_status` attribute.
  For example, `my-queue complete` or `my-queue abandon`
- Spans for `create`, `receive`, and `publish` operations SHOULD follow general `<destination name> <operation name>` pattern

### Span attributes

The following additional attributes are defined:
<!-- semconv messaging.servicebus -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`messaging.servicebus.destination.subscription_name`](../attributes-registry/messaging.md) | string | The name of the subscription in the topic messages are received from. | `mySubscription` | Conditionally Required: If messages are received from the subscription. |
| [`messaging.servicebus.disposition_status`](../attributes-registry/messaging.md) | string | Describes [settlement type](https://learn.microsoft.com/azure/service-bus-messaging/message-transfers-locks-settlement#peeklock). | `complete` | Conditionally Required: if and only if `messaging.operation` is `settle`. |
| [`messaging.servicebus.message.delivery_count`](../attributes-registry/messaging.md) | int | Number of deliveries that have been attempted for this message. | `2` | Conditionally Required: [1] |
| [`messaging.servicebus.message.enqueued_time`](../attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | Recommended |

**[1]:** If delivery count is available and is bigger than 0.
<!-- endsemconv -->

## Azure Event Hubs

`messaging.system` MUST be set to `"eventhubs"`.

### Span names

The span name SHOULD follow [general messaging span name pattern](../messaging/azure-messaging.md): it SHOULD start with the messaging destination name (Event Hubs namespace) and
contain a low-cardinality name of an operation span describes:

- Spans for `deliver` operation SHOULD follow  `<destination name> process` pattern (matching terminology used in Azure client libraries)
- Spans for `settle` operation SHOULD follow  `<destination name> checkpoint` (matching Event Hubs terminology)
- Spans for `create`, `receive`, and `publish` operations SHOULD follow general `<destination name> <operation name>` pattern

### Span attributes

The following additional attributes are defined:
<!-- semconv messaging.eventhubs -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`messaging.eventhubs.consumer.group`](../attributes-registry/messaging.md) | string | The name of the consumer group the event consumer is associated with. | `indexer` | Conditionally Required: If not default ("$Default"). |
| [`messaging.eventhubs.destination.partition.id`](../attributes-registry/messaging.md) | string | The identifier of the partition messages are sent to or received from, unique to the Event Hub which contains it. | `1` | Conditionally Required: If available. |
| [`messaging.eventhubs.message.enqueued_time`](../attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | Recommended |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
