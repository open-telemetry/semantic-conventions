# Google Cloud Run

**Status**: [Experimental][DocumentStatus]

These conventions are recommended for resources running on Cloud Run.

**Type:** `gcp.cloud_run`

**Description:** Resource attributes for Cloud Run.

<!-- semconv gcp.cloud_run -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`gcp.cloud_run.job.execution`](/docs/attributes-registry/gcp.md) | string | The name of the Cloud Run [execution](https://cloud.google.com/run/docs/managing/job-executions) being run for the Job, as set by the [`CLOUD_RUN_EXECUTION`](https://cloud.google.com/run/docs/container-contract#jobs-env-vars) environment variable. | `job-name-xxxx`; `sample-job-mdw84` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`gcp.cloud_run.job.task_index`](/docs/attributes-registry/gcp.md) | int | The index for a task within an execution as provided by the [`CLOUD_RUN_TASK_INDEX`](https://cloud.google.com/run/docs/container-contract#jobs-env-vars) environment variable. | `0`; `1` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
