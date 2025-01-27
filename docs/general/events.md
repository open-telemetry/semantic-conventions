<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
aliases: [events-general]
--->

# Semantic Conventions for Events

**Status**: [Development][DocumentStatus]

This document describes the characteristics of standalone Events that are represented
in the data model by `LogRecord`s.

Semantically, an Event is a named occurrence at an instant in time. It signals that
"this thing happened at this time" and provides additional specifics about the occurrence.
Examples of Events might include things like uncaught exceptions, button clicks, user logout,
network connection severed, etc.

In OpenTelemetry, Events are implemented as a specific type of [`LogRecord`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/specification/logs/api.md) that conforms to the conventions included here.

In addition to a required name, an Event may contain a _payload_ (body) of any type permitted
by the [LogRecord body](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#field-body).
In its implementation, the Event _payload_ (body) will constitute the `Body` of the `LogRecord`.
Like all other OpenTelemetry signals, an Event has optional attribute metadata that helps describe
the event context.

Over time, some Events will be specified by OpenTelemetry and will have documented payload structure,
field semantics, and stability and requirement levels. Other events may be user-defined and carry
bespoke user semantics. When an Event name exists in the semantic conventions, its _payload_
structure and semantics will also be defined.

## General event semantics

* An event MUST have an [Event name property](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/specification/logs/data-model.md#field-eventname)
  that uniquely identifies the event. Event names are subject to the [Naming guidelines](/docs/general/naming.md).
* Event MAY have [standard](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/specification/common#attribute)
  attributes that provide additional context about the event.
* It MAY contain a _payload_ (body) that describes the specific details of the
  named event.
* The event name uniquely identifies event structure / type of the _payload_ (body)
  and the set of attributes.
* The _payload_ (body) MAY contain any type supported by the OpenTelemetry data
  model for the log [body](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#field-body)
  and the semantic conventions will define the expected structure of the _payload_
  (body) for the event.
* The _payload_ (body) SHOULD be used to represent the structure of the event.

Recommendations for defining events:

* Use the _payload_ (body) to represent the details of the event instead of a
  collection of [standard](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/specification/common#attribute)
  attributes.
* Events SHOULD be generated / produced / recorded using the
    [Emit Event API](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/specification/logs/api.md#emit-an-event)
    to ensure that the event is created using the configured SDK instance.
  * The Emit Event API is not yet available in all OpenTelemetry SDKs. Check [spec-compliance matrix](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/spec-compliance-matrix.md#logs) to see the implementation status in corresponding language.
* It's NOT RECOMMENDED to prefix the _payload_ (body) _fields_ with the `EventName` to
  avoid redundancy and to keep the event definition clean.
* The events SHOULD document their semantic conventions including event name,
  attributes, and the payload.

Recommendations on using attributes vs. body fields:

* If the field should be comparable across events with different `EventName` (or between an event and other telemetry items),
  it should be an attribute.
* If the field is specific to the event itself, then it should be a body field.
* Body fields that belong to events with different event names are not comparable.
  For example, body field `id` on event `my_company.order_submitted` is semantically different from
  field `id` on an event with name `session.start`.

### Event payload (body)

* Common attribute naming conventions and [registry](../attributes-registry/README.md)
  requirements don't apply to event payload fields.
* The definition for OpenTelemetry defined events supports describing
  individual _fields_ (Body Fields)
  * The _fields_ are unique to the named event ([EventName](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/specification/logs/data-model.md#field-eventname)) and different events
    may use the same _field_ name to represent different data, due to the unique
    nature of the event.

## External event compatibility

When recording events from an existing system as OpenTelemetry Events, it is
possible that the existing system does not have the equivalent of a name or
requires multiple fields to identify the structure of the events. In such cases,
OpenTelemetry recommends using a combination of one or more fields as the name
such that the name identifies the event structurally. It is also recommended that
the event names have low-cardinality, so care must be taken to use fields
that identify the class of Events but not the instance of the Event.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
