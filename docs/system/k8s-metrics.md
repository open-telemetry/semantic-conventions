<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Kubernetes
--->

# Semantic conventions for Kubernetes metrics

**Status**: [Development][DocumentStatus]

## K8s metrics

This document describes instruments and attributes for common K8s level
metrics in OpenTelemetry. These metrics are collected from technology-specific,
well-defined APIs (e.g. Kubelet's API).

Metrics in `k8s.` instruments SHOULD be attached to a [K8s Resource](/docs/resource/k8s.md)
and therefore inherit its attributes, like `k8s.pod.name` and `k8s.pod.uid`.

<!-- toc -->

- [Pod metrics](#pod-metrics)
  - [Metric: `k8s.pod.uptime`](#metric-k8spoduptime)
  - [Metric: `k8s.pod.cpu.time`](#metric-k8spodcputime)
  - [Metric: `k8s.pod.cpu.usage`](#metric-k8spodcpuusage)
  - [Metric: `k8s.pod.memory.usage`](#metric-k8spodmemoryusage)
  - [Metric: `k8s.pod.network.io`](#metric-k8spodnetworkio)
  - [Metric: `k8s.pod.network.errors`](#metric-k8spodnetworkerrors)
- [Container metrics](#container-metrics)
  - [Metric: `k8s.container.status.state`](#metric-k8scontainerstatusstate)
  - [Metric: `k8s.container.status.reason`](#metric-k8scontainerstatusreason)
- [Node metrics](#node-metrics)
  - [Metric: `k8s.node.uptime`](#metric-k8snodeuptime)
  - [Metric: `k8s.node.cpu.time`](#metric-k8snodecputime)
  - [Metric: `k8s.node.cpu.usage`](#metric-k8snodecpuusage)
  - [Metric: `k8s.node.memory.usage`](#metric-k8snodememoryusage)
  - [Metric: `k8s.node.network.io`](#metric-k8snodenetworkio)
  - [Metric: `k8s.node.network.errors`](#metric-k8snodenetworkerrors)
- [Deployment metrics](#deployment-metrics)
  - [Metric: `k8s.deployment.desired_pods`](#metric-k8sdeploymentdesired_pods)
  - [Metric: `k8s.deployment.available_pods`](#metric-k8sdeploymentavailable_pods)
- [ReplicaSet metrics](#replicaset-metrics)
  - [Metric: `k8s.replicaset.desired_pods`](#metric-k8sreplicasetdesired_pods)
  - [Metric: `k8s.replicaset.available_pods`](#metric-k8sreplicasetavailable_pods)
- [ReplicationController metrics](#replicationcontroller-metrics)
  - [Metric: `k8s.replicationcontroller.desired_pods`](#metric-k8sreplicationcontrollerdesired_pods)
  - [Metric: `k8s.replicationcontroller.available_pods`](#metric-k8sreplicationcontrolleravailable_pods)
- [StatefulSet metrics](#statefulset-metrics)
  - [Metric: `k8s.statefulset.desired_pods`](#metric-k8sstatefulsetdesired_pods)
  - [Metric: `k8s.statefulset.ready_pods`](#metric-k8sstatefulsetready_pods)
  - [Metric: `k8s.statefulset.current_pods`](#metric-k8sstatefulsetcurrent_pods)
  - [Metric: `k8s.statefulset.updated_pods`](#metric-k8sstatefulsetupdated_pods)
- [HorizontalPodAutoscaler metrics](#horizontalpodautoscaler-metrics)
  - [Metric: `k8s.hpa.desired_pods`](#metric-k8shpadesired_pods)
  - [Metric: `k8s.hpa.current_pods`](#metric-k8shpacurrent_pods)
  - [Metric: `k8s.hpa.max_pods`](#metric-k8shpamax_pods)
  - [Metric: `k8s.hpa.min_pods`](#metric-k8shpamin_pods)
- [DaemonSet metrics](#daemonset-metrics)
  - [Metric: `k8s.daemonset.current_scheduled_nodes`](#metric-k8sdaemonsetcurrent_scheduled_nodes)
  - [Metric: `k8s.daemonset.desired_scheduled_nodes`](#metric-k8sdaemonsetdesired_scheduled_nodes)
  - [Metric: `k8s.daemonset.misscheduled_nodes`](#metric-k8sdaemonsetmisscheduled_nodes)
  - [Metric: `k8s.daemonset.ready_nodes`](#metric-k8sdaemonsetready_nodes)
- [Job metrics](#job-metrics)
  - [Metric: `k8s.job.active_pods`](#metric-k8sjobactive_pods)
  - [Metric: `k8s.job.failed_pods`](#metric-k8sjobfailed_pods)
  - [Metric: `k8s.job.successful_pods`](#metric-k8sjobsuccessful_pods)
  - [Metric: `k8s.job.desired_successful_pods`](#metric-k8sjobdesired_successful_pods)
  - [Metric: `k8s.job.max_parallel_pods`](#metric-k8sjobmax_parallel_pods)
- [CronJob metrics](#cronjob-metrics)
  - [Metric: `k8s.cronjob.active_jobs`](#metric-k8scronjobactive_jobs)
- [Namespace metrics](#namespace-metrics)
  - [Metric: `k8s.namespace.phase`](#metric-k8snamespacephase)
- [K8s Container metrics](#k8s-container-metrics)
  - [Metric: `k8s.container.cpu.limit`](#metric-k8scontainercpulimit)
  - [Metric: `k8s.container.cpu.request`](#metric-k8scontainercpurequest)
  - [Metric: `k8s.container.memory.limit`](#metric-k8scontainermemorylimit)
  - [Metric: `k8s.container.memory.request`](#metric-k8scontainermemoryrequest)
  - [Metric: `k8s.container.storage.limit`](#metric-k8scontainerstoragelimit)
  - [Metric: `k8s.container.storage.request`](#metric-k8scontainerstoragerequest)
  - [Metric: `k8s.container.ephemeral_storage.limit`](#metric-k8scontainerephemeral_storagelimit)
  - [Metric: `k8s.container.ephemeral_storage.request`](#metric-k8scontainerephemeral_storagerequest)
  - [Metric: `k8s.container.restart.count`](#metric-k8scontainerrestartcount)
  - [Metric: `k8s.container.ready`](#metric-k8scontainerready)

<!-- tocstop -->

## Pod metrics

**Description:** Pod level metrics captured under the namespace `k8s.pod`.

### Metric: `k8s.pod.uptime`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.uptime -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.uptime` | Gauge | `s` | The time the Pod has been running [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** Instrumentations SHOULD use a gauge with type `double` and measure uptime in seconds as a floating point number with the highest precision available.
The actual accuracy would depend on the instrumentation and operating system.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.cpu.time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.cpu.time -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.cpu.time` | Counter | `s` | Total CPU time consumed [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** Total CPU time consumed by the specific Pod on all available CPU cores

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.cpu.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.cpu.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.cpu.usage` | Gauge | `{cpu}` | Pod's CPU usage, measured in cpus. Range from 0 to the number of allocatable CPUs [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** CPU usage of the specific Pod on all available CPU cores, averaged over the sample window

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.memory.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.memory.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.memory.usage` | Gauge | `By` | Memory usage of the Pod [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** Total memory usage of the Pod

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.network.io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.network.io -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.network.io` | Counter | `By` | Network bytes for the Pod | ![Development](https://img.shields.io/badge/-development-blue) |  |

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`network.interface.name`](/docs/registry/attributes/network.md) | string | The network interface name. | `lo`; `eth0` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`network.io.direction`](/docs/registry/attributes/network.md) | string | The network IO operation direction. | `transmit` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

---

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `receive` | receive | ![Development](https://img.shields.io/badge/-development-blue) |
| `transmit` | transmit | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.network.errors`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.network.errors -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.network.errors` | Counter | `{error}` | Pod network errors | ![Development](https://img.shields.io/badge/-development-blue) |  |

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`network.interface.name`](/docs/registry/attributes/network.md) | string | The network interface name. | `lo`; `eth0` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`network.io.direction`](/docs/registry/attributes/network.md) | string | The network IO operation direction. | `transmit` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

---

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `receive` | receive | ![Development](https://img.shields.io/badge/-development-blue) |
| `transmit` | transmit | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Container metrics

**Description:** Container level metrics captured under the namespace `k8s.container`.

### Metric: `k8s.container.status.state`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.status.state -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.status.state` | UpDownCounter | `{container}` | Describes the number of K8s containers that are currently in a given state [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** All possible container states will be reported at each time interval to avoid missing metrics.
Only the value corresponding to the current state will be non-zero.

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`k8s.container.status.state`](/docs/registry/attributes/k8s.md) | string | The state of the container. [K8s ContainerState](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#containerstate-v1-core) | `terminated`; `running`; `waiting` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |

---

`k8s.container.status.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `running` | The container is running. | ![Development](https://img.shields.io/badge/-development-blue) |
| `terminated` | The container has terminated. | ![Development](https://img.shields.io/badge/-development-blue) |
| `waiting` | The container is waiting. | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.status.reason`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.status.reason -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.status.reason` | UpDownCounter | `{container}` | Describes the number of K8s containers that are currently in a state for a given reason [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** All possible container state reasons will be reported at each time interval to avoid missing metrics.
Only the value corresponding to the current state reason will be non-zero.

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`k8s.container.status.reason`](/docs/registry/attributes/k8s.md) | string | The reason for the container state. Corresponds to the `reason` field of the: [K8s ContainerStateWaiting](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#containerstatewaiting-v1-core) or [K8s ContainerStateTerminated](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#containerstateterminated-v1-core) | `ContainerCreating`; `CrashLoopBackOff`; `CreateContainerConfigError`; `ErrImagePull`; `ImagePullBackOff`; `OOMKilled`; `Completed`; `Error`; `ContainerCannotRun` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |

---

`k8s.container.status.reason` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `Completed` | The container has completed execution. | ![Development](https://img.shields.io/badge/-development-blue) |
| `ContainerCannotRun` | The container cannot run. | ![Development](https://img.shields.io/badge/-development-blue) |
| `ContainerCreating` | The container is being created. | ![Development](https://img.shields.io/badge/-development-blue) |
| `CrashLoopBackOff` | The container is in a crash loop back off state. | ![Development](https://img.shields.io/badge/-development-blue) |
| `CreateContainerConfigError` | There was an error creating the container configuration. | ![Development](https://img.shields.io/badge/-development-blue) |
| `ErrImagePull` | There was an error pulling the container image. | ![Development](https://img.shields.io/badge/-development-blue) |
| `Error` | There was an error with the container. | ![Development](https://img.shields.io/badge/-development-blue) |
| `ImagePullBackOff` | The container image pull is in back off state. | ![Development](https://img.shields.io/badge/-development-blue) |
| `OOMKilled` | The container was killed due to out of memory. | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Node metrics

**Description:** Node level metrics captured under the namespace `k8s.node`.

### Metric: `k8s.node.uptime`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.uptime -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.uptime` | Gauge | `s` | The time the Node has been running [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** Instrumentations SHOULD use a gauge with type `double` and measure uptime in seconds as a floating point number with the highest precision available.
The actual accuracy would depend on the instrumentation and operating system.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.cpu.time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.cpu.time -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.cpu.time` | Counter | `s` | Total CPU time consumed [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** Total CPU time consumed by the specific Node on all available CPU cores

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.cpu.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.cpu.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.cpu.usage` | Gauge | `{cpu}` | Node's CPU usage, measured in cpus. Range from 0 to the number of allocatable CPUs [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** CPU usage of the specific Node on all available CPU cores, averaged over the sample window

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.memory.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.memory.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.memory.usage` | Gauge | `By` | Memory usage of the Node [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** Total memory usage of the Node

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.network.io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.network.io -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.network.io` | Counter | `By` | Network bytes for the Node | ![Development](https://img.shields.io/badge/-development-blue) |  |

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`network.interface.name`](/docs/registry/attributes/network.md) | string | The network interface name. | `lo`; `eth0` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`network.io.direction`](/docs/registry/attributes/network.md) | string | The network IO operation direction. | `transmit` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

---

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `receive` | receive | ![Development](https://img.shields.io/badge/-development-blue) |
| `transmit` | transmit | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.network.errors`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.network.errors -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.network.errors` | Counter | `{error}` | Node network errors | ![Development](https://img.shields.io/badge/-development-blue) |  |

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`network.interface.name`](/docs/registry/attributes/network.md) | string | The network interface name. | `lo`; `eth0` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`network.io.direction`](/docs/registry/attributes/network.md) | string | The network IO operation direction. | `transmit` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

---

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `receive` | receive | ![Development](https://img.shields.io/badge/-development-blue) |
| `transmit` | transmit | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Deployment metrics

**Description:** Deployment level metrics captured under the namespace `k8s.deployment`.

### Metric: `k8s.deployment.desired_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.deployment.desired_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.deployment.desired_pods` | UpDownCounter | `{pod}` | Number of desired replica pods in this deployment [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `replicas` field of the
[K8s DeploymentSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#deploymentspec-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.deployment`](../resource/k8s.md#deployment) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.deployment.available_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.deployment.available_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.deployment.available_pods` | UpDownCounter | `{pod}` | Total number of available replica pods (ready for at least minReadySeconds) targeted by this deployment [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `availableReplicas` field of the
[K8s DeploymentStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#deploymentstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.deployment`](../resource/k8s.md#deployment) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## ReplicaSet metrics

**Description:** ReplicaSet level metrics captured under the namespace `k8s.replicaset`.

### Metric: `k8s.replicaset.desired_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.replicaset.desired_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.replicaset.desired_pods` | UpDownCounter | `{pod}` | Number of desired replica pods in this replicaset [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `replicas` field of the
[K8s ReplicaSetSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#replicasetspec-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.replicaset`](../resource/k8s.md#replicaset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.replicaset.available_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.replicaset.available_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.replicaset.available_pods` | UpDownCounter | `{pod}` | Total number of available replica pods (ready for at least minReadySeconds) targeted by this replicaset [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `availableReplicas` field of the
[K8s ReplicaSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#replicasetstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.replicaset`](../resource/k8s.md#replicaset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## ReplicationController metrics

**Description:** ReplicationController level metrics captured under the namespace `k8s.replicationcontroller`.

### Metric: `k8s.replicationcontroller.desired_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.replicationcontroller.desired_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.replicationcontroller.desired_pods` | UpDownCounter | `{pod}` | Number of desired replica pods in this replication controller [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `replicas` field of the
[K8s ReplicationControllerSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#replicationcontrollerspec-v1-core)

This metric SHOULD, at a minimum, be reported against a
[`k8s.replicationcontroller`](../resource/k8s.md#replicationcontroller) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.replicationcontroller.available_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.replicationcontroller.available_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.replicationcontroller.available_pods` | UpDownCounter | `{pod}` | Total number of available replica pods (ready for at least minReadySeconds) targeted by this replication controller [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `availableReplicas` field of the
[K8s ReplicationControllerStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#replicationcontrollerstatus-v1-core)

This metric SHOULD, at a minimum, be reported against a
[`k8s.replicationcontroller`](../resource/k8s.md#replicationcontroller) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## StatefulSet metrics

**Description:** StatefulSet level metrics captured under the namespace `k8s.statefulset`.

### Metric: `k8s.statefulset.desired_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.statefulset.desired_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.statefulset.desired_pods` | UpDownCounter | `{pod}` | Number of desired replica pods in this statefulset [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `replicas` field of the
[K8s StatefulSetSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulsetspec-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.statefulset`](../resource/k8s.md#statefulset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.statefulset.ready_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.statefulset.ready_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.statefulset.ready_pods` | UpDownCounter | `{pod}` | The number of replica pods created for this statefulset with a Ready Condition [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `readyReplicas` field of the
[K8s StatefulSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulsetstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.statefulset`](../resource/k8s.md#statefulset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.statefulset.current_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.statefulset.current_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.statefulset.current_pods` | UpDownCounter | `{pod}` | The number of replica pods created by the statefulset controller from the statefulset version indicated by currentRevision [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `currentReplicas` field of the
[K8s StatefulSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulsetstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.statefulset`](../resource/k8s.md#statefulset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.statefulset.updated_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.statefulset.updated_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.statefulset.updated_pods` | UpDownCounter | `{pod}` | Number of replica pods created by the statefulset controller from the statefulset version indicated by updateRevision [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `updatedReplicas` field of the
[K8s StatefulSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulsetstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.statefulset`](../resource/k8s.md#statefulset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## HorizontalPodAutoscaler metrics

**Description:** HorizontalPodAutoscaler level metrics captured under the namespace `k8s.hpa`.

### Metric: `k8s.hpa.desired_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.hpa.desired_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.desired_pods` | UpDownCounter | `{pod}` | Desired number of replica pods managed by this horizontal pod autoscaler, as last calculated by the autoscaler [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `desiredReplicas` field of the
[K8s HorizontalPodAutoscalerStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#horizontalpodautoscalerstatus-v2-autoscaling)

This metric SHOULD, at a minimum, be reported against a
[`k8s.hpa`](../resource/k8s.md#horizontalpodautoscaler) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.current_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.hpa.current_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.current_pods` | UpDownCounter | `{pod}` | Current number of replica pods managed by this horizontal pod autoscaler, as last seen by the autoscaler [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `currentReplicas` field of the
[K8s HorizontalPodAutoscalerStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#horizontalpodautoscalerstatus-v2-autoscaling)

This metric SHOULD, at a minimum, be reported against a
[`k8s.hpa`](../resource/k8s.md#horizontalpodautoscaler) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.max_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.hpa.max_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.max_pods` | UpDownCounter | `{pod}` | The upper limit for the number of replica pods to which the autoscaler can scale up [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `maxReplicas` field of the
[K8s HorizontalPodAutoscalerSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#horizontalpodautoscalerspec-v2-autoscaling)

This metric SHOULD, at a minimum, be reported against a
[`k8s.hpa`](../resource/k8s.md#horizontalpodautoscaler) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.min_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.hpa.min_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.min_pods` | UpDownCounter | `{pod}` | The lower limit for the number of replica pods to which the autoscaler can scale down [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `minReplicas` field of the
[K8s HorizontalPodAutoscalerSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#horizontalpodautoscalerspec-v2-autoscaling)

This metric SHOULD, at a minimum, be reported against a
[`k8s.hpa`](../resource/k8s.md#horizontalpodautoscaler) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## DaemonSet metrics

**Description:** DaemonSet level metrics captured under the namespace `k8s.daemonset`.

### Metric: `k8s.daemonset.current_scheduled_nodes`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.daemonset.current_scheduled_nodes -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.daemonset.current_scheduled_nodes` | UpDownCounter | `{node}` | Number of nodes that are running at least 1 daemon pod and are supposed to run the daemon pod [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `currentNumberScheduled` field of the
[K8s DaemonSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#daemonsetstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.daemonset`](../resource/k8s.md#daemonset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.daemonset.desired_scheduled_nodes`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.daemonset.desired_scheduled_nodes -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.daemonset.desired_scheduled_nodes` | UpDownCounter | `{node}` | Number of nodes that should be running the daemon pod (including nodes currently running the daemon pod) [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `desiredNumberScheduled` field of the
[K8s DaemonSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#daemonsetstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.daemonset`](../resource/k8s.md#daemonset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.daemonset.misscheduled_nodes`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.daemonset.misscheduled_nodes -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.daemonset.misscheduled_nodes` | UpDownCounter | `{node}` | Number of nodes that are running the daemon pod, but are not supposed to run the daemon pod [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `numberMisscheduled` field of the
[K8s DaemonSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#daemonsetstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.daemonset`](../resource/k8s.md#daemonset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.daemonset.ready_nodes`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.daemonset.ready_nodes -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.daemonset.ready_nodes` | UpDownCounter | `{node}` | Number of nodes that should be running the daemon pod and have one or more of the daemon pod running and ready [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `numberReady` field of the
[K8s DaemonSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#daemonsetstatus-v1-apps).

This metric SHOULD, at a minimum, be reported against a
[`k8s.daemonset`](../resource/k8s.md#daemonset) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Job metrics

**Description:** Job level metrics captured under the namespace `k8s.job`.

### Metric: `k8s.job.active_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.active_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.active_pods` | UpDownCounter | `{pod}` | The number of pending and actively running pods for a job [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `active` field of the
[K8s JobStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobstatus-v1-batch).

This metric SHOULD, at a minimum, be reported against a
[`k8s.job`](../resource/k8s.md#job) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.job.failed_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.failed_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.failed_pods` | UpDownCounter | `{pod}` | The number of pods which reached phase Failed for a job [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `failed` field of the
[K8s JobStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobstatus-v1-batch).

This metric SHOULD, at a minimum, be reported against a
[`k8s.job`](../resource/k8s.md#job) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.job.successful_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.successful_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.successful_pods` | UpDownCounter | `{pod}` | The number of pods which reached phase Succeeded for a job [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `succeeded` field of the
[K8s JobStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobstatus-v1-batch).

This metric SHOULD, at a minimum, be reported against a
[`k8s.job`](../resource/k8s.md#job) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.job.desired_successful_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.desired_successful_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.desired_successful_pods` | UpDownCounter | `{pod}` | The desired number of successfully finished pods the job should be run with [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `completions` field of the
[K8s JobSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobspec-v1-batch).

This metric SHOULD, at a minimum, be reported against a
[`k8s.job`](../resource/k8s.md#job) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.job.max_parallel_pods`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.max_parallel_pods -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.max_parallel_pods` | UpDownCounter | `{pod}` | The max desired number of pods the job should run at any given time [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `parallelism` field of the
[K8s JobSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobspec-v1-batch).

This metric SHOULD, at a minimum, be reported against a
[`k8s.job`](../resource/k8s.md#job) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## CronJob metrics

**Description:** CronJob level metrics captured under the namespace `k8s.cronjob`.

### Metric: `k8s.cronjob.active_jobs`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.cronjob.active_jobs -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.cronjob.active_jobs` | UpDownCounter | `{job}` | The number of actively running jobs for a cronjob [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric aligns with the `active` field of the
[K8s CronJobStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#cronjobstatus-v1-batch).

This metric SHOULD, at a minimum, be reported against a
[`k8s.cronjob`](../resource/k8s.md#cronjob) resource.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Namespace metrics

**Description:** Namespace level metrics captured under the namespace `k8s.namespace`.

### Metric: `k8s.namespace.phase`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.namespace.phase -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.namespace.phase` | UpDownCounter | `{namespace}` | Describes number of K8s namespaces that are currently in a given phase. [1] | ![Development](https://img.shields.io/badge/-development-blue) |  |

**[1]:** This metric SHOULD, at a minimum, be reported against a
[`k8s.namespace`](../resource/k8s.md#namespace) resource.

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`k8s.namespace.phase`](/docs/registry/attributes/k8s.md) | string | The phase of the K8s namespace. [1] | `active`; `terminating` | `Required` | ![Development](https://img.shields.io/badge/-development-blue) |

**[1] `k8s.namespace.phase`:** This attribute aligns with the `phase` field of the
[K8s NamespaceStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#namespacestatus-v1-core)

---

`k8s.namespace.phase` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `active` | Active namespace phase as described by [K8s API](https://pkg.go.dev/k8s.io/api@v0.31.3/core/v1#NamespacePhase) | ![Development](https://img.shields.io/badge/-development-blue) |
| `terminating` | Terminating namespace phase as described by [K8s API](https://pkg.go.dev/k8s.io/api@v0.31.3/core/v1#NamespacePhase) | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## K8s Container metrics

**Description:** K8s Container level metrics captured under the namespace `k8s.container`.

### Metric: `k8s.container.cpu.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.cpu.limit -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.cpu.limit` | Gauge | `{cpu}` | Maximum CPU resource limit set for the container [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.cpu.request`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.cpu.request -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.cpu.request` | Gauge | `{cpu}` | CPU resource requested for the container [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.memory.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.memory.limit -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.memory.limit` | Gauge | `By` | Maximum memory resource limit set for the container [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.memory.request`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.memory.request -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.memory.request` | Gauge | `By` | Memory resource requested for the container [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.storage.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.storage.limit -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.storage.limit` | Gauge | `By` | Maximum storage resource limit set for the container [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.storage.request`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.storage.request -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.storage.request` | Gauge | `By` | Storage resource requested for the container [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.ephemeral_storage.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.ephemeral_storage.limit -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.ephemeral_storage.limit` | Gauge | `By` | Maximum ephemeral storage resource limit set for the container [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.ephemeral_storage.request`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.ephemeral_storage.request -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.ephemeral_storage.request` | Gauge | `By` | Ephemeral storage resource requested for the container [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.restart.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.restart.count -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.restart.count` | UpDownCounter | `{restart}` | Describes how many times the container has restarted (since the last counter reset) [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** This value is pulled directly from the K8s API and the value can go indefinitely high and be reset to 0
at any time depending on how your kubelet is configured to prune dead containers.
It is best to not depend too much on the exact value but rather look at it as
either == 0, in which case you can conclude there were no restarts in the recent past, or > 0, in which case
you can conclude there were restarts in the recent past, and not try and analyze the value beyond that.

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.ready`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.ready -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->
<!-- markdownlint-capture -->
<!-- markdownlint-disable -->

| Name     | Instrument Type | Unit (UCUM) | Description    | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.ready` | UpDownCounter | `{container}` | Indicates whether the container is currently marked as ready to accept traffic, based on its readiness probe (1 = ready, 0 = not ready) [1] | ![Development](https://img.shields.io/badge/-development-blue) | `k8s.container` |

**[1]:** This metric SHOULD reflect the value of the `ready` field in the
[K8s ContainerStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#containerstatus-v1-core).

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
