<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Logs
--->

# Semantic Conventions for Feature Flags in Logs

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for recording feature flag evaluations as
a [log record](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/logs/data-model.md#log-and-event-record-definition) emitted through the
[Logger API](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/logs/bridge-api.md#emit-a-logrecord).
This is useful when a flag is evaluated outside of a transaction context
such as when the application loads or on a timer.
To record a flag evaluation as a part of a transaction context,
consider [recording it as a span event](feature-flags-spans.md).

For more information about why it is useful to capture feature flag evaluations,
refer to the [motivation](feature-flags-spans.md#motivation)
section of the trace semantic convention for feature flag evaluations.

<!-- toc -->

- [Recording an Evaluation](#recording-an-evaluation)
- [Attributes](#attributes)

<!-- tocstop -->

## Recording an Evaluation

Feature flag evaluations SHOULD be recorded as attributes on the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/logs/data-model.md#log-and-event-record-definition) passed to the [Logger](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/logs/bridge-api.md#logger) emit
operations. Evaluations MAY be recorded on "logs" or "events" depending on the
context.

## Attributes

The table below indicates which attributes should be added to the
[LogRecord](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/logs/data-model.md#log-and-event-record-definition) and their types.

<!-- semconv log-feature_flag -->
The event name MUST be `feature_flag`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`feature_flag.key`](feature-flags-spans.md) | string | The unique identifier of the feature flag. | `logo-color` | Required |
| [`feature_flag.provider_name`](feature-flags-spans.md) | string | The name of the service provider that performs the flag evaluation. | `Flag Manager` | Recommended |
| [`feature_flag.variant`](feature-flags-spans.md) | string | SHOULD be a semantic identifier for a value. If one is unavailable, a stringified version of the value can be used. [1] | `red`; `true`; `on` | Recommended |

**[1]:** A semantic identifier, commonly referred to as a variant, provides a means
for referring to a value without including the value itself. This can
provide additional context for understanding the meaning behind a value.
For example, the variant `red` maybe be used for the value `#c05543`.

A stringified version of the value can be used in situations where a
semantic identifier is unavailable. String representation of the value
should be determined by the implementer.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
