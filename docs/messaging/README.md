<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Messaging Systems
path_base_for_github_subdir:
  from: content/en/docs/specs/semconv/messaging/_index.md
  to: messaging/README.md
--->

# Semantic Conventions for Messaging Systems

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for messaging systems spans, metrics and logs.

Semantic conventions for messaging systems are defined for the following signals:

* [Messaging Spans](messaging-spans.md): Semantic Conventions for messaging *spans*.
* [Messaging Metrics](messaging-metrics.md): Semantic Conventions for messaging *metrics*.

## Technology specific semantic conventions

**Status**: [Experimental][DocumentStatus]
<!-- Individual messaging systems may be declared stable along with the corresponding messaging.system value, but this list as a whole is not intended to be stabilized. -->

Messaging system name is recorded on telemetry signals with `messaging.system` attribute.

`messaging.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used.

<!-- TODO this could be auto-generated if is implemented https://github.com/open-telemetry/build-tools/issues/192 -->
| Value  | Description | Semantic Conventions |
|---|---|---|
| `activemq` | Apache ActiveMQ |  |
| `aws_sqs` | Amazon Simple Queue Service (SQS) |  |
| `azure_eventgrid` | Azure Event Grid |  |
| `azure_eventhubs` | Azure Event Hubs |  |
| `azure_servicebus` | Azure Service Bus |  |
| `gcp_pubsub` | Google Cloud Pub/Sub | [Google Cloud Pub/Sub](gcp-pubsub.md) |
| `jms` | Java Message Service |
| `kafka` | Apache Kafka | [Kafka](kafka.md)|
| `rabbitmq` | RabbitMQ | [RabbitMQ](rabbitmq.md) |
| `rocketmq` | Apache RocketMQ | [RocketMQ](rocketmq.md) |

If none of these values apply, consider submitting a proposal to this specification to add a new system.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
