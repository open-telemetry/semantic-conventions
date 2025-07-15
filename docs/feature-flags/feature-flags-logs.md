<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Logs
--->

# Semantic conventions for feature flags in logs

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for recording feature flag evaluations as
a [log record](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#log-and-event-record-definition) emitted through the
[Logger API](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/api.md#emit-a-logrecord).
This is useful when a flag is evaluated outside of a transaction context
such as when the application loads or on a timer.

## Motivation

Feature flags are commonly used in modern applications to decouple feature releases from deployments.
Many feature flagging tools support the ability to update flag configurations in near real-time from a remote feature flag management service.
They also commonly allow rulesets to be defined that return values based on contextual information.
For example, a feature could be enabled only for a specific subset of users based on context (e.g. users email domain, membership tier, country).

Since feature flags are dynamic and affect runtime behavior, it's important to collect relevant feature flag telemetry signals.
This can be used to determine the impact a feature has on a request, enabling enhanced observability use cases, such as A/B testing or progressive feature releases.

## Recording an evaluation

Feature flag evaluations SHOULD be recorded as attributes on the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#log-and-event-record-definition) passed to the [Logger](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/api.md#logger) emit
operations. Evaluations MAY be recorded on "logs" or "events" depending on the
context.

## Events

Is now described in the namespace registry.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
