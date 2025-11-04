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

In OpenTelemetry, Events are implemented as a specific type of [`LogRecord`](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.50.0/specification/logs/api.md) that conforms to the conventions included here.

OpenTelemetry Semantic Conventions that define events SHOULD document the event name along
with attributes and the type of the body if any.

## General event semantics

* An event MUST have an [event name](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.50.0/specification/logs/data-model.md#field-eventname)
  that uniquely identifies the event structure: its [attributes](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.50.0/specification/logs/data-model.md#field-attributes)
  and the type of the [body](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.50.0/specification/logs/data-model.md#field-body).

* Event name SHOULD be of a low-cardinality.
  Event names are subject to the [Naming guidelines](/docs/general/naming.md).

* It's RECOMMENDED to use [attributes](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.50.0/specification/logs/data-model.md#field-attributes) to represent the details and additional
  context of the event.

* Events SHOULD have [severity number](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.50.0/specification/logs/data-model.md#field-severitynumber)
  specified.

<!-- Body use cases are not clear - see https://github.com/open-telemetry/semantic-conventions/issues/1651 for the context.-->

## External event compatibility

When recording events from an existing system as OpenTelemetry Events, the system
may lack a single name field or require multiple fields to identify the event.
In such cases, use a combination of fields to create a low-cardinality event name.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
