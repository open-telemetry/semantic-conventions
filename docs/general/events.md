<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
aliases: [docs/specs/semconv/general/events-general]
--->

# Semantic Conventions for Events

**Status**: [Experimental][DocumentStatus]

This document describes the characteristics of standalone Events that are represented
in the data model by `LogRecord`s.

Semantically, an Event is a named occurrence at an instant in time. It signals that
"this thing happened at this time" and provides additional specifics about the occurrence.
Examples of Events might include things like uncaught exceptions, button clicks, user logout,
network connection severed, etc.

In OpenTelemetry, Events are implemented as a specific type of `LogRecord` that conforms to
the conventions included here, and Events
[have their own API](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/event-api.md).
The API abstracts away knowledge of `LogRecord` so that users only deal with Event
semantics.

In addition to a required name, an Event may contain a _payload_ (data) of any type permitted
by the [LogRecord body](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#field-body).
In its implementation, the Event _payload_ (data) will constitute the `Body` of the `LogRecord`.
Like all other OpenTelemetry signals, an Event has optional attribute metadata that helps describe
the event context.

Over time, some Events will be specified by OpenTelemetry and will have documented payload structure,
field semantics, and stability and requirement levels. Other events may be user-defined and carry
bespoke user semantics. When an Event name exists in the semantic conventions, its _payload_
structure and semantics will also be defined.

## Event definition

<!-- semconv event -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`event.name`](../attributes-registry/event.md) | string | Identifies the class / type of event. [1] | `browser.mouse.click`; `device.app.lifecycle` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Event names are subject to the same rules as [attribute names](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/common/attribute-naming.md). Notably, event names are namespaced to avoid collisions and provide a clean separation of semantics for events in separate domains like browser, mobile, and kubernetes.
<!-- endsemconv -->

### General event semantics

* An event MUST have an `event.name` attribute that uniquely identifies the event.
* It MAY have other [standard](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/common#attribute)
  attributes that provide additional context about the event.
* It MAY contain a _payload_ (data) that describes the specific details of the
  named event.
* The structure of the named event (`event.name`) is unique to the event, this
  identifies
  * Whether the event contains a _payload_ (data), and the structure / type of
    the _payload_ (data).
  * Whether there are any expected [standard](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/common#attribute)
    attributes that are used to describe the event.
* All OpenTelemetry defined events SHOULD be defined in the semantic conventions
  to highlight the expected structure of the event.
* The _payload_ (data) MAY contain any type supported by the OpenTelemetry data
  model for the log [body](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#field-body)
  and the semantic conventions will define the expected structure of the _payload_
  (data) for the event.
* The _payload_ (data) SHOULD be used to represent the structure of the event.

Recommendations for defining events:

* Use the _payload_ (data) to represent the details of the event instead of a
  collection of [standard](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/common#attribute)
  attributes.
* Events SHOULD be generated / produced / recorded using the
    [Event API](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/event-api.md)
    to ensure that the event is created using the configured SDK instance.
  * The Event API is not yet available in all OpenTelemetry SDKs.
  * TODO: Add deep link to the [compliance matrix of the Event API](https://github.com/open-telemetry/opentelemetry-specification/blob/main/spec-compliance-matrix.md)
    when it exists.
* The _payload_ (data) _fields_ SHOULD not be prefixed with the `event.name` to
  avoid redundancy and to keep the event definition clean.

### Event payload (data)

* Common attribute naming conventions and [registry](../attributes-registry/README.md)
  requirements don't apply to event payload fields.
* The definition for OpenTelemetry defined events supports describing
  individual _fields_ (Body Fields)
  * Any _fields_ are NOT added to the Global attribute registry for use by other
    events.
  * The _fields_ are unique to the named event (`event.name`) and different events
    may use the same _field_ name to represent different data, due to the unique
    nature of the event.
* The _fields_ MAY reference / inherit details from Global attribute registry
  attributes and provide additional details specific to the event, including
  providing an _alias_ (shorter) name for the attribute.

As each `event.name` is unique and defines the structure of the event, as long
as the event follows the General event semantics it will be considered a valid
event. For example :

* [Exceptions](/docs/exceptions/exceptions-logs.md): Semantic attributes that
  may be used in describing exceptions as events.

## External event compatibility

When recording events from an existing system as OpenTelemetry Events, it is
possible that the existing system does not have the equivalent of a name or
requires multiple fields to identify the structure of the events. In such cases,
OpenTelemetry recommends using a combination of one or more fields as the name
such that the name identifies the event structurally. It is also recommended that
the event names have low-cardinality, so care must be taken to use fields
that identify the class of Events but not the instance of the Event.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
