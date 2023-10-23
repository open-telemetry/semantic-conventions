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
| `messaging.rabbitmq.delivery_tag` | int | RabbitMQ delivery tag | `123` | Conditionally Required: When messages are received or delivered. |
| `messaging.rabbitmq.destination.routing_key` | string | RabbitMQ message routing key. | `myKey` | Conditionally Required: If not empty. |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
