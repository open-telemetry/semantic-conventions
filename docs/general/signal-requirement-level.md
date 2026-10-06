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

If the OpenTelemetry API for a signal provides a generic opt-in/opt-out mechanism,
that mechanism SHOULD be used instead of a custom configuration mechanism:

- For **log-based events** and **entities**, instrumentations SHOULD use [`Logger.Enabled`](https://opentelemetry.io/docs/specs/otel/logs/api/#enabled)
  (passing the event name) to determine if the event is enabled.
- For **metrics**, instrumentations SHOULD use synchronous [`Instrument.Enabled`](https://opentelemetry.io/docs/specs/otel/metrics/api/#enabled)
  (which reflects SDK [Views](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled) and `Drop` aggregation) to check if the instrument is enabled.
- For **spans**, instrumentations SHOULD use [`Tracer.Enabled`](https://opentelemetry.io/docs/specs/otel/trace/api/#enabled)
  and standard SDK [Samplers](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampler) along with [`Span.IsRecording`](https://opentelemetry.io/docs/specs/otel/trace/api/#isrecording).

This requirement level is recommended for signals that are expensive to retrieve,
usually pose a security or privacy risk, or are not essential for most applications.
These should therefore only be enabled deliberately by a user making an informed decision.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status/
