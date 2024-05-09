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
| [`messaging.system`](/docs/attributes-registry/messaging.md) | string | Identifies the messaging product being used as recognized from the client side. [2] | `activemq`; `aws_sqs`; `eventgrid` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [3] | `amqp:decode-error`; `KAFKA_STORAGE_ERROR`; `channel-error` | `Conditionally Required` If and only if the messaging operation has failed. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.batch.message_count`](/docs/attributes-registry/messaging.md) | int | The number of messages sent, received, or processed in the scope of the batching operation. [4] | `0`; `1`; `2` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.anonymous`](/docs/attributes-registry/messaging.md) | boolean | A boolean that is true if the message destination is anonymous (could be unnamed or have auto-generated name). |  | `Conditionally Required` [6] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.name`](/docs/attributes-registry/messaging.md) | string | The message destination name [7] | `MyQueue`; `MyTopic` | `Conditionally Required` [8] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.template`](/docs/attributes-registry/messaging.md) | string | Low cardinality representation of the messaging destination name [9] | `/customers/{customerId}` | `Conditionally Required` [10] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.temporary`](/docs/attributes-registry/messaging.md) | boolean | A boolean that is true if the message destination is temporary and might not exist anymore after messages are processed. |  | `Conditionally Required` [11] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.destination.subscription_name`](/docs/attributes-registry/messaging.md) | string | The name of the subscription in the topic messages are received from. | `mySubscription` | `Conditionally Required` If messages are received from the subscription. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.disposition_status`](/docs/attributes-registry/messaging.md) | string | Describes the [settlement type](https://learn.microsoft.com/azure/service-bus-messaging/message-transfers-locks-settlement#peeklock). | `complete`; `abandon`; `dead_letter` | `Conditionally Required` if and only if `messaging.operation` is `settle`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.message.delivery_count`](/docs/attributes-registry/messaging.md) | int | Number of deliveries that have been attempted for this message. | `2` | `Conditionally Required` [12] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [13] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Conditionally Required` If available. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.client.id`](/docs/attributes-registry/messaging.md) | string | A unique identifier for the client that consumes or produces a message. | `client-5`; `myhost@8742@s8083jm` | `Recommended` If a client id is available | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.partition.id`](/docs/attributes-registry/messaging.md) | string | The identifier of the partition messages are sent to or received from, unique within the `messaging.destination.name`. | `1` | `Recommended` When applicable. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.body.size`](/docs/attributes-registry/messaging.md) | int | The size of the message body in bytes. [14] | `1439` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.conversation_id`](/docs/attributes-registry/messaging.md) | string | The conversation ID identifying the conversation to which the message belongs, represented as a string. Sometimes called "Correlation ID". | `MyConversationId` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.envelope.size`](/docs/attributes-registry/messaging.md) | int | The size of the message body and metadata in bytes. [15] | `2738` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.id`](/docs/attributes-registry/messaging.md) | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.operation.name`](/docs/attributes-registry/messaging.md) | string | The system-specific name of the messaging operation. | `ack`; `nack`; `send` | `Recommended` [16] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.servicebus.message.enqueued_time`](/docs/attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the messaging intermediary node where the operation was performed. [17] | `10.1.2.80`; `/tmp/my.sock` | `Recommended` If applicable for this messaging system. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port of the messaging intermediary node where the operation was performed. | `65123` | `Recommended` if and only if `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [18] | `80`; `8080`; `443` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** If a custom value is used, it MUST be of low cardinality.

**[2]:** The actual messaging system may differ from the one known by the client. For example, when using Kafka client library to communicate with Azure Event Hubs, the `messaging.system` is set to `kafka` based on the instrumentation best knowledge.

**[3]:** The `error.type` SHOULD be predictable, and SHOULD have low cardinality.

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

**[4]:** Instrumentations SHOULD NOT set `messaging.batch.message_count` on spans that operate with a single message. When a messaging client library supports both batch and single-message API for the same operation, instrumentations SHOULD use `messaging.batch.message_count` for batching APIs and SHOULD NOT use it for single-message APIs.

**[5]:** If the span describes an operation on a batch of messages.

**[6]:** If value is `true`. When missing, the value is assumed to be `false`.

**[7]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker doesn't have such notion, the destination name SHOULD uniquely identify the broker.

**[8]:** If span describes operation on a single message or if the value applies to all messages in the batch.

**[9]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[10]:** If available. Instrumentations MUST NOT use `messaging.destination.name` as template unless low-cardinality of destination name is guaranteed.

**[11]:** If value is `true`. When missing, the value is assumed to be `false`.

**[12]:** If delivery count is available and is bigger than 0.

**[13]:** Server domain name of the broker if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.

**[14]:** This can refer to both the compressed or uncompressed body size. If both sizes are known, the uncompressed
body size should be used.

**[15]:** This can refer to both the compressed or uncompressed size. If both sizes are known, the uncompressed
size should be used.

**[16]:** If the operation is not sufficiently described by `messaging.operation.type`.

**[17]:** Semantic conventions for individual messaging systems SHOULD document whether `network.peer.*` attributes are applicable.
Network peer address and port are important when the application interacts with individual intermediary nodes directly,
If a messaging operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.

**[18]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

`messaging.operation.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `publish` | One or more messages are provided for publishing to an intermediary. If a single message is published, the context of the "Publish" span can be used as the creation context and no "Create" span needs to be created. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `create` | A message is created. "Create" spans always refer to a single message and are used to provide a unique creation context for messages in batch publishing scenarios. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `receive` | One or more messages are requested by a consumer. This operation refers to pull-based scenarios, where consumers explicitly call methods of messaging SDKs to receive messages. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process` | One or more messages are delivered to or processed by a consumer. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `settle` | One or more messages are settled. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`messaging.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `activemq` | Apache ActiveMQ | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_sqs` | Amazon Simple Queue Service (SQS) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `eventgrid` | Azure Event Grid | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `eventhubs` | Azure Event Hubs | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `servicebus` | Azure Service Bus | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_pubsub` | Google Cloud Pub/Sub | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `jms` | Java Message Service | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `kafka` | Apache Kafka | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rabbitmq` | RabbitMQ | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rocketmq` | Apache RocketMQ | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

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
| [`messaging.system`](/docs/attributes-registry/messaging.md) | string | Identifies the messaging product being used as recognized from the client side. [2] | `activemq`; `aws_sqs`; `eventgrid` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [3] | `amqp:decode-error`; `KAFKA_STORAGE_ERROR`; `channel-error` | `Conditionally Required` If and only if the messaging operation has failed. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.batch.message_count`](/docs/attributes-registry/messaging.md) | int | The number of messages sent, received, or processed in the scope of the batching operation. [4] | `0`; `1`; `2` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.anonymous`](/docs/attributes-registry/messaging.md) | boolean | A boolean that is true if the message destination is anonymous (could be unnamed or have auto-generated name). |  | `Conditionally Required` [6] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.name`](/docs/attributes-registry/messaging.md) | string | The message destination name [7] | `MyQueue`; `MyTopic` | `Conditionally Required` [8] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.partition.id`](/docs/attributes-registry/messaging.md) | string | String representation of the partition id messages are sent to or received from, unique within the Event Hub. | `1` | `Conditionally Required` If available. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.template`](/docs/attributes-registry/messaging.md) | string | Low cardinality representation of the messaging destination name [9] | `/customers/{customerId}` | `Conditionally Required` [10] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.destination.temporary`](/docs/attributes-registry/messaging.md) | boolean | A boolean that is true if the message destination is temporary and might not exist anymore after messages are processed. |  | `Conditionally Required` [11] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.eventhubs.consumer.group`](/docs/attributes-registry/messaging.md) | string | The name of the consumer group the event consumer is associated with. | `indexer` | `Conditionally Required` If not default ("$Default"). | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [12] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Conditionally Required` If available. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.client.id`](/docs/attributes-registry/messaging.md) | string | A unique identifier for the client that consumes or produces a message. | `client-5`; `myhost@8742@s8083jm` | `Recommended` If a client id is available | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.eventhubs.message.enqueued_time`](/docs/attributes-registry/messaging.md) | int | The UTC epoch seconds at which the message has been accepted and stored in the entity. | `1701393730` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.body.size`](/docs/attributes-registry/messaging.md) | int | The size of the message body in bytes. [13] | `1439` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.conversation_id`](/docs/attributes-registry/messaging.md) | string | The conversation ID identifying the conversation to which the message belongs, represented as a string. Sometimes called "Correlation ID". | `MyConversationId` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.envelope.size`](/docs/attributes-registry/messaging.md) | int | The size of the message body and metadata in bytes. [14] | `2738` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.message.id`](/docs/attributes-registry/messaging.md) | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.operation.name`](/docs/attributes-registry/messaging.md) | string | The system-specific name of the messaging operation. | `ack`; `nack`; `send` | `Recommended` [15] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`network.peer.address`](/docs/attributes-registry/network.md) | string | Peer address of the messaging intermediary node where the operation was performed. [16] | `10.1.2.80`; `/tmp/my.sock` | `Recommended` If applicable for this messaging system. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`network.peer.port`](/docs/attributes-registry/network.md) | int | Peer port of the messaging intermediary node where the operation was performed. | `65123` | `Recommended` if and only if `network.peer.address` is set. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [17] | `80`; `8080`; `443` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** If a custom value is used, it MUST be of low cardinality.

**[2]:** The actual messaging system may differ from the one known by the client. For example, when using Kafka client library to communicate with Azure Event Hubs, the `messaging.system` is set to `kafka` based on the instrumentation best knowledge.

**[3]:** The `error.type` SHOULD be predictable, and SHOULD have low cardinality.

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

**[4]:** Instrumentations SHOULD NOT set `messaging.batch.message_count` on spans that operate with a single message. When a messaging client library supports both batch and single-message API for the same operation, instrumentations SHOULD use `messaging.batch.message_count` for batching APIs and SHOULD NOT use it for single-message APIs.

**[5]:** If the span describes an operation on a batch of messages.

**[6]:** If value is `true`. When missing, the value is assumed to be `false`.

**[7]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker doesn't have such notion, the destination name SHOULD uniquely identify the broker.

**[8]:** If span describes operation on a single message or if the value applies to all messages in the batch.

**[9]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[10]:** If available. Instrumentations MUST NOT use `messaging.destination.name` as template unless low-cardinality of destination name is guaranteed.

**[11]:** If value is `true`. When missing, the value is assumed to be `false`.

**[12]:** Server domain name of the broker if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.

**[13]:** This can refer to both the compressed or uncompressed body size. If both sizes are known, the uncompressed
body size should be used.

**[14]:** This can refer to both the compressed or uncompressed size. If both sizes are known, the uncompressed
size should be used.

**[15]:** If the operation is not sufficiently described by `messaging.operation.type`.

**[16]:** Semantic conventions for individual messaging systems SHOULD document whether `network.peer.*` attributes are applicable.
Network peer address and port are important when the application interacts with individual intermediary nodes directly,
If a messaging operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.

**[17]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

`messaging.operation.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `publish` | One or more messages are provided for publishing to an intermediary. If a single message is published, the context of the "Publish" span can be used as the creation context and no "Create" span needs to be created. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `create` | A message is created. "Create" spans always refer to a single message and are used to provide a unique creation context for messages in batch publishing scenarios. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `receive` | One or more messages are requested by a consumer. This operation refers to pull-based scenarios, where consumers explicitly call methods of messaging SDKs to receive messages. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process` | One or more messages are delivered to or processed by a consumer. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `settle` | One or more messages are settled. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`messaging.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `activemq` | Apache ActiveMQ | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_sqs` | Amazon Simple Queue Service (SQS) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `eventgrid` | Azure Event Grid | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `eventhubs` | Azure Event Hubs | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `servicebus` | Azure Service Bus | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_pubsub` | Google Cloud Pub/Sub | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `jms` | Java Message Service | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `kafka` | Apache Kafka | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rabbitmq` | RabbitMQ | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rocketmq` | Apache RocketMQ | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
