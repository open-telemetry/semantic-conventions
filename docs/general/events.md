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

In OpenTelemetry, Events are implemented as a specific type of [`LogRecord`](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/api.md)
that conforms to the conventions included here.

Semantic conventions that define events MUST document the event name and its attributes.

## General event semantics

* An event MUST have an [event name](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/data-model.md#field-eventname)
  that uniquely identifies the event structure.

* Event names SHOULD follow the [Naming guidelines](/docs/general/naming.md).

* [Attributes](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/data-model.md#field-attributes)
  SHOULD be used to represent details and provide additional context about the event.

* Events SHOULD NOT use [body](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/data-model.md#field-body).

* Events SHOULD specify a [severity number](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/logs/data-model.md#field-severitynumber).

## External event compatibility

When recording events from an existing system as OpenTelemetry Events, it's common
for the system to lack a single name field or require multiple fields to identify the event.
In such cases, instrumentation SHOULD use a combination of fields to create a low-cardinality event name.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
