<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
aliases: [docs/specs/semconv/general/metrics-general]
--->

# Metrics Semantic Conventions

**Status**: [Mixed][DocumentStatus]

<!-- toc -->

- [General Guidelines](#general-guidelines)
  - [Name Reuse Prohibition](#name-reuse-prohibition)
  - [Metric attributes](#metric-attributes)
  - [Units](#units)
  - [Naming rules for Counters and UpDownCounters](#naming-rules-for-counters-and-updowncounters)
    - [Pluralization](#pluralization)
    - [Use `count` Instead of Pluralization for UpDownCounters](#use-count-instead-of-pluralization-for-updowncounters)
    - [Do not use `total`](#do-not-use-total)
- [General Metric Semantic Conventions](#general-metric-semantic-conventions)
  - [Instrument Naming](#instrument-naming)
  - [Instrument Units](#instrument-units)
  - [Instrument Types](#instrument-types)
  - [Consistent UpDownCounter timeseries](#consistent-updowncounter-timeseries)

<!-- tocstop -->

The following semantic conventions surrounding metrics are defined:

* **[General Guidelines](#general-guidelines): General metrics guidelines.**
* [Database](/docs/database/database-metrics.md): For SQL and NoSQL client metrics.
* [FaaS](/docs/faas/faas-metrics.md): For [Function as a Service](https://wikipedia.org/wiki/Function_as_a_service) metrics.
* [HTTP](/docs/http/http-metrics.md): For HTTP client and server metrics.
* [Messaging](/docs/messaging/messaging-metrics.md): For messaging systems (queues, publish/subscribe, etc.) metrics.
* [RPC](/docs/rpc/rpc-metrics.md): For RPC client and server metrics.
* **System metrics**
  * [System](/docs/system/system-metrics.md): For standard system metrics.
  * [Hardware](/docs/system/hardware-metrics.md): For hardware-related metrics.
  * [Process](/docs/system/process-metrics.md): For standard process metrics.
  * [Runtime Environment](/docs/runtime/README.md#metrics): For runtime environment metrics.

Apart from semantic conventions for metrics, [traces](trace.md), [logs](logs.md), and [events](events.md), OpenTelemetry also
defines the concept of overarching [Resources](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/resource/sdk.md) with
their own [Resource Semantic Conventions](/docs/resource/README.md).

## General Guidelines

**Status**: [Experimental][DocumentStatus]

Metric names and attributes exist within a single universe and a single
hierarchy. Metric names and attributes MUST be considered within the universe of
all existing metric names. When defining new metric names and attributes,
consider the prior art of existing standard metrics and metrics from
frameworks/libraries.

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
and confusion for end users. (For example, prefer `process.runtime.java.gc*` over
`process.runtime.gc.*`.) Measures of many operating system metrics are similarly
ambiguous.

### Name Reuse Prohibition

A new metric MUST NOT be added with the same name as a metric that existed in
the past but was renamed (with a corresponding schema file).

When introducing a new metric name check all existing schema files to make sure
the name does not appear as a key of any "rename_metrics" section (keys denote
old metric names in rename operations).

### Metric attributes

Metric attributes SHOULD follow the general [attribute naming rules](attribute-naming.md).
In particular, metric attributes SHOULD have a namespace.

Metric attributes SHOULD be added under the metric namespace when their usage and
semantics are exclusive to the metric.

Examples:

Attributes `mode` and `mountpoint` for metric `system.filesystem.usage`
should be namespaced as `system.filesystem.mode` and `system.filesystem.mountpoint`.

Metrics can also have attributes outside of their namespace.

Examples:

Metric `http.server.request.duration` uses attributes from the registry such as
`server.port`, `error.type`.

### Units

Conventional metrics or metrics that have their units included in
OpenTelemetry metadata (e.g. `metric.WithUnit` in Go) SHOULD NOT include the
units in the metric name. Units may be included when it provides additional
meaning to the metric name. Metrics MUST, above all, be understandable and
usable.

When building components that interoperate between OpenTelemetry and a system
using the OpenMetrics exposition format, use the
[OpenMetrics Guidelines](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/compatibility/prometheus_and_openmetrics.md).

### Naming rules for Counters and UpDownCounters

#### Pluralization

Metric namespaces SHOULD NOT be pluralized.

Metric names SHOULD NOT be pluralized, unless the value being recorded
represents discrete instances of a
[countable quantity](https://wikipedia.org/wiki/Count_noun).
Generally, the name SHOULD be pluralized only if the unit of the metric in
question is a non-unit (like `{fault}` or `{operation}`).

Examples:

* `system.filesystem.utilization`, `http.server.request.duration`, and `system.cpu.time`
should not be pluralized, even if many data points are recorded.
* `system.paging.faults`, `system.disk.operations`, and `system.network.packets`
should be pluralized, even if only a single data point is recorded.

#### Use `count` Instead of Pluralization for UpDownCounters

If the value being recorded represents the count of concepts signified
by the namespace then the metric should be named `count` (within its namespace).

For example if we have a namespace `system.process` which contains all metrics related
to the processes then to represent the count of the processes we can have a metric named
`system.process.count`.

#### Do not use `total`

UpDownCounters SHOULD NOT use `_total` because then they will look like
monotonic sums.

Counters SHOULD NOT append `_total` either because then their meaning will
be confusing in delta backends.

## General Metric Semantic Conventions

**Status**: [Mixed][DocumentStatus]

The following semantic conventions aim to keep naming consistent. They
provide guidelines for most of the cases in this specification and should be
followed for other instruments not explicitly defined in this document.

### Instrument Naming

**Status**: [Experimental][DocumentStatus]

- **limit** - an instrument that measures the constant, known total amount of
something should be called `entity.limit`. For example, `system.memory.limit`
for the total amount of memory on a system.

- **usage** - an instrument that measures an amount used out of a known total
(**limit**) amount should be called `entity.usage`. For example,
`system.memory.usage` with attribute `state = used | cached | free | ...` for the
amount of memory in a each state. Where appropriate, the sum of **usage**
over all attribute values SHOULD be equal to the **limit**.

  A measure of the amount consumed of an unlimited resource, or of a resource
  whose limit is unknowable, is differentiated from **usage**. For example, the
  maximum possible amount of virtual memory that a process may consume may
  fluctuate over time and is not typically known.

- **utilization** - an instrument that measures the *fraction* of **usage**
out of its **limit** should be called `entity.utilization`. For example,
`system.memory.utilization` for the fraction of memory in use. Utilization can
be with respect to a fixed limit or a soft limit. Utilization values are
represended as a ratio and are typically in the range `[0, 1]`, but may go above 1
in case of exceeding a soft limit.

- **time** - an instrument that measures passage of time should be called
`entity.time`. For example, `system.cpu.time` with attribute `state = idle | user
| system | ...`. **time** measurements are not necessarily wall time and can
be less than or greater than the real wall time between measurements.

  **time** instruments are a special case of **usage** metrics, where the
  **limit** can usually be calculated as the sum of **time** over all attribute
  values. **utilization** for time instruments can be derived automatically
  using metric event timestamps. For example, `system.cpu.utilization` is
  defined as the difference in `system.cpu.time` measurements divided by the
  elapsed time and number of CPUs.

- **io** - an instrument that measures bidirectional data flow should be
called `entity.io` and have attributes for direction. For example,
`system.network.io`.

- Other instruments that do not fit the above descriptions may be named more
freely. For example, `system.paging.faults` and `system.network.packets`.
Units do not need to be specified in the names since they are included during
instrument creation, but can be added if there is ambiguity.

### Instrument Units

**Status**: [Stable][DocumentStatus]

Units should follow the
[Unified Code for Units of Measure](http://unitsofmeasure.org/ucum.html).

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

### Instrument Types

**Status**: [Stable][DocumentStatus]

The semantic metric conventions specification is written to use the names of the synchronous instrument types,
like `Counter` or `UpDownCounter`. However, compliant implementations MAY use the asynchronous equivalent instead,
like `Asynchronous Counter` or `Asynchronous UpDownCounter`.
Whether implementations choose the synchronous type or the asynchronous equivalent is considered to be an
implementation detail. Both choices are compliant with this specification.

### Consistent UpDownCounter timeseries

**Status**: [Experimental][DocumentStatus]

When recording `UpDownCounter` metrics, the same attribute values used to record an increment SHOULD be used to record
any associated decrement, otherwise those increments and decrements will end up as different timeseries.

For example, if you are tracking `active_requests` with an `UpDownCounter`, and you are incrementing it each time a
request starts and decrementing it each time a request ends, then any attributes which are not yet available when
incrementing the counter at request start should not be used when decrementing the counter at request end.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
