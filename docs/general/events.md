<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
aliases: [docs/specs/semconv/general/events-general]
--->

# Semantic Conventions for Event Attributes

**Status**: [Experimental][DocumentStatus]

This document describes the attributes of standalone Events that are represented
in the data model by `LogRecord`s.

The following semantic conventions for events are defined:

* **[General](#general-event-attributes): General semantic attributes that may be used in describing Events.**
* [Exceptions](/docs/exceptions/exceptions-logs.md): Semantic attributes that may be used in describing exceptions as events.

## General event attributes

Events are recorded as LogRecords that are shaped in a special way: Event
LogRecords have the attribute `event.name` that uniquely identifies the event.
Events with same `event.name` are structurally similar to one another. Events
may also have other LogRecord attributes.

When recording events from an existing system as OpenTelemetry Events, it is
possible that the existing system does not have the equivalent of a name or
requires multiple fields to identify the structure of the events. In such cases,
OpenTelemetry recommends using a combination of one or more fields as the name
such that the name identifies the event structurally. It is also recommended that
the event names have low-cardinality, so care must be taken to use fields
that identify the class of Events but not the instance of the Event.

<!-- semconv event -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `event.name` | string | Identifies the class / type of event. [1] | `browser.mouse.click`; `device.app.lifecycle` | Required |

**[1]:** Event names are subject to the same rules as [attribute names](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/common/attribute-naming.md). Notably, event names are namespaced to avoid collisions and provide a clean separation of semantics for events in separate domains like browser, mobile, and kubernetes.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
