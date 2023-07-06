<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Kafka
--->

# Semantic Conventions for Kafka

**Status**: [Experimental][DocumentStatus]

<!-- toc -->

- [Span attributes](#span-attributes)
- [Examples](#examples)
  * [Apache Kafka with Quarkus or Spring Boot Example](#apache-kafka-with-quarkus-or-spring-boot-example)
- [Metrics](#metrics)
  * [General Metrics](#general-metrics)
  * [Producer Metrics](#producer-metrics)
  * [Consumer Metrics](#consumer-metrics)

<!-- tocstop -->

The Semantic Conventions for [Apache Kafka](https://kafka.apache.org/) extend and override the [Messaging Semantic Conventions](README.md)
that describe common messaging operations attributes in addition to the Semantic Conventions
described on this page.

`messaging.system` MUST be set to `"kafka"`.

## Span attributes

For Apache Kafka, the following additional attributes are defined:

<!-- semconv messaging.kafka -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.kafka.message.key` | string | Message keys in Kafka are used for grouping alike messages to ensure they're processed on the same partition. They differ from `messaging.message.id` in that they're not unique. If the key is `null`, the attribute MUST NOT be set. [1] | `myKey` | Recommended |
| `messaging.kafka.consumer.group` | string | Name of the Kafka Consumer Group that is handling the message. Only applies to consumers, not producers. | `my-group` | Recommended |
| `messaging.kafka.destination.partition` | int | Partition the message is sent to. | `2` | Recommended |
| `messaging.kafka.message.offset` | int | The offset of a record in the corresponding Kafka partition. | `42` | Recommended |
| `messaging.kafka.message.tombstone` | boolean | A boolean that is true if the message is a tombstone. |  | Conditionally Required: [2] |

**[1]:** If the key type is not string, it's string representation has to be supplied for the attribute. If the key has no unambiguous, canonical string form, don't include its value.

**[2]:** If value is `true`. When missing, the value is assumed to be `false`.
<!-- endsemconv -->

For Apache Kafka producers, [`peer.service`](/docs/general/general-attributes.md#general-remote-service-attributes) SHOULD be set to the name of the broker or service the message will be sent to.
The `service.name` of a Consumer's Resource SHOULD match the `peer.service` of the Producer, when the message is directly passed to another service.
If an intermediary broker is present, `service.name` and `peer.service` will not be the same.

`messaging.client_id` SHOULD be set to the `client-id` of consumers, or to the `client.id` property of producers.

## Examples

### Apache Kafka with Quarkus or Spring Boot Example

Given is a process P, that publishes a message to a topic T1 on Apache Kafka.
One process, CA, receives the message and publishes a new message to a topic T2 that is then received and processed by CB.

Frameworks such as Quarkus and Spring Boot separate processing of a received message from producing subsequent messages out.
For this reason, receiving (Span Rcv1) is the parent of both processing (Span Proc1) and producing a new message (Span Prod2).
The span representing message receiving (Span Rcv1) should not set `messaging.operation` to `receive`,
as it does not only receive the message but also converts the input message to something suitable for the processing operation to consume and creates the output message from the result of processing.

```
Process P:  | Span Prod1 |
--
Process CA:              | Span Rcv1 |
                                | Span Proc1 |
                                  | Span Prod2 |
--
Process CB:                           | Span Rcv2 |
```

| Field or Attribute | Span Prod1 | Span Rcv1 | Span Proc1 | Span Prod2 | Span Rcv2
|-|-|-|-|-|-|
| Span name | `"T1 publish"` | `"T1 receive"` | `"T1 process"` | `"T2 publish"` | `"T2 receive`" |
| Parent |  | Span Prod1 | Span Rcv1 | Span Rcv1 | Span Prod2 |
| Links |  |  | |  |  |
| SpanKind | `PRODUCER` | `CONSUMER` | `CONSUMER` | `PRODUCER` | `CONSUMER` |
| Status | `Ok` | `Ok` | `Ok` | `Ok` | `Ok` |
| `peer.service` | `"myKafka"` |  |  | `"myKafka"` |  |
| `service.name` |  | `"myConsumer1"` | `"myConsumer1"` |  | `"myConsumer2"` |
| `messaging.system` | `"kafka"` | `"kafka"` | `"kafka"` | `"kafka"` | `"kafka"` |
| `messaging.destination.name` | `"T1"` | `"T1"` | `"T1"` | `"T2"` | `"T2"` |
| `messaging.operation` |  |  | `"process"` |  | `"receive"` |
| `messaging.client_id` |  | `"5"` | `"5"` | `"5"` | `"8"` |
| `messaging.kafka.message.key` | `"myKey"` | `"myKey"` | `"myKey"` | `"anotherKey"` | `"anotherKey"` |
| `messaging.kafka.consumer.group` |  | `"my-group"` | `"my-group"` |  | `"another-group"` |
| `messaging.kafka.partition` | `"1"` | `"1"` | `"1"` | `"3"` | `"3"` |
| `messaging.kafka.message.offset` | `"12"` | `"12"` | `"12"` | `"32"` | `"32"` |

## Metrics

This section defines how to apply semantic conventions when collecting Kafka metrics.

### General Metrics

**Description:** General Kafka metrics.

| Name                                         | Instrument    | Value type | Unit   | Unit ([UCUM](/docs/general/metrics-general.md#instrument-units)) | Description    | Attribute Key | Attribute Values |
| ---------------------------------------------| ------------- | ---------- | ------ | -------------------------------------------- | -------------- | ------------- | ---------------- |
| messaging.kafka.messages                     | Counter       | Int64      | messages | `{message}` | The number of messages received by the broker. | | |
| messaging.kafka.requests.failed              | Counter       | Int64      | requests | `{request}` | The number of requests to the broker resulting in a failure. | `type`  | `produce`, `fetch` |
| messaging.kafka.requests.queue               | UpDownCounter | Int64      | requests | `{request}` | The number of requests in the request queue. | | |
| messaging.kafka.network.io                   | Counter       | Int64      | bytes | `By` | The bytes received or sent by the broker. | `state` | `in`, `out` |
| messaging.kafka.purgatory.size               | UpDownCounter | Int64      | requests | `{request}` | The number of requests waiting in the purgatory.  | `type` | `produce`, `fetch` |
| messaging.kafka.partitions.all               | UpDownCounter | Int64      | partitions | `{partition}` | The number of partitions in the broker.  | | |
| messaging.kafka.partitions.offline           | UpDownCounter | Int64      | partitions | `{partition}` | The number of offline partitions. | | |
| messaging.kafka.partitions.under-replicated  | UpDownCounter | Int64      | partition  | `{partition}` | The number of under replicated partitions. | | |
| messaging.kafka.isr.operations               | Counter       | Int64      | operations | `{operation}` | The number of in-sync replica shrink and expand operations. | `operation` | `shrink`, `expand` |
| messaging.kafka.lag_max                      | Gauge         | Int64      | lag max    | `{message}`    | Max lag in messages between follower and leader replicas. | | |
| messaging.kafka.controllers.active           | UpDownCounter | Int64      | controllers | `{controller}` | The number of active controllers in the broker. | | |
| messaging.kafka.leader.elections             | Counter       | Int64      | elections | `{election}` | Leader election rate (increasing values indicates broker failures). | | |
| messaging.kafka.leader.unclean-elections     | Counter       | Int64      | elections | `{election}` | Unclean leader election rate (increasing values indicates broker failures). | | |
| messaging.kafka.brokers                      | UpDownCounter | Int64      | brokers   | `{broker}`   | Number of brokers in the cluster. | | |
| messaging.kafka.topic.partitions             | UpDownCounter | Int64      | partitions | `{partition}` | Number of partitions in topic. | `topic` | The ID (integer) of a topic |
| messaging.kafka.partition.current_offset     | Gauge         | Int64      | partition offset | `{partition offset}` | Current offset of partition of topic. | `topic` | The ID (integer) of a topic |
|                                              |               |            |                  |                      |                                       | `partition` | The number (integer) of the partition |
| messaging.kafka.partition.oldest_offset      | Gauge         | Int64      | partition offset | `{partition offset}` | Oldest offset of partition of topic | `topic` | The ID (integer) of a topic |
|                                              |               |            |                  |                      |                                     | `partition` | The number (integer) of the partition |
| messaging.kafka.partition.replicas.all       | UpDownCounter | Int64      | replicas | `{replica}` | Number of replicas for partition of topic | `topic` | The ID (integer) of a topic |
|                                              |               |            |          |              |                                           | `partition` | The number (integer) of the partition |
| messaging.kafka.partition.replicas.in_sync   | UpDownCounter | Int64      | replicas | `{replica}` | Number of synchronized replicas of partition | `topic` | The ID (integer) of a topic |
|                                              |               |            |          |              |                                              | `partition` | The number (integer) of the partition|

### Producer Metrics

**Description:** Kafka Producer level metrics.

| Name                                          | Instrument    | Value type | Unit   | Unit ([UCUM](/docs/general/metrics-general.md#instrument-units)) | Description    | Attribute Key | Attribute Values |
| --------------------------------------------- | ------------- | ---------- | ------ | -------------------------------------------- | -------------- | ------------- | ---------------- |
| messaging.kafka.producer.outgoing-bytes.rate  | Gauge         | Double     | bytes per second | `By/s` | The average number of outgoing bytes sent per second to all servers. | `client-id` | `client-id` value |
| messaging.kafka.producer.responses.rate       | Gauge         | Double     | responses per second | `{response}/s` | The average number of responses received per second. | `client-id` | `client-id` value |
| messaging.kafka.producer.bytes.rate           | Gauge         | Double     | bytes per second | `By/s` | The average number of bytes sent per second for a specific topic. | `client-id` | `client-id` value |
|                                               |               |            |                  |        |                                                                   | `topic`     | topic name        |
| messaging.kafka.producer.compression-ratio    | Gauge         | Double     | compression ratio | `{compression}` | The average compression ratio of record batches for a specific topic. | `client-id` | `client-id` value |
|                                               |               |            |                   |                 |                                                                       | `topic`     | topic name        |
| messaging.kafka.producer.record-error.rate    | Gauge         | Double     | error rate | `{error}/s` | The average per-second number of record sends that resulted in errors for a specific topic.  | `client-id` | `client-id` value |
|                                               |               |            |            |              |                                                                                              | `topic`     | topic name        |
| messaging.kafka.producer.record-retry.rate    | Gauge         | Double     | retry rate | `{retry}/s` | The average per-second number of retried record sends for a specific topic. | `client-id` | `client-id` value  |
|                                               |               |            |            |               |                                                                             | `topic`     | topic name         |
| messaging.kafka.producer.record-sent.rate     | Gauge         | Double     | records sent rate | `{record_sent}/s` | The average number of records sent per second for a specific topic.  | `client-id` | `client-id` value  |
|                                               |               |            |                   |                    |                                                                      | `topic`     | topic name         |

### Consumer Metrics

**Description:** Kafka Consumer level metrics.

| Name                                          | Instrument    | Value type | Unit   | Unit ([UCUM](/docs/general/metrics-general.md#instrument-units)) | Description    | Attribute Key | Attribute Values |
| --------------------------------------------- | ------------- | ---------- | ------ | -------------------------------------------- | -------------- | ------------- | ---------------- |
| messaging.kafka.consumer.members              | UpDownCounter | Int64      | members | `{member}` | Count of members in the consumer group | `group` | The ID (string) of a consumer group |
| messaging.kafka.consumer.offset               | Gauge         | Int64      | offset | `{offset}` | Current offset of the consumer group at partition of topic | `group` | The ID (string) of a consumer group |
|                                               |               |            |        |            |                                                            | `topic` | The ID (integer) of a topic |
|                                               |               |            |        |            |                                                            | `partition` | The number (integer) of the partition |
| messaging.kafka.consumer.offset_sum           | Gauge         | Int64      | offset sum | `{offset sum}` | Sum of consumer group offset across partitions of topic | `group` | The ID (string) of a consumer group |
|                                               |               |            |            |                |                                                         | `topic` | The ID (integer) of a topic |
| messaging.kafka.consumer.lag                  | Gauge         | Int64      | lag | `{lag}` | Current approximate lag of consumer group at partition of topic | `group` | The ID (string) of a consumer group |
|                                               |               |            |     |         |                                                                 | `topic` | The ID (integer) of a topic |
|                                               |               |            |     |         |                                                                 | `partition` | The number (integer) of the partition |
| messaging.kafka.consumer.lag_sum              | Gauge         | Int64      | lag sum | `{lag sum}` | Current approximate sum of consumer group lag across all partitions of topic | `group` | The ID (string) of a consumer group |
|                                               |               |            |         |             |                                                                              | `topic` | The ID (integer) of a topic |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
