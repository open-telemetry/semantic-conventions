<!--- Hugo front matter used to generate the website version of this page:
linkTitle: OTel Export
--->

# Semantic Conventions for OTel Export Metrics

**Status**: [Experimental][DocumentStatus]

This document describes instruments and attributes for OTel
Export level metrics. Consider the [general metric semantic
conventions](README.md#general-metric-semantic-conventions) when creating
instruments not explicitly defined in the specification.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Metric Instruments](#metric-instruments)
  * [Metric: `otel.processor.spans`](#metric-otelprocessorspans)
  * [Metric: `otel.exporter.spans`](#metric-otelexporterspans)

<!-- tocstop -->

## Metric Instruments

### Metric: `otel.processor.spans`

This metric is [required][MetricRequired].

<!-- semconv metric.otel.processor.spans(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `otel.processor.spans` | Counter | `{span}` | Measures the number of processed Spans. |
<!-- endsemconv -->

<!-- semconv metric.otel.processor.spans(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `processor.dropped` | boolean | Whether the Span was dropped or not. [1] |  | Required |
| `processor.type` | string | Type of processor being used. | `BatchSpanProcessor` | Recommended |

**[1]:** Spans may be dropped if the internal buffer is full.
<!-- endsemconv -->

### Metric: `otel.exporter.spans`

This metric is [required][MetricRequired].

<!-- semconv metric.otel.exporter.spans(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `otel.exporter.spans` | Counter | `{span}` | Measures the number of exported Spans. |
<!-- endsemconv -->

<!-- semconv metric.otel.exporter.spans(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `exporter.dropped` | boolean | Whether the Span was dropped or not. [1] |  | Required |
| `exporter.type` | string | Type of exporter being used. | `OtlpGrpcSpanExporter` | Recommended |

**[1]:** Spans may be dropped in case of failed ingestion, e.g. network problem or the exported endpoint being down.
<!-- endsemconv -->

[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.22.0/specification/metrics/metric-requirement-level.md#required
