<!--- Hugo front matter used to generate the website version of this page:
linkTitle: FaaS
--->

# FaaS

## FaaS Attributes

<!-- semconv registry.faas(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `faas.coldstart` | boolean | A boolean that is true if the serverless function is executed for the first time (aka cold-start). |  |
| `faas.cron` | string | A string containing the schedule period as [Cron Expression](https://docs.oracle.com/cd/E12058_01/doc/doc.1014/e12030/cron_expressions.htm). | `0/5 * * * ? *` |
| `faas.document.collection` | string | The name of the source on which the triggering operation was performed. For example, in Cloud Storage or S3 corresponds to the bucket name, and in Cosmos DB to the database name. | `myBucketName`; `myDbName` |
| `faas.document.name` | string | The document name/table subjected to the operation. For example, in Cloud Storage or S3 is the name of the file, and in Cosmos DB the table name. | `myFile.txt`; `myTableName` |
| `faas.document.operation` | string | Describes the type of the operation that was performed on the data. | `insert` |
| `faas.document.time` | string | A string containing the time when the data was accessed in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format expressed in [UTC](https://www.w3.org/TR/NOTE-datetime). | `2020-01-23T13:47:06Z` |
| `faas.instance` | string | The execution environment ID as a string, that will be potentially reused for other invocations to the same function/function version. [1] | `2021/06/28/[$LATEST]2f399eb14537447da05ab2a2e39309de` |
| `faas.invocation_id` | string | The invocation ID of the current function invocation. | `af9d5aa4-a685-4c5f-a22b-444f80b3cc28` |
| `faas.invoked_name` | string | The name of the invoked function. [2] | `my-function` |
| `faas.invoked_provider` | string | The cloud provider of the invoked function. [3] | `alibaba_cloud` |
| `faas.invoked_region` | string | The cloud region of the invoked function. [4] | `eu-central-1` |
| `faas.max_memory` | int | The amount of memory available to the serverless function converted to Bytes. [5] | `134217728` |
| `faas.name` | string | The name of the single function that this runtime instance executes. [6] | `my-function`; `myazurefunctionapp/some-function-name` |
| `faas.time` | string | A string containing the function invocation time in the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) format expressed in [UTC](https://www.w3.org/TR/NOTE-datetime). | `2020-01-23T13:47:06Z` |
| `faas.trigger` | string | Type of the trigger which caused this function invocation. | `datasource` |
| `faas.version` | string | The immutable version of the function being executed. [7] | `26`; `pinkfroid-00002` |

**[1]:** * **AWS Lambda:** Use the (full) log stream name.

**[2]:** SHOULD be equal to the `faas.name` resource attribute of the invoked function.

**[3]:** SHOULD be equal to the `cloud.provider` resource attribute of the invoked function.

**[4]:** SHOULD be equal to the `cloud.region` resource attribute of the invoked function.

**[5]:** It's recommended to set this attribute since e.g. too little memory can easily stop a Java AWS Lambda function from working correctly. On AWS Lambda, the environment variable `AWS_LAMBDA_FUNCTION_MEMORY_SIZE` provides this information (which must be multiplied by 1,048,576).

**[6]:** This is the name of the function as configured/deployed on the FaaS
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

**[7]:** Depending on the cloud provider and platform, use:

* **AWS Lambda:** The [function version](https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html)
  (an integer represented as a decimal string).
* **Google Cloud Run (Services):** The [revision](https://cloud.google.com/run/docs/managing/revisions)
  (i.e., the function name plus the revision suffix).
* **Google Cloud Functions:** The value of the
  [`K_REVISION` environment variable](https://cloud.google.com/functions/docs/env-var#runtime_environment_variables_set_automatically).
* **Azure Functions:** Not applicable. Do not set this attribute.

`faas.document.operation` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `insert` | When a new object is created. |
| `edit` | When an object is modified. |
| `delete` | When an object is deleted. |

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