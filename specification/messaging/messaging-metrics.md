# Semantic Conventions for Messaging Metrics

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

<!-- tocstop -->

# Semantic Conventions for Messaging Metrics

**Status**: [Experimental][DocumentStatus]

The conventions described in this section are messaging specific.

**Disclaimer:** These are initial messaging metric instruments and attributes but more may be added in the future.

<!-- toc -->
<!-- tocstop -->

## Metric: `messaging.publish.duration`

This metric is required.

When this metric is reported alongside an messaging publish span, the metric value SHOULD be the same as the corresponding span duration.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.21.0/specification/metrics/api.md#instrument-advice)
of `[ 0, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.messaging.publish.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.publish.duration` | Histogram | `s` | Measures the duration of publish operation. |
<!-- endsemconv -->

<!-- semconv metric.messaging.publish.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.system` | string | A string identifying the messaging system. | `kafka`; `rabbitmq`; `rocketmq`; `activemq`; `AmazonSQS` | Required |
| `messaging.todo.status` | string | The status of the operation: TODO | `ok`; `error`; `timeout` | Required |
| `messaging.destination.name` | string | The message destination name [1] | `MyQueue`; `MyTopic` | Conditionally Required: [2] |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [3] | `/customers/{customerId}` | Conditionally Required: if available. |
| [`network.protocol.name`](../general/general-attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `amqp`; `mqtt` | Recommended |
| [`network.protocol.version`](../general/general-attributes.md) | string | Version of the application layer protocol used. See note below. [4] | `3.1.1` | Recommended |
| [`server.address`](../general/general-attributes.md) | string | Logical server hostname, matches server FQDN if available, and IP or socket address if FQDN is not known. | `example.com` | Conditionally Required: If available. |
| [`server.port`](../general/general-attributes.md) | int | Logical server port number | `80`; `8080`; `443` | Conditionally Required: If available. |
| [`server.socket.address`](../general/general-attributes.md) | string | Physical server IP address or Unix socket address. If set from the client, should simply use the socket's peer address, and not attempt to find any actual server IP (i.e., if set from client, this may represent some proxy server instead of the logical server). | `10.5.3.2` | Recommended: If different than `server.address`. |

**[1]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker does not have such notion, the destination name SHOULD uniquely identify the broker.

**[2]:** if and only if `messaging.destination.name` is known to have low cardinality. Otherwise, `messaging.destination.template` MAY be populated.

**[3]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.
<!-- endsemconv -->

## Metric: `messaging.receive.duration`

This metric is recommended when messaging system supports poll-based receive operations.

<!-- semconv metric.messaging.receive.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.receive.duration` | Histogram | `s` | Measures the duration of receive operation. |
<!-- endsemconv -->

<!-- semconv metric.messaging.publish.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.system` | string | A string identifying the messaging system. | `kafka`; `rabbitmq`; `rocketmq`; `activemq`; `AmazonSQS` | Required |
| `messaging.todo.status` | string | The status of the operation: TODO | `ok`; `error`; `timeout` | Required |
| `messaging.destination.name` | string | The message destination name [1] | `MyQueue`; `MyTopic` | Conditionally Required: [2] |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [3] | `/customers/{customerId}` | Conditionally Required: if available. |
| [`network.protocol.name`](../general/general-attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `amqp`; `mqtt` | Recommended |
| [`network.protocol.version`](../general/general-attributes.md) | string | Version of the application layer protocol used. See note below. [4] | `3.1.1` | Recommended |
| [`server.address`](../general/general-attributes.md) | string | Logical server hostname, matches server FQDN if available, and IP or socket address if FQDN is not known. | `example.com` | Conditionally Required: If available. |
| [`server.port`](../general/general-attributes.md) | int | Logical server port number | `80`; `8080`; `443` | Conditionally Required: If available. |
| [`server.socket.address`](../general/general-attributes.md) | string | Physical server IP address or Unix socket address. If set from the client, should simply use the socket's peer address, and not attempt to find any actual server IP (i.e., if set from client, this may represent some proxy server instead of the logical server). | `10.5.3.2` | Recommended: If different than `server.address`. |

**[1]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker does not have such notion, the destination name SHOULD uniquely identify the broker.

**[2]:** if and only if `messaging.destination.name` is known to have low cardinality. Otherwise, `messaging.destination.template` MAY be populated.

**[3]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.
<!-- endsemconv -->

## Metric: `messaging.deliver.duration`

This metric is recommended when messaging system supports pull-based deliver operations.

<!-- semconv metric.messaging.deliver.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.deliver.duration` | Histogram | `s` | Measures the duration of deliver operation. |
<!-- endsemconv -->

<!-- semconv metric.messaging.deliver.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.system` | string | A string identifying the messaging system. | `kafka`; `rabbitmq`; `rocketmq`; `activemq`; `AmazonSQS` | Required |
| `messaging.todo.status` | string | The status of the operation: TODO | `ok`; `error`; `timeout` | Required |
| `messaging.destination.name` | string | The message destination name [1] | `MyQueue`; `MyTopic` | Conditionally Required: [2] |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [3] | `/customers/{customerId}` | Conditionally Required: if available. |
| [`network.protocol.name`](../general/general-attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `amqp`; `mqtt` | Recommended |
| [`network.protocol.version`](../general/general-attributes.md) | string | Version of the application layer protocol used. See note below. [4] | `3.1.1` | Recommended |
| [`server.address`](../general/general-attributes.md) | string | Logical server hostname, matches server FQDN if available, and IP or socket address if FQDN is not known. | `example.com` | Conditionally Required: If available. |
| [`server.port`](../general/general-attributes.md) | int | Logical server port number | `80`; `8080`; `443` | Conditionally Required: If available. |
| [`server.socket.address`](../general/general-attributes.md) | string | Physical server IP address or Unix socket address. If set from the client, should simply use the socket's peer address, and not attempt to find any actual server IP (i.e., if set from client, this may represent some proxy server instead of the logical server). | `10.5.3.2` | Recommended: If different than `server.address`. |

**[1]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker does not have such notion, the destination name SHOULD uniquely identify the broker.

**[2]:** if and only if `messaging.destination.name` is known to have low cardinality. Otherwise, `messaging.destination.template` MAY be populated.

**[3]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.
<!-- endsemconv -->

## Metric: `messaging.settle.duration`

This metric is recommended when messaging system supports settle operations.

<!-- semconv metric.messaging.settle.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.settle.duration` | Histogram | `s` | Measures the duration of settle operation. |
<!-- endsemconv -->

<!-- semconv metric.messaging.settle.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.system` | string | A string identifying the messaging system. | `kafka`; `rabbitmq`; `rocketmq`; `activemq`; `AmazonSQS` | Required |
| `messaging.todo.status` | string | The status of the operation: TODO | `ok`; `error`; `timeout` | Required |
| [`messaging.todo_settlement.status`](../system/messaging-metrics.md) | string | The status of the settlement: acknowledged, rejected, TODO | `ack`; `nack` | Recommended |
| `messaging.destination.name` | string | The message destination name [1] | `MyQueue`; `MyTopic` | Conditionally Required: [2] |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [3] | `/customers/{customerId}` | Conditionally Required: if available. |
| [`network.protocol.name`](../general/general-attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `amqp`; `mqtt` | Recommended |
| [`network.protocol.version`](../general/general-attributes.md) | string | Version of the application layer protocol used. See note below. [4] | `3.1.1` | Recommended |
| [`server.address`](../general/general-attributes.md) | string | Logical server hostname, matches server FQDN if available, and IP or socket address if FQDN is not known. | `example.com` | Conditionally Required: If available. |
| [`server.port`](../general/general-attributes.md) | int | Logical server port number | `80`; `8080`; `443` | Conditionally Required: If available. |
| [`server.socket.address`](../general/general-attributes.md) | string | Physical server IP address or Unix socket address. If set from the client, should simply use the socket's peer address, and not attempt to find any actual server IP (i.e., if set from client, this may represent some proxy server instead of the logical server). | `10.5.3.2` | Recommended: If different than `server.address`. |

**[1]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker does not have such notion, the destination name SHOULD uniquely identify the broker.

**[2]:** if and only if `messaging.destination.name` is known to have low cardinality. Otherwise, `messaging.destination.template` MAY be populated.

**[3]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.
<!-- endsemconv -->

## Metric: `messaging.published_messages.count`

This metric is recommended when messaging system supports batch publishing. For the systems that support single-message publishing only, message count can be derived from `messaging.publish.duration` histogram.

<!-- semconv metric.messaging.publish.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.published_messages.count` | Counter | `message` | Measures the number of published messages. |
<!-- endsemconv -->

<!-- semconv metric.messaging.publish.count(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.system` | string | A string identifying the messaging system. | `kafka`; `rabbitmq`; `rocketmq`; `activemq`; `AmazonSQS` | Required |
| `messaging.todo.status` | string | The status of the operation: TODO | `ok`; `error`; `timeout` | Required |
| `messaging.destination.name` | string | The message destination name [1] | `MyQueue`; `MyTopic` | Conditionally Required: [2] |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [3] | `/customers/{customerId}` | Conditionally Required: if available. |
| [`network.protocol.name`](../general/general-attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `amqp`; `mqtt` | Recommended |
| [`network.protocol.version`](../general/general-attributes.md) | string | Version of the application layer protocol used. See note below. [4] | `3.1.1` | Recommended |
| [`server.address`](../general/general-attributes.md) | string | Logical server hostname, matches server FQDN if available, and IP or socket address if FQDN is not known. | `example.com` | Conditionally Required: If available. |
| [`server.port`](../general/general-attributes.md) | int | Logical server port number | `80`; `8080`; `443` | Conditionally Required: If available. |
| [`server.socket.address`](../general/general-attributes.md) | string | Physical server IP address or Unix socket address. If set from the client, should simply use the socket's peer address, and not attempt to find any actual server IP (i.e., if set from client, this may represent some proxy server instead of the logical server). | `10.5.3.2` | Recommended: If different than `server.address`. |

**[1]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker does not have such notion, the destination name SHOULD uniquely identify the broker.

**[2]:** if and only if `messaging.destination.name` is known to have low cardinality. Otherwise, `messaging.destination.template` MAY be populated.

**[3]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.
<!-- endsemconv -->

## Metric: `messaging.received_messages.count`

This metric is recommended when messaging system supports batch receive. For the systems that can only receive one message, message count can be derived from `messaging.receive.duration` or `messaging.deliver.duration` histogram.

<!-- semconv metric.messaging.receive.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.received_messages.count` | Counter | `message` | Measures the number of received or delivered messages. |
<!-- endsemconv -->

<!-- semconv metric.messaging.receive.count(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.system` | string | A string identifying the messaging system. | `kafka`; `rabbitmq`; `rocketmq`; `activemq`; `AmazonSQS` | Required |
| `messaging.todo.status` | string | The status of the operation: TODO | `ok`; `error`; `timeout` | Required |
| `messaging.destination.name` | string | The message destination name [1] | `MyQueue`; `MyTopic` | Conditionally Required: [2] |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [3] | `/customers/{customerId}` | Conditionally Required: if available. |
| [`network.protocol.name`](../general/general-attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `amqp`; `mqtt` | Recommended |
| [`network.protocol.version`](../general/general-attributes.md) | string | Version of the application layer protocol used. See note below. [4] | `3.1.1` | Recommended |
| [`server.address`](../general/general-attributes.md) | string | Logical server hostname, matches server FQDN if available, and IP or socket address if FQDN is not known. | `example.com` | Conditionally Required: If available. |
| [`server.port`](../general/general-attributes.md) | int | Logical server port number | `80`; `8080`; `443` | Conditionally Required: If available. |
| [`server.socket.address`](../general/general-attributes.md) | string | Physical server IP address or Unix socket address. If set from the client, should simply use the socket's peer address, and not attempt to find any actual server IP (i.e., if set from client, this may represent some proxy server instead of the logical server). | `10.5.3.2` | Recommended: If different than `server.address`. |

**[1]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker does not have such notion, the destination name SHOULD uniquely identify the broker.

**[2]:** if and only if `messaging.destination.name` is known to have low cardinality. Otherwise, `messaging.destination.template` MAY be populated.

**[3]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.
<!-- endsemconv -->

## Metric: `messaging.settled_messages.count`

This metric is recommended when messaging system supports per-message batch settlement. For the systems that can only settle individual messages, message count can be derived from `messaging.settle.duration` histogram. Systems that support offset-based settlement, SHOULD NOT report this metric.

<!-- semconv metric.messaging.settle.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `messaging.settled_messages.count` | Counter | `message` | Measures the number of settled messages. |
<!-- endsemconv -->

<!-- semconv metric.messaging.settle.count(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `messaging.system` | string | A string identifying the messaging system. | `kafka`; `rabbitmq`; `rocketmq`; `activemq`; `AmazonSQS` | Required |
| `messaging.todo.status` | string | The status of the operation: TODO | `ok`; `error`; `timeout` | Required |
| `messaging.destination.name` | string | The message destination name [1] | `MyQueue`; `MyTopic` | Conditionally Required: [2] |
| `messaging.destination.template` | string | Low cardinality representation of the messaging destination name [3] | `/customers/{customerId}` | Conditionally Required: if available. |
| [`network.protocol.name`](../general/general-attributes.md) | string | [OSI Application Layer](https://osi-model.com/application-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `amqp`; `mqtt` | Recommended |
| [`network.protocol.version`](../general/general-attributes.md) | string | Version of the application layer protocol used. See note below. [4] | `3.1.1` | Recommended |
| [`server.address`](../general/general-attributes.md) | string | Logical server hostname, matches server FQDN if available, and IP or socket address if FQDN is not known. | `example.com` | Conditionally Required: If available. |
| [`server.port`](../general/general-attributes.md) | int | Logical server port number | `80`; `8080`; `443` | Conditionally Required: If available. |
| [`server.socket.address`](../general/general-attributes.md) | string | Physical server IP address or Unix socket address. If set from the client, should simply use the socket's peer address, and not attempt to find any actual server IP (i.e., if set from client, this may represent some proxy server instead of the logical server). | `10.5.3.2` | Recommended: If different than `server.address`. |

**[1]:** Destination name SHOULD uniquely identify a specific queue, topic or other entity within the broker. If
the broker does not have such notion, the destination name SHOULD uniquely identify the broker.

**[2]:** if and only if `messaging.destination.name` is known to have low cardinality. Otherwise, `messaging.destination.template` MAY be populated.

**[3]:** Destination names could be constructed from templates. An example would be a destination name involving a user name or product id. Although the destination name in this case is of high cardinality, the underlying template is of low cardinality and can be effectively used for grouping and aggregation.

**[4]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client used has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
