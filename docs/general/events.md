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
in a special way: Event LogRecords have the attribute
`event.name` consisting of a dot-separated `namespace` and `name` that
uniquely identifies the event (and possibly other LogRecord attributes).

The `namespace` portion is used to logically separate events from different
systems. For example, to record Events from browser apps, mobile apps and
Kubernetes, we could use `browser`, `device` and `k8s` as the `namespace` for their
Events. This provides a clean separation of semantics for events in each of the
domains.

Within a particular `namespace`, the `name` portion identifies the event.
Events with same `namespace` and `name` are structurally similar to one another. For
example, some namespaces could have well-defined schema for their events based on
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
| `event.name` | string | Consisting of a `namespace` and `name`; uniquely identifies the event. | `browser.mouse.click`; `browser.exception` | Required |

**[1]:** Events across different namespaces may have same name, yet be unrelated events.

The `namespace` portion of the name has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `browser` | Events from browser apps |
| `device` | Events from mobile apps |
| `k8s` | Events from Kubernetes |

The `namespace` and `name` portions of `event.name` MUST be separated by a period (`.`). Periods MUST NOT be used in the `name` portion of the `event.name`
value. Instead, for multi-word `name` portions, each word SHOULD be separated by underscores (i.e. use snake_case). See [Attribute Naming](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/common/attribute-naming.md) for details on namespaces and names.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
