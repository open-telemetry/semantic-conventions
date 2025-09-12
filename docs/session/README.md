<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Session
--->

# Semantic conventions for Sessions

**Status**: [Development][DocumentStatus]

This document defines semantic conventions to apply to client-side applications when tracking sessions.

Session is defined as the period of time encompassing all activities performed by the application and the actions
executed by the end user.

Consequently, a Session is represented as a collection of Logs, Events, and Spans emitted by the Client Application
throughout the Session's duration. Each Session is assigned a unique identifier, which is included as an attribute in
the Logs, Events, and Spans generated during the Session's lifecycle.

Semantic conventions for Session are defined for the following signals:

* [Session Events](session-events.md)

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
