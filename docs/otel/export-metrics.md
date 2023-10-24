<!--- Hugo front matter used to generate the website version of this page:
linkTitle: OpenTelemetry Export
--->

# Semantic Conventions for OpenTelemetry Export Metrics

**Status**: [Experimental][DocumentStatus]

This document describes instruments and attributes for OpenTelemetry
collection-level metrics. Consider the [general metric semantic
conventions](README.md#general-metric-semantic-conventions) when creating
instruments not explicitly defined in the specification.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Metric Instruments](#metric-instruments)
  * [Metric: `otel.processor.items`](#metric-otelprocessoritems)
  * [Metric: `otel.exporter.items`](#metric-otelexporteritems)

<!-- tocstop -->

## Principles used

This specification defines three levels of detail possible, allowing
for components to be used with `basic`, `normal`, and `detailed`
levels that determine which attributes are kept or removed, as by a
[Metric
view](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view).  We
rely on a conservation principle for pipelines, which states generally
that what goes in, comes out.

### Signal-independent metric names

OpenTelemetry currently has 3 signal types, but it may add more.
Instead of using the signal name in the metric names, we opt for a
general-purpose noun that usefully describes any signal.  The
signal-agnostic term used here is `items`, referring to spans, log
records, and metric data points.  An attribute to distinguish the
`signal` is used, with names designated by the project `traces`,
`logs`, and `metrics`.

Users are expected to understand that the data item for traces is a
span, for logs is a record, and for metrics is a point.

### Distinguishing Collectors from SDKs

SDKs and Collectors process the same data in a pipeline, and both
OpenTelemetry Collector and SDKs are recommended to use the metric
names specified here.  An attribute to distinguish the `domain` is
used, with values like `sdk`, `collector`.

In a multi-level collection pipeline, each layer is expected to use a
unique domain.  This enables calculating aggregates at each level in
the collection pipeline and comparing them, as a measure of aggregate
leakage.  Multi-level colletor topologies should allow configuration
of distinct domains (e.g., `agent` and `gateway`).

### Basic level of detail

At the basic level of detail, we only need to know what goes in to a
component, because we are able to infer a lot about the component by
comparing its metrics with the next component in the pipeline.  By
conservation, for example, any items that are received by a SDK
processor component and are not received by the SDK exporter component
must have been dropped.

Therefore at the basic level of detail, all items of data are counted
when they are done, regardless of the outcome.  No additional
attributes are used at this level of detail.

### Normal level of detail

At the normal level of detail, an attribute is introduced that
distinguishes whether the item was or was not successful.  A boolean
attribute `success` is introduced at this level.

It is understood that components have limited information about the
success or failure of subsequent pipeline components.  While the
veracity of `success=true` may be subject to reasonable doubt, the
`success=false` attribute should be accepted as fact.  In a SDK
configuration, the processor's `success=false` may be compared with
the exporter's `success=false` to determine the number of items
dropped by the processor, for example.

### Detailed metrics

At the detailed level of metrics, the component includes an additional
`status` to explain its outcomes.  These should be interpreted
relative to the value of the `success` attribute, which is always
present when detailed metrics are in use.  For the `success=true`
case, components may are recommended to use `reason=ok`.

Components should use short, descriptive names to explain failure
outcomes.  For example, a SDK span processor could use
`reason=queue_full` to annotate dropped spans and
`reason=export_failed` to indicate when the exporter failed.

Exporter components are encouraged to use system specific details as
the reason.  For example, gRPC-based exporter would naturally use the
string form of the gRPC status code as the reason (e.g.,
`deadline_exceeded`, `resource_exhausted`, `unimplemented`).

### Component types and optional names

Components are uniquely identified using a descriptive `name`
attribute which encompasses at least a short name describing the type
of component being used (e.g., `batch` for the SDK BatchSpanProcessor
or the Collector batch proessor).

When there is more than one component of a given type active in a
pipeline having the same `domain` and `signal` attributes, the `name`
should include additional information to disambiguate the multiple
instances using the syntax `<type>/<instance>`.  For example, if there
were two `batch` processors in a collection pipeline (e.g., one for
error spans and one for non-error spans) they might use the names
`batch/error` and `batch/noerror`.

### Use of scope attributes

The `domain`, `signal`, and `name` attributes described here are
considered scope attributes.  When these metrics are encoded using an
OTLP data representation, the `domain`, `signal`, and `name`
attributes SHOULD be encoded using ther OTLP Scope attributes field.


| Attribute  | Type | Description  | Examples  | Requirement Level | Detail level |
|---|---|---|---|---|
| `<prefix>.domain` | string | Domain of the pipeline with this component | `sdk`, `collector` | Required | Basic |
| `<prefix>.name` | string | Type and optional name of this component. | `batch`, `batch/errors` | Required | Basic |
| `<prefix>.signal` | string | Type of signal being described. | `trace`, `logs`, `metrics` | Required | Basic |

## Metric Instruments

### Metric: `otel.processor.items`

This metric is [required][MetricRequired].

<!-- semconv metric.otel.processor.items(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `otel.processor.items` | Counter | `{items}` | Measures the number of processed items (signal specific). |
<!-- endsemconv -->


<!-- semconv metric.otel.processor.items(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level | Detail Level |
|---|---|---|---|---|
| `processor.name` | string | Type and optional name of processor being used. | `batch` | Required | Basic |
| `processor.success` | boolean | Whether the item was successful or not. [1] | true, false | Recommended | Normal |
| `processor.reason` | string | Short string explaining category of success and failure. | `ok`, `queue_full`, `timeout`, `permission_denied` | Recommended | Detailed |

**[1]:** Consider `success=false` a stronger signal than `success=true`
<!-- endsemconv -->

### Metric: `otel.exporter.items`

This metric is [required][MetricRequired].

<!-- semconv metric.otel.exporter.items(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `otel.exporter.items` | Counter | `{items}` | Measures the number of exported items (signal specific). |
<!-- endsemconv -->

<!-- semconv metric.otel.exporter.items(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `exporter.name` | string | Type and optional name of exporter being used. | `otlp/grpc` | Required | Basic |
| `exporter.success` | boolean | Whether the item was successful or not. [1] | true, false | Recommended | Normal |
| `exporter.reason` | string | Short string explaining category of success and failure. | `ok`, `queue_full`, `timeout`, `permission_denied` | Recommended | Detailed |

**[1]:** Items may be dropped in case of failed ingestion, e.g. network problem or the exported endpoint being down.  Consult transport-specific instrumentation for more information about the export requests themselves, including retry attempts.
<!-- endsemconv -->

[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.22.0/specification/metrics/metric-requirement-level.md#required
