# Cloud

**Status**: [Experimental][DocumentStatus]

**type:** `cloud`

**Description:** A cloud infrastructure (e.g. GCP, Azure, AWS).

<!-- semconv cloud -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`cloud.account.id`](../attributes-registry/cloud.md) | string | The cloud account ID the resource is assigned to. | `111111111111`; `opentelemetry` | Recommended |
| [`cloud.availability_zone`](../attributes-registry/cloud.md) | string | Cloud regions often have multiple, isolated locations known as zones to increase availability. Availability zone represents the zone where the resource is running. [1] | `us-east-1c` | Recommended |
| [`cloud.platform`](../attributes-registry/cloud.md) | string | The cloud platform in use. [2] | `alibaba_cloud_ecs` | Recommended |
| [`cloud.provider`](../attributes-registry/cloud.md) | string | Name of the cloud provider. | `alibaba_cloud` | Recommended |
| [`cloud.region`](../attributes-registry/cloud.md) | string | The geographical region the resource is running. [3] | `us-central1`; `us-east-1` | Recommended |
| [`cloud.resource_id`](../attributes-registry/cloud.md) | string | Cloud provider-specific native identifier of the monitored cloud resource (e.g. an [ARN](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) on AWS, a [fully qualified resource ID](https://learn.microsoft.com/rest/api/resources/resources/get-by-id) on Azure, a [full resource name](https://cloud.google.com/apis/design/resource_names#full_resource_name) on GCP) [4] | `arn:aws:lambda:REGION:ACCOUNT_ID:function:my-function`; `//run.googleapis.com/projects/PROJECT_ID/locations/LOCATION_ID/services/SERVICE_ID`; `/subscriptions/<SUBSCIPTION_GUID>/resourceGroups/<RG>/providers/Microsoft.Web/sites/<FUNCAPP>/functions/<FUNC>` | Recommended |

**[1]:** Availability zones are called "zones" on Alibaba Cloud and Google Cloud.

**[2]:** The prefix of the service SHOULD match the one specified in `cloud.provider`.

**[3]:** Refer to your provider's docs to see the available regions, for example [Alibaba Cloud regions](https://www.alibabacloud.com/help/doc-detail/40654.htm), [AWS regions](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/), [Azure regions](https://azure.microsoft.com/global-infrastructure/geographies/), [Google Cloud regions](https://cloud.google.com/about/locations), or [Tencent Cloud regions](https://www.tencentcloud.com/document/product/213/6091).

**[4]:** On some cloud providers, it may not be possible to determine the full ID at startup,
so it may be necessary to set `cloud.resource_id` as a span attribute instead.

The exact value to use for `cloud.resource_id` depends on the cloud provider.
The following well-known definitions MUST be used if you set this attribute and they apply:

* **AWS Lambda:** The function [ARN](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html).
  Take care not to use the "invoked ARN" directly but replace any
  [alias suffix](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html)
  with the resolved function version, as the same runtime instance may be invokable with
  multiple different aliases.
* **GCP:** The [URI of the resource](https://cloud.google.com/iam/docs/full-resource-names)
* **Azure:** The [Fully Qualified Resource ID](https://docs.microsoft.com/rest/api/resources/resources/get-by-id) of the invoked function,
  *not* the function app, having the form
  `/subscriptions/<SUBSCIPTION_GUID>/resourceGroups/<RG>/providers/Microsoft.Web/sites/<FUNCAPP>/functions/<FUNC>`.
  This means that a span attribute MUST be used, as an Azure function app can host multiple functions that would usually share
  a TracerProvider.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
