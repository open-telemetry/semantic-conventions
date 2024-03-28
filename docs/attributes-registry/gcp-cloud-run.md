# Google Cloud Run

## Google Cloud Run Attributes
<!-- semconv registry.gcp.cloud_run(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `gcp.cloud_run.job.execution` | string | The name of the Cloud Run [execution](https://cloud.google.com/run/docs/managing/job-executions) being run for the Job, as set by the [`CLOUD_RUN_EXECUTION`](https://cloud.google.com/run/docs/container-contract#jobs-env-vars) environment variable. | `job-name-xxxx`; `sample-job-mdw84` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp.cloud_run.job.task_index` | int | The index for a task within an execution as provided by the [`CLOUD_RUN_TASK_INDEX`](https://cloud.google.com/run/docs/container-contract#jobs-env-vars) environment variable. | `0`; `1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->
