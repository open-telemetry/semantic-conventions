<!--- Hugo front matter used to generate the website version of this page:
linkTitle: K8s migration
--->

# K8s semantic conventions stability migration

Due to the significant number of modifications and the extensive user base
affected by them, existing K8s instrumentations published by
OpenTelemetry are required to implement a migration plan that will assist users in
transitioning to the stable K8s semantic conventions.

Specifically, when existing K8s instrumentations published by OpenTelemetry are
updated to the stable K8s semantic conventions, they:

- SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN` in
  their existing major version, which accepts:
  - `k8s` - emit the stable k8s conventions, and stop emitting
    the old k8s conventions that the instrumentation emitted previously.
  - `k8s/dup` - emit both the old and the stable k8s conventions,
    allowing for a phased rollout of the stable semantic conventions.
  - The default behavior (in the absence of one of these values) is to continue
    emitting whatever version of the old k8s conventions the
    instrumentation was emitting previously.
- Need to maintain (security patching at a minimum) their existing major version
  for at least six months after it starts emitting both sets of conventions.
- May drop the environment variable in their next major version and emit only
  the stable k8s conventions.

<!-- toc -->

- [Summary of changes](#summary-of-changes)
  - [K8s network metrics](#k8s-network-metrics)

<!-- tocstop -->

## Summary of changes

This section summarizes the changes made to the K8s semantic conventions
from a range of versions. Each starting version shows all the changes required
to bring the conventions to
[v1.TODO (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.TODO/docs/k8s/README.md).

### K8s network metrics

The K8s network metrics implemented by the Collector and specifically the
[kubeletstats](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.112.0/receiver/kubeletstatsreceiver/documentation.md)
receiver were introduced as semantic conventions in [v1.TODO](https://github.com/open-telemetry/semantic-conventions/blob/v1.TODO/docs/k8s/README.md).

The changes in their attributes are the following:

<!-- prettier-ignore-start -->
| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                       |
|------------------------------------------------------------------------------------|---------------------------|
| `interface`                                                                        | `network.interface.name`  |
| `direction`                                                                        | `network.io.direction` |
<!-- prettier-ignore-end -->
