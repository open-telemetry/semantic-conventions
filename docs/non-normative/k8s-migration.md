<!--- Hugo front matter used to generate the website version of this page:
linkTitle: K8s migration
--->

# K8s semantic conventions stability migration

Due to the significant number of modifications and the extensive user base
affected by them, existing K8s instrumentations published by
OpenTelemetry are required to implement a migration plan that will assist users in
transitioning to the stable K8s semantic conventions.

When existing K8s instrumentations published by OpenTelemetry are
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

Specifically for the Opentelemetry Collector:

The transition will happen through two different feature gates.
One for enabling the new schema called `semconv.k8s.stable`,
and one for disabling the old schema called `semconv.k8s.legacy`. Then:

- On alpha the old schema is enabled, while the new schema is disabled
- On beta/stable the old schema is disabled, while the new is enabled
- It is an error to disable both

<!-- toc -->

- [Summary of changes](#summary-of-changes)
  - [K8s network metrics](#k8s-network-metrics)

<!-- tocstop -->

## Summary of changes

This section summarizes the changes made to the K8s semantic conventions
from a range of versions. Each starting version shows all the changes required
to bring the conventions to stable (TODO: link to specific version once it exists).

### K8s network metrics

The K8s network metrics implemented by the Collector and specifically the
[kubeletstats](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.112.0/receiver/kubeletstatsreceiver/documentation.md)
receiver were introduced as semantic conventions in [v1.29.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.29.0/docs/system/k8s-metrics.md).

The changes in their attributes are the following:

<!-- prettier-ignore-start -->
| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                       |
|------------------------------------------------------------------------------------|---------------------------|
| `interface`                                                                        | `network.interface.name`  |
| `direction`                                                                        | `network.io.direction` |
<!-- prettier-ignore-end -->
