<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Messaging migration
--->

# Messaging semantic convention stability migration

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

<!-- toc -->

- [Summary of changes](#summary-of-changes)
  - [Migrating from v1.26.0](#migrating-from-v1260)
  - [Migrating from v1.25.0](#migrating-from-v1250)
  - [Migrating from v1.24.0](#migrating-from-v1240)
  - [Migrating from v1.23.0 and v1.22.0](#migrating-from-v1230-and-v1220)
  - [Migrating from v1.21.0](#migrating-from-v1210)
  - [Migrating from v1.20.0](#migrating-from-v1200)
  - [Migrating from v1.19.0 and v1.18.0 v1.17.0](#migrating-from-v1190-and-v1180-v1170)
  - [Migrating from v1.16](#migrating-from-v116)

<!-- tocstop -->

## Summary of changes

This section summarizes the changes made to the messaging semantic conventions
from a range of versions. Each starting version shows all the changes required
to bring the conventions to
[v1.TODO (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.TODO/docs/messaging/README.md).

### Migrating from v1.26.0

<!-- prettier-ignore-start -->
| New attributes ![new](https://img.shields.io/badge/new-green?style=flat) |
| -------------- |
| `messaging.consumer.group.name` |
| `messaging.destination.subscription.name` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Old ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| --- | --- |
| `messaging.eventhubs.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.message.offset` | `messaging.kafka.offset` |
| `messaging.rocketmq.client_group` | `messaging.consumer.group.name` |
| `messaging.servicebus.destination.subscription_name` | `messaging.destination.subscription.name` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Removed attributes ![removed](https://img.shields.io/badge/removed-red?style=flat) |
| ------------------ |
| `messaging.destination_publish.anonymous` |
| `messaging.destination_publish.name` |
<!-- prettier-ignore-end -->

### Migrating from v1.25.0

<!-- prettier-ignore-start -->
| New attributes ![new](https://img.shields.io/badge/new-green?style=flat) |
| -------------- |
| `messaging.consumer.group.name` |
| `messaging.destination.subscription.name` |
| `messaging.gcp_pubsub.message.ack_deadline` |
| `messaging.gcp_pubsub.message.ack_id` |
| `messaging.gcp_pubsub.message.delivery_attempt` |
| `messaging.operation.name` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Old ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| --- | --- |
| `messaging.client_id` | `messaging.client.id` |
| `messaging.eventhubs.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.message.offset` | `messaging.kafka.offset` |
| `messaging.operation` | `messaging.operation.type` |
| `messaging.rocketmq.client_group` | `messaging.consumer.group.name` |
| `messaging.servicebus.destination.subscription_name` | `messaging.destination.subscription.name` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Removed attributes ![removed](https://img.shields.io/badge/removed-red?style=flat) |
| ------------------ |
| `messaging.destination_publish.anonymous` |
| `messaging.destination_publish.name` |
<!-- prettier-ignore-end -->

### Migrating from v1.24.0

<!-- prettier-ignore-start -->
| New attributes ![new](https://img.shields.io/badge/new-green?style=flat) |
| -------------- |
| `messaging.consumer.group.name` |
| `messaging.destination.partition.id` |
| `messaging.destination.subscription.name` |
| `messaging.eventhubs.message.enqueued_time` |
| `messaging.gcp_pubsub.message.ack_deadline` |
| `messaging.gcp_pubsub.message.ack_id` |
| `messaging.gcp_pubsub.message.delivery_attempt` |
| `messaging.operation.name` |
| `messaging.rabbitmq.message.delivery_tag` |
| `messaging.servicebus.disposition_status` |
| `messaging.servicebus.message.delivery_count` |
| `messaging.servicebus.message.enqueued_time` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Old ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| --- | --- |
| `messaging.client_id` | `messaging.client.id` |
| `messaging.kafka.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.destination.partition` | `messaging.destination.partition.id` |
| `messaging.kafka.message.offset` | `messaging.kafka.offset` |
| `messaging.operation` | `messaging.operation.type` |
| `messaging.rocketmq.client_group` | `messaging.consumer.group.name` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Removed attributes ![removed](https://img.shields.io/badge/removed-red?style=flat) |
| ------------------ |
| `messaging.destination_publish.anonymous` |
| `messaging.destination_publish.name` |
| `network.protocol.name` |
| `network.protocol.version` |
| `network.transport` |
| `network.type` |
<!-- prettier-ignore-end -->

### Migrating from v1.23.0 and v1.22.0

<!-- prettier-ignore-start -->
| New attributes ![new](https://img.shields.io/badge/new-green?style=flat) |
| -------------- |
| `error.type` |
| `messaging.consumer.group.name` |
| `messaging.destination.partition.id` |
| `messaging.destination.subscription.name` |
| `messaging.eventhubs.message.enqueued_time` |
| `messaging.gcp_pubsub.message.ack_deadline` |
| `messaging.gcp_pubsub.message.ack_id` |
| `messaging.gcp_pubsub.message.delivery_attempt` |
| `messaging.gcp_pubsub.message.ordering_key` |
| `messaging.operation.name` |
| `messaging.rabbitmq.message.delivery_tag` |
| `messaging.servicebus.disposition_status` |
| `messaging.servicebus.message.delivery_count` |
| `messaging.servicebus.message.enqueued_time` |
| `server.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Old ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| --- | --- |
| `messaging.client_id` | `messaging.client.id` |
| `messaging.kafka.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.destination.partition` | `messaging.destination.partition.id` |
| `messaging.kafka.message.offset` | `messaging.kafka.offset` |
| `messaging.operation` | `messaging.operation.type` |
| `messaging.rocketmq.client_group` | `messaging.consumer.group.name` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Removed attributes ![removed](https://img.shields.io/badge/removed-red?style=flat) |
| ------------------ |
| `messaging.destination_publish.anonymous` |
| `messaging.destination_publish.name` |
| `network.protocol.name` |
| `network.protocol.version` |
| `network.transport` |
| `network.type` |
<!-- prettier-ignore-end -->

### Migrating from v1.21.0

<!-- prettier-ignore-start -->
| New attributes ![new](https://img.shields.io/badge/new-green?style=flat) |
| -------------- |
| `error.type` |
| `messaging.consumer.group.name` |
| `messaging.destination.partition.id` |
| `messaging.destination.subscription.name` |
| `messaging.eventhubs.message.enqueued_time` |
| `messaging.gcp_pubsub.message.ack_deadline` |
| `messaging.gcp_pubsub.message.ack_id` |
| `messaging.gcp_pubsub.message.delivery_attempt` |
| `messaging.gcp_pubsub.message.ordering_key` |
| `messaging.message.envelope.size` |
| `messaging.operation.name` |
| `messaging.rabbitmq.message.delivery_tag` |
| `messaging.servicebus.disposition_status` |
| `messaging.servicebus.message.delivery_count` |
| `messaging.servicebus.message.enqueued_time` |
| `server.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Old ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| --- | --- |
| `messaging.client_id` | `messaging.client.id` |
| `messaging.kafka.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.destination.partition` | `messaging.destination.partition.id` |
| `messaging.kafka.message.offset` | `messaging.kafka.offset` |
| `messaging.message.payload_compressed_size_bytes` | `messaging.message.body.size` |
| `messaging.message.payload_size_bytes` | `messaging.message.envelope.size` |
| `messaging.operation` | `messaging.operation.type` |
| `messaging.rocketmq.client_group` | `messaging.consumer.group.name` |
| `server.socket.address` | `network.peer.address` |
| `server.socket.port` | `network.peer.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Removed attributes ![removed](https://img.shields.io/badge/removed-red?style=flat) |
| ------------------ |
| `network.protocol.name` |
| `network.protocol.version` |
| `network.transport` |
| `network.type` |
| `server.socket.domain` |
<!-- prettier-ignore-end -->

### Migrating from v1.20.0

<!-- prettier-ignore-start -->
| New attributes ![new](https://img.shields.io/badge/new-green?style=flat) |
| -------------- |
| `error.type` |
| `messaging.consumer.group.name` |
| `messaging.destination.partition.id` |
| `messaging.destination.subscription.name` |
| `messaging.eventhubs.message.enqueued_time` |
| `messaging.gcp_pubsub.message.ack_deadline` |
| `messaging.gcp_pubsub.message.ack_id` |
| `messaging.gcp_pubsub.message.delivery_attempt` |
| `messaging.gcp_pubsub.message.ordering_key` |
| `messaging.message.envelope.size` |
| `messaging.operation.name` |
| `messaging.rabbitmq.message.delivery_tag` |
| `messaging.servicebus.disposition_status` |
| `messaging.servicebus.message.delivery_count` |
| `messaging.servicebus.message.enqueued_time` |
| `server.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Old ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| --- | --- |
| `messaging.client_id` | `messaging.client.id` |
| `messaging.consumer.id` | `messaging.client.id` |
| `messaging.kafka.client_id` | `messaging.client.id` |
| `messaging.kafka.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.destination.partition` | `messaging.destination.partition.id` |
| `messaging.kafka.message.offset` | `messaging.kafka.offset` |
| `messaging.message.payload_compressed_size_bytes` | `messaging.message.body.size` |
| `messaging.message.payload_size_bytes` | `messaging.message.envelope.size` |
| `messaging.operation` | `messaging.operation.type` |
| `messaging.rocketmq.client_group` | `messaging.consumer.group.name` |
| `messaging.rocketmq.client_id` | `messaging.client.id` |
| `net.peer.name` | `server.address` |
| `net.sock.peer.addr` | `network.peer.address` |
| `net.sock.peer.port` | `network.peer.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Removed attributes ![removed](https://img.shields.io/badge/removed-red?style=flat) |
| ------------------ |
| `messaging.kafka.source.partition` |
| `messaging.source.anonymous` |
| `messaging.source.name` |
| `messaging.source.template` |
| `messaging.source.temporary` |
| `net.protocol.name` |
| `net.protocol.version` |
| `net.sock.family` |
| `net.sock.peer.name` |
<!-- prettier-ignore-end -->

### Migrating from v1.19.0 and v1.18.0 v1.17.0

<!-- prettier-ignore-start -->
| New attributes ![new](https://img.shields.io/badge/new-green?style=flat) |
| -------------- |
| `error.type` |
| `messaging.consumer.group.name` |
| `messaging.destination.partition.id` |
| `messaging.destination.subscription.name` |
| `messaging.eventhubs.message.enqueued_time` |
| `messaging.gcp_pubsub.message.ack_deadline` |
| `messaging.gcp_pubsub.message.ack_id` |
| `messaging.gcp_pubsub.message.delivery_attempt` |
| `messaging.gcp_pubsub.message.ordering_key` |
| `messaging.message.envelope.size` |
| `messaging.operation.name` |
| `messaging.rabbitmq.message.delivery_tag` |
| `messaging.servicebus.disposition_status` |
| `messaging.servicebus.message.delivery_count` |
| `messaging.servicebus.message.enqueued_time` |
| `server.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Old ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| --- | --- |
| `message.servicebus.destination.subscription_name` | `messaging.destination.subscription.name` |
| `messaging.client_id` | `messaging.client.id` |
| `messaging.consumer.id` | `messaging.client.id` |
| `messaging.evenhubs.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.client_id` | `messaging.client.id` |
| `messaging.kafka.consumer.group` | `messaging.consumer.group.name` |
| `messaging.kafka.message.offset` | `messaging.kafka.offset` |
| `messaging.kafka.partition` | `messaging.destination.partition.id` |
| `messaging.message.payload_size_bytes` | `messaging.message.envelope.size` |
| `messaging.operation` | `messaging.operation.type` |
| `messaging.rocketmq.client_group` | `messaging.consumer.group.name` |
| `messaging.rocketmq.client_id` | `messaging.client.id` |
| `net.peer.name` | `server.address` |
| `net.sock.peer.addr` | `network.peer.address` |
| `net.sock.peer.port` | `network.peer.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Removed attributes ![removed](https://img.shields.io/badge/removed-red?style=flat) |
| ------------------ |
| `destination_publish.anonymous` |
| `messaging.destination.kind` |
| `messaging.kafka.source.partition` |
| `messaging.message.payload_compressed_size_bytes` |
| `messaging.source.anonymous` |
| `messaging.source.kind` |
| `messaging.source.name` |
| `messaging.source.template` |
| `messaging.source.temporary` |
| `net.app.protocol.name` |
| `net.app.protocol.version` |
| `net.sock.family` |
| `net.sock.peer.name` |
| `network.transport` |
| `network.type` |
<!-- prettier-ignore-end -->

### Migrating from v1.16

<!-- prettier-ignore-start -->
| New attributes ![new](https://img.shields.io/badge/new-green?style=flat) |
| -------------- |
| `error.type` |
| `messaging.batch.message_count` |
| `messaging.consumer.group.name` |
| `messaging.destination.anonymous` |
| `messaging.destination.partition.id` |
| `messaging.destination.subscription.name` |
| `messaging.destination.template` |
| `messaging.eventhubs.message.enqueued_time` |
| `messaging.gcp_pubsub.message.ack_deadline` |
| `messaging.gcp_pubsub.message.ack_id` |
| `messaging.gcp_pubsub.message.delivery_attempt` |
| `messaging.gcp_pubsub.message.ordering_key` |
| `messaging.message.envelope.size` |
| `messaging.operation.name` |
| `messaging.rabbitmq.message.delivery_tag` |
| `messaging.servicebus.disposition_status` |
| `messaging.servicebus.message.delivery_count` |
| `messaging.servicebus.message.enqueued_time` |
| `server.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Old ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| --- | --- |
| `messaging.consumer_id` | `messaging.client.id` |
| `messaging.conversation_id` | `messaging.message.conversation_id` |
| `messaging.destination` | `messaging.destination.name` |
| `messaging.kafka.client_id` | `messaging.client.id` |
| `messaging.kafka.consumer_group` | `messaging.consumer.group.name` |
| `messaging.kafka.message_key` | `messaging.kafka.message.key` |
| `messaging.kafka.message.offset` | `messaging.kafka.offset` |
| `messaging.kafka.partition` | `messaging.destination.partition.id` |
| `messaging.kafka.tombstone` | `messaging.kafka.message.tombstone` |
| `messaging.message_id` | `messaging.message.id` |
| `messaging.message_payload_compressed_size_bytes` | `messaging.message.body.size` |
| `messaging.message_payload_size_bytes` | `messaging.message.envelope.size` |
| `messaging.operation` | `messaging.operation.type` |
| `messaging.rabbitmq.routing_key` | `messaging.rabbitmq.destination.routing_key` |
| `messaging.rocketmq.client_group` | `messaging.consumer.group.name` |
| `messaging.rocketmq.client_id` | `messaging.client.id` |
| `messaging.rocketmq.delay_time_level` | `messaging.rocketmq.message.delay_time_level` |
| `messaging.rocketmq.delivery_timestamp` | `messaging.rocketmq.message.delivery_timestamp` |
| `messaging.rocketmq.message_group` | `messaging.rocketmq.message.group` |
| `messaging.rocketmq.message_keys` | `messaging.rocketmq.message.keys` |
| `messaging.rocketmq.message_tag` | `messaging.rocketmq.message.tag` |
| `messaging.rocketmq.message_type` | `messaging.rocketmq.message.type` |
| `messaging.temp_destination` | `messaging.destination.temporary` |
| `net.peer.name` | `server.address` |
| `net.sock.peer.addr` | `network.peer.address` |
| `net.sock.peer.port` | `network.peer.port` |
<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->
| Removed attributes ![removed](https://img.shields.io/badge/removed-red?style=flat) |
| ------------------ |
| `messaging.url` |
| `messaging.destination_kind` |
| `net.sock.family` |
| `net.sock.peer.name` |
| `messaging.protocol` |
| `messaging.protocol_version` |
<!-- prettier-ignore-end -->
