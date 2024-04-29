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

In addition to a required name, an Event may contain a _payload_ of any type permitted by the
[LogRecord body](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#field-body).
In its implementation, the Event _payload_ will constitute the `Body` of the `LogRecord`.
Like all other OpenTelemetry signals, an Event has optional attribute metadata that helps describe
the event context.

Over time, some Events will be specified by OpenTelemetry and will have documented payload structure,
field semantics, and stability and requirement levels. Other events may be user-defined and carry
bespoke user semantics. When an Event name exists in the semantic conventions, its _payload_
structure and semantics will also be defined.

The following semantic conventions for events are defined:

* [Exceptions](/docs/exceptions/exceptions-logs.md): Semantic attributes that may be used in describing exceptions as events.

## Mapping `LogRecord`s to Events

<!--TODO: update or remove this section once Event API is stable and supported by majority of languages-->

An `Event` MAY be reported as a `LogRecord`.
The following table describes attributes used to translate a `LogRecord` to `Event`.

<!-- semconv log_record.event -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`event.name`](../attributes-registry/event.md) | string | Identifies the class / type of event. [1] | `browser.mouse.click`; `device.app.lifecycle` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Event names are subject to the same rules as [attribute names](https://opentelemetry.io/docs/specs/semconv/general/attribute-naming/).
Notably, event names are namespaced to avoid collisions and provide a clean
separation of semantics for events in separate domains like browser, mobile, and
kubernetes.

Events with the same `event.name` are structurally similar to one another.

When recording events from an existing system as OpenTelemetry Events, it is
possible that the existing system does not have the equivalent of a name or
requires multiple fields to identify the structure of the events. In such cases,
OpenTelemetry recommends using a combination of one or more fields as the name
such that the name identifies the event structurally. It is also recommended that
the event names have low-cardinality, so care must be taken to use fields
that identify the class of Events but not the instance of the Event.
<!-- endsemconv -->

## Mapping Span Events to Events

<!--TODO: update or remove this section once Event API is stable and supported by majority of languages-->

Telemetry producers SHOULD use Event API to emit events. When it's not possible, they MAY emit Span Events.
The following table describes attributes used to translate a Span Event to `Event`.

<!-- semconv span_event.event -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`event.name`](../attributes-registry/event.md) | string | Identifies the class / type of event. [1] | `browser.mouse.click`; `device.app.lifecycle` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`event.data`](../attributes-registry/event.md) | string | The event payload serialized into JSON string. [2] | `{"role":"user","content":"how to use OTel Event API?"}`; `"plain string"` | `Conditionally Required` [3] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Event names are subject to the same rules as [attribute names](https://opentelemetry.io/docs/specs/semconv/general/attribute-naming/).
Notably, event names are namespaced to avoid collisions and provide a clean
separation of semantics for events in separate domains like browser, mobile, and
kubernetes.

Events with the same `event.name` are structurally similar to one another.

When recording events from an existing system as OpenTelemetry Events, it is
possible that the existing system does not have the equivalent of a name or
requires multiple fields to identify the structure of the events. In such cases,
OpenTelemetry recommends using a combination of one or more fields as the name
such that the name identifies the event structurally. It is also recommended that
the event names have low-cardinality, so care must be taken to use fields
that identify the class of Events but not the instance of the Event.

**[2]:** The `event.data` MAY be used only on Span Events to capture the event payload (body) and MUST NOT be used on `LogRecord`s or `Event`s.

**[3]:** If and only if the event has a body and is reported as a Span Event.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md

