<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Messaging Systems
path_base_for_github_subdir:
  from: tmp/semconv/docs/messaging/_index.md
  to: messaging/README.md
--->

# Semantic Conventions for Messaging Systems

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for messaging systems spans, metrics and logs.

Semantic conventions for messaging systems are defined for the following signals:

* [Messaging Spans](messaging-spans.md): Semantic Conventions for messaging *spans*.
* [Messaging Metrics](messaging-metrics.md): Semantic Conventions for messaging *metrics*.

Technology specific semantic conventions are defined for the following messaging systems:

* [Kafka](kafka.md): Semantic Conventions for *Apache Kafka*.
* [RabbitMQ](rabbitmq.md): Semantic Conventions for *RabbitMQ*.
* [RocketMQ](rocketmq.md): Semantic Conventions for *Apache RocketMQ*.
* [Google Cloud Pub/Sub](gcp-pubsub.md): Semantic Conventions for *Google Cloud Pub/Sub*.
* [Azure Service Bus](azure-messaging.md#azure-service-bus): Semantic Conventions for *Azure Service Bus*.
* [Azure Event Hubs](azure-messaging.md#azure-event-hubs): Semantic Conventions for *Azure Event Hubs*.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
