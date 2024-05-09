<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Azure Messaging
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
| [`messaging.operation.type`](/docs/attributes-registry/messaging.md) | string | A string identifying the type of the messaging operation. [1] | `publish`; `create`; `receive` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [2] | `amqp:decode-error`; `KAFKA_STORAGE_ERROR`; `channel-error` | `Conditionally Required` If and only if the messaging operation has failed. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.destination.name`](/docs/attributes-registry/messaging.md) | string | The message destination name [3] | `MyQueue`; `MyTopic` | `Conditionally Required` [4] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.destination.subscription_name`](/docs/attributes-registry/messaging.md) | string | The name of the subscription in the topic messages are received from. | `mySubscription` | `Conditionally Required` If messages are received from the subscription. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.disposition_status`](/docs/attributes-registry/messaging.md) | string | Describes the [settlement type](https://learn.microsoft.com/azure/service-bus-messaging/message-transfers-locks-settlement#peeklock). | `complete`; `abandon`; `dead_letter` | `Conditionally Required` if and only if `messaging.operation` is `settle`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.message.delivery_count`](/docs/attributes-registry/messaging.md) | int | Number of deliveries that have been attempted for this message. | `2` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [6] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Conditionally Required` If available. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.message.conversation_id`](/docs/attributes-registry/messaging.md) | string | Message [correlation Id](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messages-payloads#message-routing-and-correlation) property. | `MyConversationId` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.id`](/docs/attributes-registry/messaging.md) | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` | `Recommended` If span describes operation on a single message. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.operation.name`](/docs/attributes-registry/messaging.md) | string | The system-specific name of the messaging operation. | `ack`; `nack`; `send` | `Recommended` [7] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.message.enqueued_time`](/docs/attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [8] | `80`; `8080`; `443` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** If a custom value is used, it MUST be of low cardinality.

**[2]:** The `error.type` SHOULD be predictable, and SHOULD have low cardinality.

When `error.type` is set to a type (e.g., an exception type), its
canonical class name identifying the type within the artifact SHOULD be used.

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

**[3]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker doesn't have such notion, the destination name SHOULD uniquely identify the broker.

**[4]:** If span describes operation on a single message or if the value applies to all messages in the batch.

**[5]:** If delivery count is available and is bigger than 0.

**[6]:** Server domain name of the broker if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.

**[7]:** If the operation is not sufficiently described by `messaging.operation.type`.

**[8]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

`messaging.operation.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `publish` | One or more messages are provided for publishing to an intermediary. If a single message is published, the context of the "Publish" span can be used as the creation context and no "Create" span needs to be created. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `create` | A message is created. "Create" spans always refer to a single message and are used to provide a unique creation context for messages in batch publishing scenarios. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `receive` | One or more messages are requested by a consumer. This operation refers to pull-based scenarios, where consumers explicitly call methods of messaging SDKs to receive messages. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process` | One or more messages are delivered to or processed by a consumer. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `settle` | One or more messages are settled. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`messaging.servicebus.disposition_status` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `complete` | Message is completed | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `abandon` | Message is abandoned | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `dead_letter` | Message is sent to dead letter queue | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `defer` | Message is deferred | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Azure Event Hubs

`messaging.system` MUST be set to `"eventhubs"`.

### Span attributes

The following additional attributes are defined:
<!-- semconv messaging.eventhubs -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`messaging.operation.type`](/docs/attributes-registry/messaging.md) | string | A string identifying the type of the messaging operation. [1] | `publish`; `create`; `receive` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [2] | `amqp:decode-error`; `KAFKA_STORAGE_ERROR`; `channel-error` | `Conditionally Required` If and only if the messaging operation has failed. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.destination.name`](/docs/attributes-registry/messaging.md) | string | The message destination name [3] | `MyQueue`; `MyTopic` | `Conditionally Required` [4] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.partition.id`](/docs/attributes-registry/messaging.md) | string | String representation of the partition id messages are sent to or received from, unique within the Event Hub. | `1` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.eventhubs.consumer.group`](/docs/attributes-registry/messaging.md) | string | The name of the consumer group the event consumer is associated with. | `indexer` | `Conditionally Required` If not default ("$Default"). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [5] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Conditionally Required` If available. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.eventhubs.message.enqueued_time`](/docs/attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.id`](/docs/attributes-registry/messaging.md) | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` | `Recommended` If span describes operation on a single message. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.operation.name`](/docs/attributes-registry/messaging.md) | string | The system-specific name of the messaging operation. | `ack`; `nack`; `send` | `Recommended` [6] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [7] | `80`; `8080`; `443` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** If a custom value is used, it MUST be of low cardinality.

**[2]:** The `error.type` SHOULD be predictable, and SHOULD have low cardinality.

When `error.type` is set to a type (e.g., an exception type), its
canonical class name identifying the type within the artifact SHOULD be used.

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

**[3]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker doesn't have such notion, the destination name SHOULD uniquely identify the broker.

**[4]:** If span describes operation on a single message or if the value applies to all messages in the batch.

**[5]:** Server domain name of the broker if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.

**[6]:** If the operation is not sufficiently described by `messaging.operation.type`.

**[7]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

`messaging.operation.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `publish` | One or more messages are provided for publishing to an intermediary. If a single message is published, the context of the "Publish" span can be used as the creation context and no "Create" span needs to be created. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `create` | A message is created. "Create" spans always refer to a single message and are used to provide a unique creation context for messages in batch publishing scenarios. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `receive` | One or more messages are requested by a consumer. This operation refers to pull-based scenarios, where consumers explicitly call methods of messaging SDKs to receive messages. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process` | One or more messages are delivered to or processed by a consumer. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `settle` | One or more messages are settled. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
