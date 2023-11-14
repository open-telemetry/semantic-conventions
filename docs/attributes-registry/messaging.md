<!--- Hugo front matter used to generate the website version of this page:
--->

# Messaging

## Messaging Attributes

<!-- semconv registry.messaging(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `messaging.batch.message_count` | int | The number of messages sent, received, or processed in the scope of the batching operation. [1] | `0`; `1`; `2` |
| `messaging.client_id` | string | A unique identifier for the client that consumes or produces a message. | `client-5`; `myhost@8742@s8083jm` |
| `messaging.destination.anonymous` | boolean | A boolean that is true if the message destination is anonymous (could be unnamed or have auto-generated name). |  |
| `messaging.destination.name` | string | The message destination name [2] | `MyQueue`; `MyTopic` |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [3] | `/customers/{customerId}` |
| `messaging.destination.temporary` | boolean | A boolean that is true if the message destination is temporary and might not exist anymore after messages are processed. |  |
| `messaging.destination_publish.anonymous` | boolean | A boolean that is true if the publish message destination is anonymous (could be unnamed or have auto-generated name). |  |
| `messaging.destination_publish.name` | string | The name of the original destination the message was published to [4] | `MyQueue`; `MyTopic` |
| `messaging.kafka.consumer.group` | string | Name of the Kafka Consumer Group that is handling the message. Only applies to consumers, not producers. | `my-group` |
| `messaging.kafka.destination.partition` | int | Partition the message is sent to. | `2` |
| `messaging.kafka.message.key` | string | Message keys in Kafka are used for grouping alike messages to ensure they're processed on the same partition. They differ from `messaging.message.id` in that they're not unique. If the key is `null`, the attribute MUST NOT be set. [5] | `myKey` |
| `messaging.kafka.message.offset` | int | The offset of a record in the corresponding Kafka partition. | `42` |
| `messaging.kafka.message.tombstone` | boolean | A boolean that is true if the message is a tombstone. |  |
| `messaging.message.body.size` | int | The size of the message body in bytes. [6] | `1439` |
| `messaging.message.conversation_id` | string | The conversation ID identifying the conversation to which the message belongs, represented as a string. Sometimes called "Correlation ID". | `MyConversationId` |
| `messaging.message.envelope.size` | int | The size of the message body and metadata in bytes. [7] | `2738` |
| `messaging.message.id` | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` |
| `messaging.operation` | string | A string identifying the kind of messaging operation. [8] | `publish` |
| `messaging.rabbitmq.destination.routing_key` | string | RabbitMQ message routing key. | `myKey` |
| `messaging.rocketmq.client_group` | string | Name of the RocketMQ producer/consumer group that is handling the message. The client type is identified by the SpanKind. | `myConsumerGroup` |
| `messaging.rocketmq.consumption_model` | string | Model of message consumption. This only applies to consumer spans. | `clustering` |
| `messaging.rocketmq.message.delay_time_level` | int | The delay time level for delay message, which determines the message delay time. | `3` |
| `messaging.rocketmq.message.delivery_timestamp` | int | The timestamp in milliseconds that the delay message is expected to be delivered to consumer. | `1665987217045` |
| `messaging.rocketmq.message.group` | string | It is essential for FIFO message. Messages that belong to the same message group are always processed one by one within the same consumer group. | `myMessageGroup` |
| `messaging.rocketmq.message.keys` | string[] | Key(s) of message, another way to mark message besides message id. | `[keyA, keyB]` |
| `messaging.rocketmq.message.tag` | string | The secondary classifier of message besides topic. | `tagA` |
| `messaging.rocketmq.message.type` | string | Type of message. | `normal` |
| `messaging.rocketmq.namespace` | string | Namespace of RocketMQ resources, resources in different namespaces are individual. | `myNamespace` |
| `messaging.system` | string | An identifier for the messaging system being used. See below for a list of well-known identifiers. | `activemq` |

**[1]:** Instrumentations SHOULD NOT set `messaging.batch.message_count` on spans that operate with a single message. When a messaging client library supports both batch and single-message API for the same operation, instrumentations SHOULD use `messaging.batch.message_count` for batching APIs and SHOULD NOT use it for single-message APIs.

**[2]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker doesn't have such notion, the destination name SHOULD uniquely identify the broker.

**[3]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[4]:** The name SHOULD uniquely identify a specific queue, topic, or other entity within the broker. If
the broker doesn't have such notion, the original destination name SHOULD uniquely identify the broker.

**[5]:** If the key type is not string, it's string representation has to be supplied for the attribute. If the key has no unambiguous, canonical string form, don't include its value.

**[6]:** This can refer to both the compressed or uncompressed body size. If both sizes are known, the uncompressed
body size should be used.

**[7]:** This can refer to both the compressed or uncompressed size. If both sizes are known, the uncompressed
size should be used.

**[8]:** If a custom value is used, it MUST be of low cardinality.

`messaging.operation` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `publish` | One or more messages are provided for publishing to an intermediary. If a single message is published, the context of the "Publish" span can be used as the creation context and no "Create" span needs to be created. |
| `create` | A message is created. "Create" spans always refer to a single message and are used to provide a unique creation context for messages in batch publishing scenarios. |
| `receive` | One or more messages are requested by a consumer. This operation refers to pull-based scenarios, where consumers explicitly call methods of messaging SDKs to receive messages. |
| `deliver` | One or more messages are passed to a consumer. This operation refers to push-based scenarios, where consumer register callbacks which get called by messaging SDKs. |

`messaging.rocketmq.consumption_model` MUST be one of the following:

| Value  | Description |
|---|---|
| `clustering` | Clustering consumption model |
| `broadcasting` | Broadcasting consumption model |

`messaging.rocketmq.message.type` MUST be one of the following:

| Value  | Description |
|---|---|
| `normal` | Normal message |
| `fifo` | FIFO message |
| `delay` | Delay message |
| `transaction` | Transaction message |

`messaging.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `activemq` | Apache ActiveMQ |
| `amazon_sqs` | Amazon Simple Queue Service (SQS) |
| `gcp_pubsub` | Google Cloud Pub/Sub |
| `jms` | Java Message Service |
| `kafka` | Apache Kafka |
| `rabbitmq` | RabbitMQ |
| `rocketmq` | Apache RocketMQ |
<!-- endsemconv -->
