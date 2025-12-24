<!--- Hugo front matter used to generate the website version of this page:
linkTitle: K8s migration
--->

# K8s semantic convention stability migration

![note](https://img.shields.io/badge/warning-yellow?style=flat) K8s Semantic Conventions stability is still Wip.
This guide collects the breaking changes along the way so users can be informed in advance about upcoming changes.

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
  - [K8s Node allocatable metrics](#k8s-node-allocatable-metrics)
  - [K8s Deployment metrics](#k8s-deployment-metrics)
  - [K8s ReplicaSet metrics](#k8s-replicaset-metrics)
  - [K8s ReplicationController metrics](#k8s-replicationcontroller-metrics)
  - [K8s StatefulsSet metrics](#k8s-statefulsset-metrics)
  - [K8s HorizontalPodAutoscaler metrics](#k8s-horizontalpodautoscaler-metrics)
  - [K8s DaemonSet metrics](#k8s-daemonset-metrics)
  - [K8s Job metrics](#k8s-job-metrics)
  - [K8s Cronjob metrics](#k8s-cronjob-metrics)
  - [K8s Namespace metrics](#k8s-namespace-metrics)
  - [K8s ResourceQuota resource](#k8s-resourcequota-resource)
  - [K8s ReplicationController resource](#k8s-replicationcontroller-resource)
  - [K8s Container metrics](#k8s-container-metrics)
  - [K8s ResourceQuota metrics](#k8s-resourcequota-metrics)
  - [OpenShift ClusterResourceQuota metrics](#openshift-clusterresourcequota-metrics)
  - [K8s Node condition metrics](#k8s-node-condition-metrics)
  - [K8s Filesystem metrics](#k8s-filesystem-metrics)
  - [K8s Pod Volume metrics](#k8s-pod-volume-metrics)
  - [K8s Pod Memory metrics](#k8s-pod-memory-metrics)
  - [Container memory metrics](#container-memory-metrics)
  - [K8s Node memory metrics](#k8s-node-memory-metrics)
  - [Container Runtime](#container-runtime)
  - [K8s Pod Status Phase and Reason](#k8s-pod-status-phase-and-reason)

<!-- tocstop -->

## Summary of changes

This section summarizes the changes made to the K8s semantic conventions
from a range of versions. Each starting version shows all the changes required
to bring the conventions to stable.

### K8s network metrics

The K8s network metrics implemented by the Collector and specifically the
[kubeletstats](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.112.0/receiver/kubeletstatsreceiver/documentation.md)
receiver were introduced as semantic conventions
in [v1.29.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.29.0/docs/system/k8s-metrics.md).

The changes in their attributes are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                      |
| ---------------------------------------------------------------------------------- | ------------------------ |
| `interface`                                                                        | `network.interface.name` |
| `direction`                                                                        | `network.io.direction`   |

<!-- prettier-ignore-end -->

### K8s Node allocatable metrics

The K8s node allocatable metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.127.0/receiver/k8sclusterreceiver/documentation.md)
receiver.

The changes between collector implementation and semantic conventions:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                              |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `k8s.node.allocatable_cpu`                 (type: `gauge`)                         | `k8s.node.cpu.allocatable`               (type: `updowncounter`) |
| `k8s.node.allocatable_memory`              (type: `gauge`)                         | `k8s.node.memory.allocatable`            (type: `updowncounter`) |
| `k8s.node.allocatable_ephemeral_storage`   (type: `gauge`)                         | `k8s.node.ephemeral_storage.allocatable` (type: `updowncounter`) |
| `k8s.node.allocatable_pods`                (type: `gauge`)                         | `k8s.node.pod.allocatable`              (type: `updowncounter`)  |

<!-- prettier-ignore-end -->

### K8s Deployment metrics

The K8s Deployment metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md)

The changes in their metric names and types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                         |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `k8s.deployment.desired`       (type: `gauge`)                                     | `k8s.deployment.pod.desired` (type: `updowncounter`)        |
| `k8s.deployment.available`     (type: `gauge`)                                     | `k8s.deployment.pod.available`      (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s ReplicaSet metrics

The K8s ReplicaSet metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md).

The changes in their metric names and types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                    |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `k8s.replicaset.desired`           (type: `gauge`)                                 | `k8s.replicaset.pod.desired` (type: `updowncounter`)   |
| `k8s.replicaset.available`         (type: `gauge`)                                 | `k8s.replicaset.pod.available` (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s ReplicationController metrics

The K8s ReplicationController metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md).

The changes in their metric names and types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                               |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `k8s.replication_controller.desired`           (type: `gauge`)                     | `k8s.replicationcontroller.pod.desired` (type: `updowncounter`)   |
| `k8s.replication_controller.available`         (type: `gauge`)                     | `k8s.replicationcontroller.pod.available` (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s StatefulsSet metrics

The K8s StatefulSet metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md).

The changes in their metric types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                     |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `k8s.statefulset.desired_pods`                  (type: `gauge`)                    | `k8s.statefulset.pod.desired` (type: `updowncounter`)   |
| `k8s.statefulset.ready_pods`                  (type: `gauge`)                      | `k8s.statefulset.pod.ready` (type: `updowncounter`)     |
| `k8s.statefulset.current_pods`                       (type: `gauge`)               | `k8s.statefulset.pod.current`  (type: `updowncounter`)  |
| `k8s.statefulset.updated_pods`                      (type: `gauge`)                | `k8s.statefulset.pod.updated`   (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s HorizontalPodAutoscaler metrics

The K8s HorizontalPodAutoscaler metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md).

The changes in their metric names and types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                           |
| ---------------------------------------------------------------------------------- | --------------------------------------------- |
| `k8s.hpa.desired_replicas`                  (type: `gauge`)                        | `k8s.hpa.pod.desired` (type: `updowncounter`) |
| `k8s.hpa.current_replicas`                  (type: `gauge`)                        | `k8s.hpa.pod.current` (type: `updowncounter`) |
| `k8s.hpa.max_replicas`                       (type: `gauge`)                       | `k8s.hpa.pod.max`  (type: `updowncounter`)    |
| `k8s.hpa.min_replicas`                      (type: `gauge`)                        | `k8s.hpa.pod.min`   (type: `updowncounter`)   |

<!-- prettier-ignore-end -->

### K8s DaemonSet metrics

The K8s DaemonSet metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md).

The changes in their metric types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                            |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `k8s.daemonset.current_scheduled_nodes`                  (type: `gauge`)           | `k8s.daemonset.node.current_scheduled` (type: `updowncounter`) |
| `k8s.daemonset.desired_scheduled_nodes`                  (type: `gauge`)           | `k8s.daemonset.node.desired_scheduled` (type: `updowncounter`) |
| `k8s.daemonset.misscheduled_nodes`                       (type: `gauge`)           | `k8s.daemonset.node.misscheduled`  (type: `updowncounter`)     |
| `k8s.daemonset.ready_nodes`                      (type: `gauge`)                   | `k8s.daemonset.node.ready`   (type: `updowncounter`)           |

<!-- prettier-ignore-end -->

### K8s Job metrics

The K8s Job metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md).

The changes in their metric types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| ------------------------------------------------------ | --- |
| `k8s.job.active_pods`                  (type: `gauge`) | `k8s.job.pod.active` (type: `updowncounter`) |
| `k8s.job.failed_pods`                  (type: `gauge`) | `k8s.job.pod.failed` (type: `updowncounter`) |
| `k8s.job.desired_successful_pods`      (type: `gauge`) | `k8s.job.pod.desired_successful`  (type: `updowncounter`) |
| `k8s.job.max_parallel_pods`            (type: `gauge`) | `k8s.job.pod.max_parallel`   (type: `updowncounter`) |

### K8s Cronjob metrics

The K8s Cronjob metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md).

The changes in their metric types are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| ------------------------------------------------ | ---- |
| `k8s.cronjob.active_jobs`                  (type: `gauge`) | `k8s.cronjob.job.active` (type: `updowncounter`) |

<!-- prettier-ignore-end -->

### K8s Namespace metrics

The K8s Namespace metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.30.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.30.0/docs/system/k8s-metrics.md).

The changes in their metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| ---------------------------------------------------------------------------------- | --- |
| `k8s.namespace.phase`                  (type: `gauge`), 1 for active and 0 for terminating | `k8s.namespace.phase` (type: `updowncounter`), with the attribute `k8s.namespace.phase` indicating the phase |

<!-- prettier-ignore-end -->

### K8s ResourceQuota resource

The K8s ResourceQuota attributes implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.31.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.31.0/docs/system/k8s-metrics.md).

The changes are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| ---------------------------------------------------------------------------------- | --- |
| `k8s.resource_quota.{name,uid}` | `k8s.resourcequota.{name,uid}` |

<!-- prettier-ignore-end -->

### K8s ReplicationController resource

The K8s Replication Controller attributes implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[v1.31.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.31.0/docs/system/k8s-metrics.md).

The changes are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                    |
| ---------------------------------------------------------------------------------- | -------------------------------------- |
| `k8s.replication_controller.{name,uid}`                                            | `k8s.replicationcontroller.{name,uid}` |

### K8s Container metrics

The K8s Container metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in:

- [#2178](https://github.com/open-telemetry/semantic-conventions/pull/2178) (TODO: replace with SemConv version once
available)
- [#2074](https://github.com/open-telemetry/semantic-conventions/issues/2074)
- [#2197](https://github.com/open-telemetry/semantic-conventions/issues/2197)

The changes in their metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                               |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `k8s.container.cpu_limit`              (type: `gauge`)                             | `k8s.container.cpu.limit`       (type: `updowncounter`)           |
| `k8s.container.cpu_request`             (type: `gauge`)                            | `k8s.container.cpu.request`     (type: `updowncounter`)           |
| `k8s.container.memory_limit`            (type: `gauge`)                            | `k8s.container.memory.limit`     (type: `updowncounter`)          |
| `k8s.container.memory_request`           (type: `gauge`)                           | `k8s.container.memory.request`    (type: `updowncounter`)         |
| `k8s.container.storage_limit`             (type: `gauge`)                          | `k8s.container.storage.limit`     (type: `updowncounter`)         |
| `k8s.container.storage_request`           (type: `gauge`)                          | `k8s.container.storage.request`    (type: `updowncounter`)        |
| `k8s.container.ephemeralstorage_limit`      (type: `gauge`)                        | `k8s.container.ephemeral_storage.limit`  (type: `updowncounter`)  |
| `k8s.container.ephemeralstorage_request`     (type: `gauge`)                       | `k8s.container.ephemeral_storage.request` (type: `updowncounter`) |
| `k8s.container.restarts`                  (type: `gauge`)                          | `k8s.container.restart.count` (type: `updowncounter`)             |
| `k8s.container.ready`                  (type: `gauge`)                             | `k8s.container.ready` (type: `updowncounter`)                     |
| `k8s.container.cpu_limit_utilization` (type: `gauge`)                              | `k8s.container.cpu.limit_utilization` (type: `gauge`)             |
| `k8s.container.cpu_request_utilization` (type: `gauge`)                            | `k8s.container.cpu.request_utilization` (type: `gauge`)           |

<!-- prettier-ignore-end -->

### K8s ResourceQuota metrics

The K8s ResourceQuota metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[github.com/open-telemetry/semantic-conventions/pull/2113](https://github.com/open-telemetry/semantic-conventions/pull/2113).

These metrics were completely re-designed. The changes are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                 |
| ---------------------------------------------------------------------------------- | ----------------------------------- |
| `k8s.resource_quota.hard_limit`                                                    | `k8s.resourcequota.{resource}.hard` |
| `k8s.resource_quota.used`                                                          | `k8s.resourcequota.{resource}.used` |
| `{resource}` attribute                                                             | Split in different metrics per type |

<!-- prettier-ignore-end -->

### OpenShift ClusterResourceQuota metrics

The OpenShift ClusterResourceQuota metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[github.com/open-telemetry/semantic-conventions/pull/2779](https://github.com/open-telemetry/semantic-conventions/pull/2779).

These metrics were completely re-designed. The changes are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                      |
| ---------------------------------------------------------------------------------- | ---------------------------------------- |
| `openshift.clusterquota.hard_limit`                                                | `openshift.clusterquota.{resource}.hard` |
| `openshift.clusterquota.used`                                                      | `openshift.clusterquota.{resource}.used` |
| `{resource}` attribute                                                             | Split in different metrics per type      |

<!-- prettier-ignore-end -->

### K8s Node condition metrics

The K8s Node condition metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#2077](https://github.com/open-telemetry/semantic-conventions/issues/2077)

The changes in their metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                                                                                                                                   |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `k8s.node.condition_*`                                                             | `k8s.node.condition.status` metric [0,1] with attribute `k8s.node.condition.type` for the different conditions and `k8s.node.condition.status` for true/false/unknown |

<!-- prettier-ignore-end -->

### K8s Filesystem metrics

The K8s Filesystem metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#2392](https://github.com/open-telemetry/semantic-conventions/pull/2392)

The changes in their metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                              |
| ---------------------------------------------------------------------------------- | ------------------------------------------------ |
| `k8s.node.filesystem.available` gauge                                              | `k8s.node.filesystem.available`    updowncounter |
| `k8s.node.filesystem.capacity`   gauge                                             | `k8s.node.filesystem.capacity`     updowncounter |
| `k8s.node.filesystem.usage`      gauge                                             | `k8s.node.filesystem.usage`        updowncounter |
| `k8s.pod.filesystem.available`   gauge                                             | `k8s.pod.filesystem.available`     updowncounter |
| `k8s.pod.filesystem.capacity`    gauge                                             | `k8s.pod.filesystem.capacity`      updowncounter |
| `k8s.pod.filesystem.usage`      gauge                                              | `k8s.pod.filesystem.usage`         updowncounter |
| `container.filesystem.available`    gauge                                          | `container.filesystem.available`   updowncounter |
| `container.filesystem.capacity`      gauge                                         | `container.filesystem.capacity`    updowncounter |
| `container.filesystem.usage`        gauge                                          | `container.filesystem.usage`       updowncounter |

<!-- prettier-ignore-end -->

### K8s Pod Volume metrics

The K8s Pod volume metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.119.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#2319](https://github.com/open-telemetry/semantic-conventions/pull/2319).

The changes in these metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New |
| ---------------------------------------------------------------------------------- | --- |
| `k8s.volume.available` | `k8s.pod.volume.available` |
| `k8s.volume.capacity` | `k8s.pod.volume.capacity` |
| `k8s.volume.inodes` | `k8s.pod.volume.inode.count` |
| `k8s.volume.inodes.free` | `k8s.pod.volume.inode.free` |
| `k8s.volume.inodes.used` | `k8s.pod.volume.inode.used` |

<!-- prettier-ignore-end -->

### K8s Pod Memory metrics

The K8s Pod memory metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.119.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1490](https://github.com/open-telemetry/semantic-conventions/issues/1490).

The changes in these metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                                                     |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `k8s.pod.memory.page_faults`                                                       | `k8s.pod.memory.paging.faults` with attribute `system.paging.fault.type` set to `minor` |
| `k8s.pod.memory.major_page_faults`                                                 | `k8s.pod.memory.paging.faults` with attribute `system.paging.fault.type` set to `major` |

<!-- prettier-ignore-end -->

### Container memory metrics

The Container memory metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.119.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1490](https://github.com/open-telemetry/semantic-conventions/issues/1490).

The changes in these metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                                                       |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `container.memory.page_faults`                                                     | `container.memory.paging.faults` with attribute `system.paging.fault.type` set to `minor` |
| `container.memory.major_page_faults`                                               | `container.memory.paging.faults` with attribute `system.paging.fault.type` set to `major` |

<!-- prettier-ignore-end -->

### K8s Node memory metrics

The K8s Node memory metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.119.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#1490](https://github.com/open-telemetry/semantic-conventions/issues/1490).

The changes in these metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                                                          |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `k8s.node.memory.page_faults`                                                      | `k8s.node.memory.paging.faults` with attribute `system.paging.type` set to `minor`           |
| `k8s.node.memory.major_page_faults`                                                | `k8s.node.memory.paging.faults` with attribute `system.paging.type` set to `major`           |

<!-- prettier-ignore-end -->

### Container Runtime

The container runtime has become more descriptive with changes introduced to semantic conventions
within v1.Y.Z <!--[v1.29.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.29.0/docs/system/k8s-metrics.md)-->.

The changes in their attributes are the following:

<!-- prettier-ignore-start -->

| Old Attribute ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New Attribute |
| -------------------------------------------------------------------------------- | ------------- |
| `container.runtime` | `container.runtime.name` |

<!-- prettier-ignore-end -->

### K8s Pod Status Phase and Reason

The K8s Pod Status Phase and Reason metrics implemented by the Collector and specifically the
[k8scluster](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.115.0/receiver/k8sclusterreceiver/documentation.md)
receiver were introduced as semantic conventions in
[#2075](https://github.com/open-telemetry/semantic-conventions/issues/2075)

The changes in their metrics are the following:

<!-- prettier-ignore-start -->

| Old (Collector) ![changed](https://img.shields.io/badge/changed-orange?style=flat) | New                                                                                                   |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `k8s.pod.status_reason`    metric [1,6]                                            | `k8s.pod.status.reason` metric [0,1] with attribute `k8s.pod.status.reason` for the different reasons |
| `k8s.pod.phase`       metric [1, 5]                                                | `k8s.pod.status.phase` metric [0,1] with attribute `k8s.pod.phase` for the different phases           |

<!-- prettier-ignore-end -->
