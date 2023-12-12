<!--- Hugo front matter used to generate the website version of this page:
linkTitle: OpenTelemetry Pipeline Metrics
--->

# Semantic Conventions for OpenTelemetry Pipeline Metrics

**Status**: [Experimental][DocumentStatus]

This document describes instruments and attributes for OpenTelemetry
Pipeline metrics, including SDK and Collector components that form a
delivery network for telemetry data.  These metrics are applied to a
reduced set of general-purpose component names, as they are known in
the OpenTelemetry Collector:

- Receiver: a producer of telemetry data that places data into a local pipeline
- Processor: an interior component of a local pipeline
- Exporter: a consumer of telemetry data that sends data into a remote pipeline.

The distinction between local and remote is helpful because as
telemetry data passes through multiple stages in a pipeline, for
example an SDK followed by one or more Collectors, success and failure
depends on both the configuration of the pipeline as well as external
factors.

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

OpenTelemetry specifies two sets of metric names having similar
definitions, one for SDKs and one for Collectors.  Taken as a whole,
these conventions enable comparison of success and failure between
stages of the pipeline.  For example, the total success rate for a
pipeline is defined as the number of data items (i.e., trace spans,
metric data points, log records, etc.)  received at the end of the
pipeline deivided by the of data items produced at the start of the
pipeline

### General-purpose names

The three primary metric name components are `receiver`, `processor`,
and `exporter`.  One of these three should be applied whether or not
it is the actual component type name, considering its logical purpose.

For OpenTelemetry Collectors, the `connector` component should be
described by two sets of pipeline metrics, one `exporter` and one
`receiver`.

For SDKs, the distinction between exporter and processor is documented
in the in the [library
guidelines](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/library-guidelines.md#requirements).
SDKs do not have receiver metrics, only `processor` and `exporter`
definitions apply.

- the Metric Reader pipeline component is described as a `processor`, 
- the Trace Sampler pipeline component is described as a `processor`.

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

### Multi-Collector pipelines

When more than one OpenTelemetry Collector is used in a pipeline,
users are recommended to apply resource-level attributes to the
telemetry emitted in different stages so that stages can be easily
distinguished when applying aggregation.  TODO: see #554.

## Metric Instruments

### Metric: `otelsdk.exporter.items`

This metric is [required][MetricRequired] for OpenTelemetry Collectors.

<!-- semconv metric.otel.exporter.items(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `otelcol.receiver.items` | Counter | `{items}` | Measures the number of received items (signal specific) in an OpenTelemetry Collector. |
<!-- endsemconv -->

<!-- semconv metric.otel.exporter.items(full) -->
| Attribute          | Type    | Description                                              | Examples                                           | Requirement Level |
|--------------------|---------|----------------------------------------------------------|----------------------------------------------------|-------------------|
| `exporter.name`    | string  | Type and optional name of this exporter.                 | `otlp/http`, `otlp/grpc`                           | Required          |
| `exporter.signal`  | string  | Type of signal being described.                          | `trace`, `logs`, `metrics`                         | Required          |
| `exporter.success` | boolean | Whether the item was successful or not. [1]              | true, false                                        | Recommended       |
| `exporter.reason`  | string  | Short string explaining category of success and failure. | `ok`, `queue_full`, `timeout`, `permission_denied` | Detailed          |

### Metric: `otelsdk.processor.items`, `otelcol.processor.items`

This metric is [required][MetricRequired].

<!-- semconv metric.otel.processor.items(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `otelsdk.processor.items` | Counter | `{items}` | Measures the number of processed items (signal specific) in an OpenTelemetry SDK. |
| `otelcol.processor.items` | Counter | `{items}` | Measures the number of processed items (signal specific) in an OpenTelemetry Collector. |
<!-- endsemconv -->


<!-- semconv metric.otel.processor.items(full) -->
| Attribute           | Type    | Description                                              | Examples                                           | Requirement Level |
|---------------------|---------|----------------------------------------------------------|----------------------------------------------------|-------------------|
| `processor.name`    | string  | Type and optional name of this exporter.                 | `batch`, `batch/errors`                            | Required          |
| `processor.signal`  | string  | Type of signal being described.                          | `trace`, `logs`, `metrics`                         | Required          |
| `processor.success` | boolean | Whether the item was successful or not. [1]              | true, false                                        | Recommended       |
| `processor.reason`  | string  | Short string explaining category of success and failure. | `ok`, `queue_full`, `timeout`, `permission_denied` | Detailed          |

**[1]:** Consider `success=false` a stronger signal than `success=true`
<!-- endsemconv -->

### Metric: `otelsdk.exporter.items`

This metric is [required][MetricRequired].

<!-- semconv metric.otel.exporter.items(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `otelcol.exporter.items` | Counter | `{items}` | Measures the number of exported items (signal specific) in an OpenTelemetry SDK. |
| `otelsdk.exporter.items` | Counter | `{items}` | Measures the number of exported items (signal specific) in an OpenTelemetry Collector. |
<!-- endsemconv -->

<!-- semconv metric.otel.exporter.items(full) -->
| Attribute          | Type    | Description                                              | Examples                                           | Requirement Level |
|--------------------|---------|----------------------------------------------------------|----------------------------------------------------|-------------------|
| `exporter.name`    | string  | Type and optional name of this exporter.                 | `otlp/http`, `otlp/grpc`                           | Required          |
| `exporter.signal`  | string  | Type of signal being described.                          | `trace`, `logs`, `metrics`                         | Required          |
| `exporter.success` | boolean | Whether the item was successful or not. [1]              | true, false                                        | Recommended       |
| `exporter.reason`  | string  | Short string explaining category of success and failure. | `ok`, `queue_full`, `timeout`, `permission_denied` | Detailed          |

**[1]:** Items may be dropped in case of failed ingestion, e.g. network problem or the exported endpoint being down.  Consult transport-specific instrumentation for more information about the export requests themselves, including retry attempts.
<!-- endsemconv -->

[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.22.0/specification/metrics/metric-requirement-level.md#required
