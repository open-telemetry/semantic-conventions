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

**Disclaimer:** These are initial FaaS metric instruments and attributes but more may be added in the future.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Metric Instruments](#metric-instruments)
  * [Metric: `faas.invoke_duration`](#metric-faasinvoke_duration)
  * [Metric: `faas.init_duration`](#metric-faasinit_duration)
  * [Metric: `faas.coldstarts`](#metric-faascoldstarts)
  * [Metric: `faas.errors`](#metric-faaserrors)
  * [Metric: `faas.invocations`](#metric-faasinvocations)
  * [Metric: `faas.timeouts`](#metric-faastimeouts)
  * [Metric: `faas.mem_usage`](#metric-faasmem_usage)
  * [Metric: `faas.cpu_usage`](#metric-faascpu_usage)
  * [Metric: `faas.net_io`](#metric-faasnet_io)
- [Attributes](#attributes)
- [References](#references)
  * [Metric References](#metric-references)

<!-- tocstop -->

## Metric Instruments

The following metric instruments describe FaaS operations.

### Metric: `faas.invoke_duration`

This metric is [required][MetricRequired].

<!-- semconv metric.faas.invoke_duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.invoke_duration` | Histogram | `ms` | Measures the duration of the invocation |
<!-- endsemconv -->

<!-- semconv metric.faas.invoke_duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->

### Metric: `faas.init_duration`

This metric is [required][MetricRequired].

<!-- semconv metric.faas.init_duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.init_duration` | Histogram | `ms` | Measures the duration of the function's initialization, such as a cold start |
<!-- endsemconv -->

<!-- semconv metric.faas.init_duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->

### Metric: `faas.coldstarts`

This metric is [required][MetricRequired].

<!-- semconv metric.faas.coldstarts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.coldstarts` | Counter | `{coldstart}` | Number of invocation cold starts |
<!-- endsemconv -->

<!-- semconv metric.faas.coldstarts(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->

### Metric: `faas.errors`

This metric is [required][MetricRequired].

<!-- semconv metric.faas.errors(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.errors` | Counter | `{error}` | Number of invocation errors |
<!-- endsemconv -->

<!-- semconv metric.faas.errors(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->

### Metric: `faas.invocations`

This metric is [required][MetricRequired].

<!-- semconv metric.faas.invocations(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.invocations` | Counter | `{invocation}` | Number of successful invocations |
<!-- endsemconv -->

<!-- semconv metric.faas.invocations(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->

### Metric: `faas.timeouts`

This metric is [required][MetricRequired].

<!-- semconv metric.faas.timeouts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.timeouts` | Counter | `{timeout}` | Number of invocation timeouts |
<!-- endsemconv -->

<!-- semconv metric.faas.timeouts(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->

### Metric: `faas.mem_usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.mem_usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.mem_usage` | Histogram | `By` | Distribution of max memory usage per invocation |
<!-- endsemconv -->

<!-- semconv metric.faas.mem_usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->

### Metric: `faas.cpu_usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.cpu_usage(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.cpu_usage` | Histogram | `ms` | Distribution of CPU usage per invocation |
<!-- endsemconv -->

<!-- semconv metric.faas.cpu_usage(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->

### Metric: `faas.net_io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.faas.net_io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `faas.net_io` | Histogram | `By` | Distribution of net I/O usage per invocation |
<!-- endsemconv -->

<!-- semconv metric.faas.net_io(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.invoked_name` | string | The name of the invoked function. [1] | `my-function` | Required |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [2] | `alibaba_cloud` | Required |
| `faas.invoked_region` | string | The cloud region of the invoked function. [3] | `eu-central-1` | Conditionally Required: [4] |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` | Recommended |

**[1]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[2]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[4]:** For some cloud providers, like AWS or GCP, the region in which a function is hosted is essential to uniquely identify the function and also part of its endpoint. Since it's part of the endpoint being called, the region is always known to clients. In these cases, `faas.invoked_region` MUST be set accordingly. If the region is unknown to the client or not required for identifying the invoked function, setting `faas.invoked_region` is optional.

`faas.invoked_provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `alibaba_cloud` | Alibaba Cloud |
| `aws` | Amazon Web Services |
| `azure` | Microsoft Azure |
| `gcp` | Google Cloud Platform |
| `tencent_cloud` | Tencent Cloud |

`faas.trigger` MUST be one of the following:

| Value  | Description |
|---|---|
| `datasource` | A response to some data source operation such as a database or filesystem read/write |
| `http` | To provide an answer to an inbound HTTP request |
| `pubsub` | A function is set to be executed when messages are sent to a messaging system |
| `timer` | A function is scheduled to be executed regularly |
| `other` | If none of the others apply |
<!-- endsemconv -->
>>>>>>> 1cf9e98 (Generate FaaS metrics from YAML)

## Attributes

More details on these attributes, the function name and the difference compared to the faas.invoked_name can be found at the related [FaaS tracing specification](faas-spans.md).
For incoming FaaS invocations, the function for which metrics are reported is already described by its [FaaS resource attributes](/docs/resource/faas.md).
Outgoing FaaS invocations are identified using the `faas.invoked_*` attributes above.
`faas.trigger` SHOULD be included in all metric events while `faas.invoked_*` attributes apply on outgoing FaaS invocation events only.

## References

### Metric References

Below are links to documentation regarding metrics that are available with different
FaaS providers. This list is not exhaustive.

* [AWS Lambda Metrics](https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics.html)
* [AWS Lambda Insight Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-metrics.html)
* [Azure Functions Metrics](https://docs.microsoft.com/azure/azure-monitor/platform/metrics-supported)
* [Google CloudFunctions Metrics](https://cloud.google.com/monitoring/api/metrics_gcp#gcp-cloudfunctions)
* [OpenFaas Metrics](https://docs.openfaas.com/architecture/metrics/)

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
[MetricRequired]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/metric-requirement-level.md#required
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/metrics/metric-requirement-level.md#recommended
