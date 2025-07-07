<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
aliases: [events-general]
--->

# Semantic conventions for events

**Status**: [Development][DocumentStatus]

This document describes the characteristics of standalone Events that are represented
in the data model by `LogRecord`s.

Semantically, an Event is a named occurrence at an instant in time. It signals that
"this thing happened at this time" and provides additional specifics about the occurrence.
Examples of Events might include things like button clicks, user logout,
network connection severed, etc.

In OpenTelemetry, Events are implemented as a specific type of [`LogRecord`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/api.md) that conforms to the conventions included here.

OpenTelemetry Semantic Conventions that define events SHOULD document the event name along
with attributes and the type of the body if any.

## General event semantics

* An event MUST have an [Event name property](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#field-eventname)
  that uniquely identifies the event. Event names are subject to the [Naming guidelines](/docs/general/naming.md). Event name SHOULD be of a low-cardinality.
* Events MAY have [attributes](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#field-attributes)
  that provide additional context about the event.
* Events MAY contain a [body](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#field-body) of type [`any`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#type-any).
* The event name uniquely identifies event structure: the set of attributes and
  the type of the body.
* Events MAY have [severity number](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#field-severitynumber).

It's RECOMMENDED to use the collection of attributes to represent the details of
the event.

<!-- Body use cases are not clear - see https://github.com/open-telemetry/semantic-conventions/issues/1651 for the context.-->

## External event compatibility

When recording events from an existing system as OpenTelemetry Events, the system
may lack a single name field or require multiple fields to identify the event.
In such cases, use a combination of fields to create a low-cardinality event name.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
