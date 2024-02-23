<!--- Hugo front matter used to generate the website version of this page:
linkTitle: RabbitMQ
--->

# Semantic Conventions for RabbitMQ

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [RabbitMQ](https://www.rabbitmq.com/) extend and override the [Messaging Semantic Conventions](README.md)
that describe common messaging operations attributes in addition to the Semantic Conventions
described on this page.

`messaging.system` MUST be set to `"rabbitmq"`.

## RabbitMQ attributes

In RabbitMQ, the destination is defined by an *exchange* and a *routing key*.
`messaging.destination.name` MUST be set to the name of the exchange. This will be an empty string if the default exchange is used.

<!-- semconv messaging.rabbitmq(full,tag=tech-specific-rabbitmq) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`messaging.rabbitmq.destination.routing_key`](../attributes-registry/messaging.md) | string | RabbitMQ message routing key. | `myKey` | Conditionally Required: If not empty. |
| [`messaging.rabbitmq.message.delivery_tag`](../attributes-registry/messaging.md) | int | RabbitMQ message delivery tag | `123` | Conditionally Required: When available. |
| [`network.peer.address`](../attributes-registry/network.md) | string | Peer address of the network connection - IP address or Unix domain socket name. [1] | `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`network.peer.port`](../attributes-registry/network.md) | int | Peer port number of the network connection. | `65123` | Recommended |

**[1]:** If a database operation involved multiple network calls (for example retries), the address of the last contacted node SHOULD be used.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
