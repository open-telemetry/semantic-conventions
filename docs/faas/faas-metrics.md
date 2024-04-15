<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
--->

# Semantic Conventions for FaaS Metrics

**Status**: [Experimental][DocumentStatus]

This document defines how to describe an instance of a function that runs without provisioning
or managing of servers (also known as serverless functions or Function as a Service (FaaS)) with metrics.

The conventions described in this section are FaaS (function as a service) specific. When FaaS operations occur,
metric events about those operations will be generated and reported to provide insights into the
operations. By adding FaaS attributes to metric events it allows for finely tuned filtering.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Metric Instruments](#metric-instruments)
  - [FaaS Instance](#faas-instance)
    - [Metric: `faas.invoke_duration`](#metric-faasinvoke_duration)
    - [Metric: `faas.init_duration`](#metric-faasinit_duration)
    - [Metric: `faas.coldstarts`](#metric-faascoldstarts)
    - [Metric: `faas.errors`](#metric-faaserrors)
    - [Metric: `faas.invocations`](#metric-faasinvocations)
    - [Metric: `faas.timeouts`](#metric-faastimeouts)
    - [Metric: `faas.mem_usage`](#metric-faasmem_usage)
    - [Metric: `faas.cpu_usage`](#metric-faascpu_usage)
    - [Metric: `faas.net_io`](#metric-faasnet_io)
- [References](#references)
  - [Metric References](#metric-references)

<!-- tocstop -->

## Metric Instruments

The following metric instruments describe FaaS operations.

### FaaS Instance

The following metrics are recorded by the FaaS instance.

#### Metric: `faas.invoke_duration`

This metric is [recommended][MetricRecommended].

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/metrics/api.md#instrument-advice)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.faas.invoke_duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.invoke_duration` | Histogram | `s` | Measures the duration of the function's logic execution | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.invoke_duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

#### Metric: `faas.init_duration`

This metric is [recommended][MetricRecommended].

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/metrics/api.md#instrument-advice)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.faas.init_duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.init_duration` | Histogram | `s` | Measures the duration of the function's initialization, such as a cold start | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.init_duration(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

#### Metric: `faas.coldstarts`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.coldstarts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.coldstarts` | Counter | `{coldstart}` | Number of invocation cold starts | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.coldstarts(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

#### Metric: `faas.errors`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.errors(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.errors` | Counter | `{error}` | Number of invocation errors | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.errors(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

#### Metric: `faas.invocations`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.invocations(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.invocations` | Counter | `{invocation}` | Number of successful invocations | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.invocations(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

#### Metric: `faas.timeouts`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.timeouts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.timeouts` | Counter | `{timeout}` | Number of invocation timeouts | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.timeouts(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

#### Metric: `faas.mem_usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.mem_usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.mem_usage` | Histogram | `By` | Distribution of max memory usage per invocation | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.mem_usage(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

#### Metric: `faas.cpu_usage`

This metric is [recommended][MetricRecommended].

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/metrics/api.md#instrument-advice)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.faas.cpu_usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.cpu_usage` | Histogram | `s` | Distribution of CPU usage per invocation | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.cpu_usage(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

#### Metric: `faas.net_io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.net_io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `faas.net_io` | Histogram | `By` | Distribution of net I/O usage per invocation | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.faas.net_io(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`faas.trigger`](../attributes-registry/faas.md) | string | Type of the trigger which caused this function invocation. | `datasource` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`faas.trigger` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `http` | To provide an answer to an inbound HTTP request | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `timer` | A function is scheduled to be executed regularly | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | If none of the others apply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## References

### Metric References

Below are links to documentation regarding metrics that are available with different
FaaS providers. This list is not exhaustive.

* [AWS Lambda Metrics](https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics.html)
* [AWS Lambda Insight Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-metrics.html)
* [Azure Functions Metrics](https://docs.microsoft.com/azure/azure-monitor/platform/metrics-supported)
* [Google CloudFunctions Metrics](https://cloud.google.com/monitoring/api/metrics_gcp#gcp-cloudfunctions)
* [OpenFaas Metrics](https://docs.openfaas.com/architecture/metrics/)

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
