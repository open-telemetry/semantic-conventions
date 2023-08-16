# Semantic conventions for session

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions to apply to client-side applications when tracking sessions.

Session is defined as the period of time encompassing all activities performed by the application and the actions
executed by the end user. 

Consequently, a Session is represented as a collection of Logs, Events, and Spans emitted by the Client Application
throughout the Session's duration. Each Session is assigned a unique identifier, which is included as an attribute in
the Logs, Events, and Spans generated during the Session's lifecycle.



## Attributes

<!-- semconv session-id -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `session.id` | string | A GUID to identify the current session. | `00112233-4455-6677-8899-aabbccddeeff` | Opt-In |
| `session.duration` | double | The fractional-second duration of the associated session id. This may be attached to a session event generated at session end. | `29.5` | Opt-In |
| `session.start` | int | The timestamp in Unix milliseconds the session started. This may be attached to an event generated at session start. | `1665987217045` | Opt-In |
<!-- endsemconv -->



[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
