<!--- Hugo front matter used to generate the website version of this page:
linkTitle: FaaS
--->

# FaaS

## FaaS Attributes

<!-- semconv registry.faas -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `faas.instance` | string | The execution environment ID as a string, that will be potentially reused for other invocations to the same function/function version. [1] | `2021/06/28/[$LATEST]2f399eb14537447da05ab2a2e39309de` | Recommended |
| `faas.max_memory` | int | The amount of memory available to the serverless function converted to Bytes. [2] | `134217728` | Recommended |
| `faas.name` | string | The name of the single function that this runtime instance executes. [3] | `my-function`; `myazurefunctionapp/some-function-name` | Recommended |
| `faas.version` | string | The immutable version of the function being executed. [4] | `26`; `pinkfroid-00002` | Recommended |

**[1]:** * **AWS Lambda:** Use the (full) log stream name.

**[2]:** It's recommended to set this attribute since e.g. too little memory can easily stop a Java AWS Lambda function from working correctly. On AWS Lambda, the environment variable `AWS_LAMBDA_FUNCTION_MEMORY_SIZE` provides this information (which must be multiplied by 1,048,576).

**[3]:** This is the name of the function as configured/deployed on the FaaS
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

**[4]:** Depending on the cloud provider and platform, use:

* **AWS Lambda:** The [function version](https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html)
  (an integer represented as a decimal string).
* **Google Cloud Run (Services):** The [revision](https://cloud.google.com/run/docs/managing/revisions)
  (i.e., the function name plus the revision suffix).
* **Google Cloud Functions:** The value of the
  [`K_REVISION` environment variable](https://cloud.google.com/functions/docs/env-var#runtime_environment_variables_set_automatically).
* **Azure Functions:** Not applicable. Do not set this attribute.
<!-- endsemconv -->