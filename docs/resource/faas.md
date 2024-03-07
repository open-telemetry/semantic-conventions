# Function as a Service

**Status**: [Experimental][DocumentStatus]

**type:** `faas`

**Description:** A "function as a service" aka "serverless function" instance.

See also:

- The [Trace semantic conventions for FaaS](/docs/faas/faas-spans.md)
- The [Cloud resource conventions](cloud.md)

## FaaS resource attributes

<!-- semconv faas_resource -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`cloud.resource_id`](../attributes-registry/cloud.md) | string | Cloud provider-specific native identifier of the monitored cloud resource (e.g. an [ARN](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) on AWS, a [fully qualified resource ID](https://learn.microsoft.com/rest/api/resources/resources/get-by-id) on Azure, a [full resource name](https://cloud.google.com/apis/design/resource_names#full_resource_name) on GCP) [1] | `arn:aws:lambda:REGION:ACCOUNT_ID:function:my-function`; `//run.googleapis.com/projects/PROJECT_ID/locations/LOCATION_ID/services/SERVICE_ID`; `/subscriptions/<SUBSCIPTION_GUID>/resourceGroups/<RG>/providers/Microsoft.Web/sites/<FUNCAPP>/functions/<FUNC>` | Recommended |
| [`faas.instance`](../attributes-registry/faas.md) | string | The execution environment ID as a string, that will be potentially reused for other invocations to the same function/function version. [2] | `2021/06/28/[$LATEST]2f399eb14537447da05ab2a2e39309de` | Recommended |
| [`faas.max_memory`](../attributes-registry/faas.md) | int | The amount of memory available to the serverless function converted to Bytes. [3] | `134217728` | Recommended |
| [`faas.name`](../attributes-registry/faas.md) | string | The name of the single function that this runtime instance executes. [4] | `my-function`; `myazurefunctionapp/some-function-name` | Required |
| [`faas.version`](../attributes-registry/faas.md) | string | The immutable version of the function being executed. [5] | `26`; `pinkfroid-00002` | Recommended |

**[1]:** On some cloud providers, it may not be possible to determine the full ID at startup,
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

**[2]:** * **AWS Lambda:** Use the (full) log stream name.

**[3]:** It's recommended to set this attribute since e.g. too little memory can easily stop a Java AWS Lambda function from working correctly. On AWS Lambda, the environment variable `AWS_LAMBDA_FUNCTION_MEMORY_SIZE` provides this information (which must be multiplied by 1,048,576).

**[4]:** This is the name of the function as configured/deployed on the FaaS
platform and is usually different from the name of the callback
function (which may be stored in the
[`code.namespace`/`code.function`](/docs/general/attributes.md#source-code-attributes)
span attributes).

For some cloud providers, the above definition is ambiguous. The following
definition of function name MUST be used for this attribute
(and consequently the span name) for the listed cloud providers/products:

* **Azure:**  The full name `<FUNCAPP>/<FUNC>`, i.e., function app name
  followed by a forward slash followed by the function name (this form
  can also be seen in the resource JSON for the function).
  This means that a span attribute MUST be used, as an Azure function
  app can host multiple functions that would usually share
  a TracerProvider (see also the `cloud.resource_id` attribute).

**[5]:** Depending on the cloud provider and platform, use:

* **AWS Lambda:** The [function version](https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html)
  (an integer represented as a decimal string).
* **Google Cloud Run (Services):** The [revision](https://cloud.google.com/run/docs/managing/revisions)
  (i.e., the function name plus the revision suffix).
* **Google Cloud Functions:** The value of the
  [`K_REVISION` environment variable](https://cloud.google.com/functions/docs/env-var#runtime_environment_variables_set_automatically).
* **Azure Functions:** Not applicable. Do not set this attribute.
<!-- endsemconv -->

Note: The resource attribute `faas.instance` differs from the span attribute `faas.invocation_id`. For more information see the [Semantic conventions for FaaS spans](/docs/faas/faas-spans.md#difference-between-invocation-and-instance).

## Using span attributes instead of resource attributes

There are cases where a FaaS resource attribute is better applied as a span
attribute instead.
See the [FaaS trace conventions](/docs/faas/faas-spans.md) for more.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
