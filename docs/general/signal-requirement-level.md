---
title: Requirement levels on signals and entities
---

# Requirement levels on signals and entities

**Status**: [Development][DocumentStatus]

<details>
<summary>Table of Contents</summary>

<!-- START doctoc -->

- [Recommended](#recommended)
- [Opt-In](#opt-in)

<!-- END doctoc -->

</details>

We use *signal* to cover metrics, spans, log-based
events, and entities.
The following signal requirement levels are specified:

- [Recommended](#recommended)
- [Opt-In](#opt-in)

## Recommended

Instrumentations SHOULD emit the signal by default when instrumentation is enabled.

This requirement level is recommended for signals that are readily available and
can be efficiently emitted, are not expected to include sensitive information, and
are essential for most applications.

Instrumentations MAY offer a configuration option to disable Recommended signals.

## Opt-In

Instrumentations SHOULD emit the signal if and only if the user configures
the instrumentation to do so. Instrumentations that don't support configuration
MUST NOT emit `Opt-In` signals.

This requirement level is recommended for signals that are expensive to retrieve,
usually pose a security or privacy risk, or are not essential for most applications.
These should therefore only be enabled deliberately by a user making an informed decision.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
