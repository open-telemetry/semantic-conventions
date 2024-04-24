<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
--->

# Event

## Event Attributes

<!-- semconv registry.event(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `event.body` | string | The body of the event serialized into JSON string. [1] | `{"role":"user","content":"how to use Events API?"}`; `"plain string"` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `event.name` | string | Identifies the class / type of event. [2] | `browser.mouse.click`; `device.app.lifecycle` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The `event.body` MAY be used only on Span Events to capture the body (payload) and MUST NOT be used when emitting Log Records or Events.

**[2]:** Event names are subject to the same rules as [attribute names](https://opentelemetry.io/docs/specs/semconv/general/attribute-naming/).
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
