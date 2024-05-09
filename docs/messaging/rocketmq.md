<!--- Hugo front matter used to generate the website version of this page:
linkTitle: RocketMQ
--->

# Semantic Conventions for RocketMQ

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Apache RocketMQ](https://rocketmq.apache.org/) extend and override the [Messaging Semantic Conventions](README.md)
that describe common messaging operations attributes in addition to the Semantic Conventions
described on this page.

`messaging.system` MUST be set to `"rocketmq"`.

## Apache RocketMQ attributes

Specific attributes for Apache RocketMQ are defined below.

<!-- semconv messaging.rocketmq(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`messaging.operation.type`](/docs/attributes-registry/messaging.md) | string | A string identifying the type of the messaging operation. [1] | `publish`; `create`; `receive` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.client_group`](/docs/attributes-registry/messaging.md) | string | Name of the RocketMQ producer/consumer group that is handling the message. The client type is identified by the SpanKind. | `myConsumerGroup` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.namespace`](/docs/attributes-registry/messaging.md) | string | Namespace of RocketMQ resources, resources in different namespaces are individual. | `myNamespace` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`error.type`](/docs/attributes-registry/error.md) | string | Describes a class of error the operation ended with. [2] | `amqp:decode-error`; `KAFKA_STORAGE_ERROR`; `channel-error` | `Conditionally Required` If and only if the messaging operation has failed. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.destination.name`](/docs/attributes-registry/messaging.md) | string | The message destination name [3] | `MyQueue`; `MyTopic` | `Conditionally Required` [4] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.message.delay_time_level`](/docs/attributes-registry/messaging.md) | int | The delay time level for delay message, which determines the message delay time. | `3` | `Conditionally Required` [5] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.message.delivery_timestamp`](/docs/attributes-registry/messaging.md) | int | The timestamp in milliseconds that the delay message is expected to be delivered to consumer. | `1665987217045` | `Conditionally Required` [6] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.message.group`](/docs/attributes-registry/messaging.md) | string | It is essential for FIFO message. Messages that belong to the same message group are always processed one by one within the same consumer group. | `myMessageGroup` | `Conditionally Required` If the message type is FIFO. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.address`](/docs/attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [7] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | `Conditionally Required` If available. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`messaging.message.id`](/docs/attributes-registry/messaging.md) | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` | `Recommended` If span describes operation on a single message. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.operation.name`](/docs/attributes-registry/messaging.md) | string | The system-specific name of the messaging operation. | `ack`; `nack`; `send` | `Recommended` [8] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.consumption_model`](/docs/attributes-registry/messaging.md) | string | Model of message consumption. This only applies to consumer spans. | `clustering`; `broadcasting` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.message.keys`](/docs/attributes-registry/messaging.md) | string[] | Key(s) of message, another way to mark message besides message id. | `keyA`; `keyB` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.message.tag`](/docs/attributes-registry/messaging.md) | string | The secondary classifier of message besides topic. | `tagA` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`messaging.rocketmq.message.type`](/docs/attributes-registry/messaging.md) | string | Type of message. | `normal`; `fifo`; `delay` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`server.port`](/docs/attributes-registry/server.md) | int | Server port number. [9] | `80`; `8080`; `443` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

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

**[5]:** If the message type is delay and delivery timestamp is not specified.

**[6]:** If the message type is delay and delay time level is not specified.

**[7]:** Server domain name of the broker if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.

**[8]:** If the operation is not sufficiently described by `messaging.operation.type`.

**[9]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

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

`messaging.rocketmq.consumption_model` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `clustering` | Clustering consumption model | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `broadcasting` | Broadcasting consumption model | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`messaging.rocketmq.message.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `normal` | Normal message | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fifo` | FIFO message | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `delay` | Delay message | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `transaction` | Transaction message | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

`messaging.client.id` SHOULD be set to the client ID that is automatically generated by the Apache RocketMQ SDK.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
