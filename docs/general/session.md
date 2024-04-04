# Semantic conventions for session

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions to apply to client-side applications when tracking sessions.

Session is defined as the period of time encompassing all activities performed by the application and the actions
executed by the end user.

Consequently, a Session is represented as a collection of Logs, Events, and Spans emitted by the Client Application
throughout the Session's duration. Each Session is assigned a unique identifier, which is included as an attribute in
the Logs, Events, and Spans generated during the Session's lifecycle.

When a session reaches end of life, typically due to user inactivity or session timeout, a new session identifier
will be assigned. The previous session identifier may be provided by the instrumentation so that telemetry
backends can link the two sessions.

## Attributes

<!-- semconv session-id -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`session.id`](../attributes-registry/session.md) | string | A unique id to identify a session. | `00112233-4455-6677-8899-aabbccddeeff` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`session.previous_id`](../attributes-registry/session.md) | string | The previous `session.id` for this user, when known. | `00112233-4455-6677-8899-aabbccddeeff` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
