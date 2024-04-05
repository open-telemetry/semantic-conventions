<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic Conventions for Feature Flags in Spans

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for recording dynamic feature flag
evaluations within a transaction as span events.
To record an evaluation outside of a transaction context, consider
[recording it as a log record](feature-flags-logs.md).

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Motivation](#motivation)
- [Overview](#overview)
- [Convention](#convention)

<!-- tocstop -->

## Motivation

Features flags are commonly used in modern applications to decouple feature releases from deployments.
Many feature flagging tools support the ability to update flag configurations in near real-time from a remote feature flag management service.
They also commonly allow rulesets to be defined that return values based on contextual information.
For example, a feature could be enabled only for a specific subset of users based on context (e.g. users email domain, membership tier, country).

Since feature flags are dynamic and affect runtime behavior, it's important to collect relevant feature flag telemetry signals.
This can be used to determine the impact a feature has on a request, enabling enhanced observability use cases, such as A/B testing or progressive feature releases.

## Overview

The following semantic convention defines how feature flags can be represented as an `Event` in OpenTelemetry.
The terminology was defined in the [OpenFeature specification](https://docs.openfeature.dev/docs/specification/), which represents an industry consensus.
It's intended to be vendor neutral and provide flexibility for current and future use cases.

## Convention

A flag evaluation SHOULD be recorded as an Event on the span during which it occurred.

<!-- semconv feature_flag -->
The event name MUST be `feature_flag`.

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`feature_flag.key`](../attributes-registry/feature-flag.md) | string | The unique identifier of the feature flag. | `logo-color` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`feature_flag.provider_name`](../attributes-registry/feature-flag.md) | string | The name of the service provider that performs the flag evaluation. | `Flag Manager` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`feature_flag.variant`](../attributes-registry/feature-flag.md) | string | SHOULD be a semantic identifier for a value. If one is unavailable, a stringified version of the value can be used. [1] | `red`; `true`; `on` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** A semantic identifier, commonly referred to as a variant, provides a means
for referring to a value without including the value itself. This can
provide additional context for understanding the meaning behind a value.
For example, the variant `red` maybe be used for the value `#c05543`.

A stringified version of the value can be used in situations where a
semantic identifier is unavailable. String representation of the value
should be determined by the implementer.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
