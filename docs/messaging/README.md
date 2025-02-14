<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Messaging
--->

# Semantic conventions for messaging systems

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for messaging systems spans, metrics and logs.

> [!Warning]
>
> Existing messaging instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/messaging/messaging-spans.md)
> (or prior):
>
> * SHOULD NOT change the version of the messaging conventions that they emit by default
>   until the messaging semantic conventions are marked stable.
>   Conventions include, but are not limited to, attributes,
>   metric and span names, span kind and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The list of values includes:
>   * `messaging` - emit the new, stable messaging conventions,
>     and stop emitting the old experimental messaging conventions
>     that the instrumentation emitted previously.
>   * `messaging/dup` - emit both the old and the stable messaging conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental messaging conventions
>     the instrumentation was emitting previously.
>   * Note: `messaging/dup` has higher precedence than `messaging` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version.
> * SHOULD emit the new, stable values for span name, span kind and similar "single"
> valued concepts when `messaging/dup` is present in the list.

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
