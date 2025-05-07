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

In OpenTelemetry, Events are implemented as a specific type of [`LogRecord`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.44.0/specification/logs/api.md) that conforms to the conventions included here.

Events SHOULD be generated / produced / recorded using the
[Logs API](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.44.0/specification/logs/api.md#emit-a-logrecord)
to ensure that the event is created using the configured SDK instance.

OpenTelemetry Semantic Convention that define events SHOULD document the event name along
with attributes and the type of the body.

## General event semantics

* An event MUST have an [Event name property](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.44.0/specification/logs/data-model.md#field-eventname)
  that uniquely identifies the event. Event names are subject to the [Naming guidelines](/docs/general/naming.md). Event name SHOULD be of a low-cardinality.
* Events MAY have [extended](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.44.0/specification/logs/data-model.md#field-attributes) attributes
  attributes that provide additional context about the event.
* Events MAY contain a body.
* The event name uniquely identifies event structure: the type of the body and the
  set of attributes.
* The body MAY contain any type supported by the OpenTelemetry data
  model for the log [body](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.44.0/specification/logs/data-model.md#field-body).

Recommendations on using attributes vs. body fields:

It's RECOMMENDED to use the collection of attributes to represent the details of
the event.

Body SHOULD be used when bridging logs and MAY be used when mapping externally defined
events into OpenTelemetry Events.

<!-- Body use cases are not clear - see https://github.com/open-telemetry/semantic-conventions/issues/1651 for the context.-->

### Event payload (body)

* The definition for OpenTelemetry defined events supports describing
  individual body fields.

  The _fields_ are unique to the named event. Different events may use the same
  field name to represent different data.

  For example, body field `id` on event `my_company.order_submitted` is semantically different from
  field `id` on an event with name `session.start`.

* It's NOT RECOMMENDED to prefix the body fields with the `EventName` to
  avoid redundancy and to keep the event definition clean.

* Common attribute naming conventions and [registry](../attributes-registry/README.md)
  requirements don't apply to event payload fields.

## External event compatibility

When recording events from an existing system as OpenTelemetry Events, the system
may lack a single name field or require multiple fields to identify the event.
In such cases, use a combination of fields to create a low-cardinality name.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
