
<!--- Hugo front matter used to generate the website version of this page:
--->

# GCP

- [gcp cloud_run](#gcp cloud_run)
- [gcp gce](#gcp gce)


## gcp cloud_run Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `gcp.cloud_run.job.execution` | string | The name of the Cloud Run [execution](https://cloud.google.com/run/docs/managing/job-executions) being run for the Job, as set by the [`CLOUD_RUN_EXECUTION`](https://cloud.google.com/run/docs/container-contract#jobs-env-vars) environment variable.  | `job-name-xxxx`; `sample-job-mdw84` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp.cloud_run.job.task_index` | int | The index for a task within an execution as provided by the [`CLOUD_RUN_TASK_INDEX`](https://cloud.google.com/run/docs/container-contract#jobs-env-vars) environment variable.  | `0`; `1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|



## gcp gce Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `gcp.gce.instance.hostname` | string | The hostname of a GCE instance. This is the full value of the default or [custom hostname](https://cloud.google.com/compute/docs/instances/custom-hostname-vm).  | `my-host1234.example.com`; `sample-vm.us-west1-b.c.my-project.internal` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gcp.gce.instance.name` | string | The instance name of a GCE instance. This is the value provided by `host.name`, the visible name of the instance in the Cloud Console UI, and the prefix for the default hostname of the instance as defined by the [default internal DNS name](https://cloud.google.com/compute/docs/internal-dns#instance-fully-qualified-domain-names).  | `instance-1`; `my-vm-name` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|


