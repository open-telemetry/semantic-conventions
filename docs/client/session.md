# Semantic conventions for session
This document defines semantic conventions to apply to client-side applications when tracking sessions.

Session is defined as the period of time encompassing all activities performed by the application and the actions
executed by the end user. The period of time is defined by the initial activity and concluded after a period of
inactivity, or explicitly ended after a maximum duration is reached.

Consequently, a Session is represented as a collection of Logs, Events, and Spans emitted by the Client Application
throughout the Session's duration. Each Session is assigned a unique identifier, which is included as an attribute in
the Logs, Events, and Spans generated during the Session's lifecycle.

## Attributes

<!-- semconv client-session-id -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `client.session_id` | string | A GUID. | `00112233-4455-6677-8899-aabbccddeeff` | Opt-In |
<!-- endsemconv -->

## How a session operates

After a period of timeout, `client.session_id` MUST be refreshed.
The timeout period MUST be restarted when any Logs, Events, or Spans are recorded.
The session timeout period CAN be customized.
Default session timeout SHOULD be 30 minutes. Session timeout period SHOULD be established when the instrumentation is
first configured and MUST NOT be updated in the middle of a session.

Maximum session length SHOULD NOT exceed 4 hours.