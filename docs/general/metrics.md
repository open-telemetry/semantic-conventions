<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
aliases: [metrics-general]
--->

# Metrics semantic conventions

**Status**: [Mixed][DocumentStatus]

<!-- toc -->

- [General guidelines](#general-guidelines)
  - [Units](#units)
  - [Instrument units](#instrument-units)
  - [Instrument types](#instrument-types)
  - [Consistent UpDownCounter timeseries](#consistent-updowncounter-timeseries)

<!-- tocstop -->

The following semantic conventions surrounding metrics are defined:

* **[General Guidelines](#general-guidelines): General metrics guidelines.**
* [Database](/docs/db/database-metrics.md): For SQL and NoSQL client metrics.
* [FaaS](/docs/faas/faas-metrics.md): For [Function as a Service](https://wikipedia.org/wiki/Function_as_a_service) metrics.
* [GenAI](/docs/gen-ai/gen-ai-metrics.md): For Generative AI metrics.
* [HTTP](/docs/http/http-metrics.md): For HTTP client and server metrics.
* [Messaging](/docs/messaging/messaging-metrics.md): For messaging systems (queues, publish/subscribe, etc.) metrics.
* [RPC](/docs/rpc/rpc-metrics.md): For RPC client and server metrics.
* [.NET](/docs/dotnet/README.md): For network-related metrics emitted by .NET runtime components.
* **System metrics**
  * [System](/docs/system/system-metrics.md): For standard system metrics.
  * [Container](/docs/system/container-metrics.md)
  * [Hardware](/docs/hardware/README.md): For hardware-related metrics.
  * [K8s](/docs/system/k8s-metrics.md): For K8s metrics.
  * [Process](/docs/system/process-metrics.md): For standard process metrics.
  * [Runtime Environment](/docs/runtime/README.md#metrics): For runtime environment metrics.
* [OTel SDK Telemetry](/docs/otel/sdk-metrics.md): Metrics emitted by the OpenTelemetry SDK components.

Apart from semantic conventions for metrics, [traces](trace.md), [logs](logs.md), and [events](events.md), OpenTelemetry also
defines the concept of overarching [Resources](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.51.0/specification/resource/sdk.md) with
their own [Resource Semantic Conventions](/docs/resource/README.md).

## General guidelines

**Status**: [Development][DocumentStatus]

When defining new metric names and attributes, consider the prior art of
existing standard metrics and metrics from frameworks/libraries.

Associated metrics SHOULD be nested together in a hierarchy based on their
usage. Define a top-level hierarchy for common metric categories: for OS
metrics, like CPU and network; for app runtimes, like GC internals. Libraries
and frameworks should nest their metrics into a hierarchy as well. This aids
in discovery and adhoc comparison. This allows a user to find similar metrics
given a certain metric.

The hierarchical structure of metrics defines the namespacing. Supporting
OpenTelemetry artifacts define the metric structures and hierarchies for some
categories of metrics, and these can assist decisions when creating future
metrics.

Common attributes SHOULD be consistently named. This aids in discoverability and
disambiguates similar attributes to metric names.

["As a rule of thumb, **aggregations** over all the attributes of a given
metric **SHOULD** be
meaningful,"](https://prometheus.io/docs/practices/naming/#metric-names) as
Prometheus recommends.

Semantic ambiguity SHOULD be avoided. Use prefixed metric names in cases
where similar metrics have significantly different implementations across the
breadth of all existing metrics. For example, every garbage collected runtime
has slightly different strategies and measures. Using a single set of metric
names for GC, not divided by the runtime, could create dissimilar comparisons
and confusion for end users. (For example, prefer `jvm.gc*` over
`gc.*`.) Measures of many operating system metrics are similarly
ambiguous.

Metric names and attributes SHOULD follow the general [naming guidelines](naming.md).

### Units

Conventional metrics or metrics that have their units included in
OpenTelemetry metadata (e.g. `metric.WithUnit` in Go) SHOULD NOT include the
units in the metric name. Units may be included when it provides additional
meaning to the metric name. Metrics MUST, above all, be understandable and
usable.

When building components that interoperate between OpenTelemetry and a system
using the OpenMetrics exposition format, use the
[OpenMetrics Guidelines](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.51.0/specification/compatibility/prometheus_and_openmetrics.md).

### Instrument units

**Status**: [Stable][DocumentStatus]

Units should follow the
[Unified Code for Units of Measure](https://ucum.org/ucum).

- Instruments for **utilization** metrics (that measure the fraction out of a
total) are dimensionless and SHOULD use the default unit `1` (the unity).
- All non-units that use curly braces to annotate a quantity need to match the
  grammatical number of the quantity it represent. For example if measuring the
  number of individual requests to a process the unit would be `{request}`, not
  `{requests}`.
- Instruments that measure an integer count of something SHOULD only use
[annotations](https://ucum.org/ucum.html#para-curly) with curly braces to
give additional meaning *without* the leading default unit (`1`). For example,
use `{packet}`, `{error}`, `{fault}`, etc.
- Instrument units other than `1` and those that use
  [annotations](https://ucum.org/ucum.html#para-curly) SHOULD be specified using
  the UCUM case sensitive ("c/s") variant.
  For example, "Cel" for the unit with full name "degree Celsius".
- Instruments SHOULD use non-prefixed units (i.e. `By` instead of `MiBy`)
  unless there is good technical reason to not do so.
- When instruments are measuring durations, seconds (i.e. `s`) SHOULD be used.

### Instrument types

**Status**: [Stable][DocumentStatus]

The semantic metric conventions specification is written to use the names of the synchronous instrument types,
like `Counter` or `UpDownCounter`. However, compliant implementations MAY use the asynchronous equivalent instead,
like `Asynchronous Counter` or `Asynchronous UpDownCounter`.
Whether implementations choose the synchronous type or the asynchronous equivalent is considered to be an
implementation detail. Both choices are compliant with this specification.

### Consistent UpDownCounter timeseries

**Status**: [Development][DocumentStatus]

When recording `UpDownCounter` metrics, the same attribute values used to record an increment SHOULD be used to record
any associated decrement, otherwise those increments and decrements will end up as different timeseries.

For example, if you are tracking `active_requests` with an `UpDownCounter`, and you are incrementing it each time a
request starts and decrementing it each time a request ends, then any attributes which are not yet available when
incrementing the counter at request start should not be used when decrementing the counter at request end.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
