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

Events are recorded as LogRecords that are shaped
in a special way: Event LogRecords have the attributes `event.domain`
and `event.name` (and possibly other LogRecord attributes).

The `event.domain` attribute is used to logically separate events from different
systems. For example, to record Events from browser apps, mobile apps and
Kubernetes, we could use `browser`, `device` and `k8s` as the domain for their
Events. This provides a clean separation of semantics for events in each of the
domains.

Within a particular domain, the `event.name` attribute identifies the event.
Events with same domain and name are structurally similar to one another. For
example, some domains could have well-defined schema for their events based on
event names.

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
| `event.domain` | string | The domain identifies the business context for the events. [1] | `browser` | Required |
| `event.name` | string | The name identifies the event. | `click`; `exception` | Required |

**[1]:** Events across different domains may have same `event.name`, yet be
unrelated events.

`event.domain` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `browser` | Events from browser apps |
| `device` | Events from mobile apps |
| `k8s` | Events from Kubernetes |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
