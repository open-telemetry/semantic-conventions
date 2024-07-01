# Messaging semantic convention stability migration guide

Due to the significant number of modifications and the extensive user base
affected by them, existing messaging instrumentations published by
OpenTelemetry are required to implement a migration plan that will assist users in
transitioning to the stable messaging semantic conventions.

Specifically, when existing messaging instrumentations published by OpenTelemetry are
updated to the stable messaging semantic conventions, they:

- SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN` in
  their existing major version, which accepts:
  - `messaging` - emit the stable messaging conventions, and stop emitting
    the old messaging conventions that the instrumentation emitted previously.
  - `messaging/dup` - emit both the old and the stable messaging conventions,
    allowing for a phased rollout of the stable semantic conventions.
  - The default behavior (in the absence of one of these values) is to continue
    emitting whatever version of the old messaging conventions the
    instrumentation was emitting previously.
- Need to maintain (security patching at a minimum) their existing major version
  for at least six months after it starts emitting both sets of conventions.
- May drop the environment variable in their next major version and emit only
  the stable messaging conventions.

## Summary of changes

This section summarizes the changes made to the messaging semantic conventions
from
[v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/messaging/README.md).
to
[v1.TODO (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.TODO/docs/messaging/README.md).

### Common messaging attributes

#### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.destination.partition.id` |
| `messaging.operation.name` |
| `error.type` |
| `server.port` |
<!-- prettier-ignore-end -->

#### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.system` from string to enum |  |
| `messaging.operation` → `messaging.operation.type` |  |
| `messaging.client_id` → `messaging.client.id` |  |
<!-- prettier-ignore-end -->

### Removed attributes

<!-- prettier-ignore-start -->
| Removed attributes |
| -------------- |
| `network.transport` |
| `network.type` |
| `network.protocol.name` |
| `network.protocol.version` |
<!-- prettier-ignore-end -->

### Kafka attributes

#### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.operation.type` |
| `error.type` |
| `messaging.batch.message_count` |
| `messaging.destination.name` |
| `server.address` |
| `messaging.client.id` |
| `messaging.message.body.size` |
| `messaging.message.id` |
| `messaging.operation.name` |
| `server.port` |
<!-- prettier-ignore-end -->

#### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.kafka.partition` → `messaging.destination.partition.id` |  |

<!-- prettier-ignore-end -->

### RabbitMQ attributes

#### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.rabbitmq.message.delivery_tag` |
| `network.peer.address` |
| `network.peer.port` |
| `messaging.operation.type` |
| `error.type` |
| `messaging.destination.name` |
| `server.address` |
| `messaging.message.body.size` |
| `messaging.message.conversation_id` |
| `messaging.message.id` |
| `messaging.operation.name` |
| `server.port` |
<!-- prettier-ignore-end -->

#### RocketMQ attributes

##### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.operation.type` |
| `error.type` |
| `messaging.batch.message_count` |
| `messaging.destination.name` |
| `server.address` |
| `messaging.client.id` |
| `messaging.message.body.size` |
| `messaging.message.id` |
| `messaging.operation.name` |
| `server.port` |
<!-- prettier-ignore-end -->

### Azure Servicebus

#### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.operation.type` |
| `error.type` |
| `messaging.batch.message_count` |
| `messaging.destination.name` |
| `messaging.servicebus.destination.subscription_name` |
| `messaging.servicebus.disposition_status` |
| `messaging.servicebus.message.delivery_count` |
| `server.address` |
| `messaging.message.conversation_id` |
| `messaging.message.id` |
| `messaging.operation.name` |
| `messaging.servicebus.message.enqueued_time` |
| `messaging.destination.partition.id` |
| `messaging.eventhubs.consumer.group` |
| `messaging.eventhubs.message.enqueued_time` |
<!-- prettier-ignore-end -->

### Azure Event Hubs

#### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.operation.type` |
| `error.type` |
| `messaging.batch.message_count` |
| `messaging.destination.name` |
| `messaging.destination.partition.id` |
| `messaging.eventhubs.consumer.group` |
| `server.address` |
| `messaging.servicebus.message.enqueued_time` |
| `messaging.message.id` |
| `messaging.operation.name` |
| `server.port` |
<!-- prettier-ignore-end -->

### GCP Pubsub attributes

#### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.operation.type` |
| `error.type` |
| `messaging.batch.message_count` |
| `messaging.destination.name` |
| `messaging.gcp_pubsub.message.ordering_key` |
| `server.address` |
| `messaging.gcp_pubsub.message.ack_deadline` |
| `messaging.gcp_pubsub.message.ack_id` |
| `messaging.gcp_pubsub.message.delivery_attempt` |
| `messaging.message.id` |
| `messaging.operation.name` |
| `server.port` |
<!-- prettier-ignore-end -->

## Migrating from a version prior to v1.24.0?

In addition to the changes made to the Messaging semantic conventions
from
[v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/messaging/README.md)
to
[v1.TODO (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.TODO/docs/messaging/README.md),
there are additional changes if you are migrating to v1.TODO from a version prior to v1.24.0.

### Migrating from `<= v1.23.0`

- Initial version of new trace structure [#284](https://github.com/open-telemetry/semantic-conventions/pull/284)
  - Using links to correlate producer to consumers
  - Concept of create spans
  - Model traces for pull and push based scenarios"

### Migrating from `<= v1.22.0`

#### Common messaging attributes

##### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.message.envelope.size` |
| `messaging.destination_publish.name` |
| `messaging.destination_publish.anonymous` |
<!-- prettier-ignore-end -->

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.message.payload_size_bytes` → `messaging.message.body.size` |  |
| `server.socket.address` → `network.peer.address` |  |
| `server.socket.port` → `network.peer.port` |  |
<!-- prettier-ignore-end -->

##### Removed attributes

<!-- prettier-ignore-start -->
| Removed attributes |
| -------------- |
| `server.socket.domain` |
| `messaging.message.payload_compressed_size_bytes` |
<!-- prettier-ignore-end -->

### Migrating from `<= v1.21.0`

#### Common messaging attributes

##### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `network.transport` |
| `network.type` |
<!-- prettier-ignore-end -->

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.consumer.id` →  `messaging.client_id` |  |
| `net.peer.name` →  `server.address` |  |
| `net.protocol.name` →  `network.protocol.name` |  |
| `net.protocol.version` →  `network.protocol.version` |  |
| `net.sock.peer.addr` →  `server.socket.address` |  |
| `net.sock.peer.name` →  `server.socket.domain` |  |
| `net.sock.peer.port` →  `server.socket.port` |  |
<!-- prettier-ignore-end -->

#### Removed attributes

<!-- prettier-ignore-start -->
| Removed attributes |
| -------------- |
| `net.sock.family` |
| `messaging.source.anonymous` |
| `messaging.source.name` |
| `messaging.source.template` |
| `messaging.source.temporary` |
<!-- prettier-ignore-end -->

#### Kafka attributes

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.kafka.client_id` →  `messaging.client_id` |  |
<!-- prettier-ignore-end -->

##### Removed attributes

<!-- prettier-ignore-start -->
| Removed attributes |
| -------------- |
| `messaging.kafka.source.partition` |
<!-- prettier-ignore-end -->

#### RocketMQ attributes

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.rocketmq.client_id` →  `messaging.client_id` |  |
<!-- prettier-ignore-end -->

### Migrating from `<= v1.20.0`

#### Common messaging attributes

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `net.app.protocol.name` →  `net.protocol.name` |  |
| `net.app.protocol.version` →  `net.protocol.version` |  |
<!-- prettier-ignore-end -->

##### Removed attributes

<!-- prettier-ignore-start -->
| Removed attributes |
| -------------- |
| `messaging.destination.kind` |
| `messaging.source.kind` |
<!-- prettier-ignore-end -->

### Migrating from `<= v1.19.0`

No changes

### Migrating from `<= v1.18.0`

No changes

### Migrating from `<= v1.17.0`

#### Common messaging attributes

##### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.batch.message_count` |
| `messaging.destination.anonymous` |
| `messaging.destination.template` |
| `messaging.source.anonymous` |
| `messaging.source.kind` |
| `messaging.source.name` |
| `messaging.source.template` |
| `messaging.source.temporary` |
<!-- prettier-ignore-end -->

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.destination` →  `messaging.destination.name` |  |
| `messaging.destination_kind` →  `messaging.destination.kind` |  |
| `messaging.temp_destination` →  `messaging.destination.temporary` |  |
| `messaging.protocol` →  `net.app.protocol.name` |  |
| `messaging.protocol_version` →  `net.app.protocol.version` |  |
| `messaging.consumer_id` →  `messaging.consumer.id` |  |
| `messaging.message_id` →  `messaging.message.id` |  |
| `messaging.conversation_id` →  `messaging.message.conversation_id` |  |
| `messaging.message_payload_size_bytes` →  `messaging.message.payload_size_bytes` |  |
| `messaging.message_payload_compressed_size_bytes` →  `messaging.message.payload_compressed_size_bytes` |  |
<!-- prettier-ignore-end -->

##### Removed attributes

<!-- prettier-ignore-start -->
| Removed attributes |
| -------------- |
| `messaging.url` |
<!-- prettier-ignore-end -->

#### Kafka attributes

##### New attributes

<!-- prettier-ignore-start -->
| New attributes |
| -------------- |
| `messaging.kafka.source.partition` |
<!-- prettier-ignore-end -->

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.kafka.message_key` →  `messaging.kafka.message.key` |  |
| `messaging.kafka.consumer_group` →  `messaging.kafka.consumer.group` |  |
| `messaging.kafka.partition` →  `messaging.kafka.destination.partition` |  |
| `messaging.kafka.tombstone` →  `messaging.kafka.message.tombstone` |  |
<!-- prettier-ignore-end -->

#### RabbitMQ attributes

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.rabbitmq.routing_key` →  `messaging.rabbitmq.destination.routing_key` |  |
<!-- prettier-ignore-end -->

#### RocketMQ attributes

##### Changed attributes

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| ---------------- | -------- |
| `messaging.rocketmq.message_type` →  `messaging.rocketmq.message.type` |  |
| `messaging.rocketmq.message_tag` →  `messaging.rocketmq.message.tag` |  |
| `messaging.rocketmq.message_keys` →  `messaging.rocketmq.message.keys` |  |
| `messaging.rocketmq.delivery_timestamp` →  `messaging.rocketmq.message.delivery_timestamp` |  |
| `messaging.rocketmq.delay_time_level` →  `messaging.rocketmq.message.delay_time_level` |  |
| `messaging.rocketmq.message_group` →  `messaging.rocketmq.message.group` |  |
<!-- prettier-ignore-end -->
