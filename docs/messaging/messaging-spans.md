# Messaging Systems

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Definitions](#definitions)
  * [Message](#message)
  * [Producer](#producer)
  * [Consumer](#consumer)
  * [Intermediary](#intermediary)
  * [Destinations](#destinations)
  * [Message consumption](#message-consumption)
  * [Conversations](#conversations)
  * [Temporary and anonymous destinations](#temporary-and-anonymous-destinations)
- [Conventions](#conventions)
  * [Context propagation](#context-propagation)
  * [Span name](#span-name)
  * [Operation names](#operation-names)
  * [Span kind](#span-kind)
  * [Trace structure](#trace-structure)
    + [Producer spans](#producer-spans)
    + [Consumer spans](#consumer-spans)
- [Messaging attributes](#messaging-attributes)
  * [Attribute namespaces](#attribute-namespaces)
  * [Consumer attributes](#consumer-attributes)
  * [Per-message attributes](#per-message-attributes)
  * [Attributes specific to certain messaging systems](#attributes-specific-to-certain-messaging-systems)
- [Examples](#examples)
  * [Topic with multiple consumers](#topic-with-multiple-consumers)
  * [Batch delivering](#batch-delivering)
- [Semantic Conventions for specific messaging technologies](#semantic-conventions-for-specific-messaging-technologies)

<!-- tocstop -->

> **Warning**
> Existing Messaging instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/messaging.md)
> (or prior):
>
> * SHOULD NOT change the version of the networking conventions that they emit
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking conventions which are also used
>   in Messaging instrumentations). Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The only values defined so far are:
>   * `http` - emit the new, stable networking conventions,
>     and stop emitting the old experimental networking conventions
>     that the instrumentation emitted previously.
>   * `http/dup` - emit both the old and the stable networking conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental networking conventions
>     the instrumentation was emitting previously.
>   * Note: `http/dup` has higher precedence than `http` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version (stable
>   next major version SHOULD NOT be released prior to October 1, 2023).

## Definitions

### Message

Although messaging systems are not as standardized as, e.g., HTTP, it is assumed that the following definitions are applicable to most of them that have similar concepts at all (names borrowed mostly from JMS):

A *message* is an envelope with a potentially empty body.
This envelope may offer the possibility to convey additional metadata, often in key/value form.

A message is sent by a message *producer* to:

* Physically: some message *broker* (which can be e.g., a single server, or a cluster, or a local process reached via IPC). The broker handles the actual delivery, re-delivery, persistence, etc. In some messaging systems the broker may be identical or co-located with (some) message consumers.
With Apache Kafka, the physical broker a message is written to depends on the number of partitions, and which broker is the *leader* of the partition the record is written to.
* Logically: some particular message *destination*.

Messages can be delivered to 0, 1, or multiple consumers depending on the dispatching semantic of the protocol.

### Producer

The "producer" is a specific instance, process or device that creates and
publishes a message. "Publishing" is the process of sending a message or batch
of messages to the intermediary or consumer.

### Consumer

A "consumer" receives the message and acts upon it. It uses the context and
data to execute some logic, which might lead to the occurrence of new events.

The consumer receives, processes, and settles a message. "Receiving" is the
process of obtaining a message from the intermediary, "processing" is the
process of acting on the information a message contains, "settling" is the
process of notifying an intermediary that a message was processed successfully.

### Intermediary

An "intermediary" receives a message to forward it to the next receiver, which
might be another intermediary or a consumer.

### Destinations

A destination represents the entity within a messaging system where
messages are published to and consumed from.

A destination is usually uniquely identified by its name within
the messaging system instance.
Examples of a destination name would be an URL or a simple one-word identifier.

In some use cases, messages are routed within one or multiple brokers. In such
cases, the destination the message was originally published to is different
from the destination it is being consumed from. When information about the
destination where the message was originally published to is available, consumers
can record them under the `destination_publish` namespace.

Typical examples of destinations include Kafka topics, RabbitMQ queues and topics.

### Message consumption

The consumption of a message can happen in multiple steps.
First, the lower-level receiving of a message at a consumer, and then the logical processing of the message.
Often, the waiting for a message is not particularly interesting and hidden away in a framework that only invokes some handler function to process a message once one is received
(in the same way that the listening on a TCP port for an incoming HTTP message is not particularly interesting).

### Conversations

In some messaging systems, a message can receive one or more reply messages that answers a particular other message that was sent earlier. All messages that are grouped together by such a reply-relationship are called a *conversation*.
The grouping usually happens through some sort of "In-Reply-To:" meta information or an explicit *conversation ID* (sometimes called *correlation ID*).
Sometimes a conversation can span multiple message destinations (e.g. initiated via a topic, continued on a temporary one-to-one queue).

### Temporary and anonymous destinations

Some messaging systems support the concept of *temporary destination* (often only temporary queues) that are established just for a particular set of communication partners (often one to one) or conversation.
Often such destinations are also unnamed (anonymous) or have an auto-generated name.

## Conventions

Given these definitions, the remainder of this section describes the semantic conventions for Spans describing interactions with messaging systems.

### Context propagation

A message may traverse many different components and layers in one or more intermediaries
when it is propagated from the producer to the consumer(s). To be able to correlate
consumer traces with producer traces using the existing context propagation mechanisms,
all components must propagate context down the chain.

Messaging systems themselves may trace messages as the messages travels from
producers to consumers. Such tracing would cover the transport layer but would
not help in correlating producers with consumers. To be able to directly
correlate producers with consumers, another context that is propagated with
the message is required.

A message *creation context* allows correlating producers with consumers
of a message and model the dependencies between them,
regardless of the underlying messaging transport mechanism and its instrumentation.

The message creation context is created by the producer and should be propagated
to the consumer(s). Consumer traces cannot be directly correlated with producer
traces if the message creation context is not attached and propagated with the message.

A producer SHOULD attach a message creation context to each message.
If possible, the message creation context SHOULD be attached
in such a way that it cannot be changed by intermediaries.

> This document does not specify the exact mechanisms on how the creation context
> is attached/extracted to/from messages. Future versions of these conventions
> will give clear recommendations, following industry standards including, but not limited to
> [Trace Context: AMQP protocol](https://w3c.github.io/trace-context-amqp/) and
> [Trace Context: MQTT protocol](https://w3c.github.io/trace-context-mqtt/)
> once those standards reach a stable state.

### Span name

The span name SHOULD be set to the message destination name and the operation being performed in the following format:

```
<destination name> <operation name>
```

The destination name SHOULD only be used for the span name if it is known to be of low cardinality (cf. [general span name guidelines](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/trace/api.md#span)).
This can be assumed if it is statically derived from application code or configuration.
Wherever possible, the real destination names after resolving logical or aliased names SHOULD be used.
If the destination name is dynamic, such as a [conversation ID](#conversations) or a value obtained from a `Reply-To` header, it SHOULD NOT be used for the span name.
In these cases, an artificial destination name that best expresses the destination, or a generic, static fallback like `"(anonymous)"` for [anonymous destinations](#temporary-and-anonymous-destinations) SHOULD be used instead.

The values allowed for `<operation name>` are defined in the section [Operation names](#operation-names) below.
If the format above is used, the operation name MUST match the `messaging.operation` attribute defined for message consumer spans below.

Examples:

* `shop.orders publish`
* `shop.orders receive`
* `shop.orders process`
* `print_jobs publish`
* `topic with spaces process`
* `AuthenticationRequest-Conversations process`
* `(anonymous) publish` (`(anonymous)` being a stable identifier for an unnamed destination)

### Operation names

The following operations related to messages are defined for these semantic conventions:

| Operation name | Description |
| -------------- | ----------- |
| `publish`      | One or more messages are provided for publishing to an intermediary. If a single message is published, the context of the "Publish" span can be used as the creation context and no "Create" span needs to be created. |
| `create`       | A message is created. "Create" spans always refer to a single message and are used to provide a unique creation context for messages in batch publishing scenarios. |
| `receive`      | One or more messages are requested by a consumer. This operation refers to pull-based scenarios, where consumers explicitly call methods of messaging SDKs to receive messages. |
| `deliver`      | One or more messages are passed to a consumer. This operation refers to push-based scenarios, where consumer register callbacks which get called by messaging SDKs. |

### Span kind

[Span kinds](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/api.md#spankind)
SHOULD be set according to the following table, based on the operation a span describes.

| Operation name | Span kind|
|----------------|-------------|
| `publish`      | `PRODUCER` if the context of the "Publish" span is used as creation context. |
| `create`       | `PRODUCER` |
| `receive`      | `CONSUMER` |
| `deliver`      | `CONSUMER` |

For cases not covered by the table above, the span kind should be set according
to the [generic specification about span kinds](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/api.md#spankind),
e. g. it should be set to CLIENT for the "Publish" span if its context is not
used as creation context and if the "Publish" span models a synchronous call to
the intermediary.

Setting span kinds according to this table ensures that span links between
consumers and producers always exist between a PRODUCER span on the producer
side and a CONSUMER span on the consumer side. This allows analysis tools to
interpret linked traces without the need for additional semantic hints.

### Trace structure

#### Producer spans

"Publish" spans SHOULD be created for operations of providing messages for
sending or publishing to an intermediary. A single "Publish" span can account
for a single message, or for multiple messages (in the case of providing
messages in batches). "Create" spans MAY be created. A single "Create" span
SHOULD account only for a single message. "Create" spans SHOULD either be
children or links of the related "Publish" span.

If a "Create" span exists for a message, its context SHOULD be injected into
the message. If no "Create" span exists and no custom creation context is
injected into the message, the context of the related "Publish" span SHOULD be
injected into the message.

#### Consumer spans

"Deliver" spans SHOULD be created for operations of passing messages to the
application when those operations are not initiated by the application code
(push-based scenarios).

"Receive" spans SHOULD be created for operations of passing messages to the
application when those operations are initiated by the application code
(pull-based scenarios).

"Deliver" or "Receive" spans MUST NOT be created for messages that are
pre-fetched or cached by messaging libraries or SDKs until they are forwarded
to the caller.

A single "Deliver" or "Receive" span can account for a single message, for a
batch of messages, or for no message at all (if it is signalled that no
messages were received). For each message it accounts for, the "Deliver" or
"Receive" span SHOULD link to the message's creation context.

## Messaging attributes

<!-- semconv messaging -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.batch.message_count` | int | The number of messages sent, received, or processed in the scope of the batching operation. [1] | `0`; `1`; `2` | Conditionally Required: [2] |
| `messaging.client_id` | string | A unique identifier for the client that consumes or produces a message. | `client-5`; `myhost@8742@s8083jm` | Recommended: If a client id is available |
| `messaging.destination.anonymous` | boolean | A boolean that is true if the message destination is anonymous (could be unnamed or have auto-generated name). |  | Conditionally Required: [3] |
| `messaging.destination.name` | string | The message destination name [4] | `MyQueue`; `MyTopic` | Conditionally Required: [5] |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [6] | `/customers/{customerId}` | Conditionally Required: [7] |
| `messaging.destination.temporary` | boolean | A boolean that is true if the message destination is temporary and might not exist anymore after messages are processed. |  | Conditionally Required: [8] |
| `messaging.message.body.size` | int | The size of the message body in bytes. [9] | `1439` | Recommended: [10] |
| `messaging.message.conversation_id` | string | The [conversation ID](#conversations) identifying the conversation to which the message belongs, represented as a string. Sometimes called "Correlation ID". | `MyConversationId` | Recommended: [11] |
| `messaging.message.envelope.size` | int | The size of the message body and metadata in bytes. [12] | `2738` | Recommended: [13] |
| `messaging.message.id` | string | A value used by the messaging system as an identifier for the message, represented as a string. | `452a7c7c7c7048c2f887f61572b18fc2` | Recommended: [14] |
| `messaging.operation` | string | A string identifying the kind of messaging operation as defined in the [Operation names](#operation-names) section above. [15] | `publish` | Required |
| `messaging.system` | string | A string identifying the messaging system. | `kafka`; `rabbitmq`; `rocketmq`; `activemq`; `AmazonSQS` | Required |
| [`network.protocol.name`](../general/attributes.md) | string | [OSI application layer](https://osi-model.com/application-layer/) or non-OSI equivalent. [16] | `amqp`; `mqtt` | Recommended |
| [`network.protocol.version`](../general/attributes.md) | string | Version of the protocol specified in `network.protocol.name`. [17] | `3.1.1` | Recommended |
| [`network.transport`](../general/attributes.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://en.wikipedia.org/wiki/Inter-process_communication). [18] | `tcp`; `udp` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI network layer](https://osi-model.com/network-layer/) or non-OSI equivalent. [19] | `ipv4`; `ipv6` | Recommended |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [20] | `example.com` | Conditionally Required: If available. |
| [`server.socket.address`](../general/attributes.md) | string | Server address of the socket connection - IP address or Unix domain socket name. [21] | `10.5.3.2` | Recommended: If different than `server.address`. |
| [`server.socket.domain`](../general/attributes.md) | string | Immediate server peer's domain name if available without reverse DNS lookup [22] | `proxy.example.com` | Recommended: [23] |
| [`server.socket.port`](../general/attributes.md) | int | Server port number of the socket connection. [24] | `16456` | Recommended: If different than `server.port`. |

**[1]:** Instrumentations SHOULD NOT set `messaging.batch.message_count` on spans that operate with a single message. When a messaging client library supports both batch and single-message API for the same operation, instrumentations SHOULD use `messaging.batch.message_count` for batching APIs and SHOULD NOT use it for single-message APIs.

**[2]:** If the span describes an operation on a batch of messages.

**[3]:** If value is `true`. When missing, the value is assumed to be `false`.

**[4]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker does not have such notion, the destination name SHOULD uniquely identify the broker.

**[5]:** If span describes operation on a single message or if the value applies to all messages in the batch.

**[6]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[7]:** If available. Instrumentations MUST NOT use `messaging.destination.name` as template unless low-cardinality of destination name is guaranteed.

**[8]:** If value is `true`. When missing, the value is assumed to be `false`.

**[9]:** This can refer to both the compressed or uncompressed body size. If both sizes are known, the uncompressed
body size should be used.

**[10]:** Only if span represents operation on a single message.

**[11]:** Only if span represents operation on a single message.

**[12]:** This can refer to both the compressed or uncompressed size. If both sizes are known, the uncompressed
size should be used.

**[13]:** Only if span represents operation on a single message.

**[14]:** Only for spans that represent an operation on a single message.

**[15]:** If a custom value is used, it MUST be of low cardinality.

**[16]:** The value SHOULD be normalized to lowercase.

**[17]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[18]:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport, for example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[19]:** The value SHOULD be normalized to lowercase.

**[20]:** This should be the IP/hostname of the broker (or other network-level peer) this specific message is sent to/received from.

**[21]:** When observed from the client side, this SHOULD represent the immediate server peer address.
When observed from the server side, this SHOULD represent the physical server address.

**[22]:** Typically observed from the client side, and represents a proxy or other intermediary domain name.

**[23]:** If different than `server.address` and if `server.socket.address` is set.

**[24]:** When observed from the client side, this SHOULD represent the immediate server peer port.
When observed from the server side, this SHOULD represent the physical server port.

`messaging.operation` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `publish` | publish |
| `receive` | receive |
| `process` | process |
<!-- endsemconv -->

Additionally `server.port` from the [network attributes][] is recommended.
Furthermore, it is strongly recommended to add the [`network.transport`][] attribute and follow its guidelines, especially for in-process queueing systems (like [Hangfire][], for example).
These attributes should be set to the broker to which the message is sent/from which it is received.

### Attribute namespaces

- `messaging.message`: Contains attributes that describe individual messages
- `messaging.destination`: Contains attributes that describe the logical entity messages are published to. See [Destinations](#destinations) for more details
- `messaging.destination_publish`: Contains attributes that describe the logical entity messages were originally published to. See [Destinations](#destinations) for more details
- `messaging.batch`: Contains attributes that describe batch operations
- `messaging.consumer`: Contains attributes that describe application instance that consumes a message. See [consumer](#consumer) for more details

Communication with broker is described with general [network attributes].

Messaging system-specific attributes MUST be defined in the corresponding `messaging.{system}` namespace
as described in [Attributes specific to certain messaging systems](#attributes-specific-to-certain-messaging-systems).

[network attributes]: /docs/general/attributes.md#server-and-client-attributes
[`network.transport`]: /docs/general/attributes.md#network-attributes
[Hangfire]: https://www.hangfire.io/

### Consumer attributes

The following additional attributes describe message consumer operations.

Since messages could be routed by brokers, the destination messages are published
to may not match with the destination they are consumed from.

If information about the original destination is available on the consumer,
consumer instrumentations SHOULD populate the attributes
under the namespace `messaging.destination_publish.*`

<!-- semconv messaging.destination_publish -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.destination_publish.anonymous` | boolean | A boolean that is true if the publish message destination is anonymous (could be unnamed or have auto-generated name). |  | Recommended |
| `messaging.destination_publish.name` | string | The name of the original destination the message was published to [1] | `MyQueue`; `MyTopic` | Recommended |

**[1]:** The name SHOULD uniquely identify a specific queue, topic, or other entity within the broker. If
the broker does not have such notion, the original destination name SHOULD uniquely identify the broker.
<!-- endsemconv -->

### Per-message attributes

All messaging operations (`publish`, `receive`, `process`, or others not covered by this specification) can describe both single and/or batch of messages.
Attributes in the `messaging.message` or `messaging.{system}.message` namespace describe individual messages. For single-message operations they SHOULD be set on corresponding span.

For batch operations, per-message attributes are usually different and cannot be set on the corresponding span. In such cases the attributes SHOULD be set on links. See [Batch Delivering](#batch-delivering) for more information on correlation using links.

Some messaging systems (e.g., Kafka, Azure EventGrid) allow publishing a single batch of messages to different topics. In such cases, the attributes in `messaging.destination` MAY be
set on links. Instrumentations MAY set destination attributes on the span if all messages in the batch share the same destination.

### Attributes specific to certain messaging systems

All attributes that are specific for a messaging system SHOULD be populated in `messaging.{system}` namespace. Attributes that describe a message, a destination, a consumer, or a batch of messages SHOULD be populated under the corresponding namespace:

* `messaging.{system}.message.*`: Describes attributes for individual messages
* `messaging.{system}.destination.*`: Describes the destination a message (or a batch) are published to and received from respectively. The combination of attributes in these namespaces should uniquely identify the entity and include properties significant for this messaging system. For example, Kafka instrumentations should include partition identifier.
* `messaging.{system}.consumer.*`: Describes message consumer properties
* `messaging.{system}.batch.*`: Describes message batch properties

## Examples

### Topic with multiple consumers

Given is a publisher that publishes a message to a topic "T" on Kafka, and two consumers which both get the message delivered.

```mermaid
flowchart LR;
  subgraph PRODUCER
  direction TB
  P[Span Publish A]
  end
  subgraph CONSUMER1
  direction TB
  R1[Span Deliver A 1]
  end
  subgraph CONSUMER2
  direction TB
  R2[Span Deliver A 2]
  end
  P-. link .-R1;
  P-. link .-R2;

  classDef normal fill:green
  class P,R1,R2 normal
  linkStyle 0,1 color:green,stroke:green
```

| Field or Attribute | Span Publish A | Span Deliver A 1| Span Deliver A 2 |
|-|-|-|-|
| Span name | `T publish` | `T deliver` | `T deliver` |
| Parent | | | |
| Links |  | `T publish` | `T publish` |
| SpanKind | `PRODUCER` | `CONSUMER` | `CONSUMER` |
| Status | `Ok` | `Ok` | `Ok` |
| `server.address` | `"ms"` | `"ms"` | `"ms"` |
| `server.port` | `1234` | `1234` | `1234` |
| `messaging.system` | `"kafka"` | `"kafka"` | `"kafka"` |
| `messaging.destination.name` | `"T"` | `"T"` | `"T"` |
| `messaging.operation` | `"publish"` | `"deliver"` | `"deliver"` |
| `messaging.message.id` | `"a"` | `"a"`| `"a"` |

### Batch delivering

Given is a publisher that publishes two messages to a queue "Q" on RabbitMQ, and a consumer which receives both messages in one batch.

```mermaid
flowchart LR;
  subgraph PRODUCER
  direction TB
  PA[Span Publish A]
  PB[Span Publish B]
  end
  subgraph CONSUMER1
  direction TB
  D1[Span Receive A B]
  end
  PA-. link .-D1;
  PB-. link .-D1;

  classDef normal fill:green
  class PA,PB,D1 normal
  linkStyle 0,1 color:green,stroke:green
```

| Field or Attribute | Span Publish A | Span Publish B | Span Receive A B |
|-|-|-|-|
| Span name | `Q publish` | `Q publish` | `Q receive` |
| Parent |  |  |  |
| Links |  |  | Span Publish A, Span Publish B |
| Link attributes |  |  | Span Publish A: `messaging.message.id`: `"a1"`  |
|                 |  |  | Span Publish B: `messaging.message.id`: `"a2"`  |
| SpanKind | `PRODUCER` | `PRODUCER` | `CONSUMER` |
| Status | `Ok` | `Ok` | `Ok` |
| `server.address` | `"ms"` | `"ms"` | `"ms"` |
| `server.port` | `1234` | `1234` | `1234` |
| `messaging.system` | `"rabbitmq"` | `"rabbitmq"` | `"rabbitmq"` |
| `messaging.destination.name` | `"Q"` | `"Q"` | `"Q"` |
| `messaging.operation` | `"publish"` | `"publish"` | `"receive"` |
| `messaging.message.id` | `"a1"` | `"a2"` | |
| `messaging.batch.message_count` |  |  | 2 |

## Semantic Conventions for specific messaging technologies

More specific Semantic Conventions are defined for the following messaging technologies:

* [Kafka](kafka.md): Semantic Conventions for *Apache Kafka*.
* [RabbitMQ](rabbitmq.md): Semantic Conventions for *RabbitMQ*.
* [RocketMQ](rocketmq.md): Semantic Conventions for *Apache RocketMQ*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
