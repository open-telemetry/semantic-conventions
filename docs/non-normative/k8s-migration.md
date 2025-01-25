<!--- Hugo front matter used to generate the website version of this page:
linkTitle: K8s migration
--->

# K8s Semantic Convention Stability Migration

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
One for enabling the new schema called `semconv.k8s.enableStable`,
and one for disabling the old schema called `semconv.k8s.disableLegacy`. Then:

- On alpha the old schema is enabled by default (`semconv.k8s.disableLegacy` defaults to false),
  while the new schema is disabled by default (`semconv.k8s.enableStable` defaults to false).
- On beta/stable the old schema is disabled by default (`semconv.k8s.disableLegacy` defaults to true),
  while the new is enabled by default (`semconv.k8s.enableStable` defaults to true).
- It is an error to disable both schemas
- Both schemas can be enabled with `--feature-gates=-semconv.k8s.disableLegacy,+semconv.k8s.enableStable`.

<!-- toc -->

- [Summary of changes](#summary-of-changes)
  - [K8s network metrics](#k8s-network-metrics)
  - [K8s Deployment metrics](#k8s-deployment-metrics)
  - [K8s ReplicaSet metrics](#k8s-replicaset-metrics)
  - [K8s ReplicationController metrics](#k8s-replicationcontroller-metrics)
  - [K8s StatefulsSet metrics](#k8s-statefulsset-metrics)
  - [K8s HorizontalPodAutoscaler metrics](#k8s-horizontalpodautoscaler-metrics)
  - [K8s DaemonSet metrics](#k8s-daemonset-metrics)
  - [K8s Job metrics](#k8s-job-metrics)
  - [K8s Cronjob metrics](#k8s-cronjob-metrics)
  - [K8s Namespace metrics](#k8s-namespace-metrics)

<!-- tocstop -->

## Summary of changes

This section summarizes the changes made to the K8s semantic conventions
from a range of versions. Each starting version shows all the changes required
to bring the conventions to stable (TODO: link to specific version once it exists).

### K8s network metrics

The K8s network metrics implemented by the Collector and specifically the
[kubeletstats](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.112.0/receiver/kubeletstatsreceiver/documentation.md)
receiver were introduced as semantic conventions
in [v1.29.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.29.0/docs/system/k8s-metrics.md).

The changes in their attributes are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                      |
|------------------------------------------------------------------------------------|--------------------------|
| `interface`                                                                        | `network.interface.name` |
| `direction`                                                                        | `network.io.direction`   |

<!-- prettier-ignore-end -->

### K8s Deployment metrics

The K8s Deployment metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1636](https://github.com/open-telemetry/semantic-conventions/pull/1636) (TODO: replace with SemConv version once
available).

The changes in their metric names and types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                          |
|------------------------------------------------------------------------------------|--------------------------------------------------------------|
| `k8s.deployment.desired`       (type: `gauge`)                                     | `k8s.deployment.desired_pods` (type: `updowncounter`)        |
| `k8s.deployment.available`     (type: `gauge`)                                     | `k8s.deployment.available_pods`      (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s ReplicaSet metrics

The K8s ReplicaSet metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1636](https://github.com/open-telemetry/semantic-conventions/pull/1636) (TODO: replace with SemConv version once
available).

The changes in their metric names and types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                     |
|------------------------------------------------------------------------------------|---------------------------------------------------------|
| `k8s.replicaset.desired`           (type: `gauge`)                                 | `k8s.replicaset.desired_pods` (type: `updowncounter`)   |
| `k8s.replicaset.available`         (type: `gauge`)                                 | `k8s.replicaset.available_pods` (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s ReplicationController metrics

The K8s ReplicationController metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1636](https://github.com/open-telemetry/semantic-conventions/pull/1636) (TODO: replace with SemConv version once
available).

The changes in their metric names and types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                                 |
|------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `k8s.replication_controller.desired`           (type: `gauge`)                     | `k8s.replication_controller.desired_pods` (type: `updowncounter`)   |
| `k8s.replication_controller.available`         (type: `gauge`)                     | `k8s.replication_controller.available_pods` (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s StatefulsSet metrics

The K8s StatefulsSet metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1636](https://github.com/open-telemetry/semantic-conventions/pull/1636) (TODO: replace with SemConv version once
available).

The changes in their metric types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                      |
|------------------------------------------------------------------------------------|----------------------------------------------------------|
| `k8s.statefulset.desired_pods`                  (type: `gauge`)                    | `k8s.statefulset.desired_pods` (type: `updowncounter`)   |
| `k8s.statefulset.ready_pods`                  (type: `gauge`)                      | `k8s.statefulset.ready_pods` (type: `updowncounter`)     |
| `k8s.statefulset.current_pods`                       (type: `gauge`)               | `k8s.statefulset.current_pods`  (type: `updowncounter`)  |
| `k8s.statefulset.updated_pods`                      (type: `gauge`)                | `k8s.statefulset.updated_pods`   (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s HorizontalPodAutoscaler metrics

The K8s HorizontalPodAutoscaler metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1636](https://github.com/open-telemetry/semantic-conventions/pull/1636) (TODO: replace with SemConv version once
available).

The changes in their metric names and types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                            |
|------------------------------------------------------------------------------------|------------------------------------------------|
| `k8s.hpa.desired_replicas`                  (type: `gauge`)                        | `k8s.hpa.desired_pods` (type: `updowncounter`) |
| `k8s.hpa.current_replicas`                  (type: `gauge`)                        | `k8s.hpa.current_pods` (type: `updowncounter`) |
| `k8s.hpa.max_replicas`                       (type: `gauge`)                       | `k8s.hpa.max_pods`  (type: `updowncounter`)    |
| `k8s.hpa.min_replicas`                      (type: `gauge`)                        | `k8s.hpa.min_pods`   (type: `updowncounter`)   |

<!-- prettier-ignore-end -->

### K8s DaemonSet metrics

The K8s DaemonSet metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1649](https://github.com/open-telemetry/semantic-conventions/pull/1649) (TODO: replace with SemConv version once
available).

The changes in their metric types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                             |
|------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| `k8s.daemonset.current_scheduled_nodes`                  (type: `gauge`)           | `k8s.daemonset.current_scheduled_nodes` (type: `updowncounter`) |
| `k8s.daemonset.desired_scheduled_nodes`                  (type: `gauge`)           | `k8s.daemonset.desired_scheduled_nodes` (type: `updowncounter`) |
| `k8s.daemonset.misscheduled_nodes`                       (type: `gauge`)           | `k8s.daemonset.misscheduled_nodes`  (type: `updowncounter`)     |
| `k8s.daemonset.ready_nodes`                      (type: `gauge`)                   | `k8s.daemonset.ready_nodes`   (type: `updowncounter`)           |

<!-- prettier-ignore-end -->

### K8s Job metrics

The K8s Job metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1649](https://github.com/open-telemetry/semantic-conventions/pull/1660) (TODO: replace with SemConv version once
available).

The changes in their metric types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                    |
|----------------------------------------------------------|----------------------------------------|
| `k8s.job.active_pods`                  (type: `gauge`) | `k8s.job.active_pods` (type: `updowncounter`) |
| `k8s.job.failed_pods`                  (type: `gauge`) | `k8s.job.failed_pods` (type: `updowncounter`) |
| `k8s.job.desired_successful_pods`                       (type: `gauge`) | `k8s.job.desired_successful_pods`  (type: `updowncounter`) |
| `k8s.job.max_parallel_pods`                      (type: `gauge`) | `k8s.job.max_parallel_pods`   (type: `updowncounter`) |

### K8s Cronjob metrics

The K8s Cronjob metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1649](https://github.com/open-telemetry/semantic-conventions/pull/1660) (TODO: replace with SemConv version once
available).

The changes in their metric types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                            |
|--------------------------------------------------|--------------------------------|
| `k8s.cronjob.active_jobs`                  (type: `gauge`) | `k8s.cronjob.active_jobs` (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s Namespace metrics

The K8s Namespace metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1649](https://github.com/open-telemetry/semantic-conventions/pull/1668) (TODO: replace with SemConv version once
available).

The changes in their metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                                                            |
|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| `k8s.namespace.phase`                  (type: `gauge`), 1 for active and 0 for terminating                      | `k8s.namespace.phase` (type: `updowncounter`), with the attribute `k8s.namespace.phase` indicating the phase |

<!-- prettier-ignore-end -->
