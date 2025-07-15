<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Session
--->

# Semantic conventions for session

**Status**: [Development][DocumentStatus]

This document defines semantic conventions to apply to client-side applications when tracking sessions.

Session is defined as the period of time encompassing all activities performed by the application and the actions
executed by the end user.

Consequently, a Session is represented as a collection of Logs, Events, and Spans emitted by the Client Application
throughout the Session's duration. Each Session is assigned a unique identifier, which is included as an attribute in
the Logs, Events, and Spans generated during the Session's lifecycle.

When a session reaches end of life, typically due to user inactivity or session timeout, a new session identifier
will be assigned. The previous session identifier may be provided by the instrumentation so that telemetry
backends can link the two sessions (see Session Start Event).

## Attributes

Is now described in the attributes registry.

## Events

Is now described in the namespace registry.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
