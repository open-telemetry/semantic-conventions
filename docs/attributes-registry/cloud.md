
<!--- Hugo front matter used to generate the website version of this page:
--->

# CLOUD

- [cloud](#cloud)


## cloud Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `cloud.account.id` | string | The cloud account ID the resource is assigned to.  | `111111111111`; `opentelemetry` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cloud.availability_zone` | string | Cloud regions often have multiple, isolated locations known as zones to increase availability. Availability zone represents the zone where the resource is running. [1] | `us-east-1c` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cloud.platform` | string | The cloud platform in use. [2] | `alibaba_cloud_ecs`; `alibaba_cloud_fc`; `alibaba_cloud_openshift`; `aws_ec2`; `aws_ecs`; `aws_eks`; `aws_lambda`; `aws_elastic_beanstalk`; `aws_app_runner`; `aws_openshift`; `azure_vm`; `azure_container_apps`; `azure_container_instances`; `azure_aks`; `azure_functions`; `azure_app_service`; `azure_openshift`; `gcp_bare_metal_solution`; `gcp_compute_engine`; `gcp_cloud_run`; `gcp_kubernetes_engine`; `gcp_cloud_functions`; `gcp_app_engine`; `gcp_openshift`; `ibm_cloud_openshift`; `tencent_cloud_cvm`; `tencent_cloud_eks`; `tencent_cloud_scf` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cloud.provider` | string | Name of the cloud provider.  | `alibaba_cloud`; `aws`; `azure`; `gcp`; `heroku`; `ibm_cloud`; `tencent_cloud` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cloud.region` | string | The geographical region the resource is running. [3] | `us-central1`; `us-east-1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cloud.resource_id` | string | Cloud provider-specific native identifier of the monitored cloud resource (e.g. an [ARN](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) on AWS, a [fully qualified resource ID](https://learn.microsoft.com/rest/api/resources/resources/get-by-id) on Azure, a [full resource name](https://cloud.google.com/apis/design/resource_names#full_resource_name) on GCP) [4] | `arn:aws:lambda:REGION:ACCOUNT_ID:function:my-function`; `//run.googleapis.com/projects/PROJECT_ID/locations/LOCATION_ID/services/SERVICE_ID`; `/subscriptions/<SUBSCIPTION_GUID>/resourceGroups/<RG>/providers/Microsoft.Web/sites/<FUNCAPP>/functions/<FUNC>` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|

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


`cloud.platform` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `alibaba_cloud_ecs` | Alibaba Cloud Elastic Compute Service |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `alibaba_cloud_fc` | Alibaba Cloud Function Compute |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `alibaba_cloud_openshift` | Red Hat OpenShift on Alibaba Cloud |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_ec2` | AWS Elastic Compute Cloud |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_ecs` | AWS Elastic Container Service |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_eks` | AWS Elastic Kubernetes Service |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_lambda` | AWS Lambda |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_elastic_beanstalk` | AWS Elastic Beanstalk |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_app_runner` | AWS App Runner |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws_openshift` | Red Hat OpenShift on AWS (ROSA) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `azure_vm` | Azure Virtual Machines |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `azure_container_apps` | Azure Container Apps |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `azure_container_instances` | Azure Container Instances |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `azure_aks` | Azure Kubernetes Service |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `azure_functions` | Azure Functions |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `azure_app_service` | Azure App Service |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `azure_openshift` | Azure Red Hat OpenShift |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_bare_metal_solution` | Google Bare Metal Solution (BMS) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_compute_engine` | Google Cloud Compute Engine (GCE) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_cloud_run` | Google Cloud Run |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_kubernetes_engine` | Google Cloud Kubernetes Engine (GKE) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_cloud_functions` | Google Cloud Functions (GCF) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_app_engine` | Google Cloud App Engine (GAE) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp_openshift` | Red Hat OpenShift on Google Cloud |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ibm_cloud_openshift` | Red Hat OpenShift on IBM Cloud |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tencent_cloud_cvm` | Tencent Cloud Cloud Virtual Machine (CVM) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tencent_cloud_eks` | Tencent Cloud Elastic Kubernetes Service (EKS) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tencent_cloud_scf` | Tencent Cloud Serverless Cloud Function (SCF) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`cloud.provider` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `alibaba_cloud` | Alibaba Cloud |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws` | Amazon Web Services |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `azure` | Microsoft Azure |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp` | Google Cloud Platform |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `heroku` | Heroku Platform as a Service |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ibm_cloud` | IBM Cloud |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tencent_cloud` | Tencent Cloud |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |

