<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Kubernetes
--->

# Semantic conventions for Kubernetes metrics

**Status**: [Development][DocumentStatus]

## K8s metrics

This document describes instruments and attributes for common K8s level
metrics in OpenTelemetry. These metrics are collected from technology-specific,
well-defined APIs (e.g. Kubelet's API).

Metrics in `k8s.` instruments SHOULD be attached to a [K8s Resource](/docs/resource/k8s/README.md)
and therefore inherit its attributes, like `k8s.pod.name` and `k8s.pod.uid`.

<!-- toc -->

- [Pod metrics](#pod-metrics)
  - [Metric: `k8s.pod.uptime`](#metric-k8spoduptime)
  - [Metric: `k8s.pod.phase`](#metric-k8spodphase)
  - [Metric: `k8s.pod.status.reason`](#metric-k8spodstatusreason)
  - [Metric: `k8s.pod.cpu.time`](#metric-k8spodcputime)
  - [Metric: `k8s.pod.cpu.usage`](#metric-k8spodcpuusage)
  - [Metric: `k8s.pod.memory.usage`](#metric-k8spodmemoryusage)
  - [Metric: `k8s.pod.memory.available`](#metric-k8spodmemoryavailable)
  - [Metric: `k8s.pod.memory.rss`](#metric-k8spodmemoryrss)
  - [Metric: `k8s.pod.memory.working_set`](#metric-k8spodmemoryworking_set)
  - [Metric: `k8s.pod.memory.paging.faults`](#metric-k8spodmemorypagingfaults)
  - [Metric: `k8s.pod.network.io`](#metric-k8spodnetworkio)
  - [Metric: `k8s.pod.network.errors`](#metric-k8spodnetworkerrors)
  - [Metric: `k8s.pod.filesystem.available`](#metric-k8spodfilesystemavailable)
  - [Metric: `k8s.pod.filesystem.capacity`](#metric-k8spodfilesystemcapacity)
  - [Metric: `k8s.pod.filesystem.usage`](#metric-k8spodfilesystemusage)
  - [Metric: `k8s.pod.volume.available`](#metric-k8spodvolumeavailable)
  - [Metric: `k8s.pod.volume.capacity`](#metric-k8spodvolumecapacity)
  - [Metric: `k8s.pod.volume.usage`](#metric-k8spodvolumeusage)
  - [Metric: `k8s.pod.volume.inode.count`](#metric-k8spodvolumeinodecount)
  - [Metric: `k8s.pod.volume.inode.used`](#metric-k8spodvolumeinodeused)
  - [Metric: `k8s.pod.volume.inode.free`](#metric-k8spodvolumeinodefree)
- [Container metrics](#container-metrics)
  - [Metric: `k8s.container.status.state`](#metric-k8scontainerstatusstate)
  - [Metric: `k8s.container.status.reason`](#metric-k8scontainerstatusreason)
- [Node metrics](#node-metrics)
  - [Metric: `k8s.node.uptime`](#metric-k8snodeuptime)
  - [Metric: `k8s.node.cpu.allocatable`](#metric-k8snodecpuallocatable)
  - [Metric: `k8s.node.memory.allocatable`](#metric-k8snodememoryallocatable)
  - [Metric: `k8s.node.ephemeral_storage.allocatable`](#metric-k8snodeephemeral_storageallocatable)
  - [Metric: `k8s.node.pod.allocatable`](#metric-k8snodepodallocatable)
  - [Metric: `k8s.node.condition.status`](#metric-k8snodeconditionstatus)
  - [Metric: `k8s.node.cpu.time`](#metric-k8snodecputime)
  - [Metric: `k8s.node.cpu.usage`](#metric-k8snodecpuusage)
  - [Metric: `k8s.node.memory.usage`](#metric-k8snodememoryusage)
  - [Metric: `k8s.node.memory.available`](#metric-k8snodememoryavailable)
  - [Metric: `k8s.node.memory.rss`](#metric-k8snodememoryrss)
  - [Metric: `k8s.node.memory.working_set`](#metric-k8snodememoryworking_set)
  - [Metric: `k8s.node.memory.paging.faults`](#metric-k8snodememorypagingfaults)
  - [Metric: `k8s.node.network.io`](#metric-k8snodenetworkio)
  - [Metric: `k8s.node.network.errors`](#metric-k8snodenetworkerrors)
  - [Metric: `k8s.node.filesystem.available`](#metric-k8snodefilesystemavailable)
  - [Metric: `k8s.node.filesystem.capacity`](#metric-k8snodefilesystemcapacity)
  - [Metric: `k8s.node.filesystem.usage`](#metric-k8snodefilesystemusage)
- [Deployment metrics](#deployment-metrics)
  - [Metric: `k8s.deployment.pod.desired`](#metric-k8sdeploymentpoddesired)
  - [Metric: `k8s.deployment.pod.available`](#metric-k8sdeploymentpodavailable)
- [ReplicaSet metrics](#replicaset-metrics)
  - [Metric: `k8s.replicaset.pod.desired`](#metric-k8sreplicasetpoddesired)
  - [Metric: `k8s.replicaset.pod.available`](#metric-k8sreplicasetpodavailable)
- [ReplicationController metrics](#replicationcontroller-metrics)
  - [Metric: `k8s.replicationcontroller.pod.desired`](#metric-k8sreplicationcontrollerpoddesired)
  - [Metric: `k8s.replicationcontroller.pod.available`](#metric-k8sreplicationcontrollerpodavailable)
- [StatefulSet metrics](#statefulset-metrics)
  - [Metric: `k8s.statefulset.pod.desired`](#metric-k8sstatefulsetpoddesired)
  - [Metric: `k8s.statefulset.pod.ready`](#metric-k8sstatefulsetpodready)
  - [Metric: `k8s.statefulset.pod.current`](#metric-k8sstatefulsetpodcurrent)
  - [Metric: `k8s.statefulset.pod.updated`](#metric-k8sstatefulsetpodupdated)
- [HorizontalPodAutoscaler metrics](#horizontalpodautoscaler-metrics)
  - [Metric: `k8s.hpa.pod.desired`](#metric-k8shpapoddesired)
  - [Metric: `k8s.hpa.pod.current`](#metric-k8shpapodcurrent)
  - [Metric: `k8s.hpa.pod.max`](#metric-k8shpapodmax)
  - [Metric: `k8s.hpa.pod.min`](#metric-k8shpapodmin)
  - [Metric: `k8s.hpa.metric.target.cpu.value`](#metric-k8shpametrictargetcpuvalue)
  - [Metric: `k8s.hpa.metric.target.cpu.average_value`](#metric-k8shpametrictargetcpuaverage_value)
  - [Metric: `k8s.hpa.metric.target.cpu.average_utilization`](#metric-k8shpametrictargetcpuaverage_utilization)
- [DaemonSet metrics](#daemonset-metrics)
  - [Metric: `k8s.daemonset.node.current_scheduled`](#metric-k8sdaemonsetnodecurrent_scheduled)
  - [Metric: `k8s.daemonset.node.desired_scheduled`](#metric-k8sdaemonsetnodedesired_scheduled)
  - [Metric: `k8s.daemonset.node.misscheduled`](#metric-k8sdaemonsetnodemisscheduled)
  - [Metric: `k8s.daemonset.node.ready`](#metric-k8sdaemonsetnodeready)
- [Job metrics](#job-metrics)
  - [Metric: `k8s.job.pod.active`](#metric-k8sjobpodactive)
  - [Metric: `k8s.job.pod.failed`](#metric-k8sjobpodfailed)
  - [Metric: `k8s.job.pod.successful`](#metric-k8sjobpodsuccessful)
  - [Metric: `k8s.job.pod.desired_successful`](#metric-k8sjobpoddesired_successful)
  - [Metric: `k8s.job.pod.max_parallel`](#metric-k8sjobpodmax_parallel)
- [CronJob metrics](#cronjob-metrics)
  - [Metric: `k8s.cronjob.job.active`](#metric-k8scronjobjobactive)
- [Namespace metrics](#namespace-metrics)
  - [Metric: `k8s.namespace.phase`](#metric-k8snamespacephase)
- [K8s Container metrics](#k8s-container-metrics)
  - [Metric: `k8s.container.cpu.limit_utilization`](#metric-k8scontainercpulimit_utilization)
  - [Metric: `k8s.container.cpu.request_utilization`](#metric-k8scontainercpurequest_utilization)
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
- [Resource Quota metrics](#resource-quota-metrics)
  - [Metric: `k8s.resourcequota.cpu.limit.hard`](#metric-k8sresourcequotacpulimithard)
  - [Metric: `k8s.resourcequota.cpu.limit.used`](#metric-k8sresourcequotacpulimitused)
  - [Metric: `k8s.resourcequota.cpu.request.hard`](#metric-k8sresourcequotacpurequesthard)
  - [Metric: `k8s.resourcequota.cpu.request.used`](#metric-k8sresourcequotacpurequestused)
  - [Metric: `k8s.resourcequota.memory.limit.hard`](#metric-k8sresourcequotamemorylimithard)
  - [Metric: `k8s.resourcequota.memory.limit.used`](#metric-k8sresourcequotamemorylimitused)
  - [Metric: `k8s.resourcequota.memory.request.hard`](#metric-k8sresourcequotamemoryrequesthard)
  - [Metric: `k8s.resourcequota.memory.request.used`](#metric-k8sresourcequotamemoryrequestused)
  - [Metric: `k8s.resourcequota.hugepage_count.request.hard`](#metric-k8sresourcequotahugepage_countrequesthard)
  - [Metric: `k8s.resourcequota.hugepage_count.request.used`](#metric-k8sresourcequotahugepage_countrequestused)
  - [Metric: `k8s.resourcequota.storage.request.hard`](#metric-k8sresourcequotastoragerequesthard)
  - [Metric: `k8s.resourcequota.storage.request.used`](#metric-k8sresourcequotastoragerequestused)
  - [Metric: `k8s.resourcequota.persistentvolumeclaim_count.hard`](#metric-k8sresourcequotapersistentvolumeclaim_counthard)
  - [Metric: `k8s.resourcequota.persistentvolumeclaim_count.used`](#metric-k8sresourcequotapersistentvolumeclaim_countused)
  - [Metric: `k8s.resourcequota.ephemeral_storage.request.hard`](#metric-k8sresourcequotaephemeral_storagerequesthard)
  - [Metric: `k8s.resourcequota.ephemeral_storage.request.used`](#metric-k8sresourcequotaephemeral_storagerequestused)
  - [Metric: `k8s.resourcequota.ephemeral_storage.limit.hard`](#metric-k8sresourcequotaephemeral_storagelimithard)
  - [Metric: `k8s.resourcequota.ephemeral_storage.limit.used`](#metric-k8sresourcequotaephemeral_storagelimitused)
  - [Metric: `k8s.resourcequota.object_count.hard`](#metric-k8sresourcequotaobject_counthard)
  - [Metric: `k8s.resourcequota.object_count.used`](#metric-k8sresourcequotaobject_countused)

<!-- tocstop -->

## Pod metrics

**Description:** Pod level metrics captured under the namespace `k8s.pod`.

### Metric: `k8s.pod.uptime`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.uptime -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.uptime` | Gauge | `s` | The time the Pod has been running. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** Instrumentations SHOULD use a gauge with type `double` and measure uptime in seconds as a floating point number with the highest precision available.
The actual accuracy would depend on the instrumentation and operating system.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.phase`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.status.phase -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.status.phase` | UpDownCounter | `{pod}` | Describes number of K8s Pods that are currently in a given phase. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** All possible pod phases will be reported at each time interval to avoid missing metrics.
Only the value corresponding to the current phase will be non-zero.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.pod.status.phase`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The phase for the pod. Corresponds to the `phase` field of the: [K8s PodStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.33/#podstatus-v1-core) | `Pending`; `Running` |

---

`k8s.pod.status.phase` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `Failed` | All containers in the pod have terminated, and at least one container has terminated in a failure (exited with a non-zero exit code or was stopped by the system). | ![Development](https://img.shields.io/badge/-development-blue) |
| `Pending` | The pod has been accepted by the system, but one or more of the containers has not been started. This includes time before being bound to a node, as well as time spent pulling images onto the host. | ![Development](https://img.shields.io/badge/-development-blue) |
| `Running` | The pod has been bound to a node and all of the containers have been started. At least one container is still running or is in the process of being restarted. | ![Development](https://img.shields.io/badge/-development-blue) |
| `Succeeded` | All containers in the pod have voluntarily terminated with a container exit code of 0, and the system is not going to restart any of these containers. | ![Development](https://img.shields.io/badge/-development-blue) |
| `Unknown` | For some reason the state of the pod could not be obtained, typically due to an error in communicating with the host of the pod. | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.status.reason`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.status.reason -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.status.reason` | UpDownCounter | `{pod}` | Describes the number of K8s Pods that are currently in a state for a given reason. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** All possible pod status reasons will be reported at each time interval to avoid missing metrics.
Only the value corresponding to the current reason will be non-zero.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.pod.status.reason`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The reason for the pod state. Corresponds to the `reason` field of the: [K8s PodStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.33/#podstatus-v1-core) | `Evicted`; `NodeAffinity` |

---

`k8s.pod.status.reason` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `Evicted` | The pod is evicted. | ![Development](https://img.shields.io/badge/-development-blue) |
| `NodeAffinity` | The pod is in a status because of its node affinity | ![Development](https://img.shields.io/badge/-development-blue) |
| `NodeLost` | The reason on a pod when its state cannot be confirmed as kubelet is unresponsive on the node it is (was) running. | ![Development](https://img.shields.io/badge/-development-blue) |
| `Shutdown` | The node is shutdown | ![Development](https://img.shields.io/badge/-development-blue) |
| `UnexpectedAdmissionError` | The pod was rejected admission to the node because of an error during admission that could not be categorized. | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.cpu.time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.cpu.time -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.cpu.time` | Counter | `s` | Total CPU time consumed. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** Total CPU time consumed by the specific Pod on all available CPU cores

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.cpu.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.cpu.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.cpu.usage` | Gauge | `{cpu}` | Pod's CPU usage, measured in cpus. Range from 0 to the number of allocatable CPUs. [1] | ![Development](https://img.shields.io/badge/-development-blue) | |

**[1]:** CPU usage of the specific Pod on all available CPU cores, averaged over the sample window

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.memory.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.memory.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.memory.usage` | Gauge | `By` | Memory usage of the Pod. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** Total memory usage of the Pod

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.memory.available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.memory.available -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.memory.available` | UpDownCounter | `By` | Pod memory available. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** Available memory for use.  This is defined as the memory limit - workingSetBytes. If memory limit is undefined, the available bytes is omitted.
This metric is derived from the [MemoryStats.AvailableBytes](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) field of the [PodStats.Memory](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#PodStats) of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.memory.rss`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.memory.rss -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.memory.rss` | UpDownCounter | `By` | Pod memory RSS. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** The amount of anonymous and swap cache memory (includes transparent hugepages).
This metric is derived from the [MemoryStats.RSSBytes](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) field of the [PodStats.Memory](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#PodStats) of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.memory.working_set`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.memory.working_set -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.memory.working_set` | UpDownCounter | `By` | Pod memory working set. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** The amount of working set memory. This includes recently accessed memory, dirty memory, and kernel memory. WorkingSetBytes is <= UsageBytes.
This metric is derived from the [MemoryStats.WorkingSetBytes](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) field of the [PodStats.Memory](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#PodStats) of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.memory.paging.faults`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.memory.paging.faults -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.memory.paging.faults` | Counter | `{fault}` | Pod memory paging faults. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** Cumulative number of major/minor page faults.
This metric is derived from the [MemoryStats.PageFaults](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) and [MemoryStats.MajorPageFaults](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) field of the [PodStats.Memory](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#PodStats) of the Kubelet's stats API.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`system.paging.fault.type`](/docs/registry/attributes/system.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The paging fault type | `minor` |

---

`system.paging.fault.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `major` | major | ![Development](https://img.shields.io/badge/-development-blue) |
| `minor` | minor | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.network.io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.network.io -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.network.io` | Counter | `By` | Network bytes for the Pod. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`network.interface.name`](/docs/registry/attributes/network.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The network interface name. | `lo`; `eth0` |
| [`network.io.direction`](/docs/registry/attributes/network.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The network IO operation direction. | `transmit` |

---

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `receive` | receive | ![Development](https://img.shields.io/badge/-development-blue) |
| `transmit` | transmit | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.network.errors`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.network.errors -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.network.errors` | Counter | `{error}` | Pod network errors. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`network.interface.name`](/docs/registry/attributes/network.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The network interface name. | `lo`; `eth0` |
| [`network.io.direction`](/docs/registry/attributes/network.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The network IO operation direction. | `transmit` |

---

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `receive` | receive | ![Development](https://img.shields.io/badge/-development-blue) |
| `transmit` | transmit | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.filesystem.available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.filesystem.available -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.filesystem.available` | UpDownCounter | `By` | Pod filesystem available bytes. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This metric is derived from the
[FsStats.AvailableBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#FsStats) field
of the [PodStats.EphemeralStorage](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats)
of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.filesystem.capacity`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.filesystem.capacity -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.filesystem.capacity` | UpDownCounter | `By` | Pod filesystem capacity. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This metric is derived from the
[FsStats.CapacityBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#FsStats) field
of the [PodStats.EphemeralStorage](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats)
of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.filesystem.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.filesystem.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.filesystem.usage` | UpDownCounter | `By` | Pod filesystem usage. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This may not equal capacity - available.

This metric is derived from the
[FsStats.UsedBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#FsStats) field
of the [PodStats.EphemeralStorage](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats)
of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.volume.available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.volume.available -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.volume.available` | UpDownCounter | `By` | Pod volume storage space available. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This metric is derived from the
[VolumeStats.AvailableBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#VolumeStats) field
of the [PodStats](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats) of the
Kubelet's stats API.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.volume.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the K8s volume. | `volume0` |
| [`k8s.volume.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of the K8s volume. | `emptyDir`; `persistentVolumeClaim` |

---

`k8s.volume.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `configMap` | A [configMap](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#configmap) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `downwardAPI` | A [downwardAPI](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#downwardapi) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `emptyDir` | An [emptyDir](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#emptydir) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `local` | A [local](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#local) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `persistentVolumeClaim` | A [persistentVolumeClaim](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `secret` | A [secret](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#secret) volume | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.volume.capacity`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.volume.capacity -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.volume.capacity` | UpDownCounter | `By` | Pod volume total capacity. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This metric is derived from the
[VolumeStats.CapacityBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#VolumeStats) field
of the [PodStats](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats) of the
Kubelet's stats API.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.volume.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the K8s volume. | `volume0` |
| [`k8s.volume.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of the K8s volume. | `emptyDir`; `persistentVolumeClaim` |

---

`k8s.volume.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `configMap` | A [configMap](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#configmap) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `downwardAPI` | A [downwardAPI](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#downwardapi) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `emptyDir` | An [emptyDir](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#emptydir) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `local` | A [local](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#local) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `persistentVolumeClaim` | A [persistentVolumeClaim](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `secret` | A [secret](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#secret) volume | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.volume.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.volume.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.volume.usage` | UpDownCounter | `By` | Pod volume usage. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This may not equal capacity - available.

This metric is derived from the
[VolumeStats.UsedBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#VolumeStats) field
of the [PodStats](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats) of the
Kubelet's stats API.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.volume.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the K8s volume. | `volume0` |
| [`k8s.volume.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of the K8s volume. | `emptyDir`; `persistentVolumeClaim` |

---

`k8s.volume.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `configMap` | A [configMap](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#configmap) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `downwardAPI` | A [downwardAPI](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#downwardapi) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `emptyDir` | An [emptyDir](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#emptydir) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `local` | A [local](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#local) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `persistentVolumeClaim` | A [persistentVolumeClaim](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `secret` | A [secret](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#secret) volume | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.volume.inode.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.volume.inode.count -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.volume.inode.count` | UpDownCounter | `{inode}` | The total inodes in the filesystem of the Pod's volume. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This metric is derived from the
[VolumeStats.Inodes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#VolumeStats) field
of the [PodStats](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats) of the
Kubelet's stats API.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.volume.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the K8s volume. | `volume0` |
| [`k8s.volume.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of the K8s volume. | `emptyDir`; `persistentVolumeClaim` |

---

`k8s.volume.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `configMap` | A [configMap](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#configmap) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `downwardAPI` | A [downwardAPI](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#downwardapi) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `emptyDir` | An [emptyDir](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#emptydir) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `local` | A [local](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#local) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `persistentVolumeClaim` | A [persistentVolumeClaim](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `secret` | A [secret](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#secret) volume | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.volume.inode.used`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.volume.inode.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.volume.inode.used` | UpDownCounter | `{inode}` | The inodes used by the filesystem of the Pod's volume. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This metric is derived from the
[VolumeStats.InodesUsed](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#VolumeStats) field
of the [PodStats](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats) of the
Kubelet's stats API.

This may not be equal to `inodes - free` because filesystem may share inodes with other filesystems.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.volume.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the K8s volume. | `volume0` |
| [`k8s.volume.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of the K8s volume. | `emptyDir`; `persistentVolumeClaim` |

---

`k8s.volume.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `configMap` | A [configMap](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#configmap) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `downwardAPI` | A [downwardAPI](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#downwardapi) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `emptyDir` | An [emptyDir](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#emptydir) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `local` | A [local](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#local) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `persistentVolumeClaim` | A [persistentVolumeClaim](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `secret` | A [secret](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#secret) volume | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.pod.volume.inode.free`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.pod.volume.inode.free -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.pod.volume.inode.free` | UpDownCounter | `{inode}` | The free inodes in the filesystem of the Pod's volume. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.pod`](/docs/registry/entities/k8s.md#k8s-pod) |

**[1]:** This metric is derived from the
[VolumeStats.InodesFree](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#VolumeStats) field
of the [PodStats](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#PodStats) of the
Kubelet's stats API.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.volume.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the K8s volume. | `volume0` |
| [`k8s.volume.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of the K8s volume. | `emptyDir`; `persistentVolumeClaim` |

---

`k8s.volume.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `configMap` | A [configMap](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#configmap) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `downwardAPI` | A [downwardAPI](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#downwardapi) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `emptyDir` | An [emptyDir](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#emptydir) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `local` | A [local](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#local) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `persistentVolumeClaim` | A [persistentVolumeClaim](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#persistentvolumeclaim) volume | ![Development](https://img.shields.io/badge/-development-blue) |
| `secret` | A [secret](https://v1-30.docs.kubernetes.io/docs/concepts/storage/volumes/#secret) volume | ![Development](https://img.shields.io/badge/-development-blue) |

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

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.status.state` | UpDownCounter | `{container}` | Describes the number of K8s containers that are currently in a given state. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** All possible container states will be reported at each time interval to avoid missing metrics.
Only the value corresponding to the current state will be non-zero.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.container.status.state`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The state of the container. [K8s ContainerState](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#containerstate-v1-core) | `terminated`; `running`; `waiting` |

---

`k8s.container.status.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `running` | The container is running. | ![Development](https://img.shields.io/badge/-development-blue) |
| `terminated` | The container has terminated. | ![Development](https://img.shields.io/badge/-development-blue) |
| `waiting` | The container is waiting. | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.status.reason`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.status.reason -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.status.reason` | UpDownCounter | `{container}` | Describes the number of K8s containers that are currently in a state for a given reason. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** All possible container state reasons will be reported at each time interval to avoid missing metrics.
Only the value corresponding to the current state reason will be non-zero.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.container.status.reason`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The reason for the container state. Corresponds to the `reason` field of the: [K8s ContainerStateWaiting](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#containerstatewaiting-v1-core) or [K8s ContainerStateTerminated](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#containerstateterminated-v1-core) | `ContainerCreating`; `CrashLoopBackOff`; `CreateContainerConfigError`; `ErrImagePull`; `ImagePullBackOff`; `OOMKilled`; `Completed`; `Error`; `ContainerCannotRun` |

---

`k8s.container.status.reason` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `Completed` | The container has completed execution. | ![Development](https://img.shields.io/badge/-development-blue) |
| `ContainerCannotRun` | The container cannot run. | ![Development](https://img.shields.io/badge/-development-blue) |
| `ContainerCreating` | The container is being created. | ![Development](https://img.shields.io/badge/-development-blue) |
| `CrashLoopBackOff` | The container is in a crash loop back off state. | ![Development](https://img.shields.io/badge/-development-blue) |
| `CreateContainerConfigError` | There was an error creating the container configuration. | ![Development](https://img.shields.io/badge/-development-blue) |
| `ErrImagePull` | There was an error pulling the container image. | ![Development](https://img.shields.io/badge/-development-blue) |
| `Error` | There was an error with the container. | ![Development](https://img.shields.io/badge/-development-blue) |
| `ImagePullBackOff` | The container image pull is in back off state. | ![Development](https://img.shields.io/badge/-development-blue) |
| `OOMKilled` | The container was killed due to out of memory. | ![Development](https://img.shields.io/badge/-development-blue) |

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

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.uptime` | Gauge | `s` | The time the Node has been running. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** Instrumentations SHOULD use a gauge with type `double` and measure uptime in seconds as a floating point number with the highest precision available.
The actual accuracy would depend on the instrumentation and operating system.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.cpu.allocatable`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.cpu.allocatable -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.cpu.allocatable` | UpDownCounter | `{cpu}` | Amount of cpu allocatable on the node. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.memory.allocatable`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.memory.allocatable -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.memory.allocatable` | UpDownCounter | `By` | Amount of memory allocatable on the node. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.ephemeral_storage.allocatable`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.ephemeral_storage.allocatable -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.ephemeral_storage.allocatable` | UpDownCounter | `By` | Amount of ephemeral-storage allocatable on the node. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.pod.allocatable`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.pod.allocatable -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.pod.allocatable` | UpDownCounter | `{pod}` | Amount of pods allocatable on the node. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.condition.status`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.condition.status -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.condition.status` | UpDownCounter | `{node}` | Describes the condition of a particular Node. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** All possible node condition pairs (type and status) will be reported at each time interval to avoid missing metrics. Condition pairs corresponding to the current conditions' statuses will be non-zero.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.node.condition.status`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The status of the condition, one of True, False, Unknown. [1] | `true`; `false`; `unknown` |
| [`k8s.node.condition.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The condition type of a K8s Node. [2] | `Ready`; `DiskPressure` |

**[1] `k8s.node.condition.status`:** This attribute aligns with the `status` field of the
[NodeCondition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#nodecondition-v1-core)

**[2] `k8s.node.condition.type`:** K8s Node conditions as described
by [K8s documentation](https://v1-32.docs.kubernetes.io/docs/reference/node/node-status/#condition).

This attribute aligns with the `type` field of the
[NodeCondition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#nodecondition-v1-core)

The set of possible values is not limited to those listed here. Managed Kubernetes environments,
or custom controllers MAY introduce additional node condition types.
When this occurs, the exact value as reported by the Kubernetes API SHOULD be used.

---

`k8s.node.condition.status` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `false` | condition_false | ![Development](https://img.shields.io/badge/-development-blue) |
| `true` | condition_true | ![Development](https://img.shields.io/badge/-development-blue) |
| `unknown` | condition_unknown | ![Development](https://img.shields.io/badge/-development-blue) |

---

`k8s.node.condition.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `DiskPressure` | Pressure exists on the disk size—that is, if the disk capacity is low | ![Development](https://img.shields.io/badge/-development-blue) |
| `MemoryPressure` | Pressure exists on the node memory—that is, if the node memory is low | ![Development](https://img.shields.io/badge/-development-blue) |
| `NetworkUnavailable` | The network for the node is not correctly configured | ![Development](https://img.shields.io/badge/-development-blue) |
| `PIDPressure` | Pressure exists on the processes—that is, if there are too many processes on the node | ![Development](https://img.shields.io/badge/-development-blue) |
| `Ready` | The node is healthy and ready to accept pods | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.cpu.time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.cpu.time -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.cpu.time` | Counter | `s` | Total CPU time consumed. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** Total CPU time consumed by the specific Node on all available CPU cores

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.cpu.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.cpu.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.cpu.usage` | Gauge | `{cpu}` | Node's CPU usage, measured in cpus. Range from 0 to the number of allocatable CPUs. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** CPU usage of the specific Node on all available CPU cores, averaged over the sample window

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.memory.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.memory.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.memory.usage` | Gauge | `By` | Memory usage of the Node. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** Total memory usage of the Node

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.memory.available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.memory.available -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.memory.available` | UpDownCounter | `By` | Node memory available. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** Available memory for use.  This is defined as the memory limit - workingSetBytes. If memory limit is undefined, the available bytes is omitted.
This metric is derived from the [MemoryStats.AvailableBytes](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) field of the [NodeStats.Memory](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#NodeStats) of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.memory.rss`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.memory.rss -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.memory.rss` | UpDownCounter | `By` | Node memory RSS. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** The amount of anonymous and swap cache memory (includes transparent hugepages).
This metric is derived from the [MemoryStats.RSSBytes](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) field of the [NodeStats.Memory](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#NodeStats) of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.memory.working_set`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.memory.working_set -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.memory.working_set` | UpDownCounter | `By` | Node memory working set. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** The amount of working set memory. This includes recently accessed memory, dirty memory, and kernel memory. WorkingSetBytes is <= UsageBytes.
This metric is derived from the [MemoryStats.WorkingSetBytes](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) field of the [NodeStats.Memory](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#NodeStats) of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.memory.paging.faults`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.memory.paging.faults -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.memory.paging.faults` | Counter | `{fault}` | Node memory paging faults. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** Cumulative number of major/minor page faults.
This metric is derived from the [MemoryStats.PageFaults](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) and [MemoryStats.MajorPageFaults](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#MemoryStats) fields of the [NodeStats.Memory](https://pkg.go.dev/k8s.io/kubelet@v0.34.0/pkg/apis/stats/v1alpha1#NodeStats) of the Kubelet's stats API.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`system.paging.fault.type`](/docs/registry/attributes/system.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The paging fault type | `minor` |

---

`system.paging.fault.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `major` | major | ![Development](https://img.shields.io/badge/-development-blue) |
| `minor` | minor | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.network.io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.network.io -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.network.io` | Counter | `By` | Network bytes for the Node. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`network.interface.name`](/docs/registry/attributes/network.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The network interface name. | `lo`; `eth0` |
| [`network.io.direction`](/docs/registry/attributes/network.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The network IO operation direction. | `transmit` |

---

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `receive` | receive | ![Development](https://img.shields.io/badge/-development-blue) |
| `transmit` | transmit | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.network.errors`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.network.errors -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.network.errors` | Counter | `{error}` | Node network errors. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`network.interface.name`](/docs/registry/attributes/network.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The network interface name. | `lo`; `eth0` |
| [`network.io.direction`](/docs/registry/attributes/network.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The network IO operation direction. | `transmit` |

---

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `receive` | receive | ![Development](https://img.shields.io/badge/-development-blue) |
| `transmit` | transmit | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.filesystem.available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.filesystem.available -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.filesystem.available` | UpDownCounter | `By` | Node filesystem available bytes. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** This metric is derived from the
[FsStats.AvailableBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#FsStats) field
of the [NodeStats.Fs](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#NodeStats)
of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.filesystem.capacity`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.filesystem.capacity -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.filesystem.capacity` | UpDownCounter | `By` | Node filesystem capacity. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** This metric is derived from the
[FsStats.CapacityBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#FsStats) field
of the [NodeStats.Fs](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#NodeStats)
of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.node.filesystem.usage`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.node.filesystem.usage -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.node.filesystem.usage` | UpDownCounter | `By` | Node filesystem usage. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.node`](/docs/registry/entities/k8s.md#k8s-node) |

**[1]:** This may not equal capacity - available.

This metric is derived from the
[FsStats.UsedBytes](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#FsStats) field
of the [NodeStats.Fs](https://pkg.go.dev/k8s.io/kubelet@v0.33.0/pkg/apis/stats/v1alpha1#NodeStats)
of the Kubelet's stats API.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Deployment metrics

**Description:** Deployment level metrics captured under the namespace `k8s.deployment`.

### Metric: `k8s.deployment.pod.desired`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.deployment.pod.desired -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.deployment.pod.desired` | UpDownCounter | `{pod}` | Number of desired replica pods in this deployment. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.deployment`](/docs/registry/entities/k8s.md#k8s-deployment) |

**[1]:** This metric aligns with the `replicas` field of the
[K8s DeploymentSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#deploymentspec-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.deployment.pod.available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.deployment.pod.available -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.deployment.pod.available` | UpDownCounter | `{pod}` | Total number of available replica pods (ready for at least minReadySeconds) targeted by this deployment. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.deployment`](/docs/registry/entities/k8s.md#k8s-deployment) |

**[1]:** This metric aligns with the `availableReplicas` field of the
[K8s DeploymentStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#deploymentstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## ReplicaSet metrics

**Description:** ReplicaSet level metrics captured under the namespace `k8s.replicaset`.

### Metric: `k8s.replicaset.pod.desired`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.replicaset.pod.desired -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.replicaset.pod.desired` | UpDownCounter | `{pod}` | Number of desired replica pods in this replicaset. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.replicaset`](/docs/registry/entities/k8s.md#k8s-replicaset) |

**[1]:** This metric aligns with the `replicas` field of the
[K8s ReplicaSetSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#replicasetspec-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.replicaset.pod.available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.replicaset.pod.available -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.replicaset.pod.available` | UpDownCounter | `{pod}` | Total number of available replica pods (ready for at least minReadySeconds) targeted by this replicaset. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.replicaset`](/docs/registry/entities/k8s.md#k8s-replicaset) |

**[1]:** This metric aligns with the `availableReplicas` field of the
[K8s ReplicaSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#replicasetstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## ReplicationController metrics

**Description:** ReplicationController level metrics captured under the namespace `k8s.replicationcontroller`.

### Metric: `k8s.replicationcontroller.pod.desired`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.replicationcontroller.pod.desired -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.replicationcontroller.pod.desired` | UpDownCounter | `{pod}` | Number of desired replica pods in this replication controller. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.replicationcontroller`](/docs/registry/entities/k8s.md#k8s-replicationcontroller) |

**[1]:** This metric aligns with the `replicas` field of the
[K8s ReplicationControllerSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#replicationcontrollerspec-v1-core)

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.replicationcontroller.pod.available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.replicationcontroller.pod.available -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.replicationcontroller.pod.available` | UpDownCounter | `{pod}` | Total number of available replica pods (ready for at least minReadySeconds) targeted by this replication controller. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.replicationcontroller`](/docs/registry/entities/k8s.md#k8s-replicationcontroller) |

**[1]:** This metric aligns with the `availableReplicas` field of the
[K8s ReplicationControllerStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#replicationcontrollerstatus-v1-core)

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## StatefulSet metrics

**Description:** StatefulSet level metrics captured under the namespace `k8s.statefulset`.

### Metric: `k8s.statefulset.pod.desired`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.statefulset.pod.desired -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.statefulset.pod.desired` | UpDownCounter | `{pod}` | Number of desired replica pods in this statefulset. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.statefulset`](/docs/registry/entities/k8s.md#k8s-statefulset) |

**[1]:** This metric aligns with the `replicas` field of the
[K8s StatefulSetSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulsetspec-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.statefulset.pod.ready`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.statefulset.pod.ready -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.statefulset.pod.ready` | UpDownCounter | `{pod}` | The number of replica pods created for this statefulset with a Ready Condition. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.statefulset`](/docs/registry/entities/k8s.md#k8s-statefulset) |

**[1]:** This metric aligns with the `readyReplicas` field of the
[K8s StatefulSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulsetstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.statefulset.pod.current`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.statefulset.pod.current -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.statefulset.pod.current` | UpDownCounter | `{pod}` | The number of replica pods created by the statefulset controller from the statefulset version indicated by currentRevision. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.statefulset`](/docs/registry/entities/k8s.md#k8s-statefulset) |

**[1]:** This metric aligns with the `currentReplicas` field of the
[K8s StatefulSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulsetstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.statefulset.pod.updated`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.statefulset.pod.updated -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.statefulset.pod.updated` | UpDownCounter | `{pod}` | Number of replica pods created by the statefulset controller from the statefulset version indicated by updateRevision. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.statefulset`](/docs/registry/entities/k8s.md#k8s-statefulset) |

**[1]:** This metric aligns with the `updatedReplicas` field of the
[K8s StatefulSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulsetstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## HorizontalPodAutoscaler metrics

**Description:** HorizontalPodAutoscaler level metrics captured under the namespace `k8s.hpa`.

### Metric: `k8s.hpa.pod.desired`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.hpa.pod.desired -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.pod.desired` | UpDownCounter | `{pod}` | Desired number of replica pods managed by this horizontal pod autoscaler, as last calculated by the autoscaler. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.hpa`](/docs/registry/entities/k8s.md#k8s-hpa) |

**[1]:** This metric aligns with the `desiredReplicas` field of the
[K8s HorizontalPodAutoscalerStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#horizontalpodautoscalerstatus-v2-autoscaling)

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.pod.current`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.hpa.pod.current -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.pod.current` | UpDownCounter | `{pod}` | Current number of replica pods managed by this horizontal pod autoscaler, as last seen by the autoscaler. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.hpa`](/docs/registry/entities/k8s.md#k8s-hpa) |

**[1]:** This metric aligns with the `currentReplicas` field of the
[K8s HorizontalPodAutoscalerStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#horizontalpodautoscalerstatus-v2-autoscaling)

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.pod.max`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.hpa.pod.max -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.pod.max` | UpDownCounter | `{pod}` | The upper limit for the number of replica pods to which the autoscaler can scale up. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.hpa`](/docs/registry/entities/k8s.md#k8s-hpa) |

**[1]:** This metric aligns with the `maxReplicas` field of the
[K8s HorizontalPodAutoscalerSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#horizontalpodautoscalerspec-v2-autoscaling)

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.pod.min`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.hpa.pod.min -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.pod.min` | UpDownCounter | `{pod}` | The lower limit for the number of replica pods to which the autoscaler can scale down. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.hpa`](/docs/registry/entities/k8s.md#k8s-hpa) |

**[1]:** This metric aligns with the `minReplicas` field of the
[K8s HorizontalPodAutoscalerSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#horizontalpodautoscalerspec-v2-autoscaling)

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.metric.target.cpu.value`

This metric is [opt-in][MetricOptIn].

<!-- semconv metric.k8s.hpa.metric.target.cpu.value -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.metric.target.cpu.value` | Gauge | `{cpu}` | Target value for CPU resource in HPA config. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.hpa`](/docs/registry/entities/k8s.md#k8s-hpa); [`k8s.namespace`](/docs/registry/entities/k8s.md#k8s-namespace) |

**[1]:** This metric aligns with the `value` field of the
[K8s HPA MetricTarget](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#metrictarget-v2-autoscaling).
If the type of the metric is [`ContainerResource`](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-metrics-apis),
the `k8s.container.name` attribute MUST be set to identify the specific container within the pod to which the metric applies.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.container.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [1] | string | The name of the Container from Pod specification, must be unique within a Pod. Container runtime usually uses different globally unique name (`container.name`). | `redis` |
| [`k8s.hpa.metric.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of metric source for the horizontal pod autoscaler. [2] | `Resource`; `ContainerResource` |

**[1] `k8s.container.name`:** if and only if k8s.hpa.metric.type is ContainerResource

**[2] `k8s.hpa.metric.type`:** This attribute reflects the `type` field of spec.metrics[] in the HPA.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.metric.target.cpu.average_value`

This metric is [opt-in][MetricOptIn].

<!-- semconv metric.k8s.hpa.metric.target.cpu.average_value -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.metric.target.cpu.average_value` | Gauge | `{cpu}` | Target average value for CPU resource in HPA config. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.hpa`](/docs/registry/entities/k8s.md#k8s-hpa); [`k8s.namespace`](/docs/registry/entities/k8s.md#k8s-namespace) |

**[1]:** This metric aligns with the `averageValue` field of the
[K8s HPA MetricTarget](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#metrictarget-v2-autoscaling).
If the type of the metric is [`ContainerResource`](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-metrics-apis),
the `k8s.container.name` attribute MUST be set to identify the specific container within the pod to which the metric applies.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.container.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [1] | string | The name of the Container from Pod specification, must be unique within a Pod. Container runtime usually uses different globally unique name (`container.name`). | `redis` |
| [`k8s.hpa.metric.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of metric source for the horizontal pod autoscaler. [2] | `Resource`; `ContainerResource` |

**[1] `k8s.container.name`:** if and only if k8s.hpa.metric.type is ContainerResource

**[2] `k8s.hpa.metric.type`:** This attribute reflects the `type` field of spec.metrics[] in the HPA.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.hpa.metric.target.cpu.average_utilization`

This metric is [opt-in][MetricOptIn].

<!-- semconv metric.k8s.hpa.metric.target.cpu.average_utilization -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.hpa.metric.target.cpu.average_utilization` | Gauge | `1` | Target average utilization, in percentage, for CPU resource in HPA config. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.hpa`](/docs/registry/entities/k8s.md#k8s-hpa); [`k8s.namespace`](/docs/registry/entities/k8s.md#k8s-namespace) |

**[1]:** This metric aligns with the `averageUtilization` field of the
[K8s HPA MetricTarget](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#metrictarget-v2-autoscaling).
If the type of the metric is [`ContainerResource`](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-metrics-apis),
the `k8s.container.name` attribute MUST be set to identify the specific container within the pod to which the metric applies.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.container.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [1] | string | The name of the Container from Pod specification, must be unique within a Pod. Container runtime usually uses different globally unique name (`container.name`). | `redis` |
| [`k8s.hpa.metric.type`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | The type of metric source for the horizontal pod autoscaler. [2] | `Resource`; `ContainerResource` |

**[1] `k8s.container.name`:** if and only if k8s.hpa.metric.type is ContainerResource.

**[2] `k8s.hpa.metric.type`:** This attribute reflects the `type` field of spec.metrics[] in the HPA.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## DaemonSet metrics

**Description:** DaemonSet level metrics captured under the namespace `k8s.daemonset`.

### Metric: `k8s.daemonset.node.current_scheduled`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.daemonset.node.current_scheduled -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.daemonset.node.current_scheduled` | UpDownCounter | `{node}` | Number of nodes that are running at least 1 daemon pod and are supposed to run the daemon pod. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.daemonset`](/docs/registry/entities/k8s.md#k8s-daemonset) |

**[1]:** This metric aligns with the `currentNumberScheduled` field of the
[K8s DaemonSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#daemonsetstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.daemonset.node.desired_scheduled`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.daemonset.node.desired_scheduled -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.daemonset.node.desired_scheduled` | UpDownCounter | `{node}` | Number of nodes that should be running the daemon pod (including nodes currently running the daemon pod). [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.daemonset`](/docs/registry/entities/k8s.md#k8s-daemonset) |

**[1]:** This metric aligns with the `desiredNumberScheduled` field of the
[K8s DaemonSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#daemonsetstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.daemonset.node.misscheduled`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.daemonset.node.misscheduled -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.daemonset.node.misscheduled` | UpDownCounter | `{node}` | Number of nodes that are running the daemon pod, but are not supposed to run the daemon pod. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.daemonset`](/docs/registry/entities/k8s.md#k8s-daemonset) |

**[1]:** This metric aligns with the `numberMisscheduled` field of the
[K8s DaemonSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#daemonsetstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.daemonset.node.ready`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.daemonset.node.ready -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.daemonset.node.ready` | UpDownCounter | `{node}` | Number of nodes that should be running the daemon pod and have one or more of the daemon pod running and ready. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.daemonset`](/docs/registry/entities/k8s.md#k8s-daemonset) |

**[1]:** This metric aligns with the `numberReady` field of the
[K8s DaemonSetStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#daemonsetstatus-v1-apps).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Job metrics

**Description:** Job level metrics captured under the namespace `k8s.job`.

### Metric: `k8s.job.pod.active`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.pod.active -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.pod.active` | UpDownCounter | `{pod}` | The number of pending and actively running pods for a job. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.job`](/docs/registry/entities/k8s.md#k8s-job) |

**[1]:** This metric aligns with the `active` field of the
[K8s JobStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobstatus-v1-batch).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.job.pod.failed`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.pod.failed -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.pod.failed` | UpDownCounter | `{pod}` | The number of pods which reached phase Failed for a job. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.job`](/docs/registry/entities/k8s.md#k8s-job) |

**[1]:** This metric aligns with the `failed` field of the
[K8s JobStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobstatus-v1-batch).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.job.pod.successful`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.pod.successful -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.pod.successful` | UpDownCounter | `{pod}` | The number of pods which reached phase Succeeded for a job. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.job`](/docs/registry/entities/k8s.md#k8s-job) |

**[1]:** This metric aligns with the `succeeded` field of the
[K8s JobStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobstatus-v1-batch).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.job.pod.desired_successful`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.pod.desired_successful -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.pod.desired_successful` | UpDownCounter | `{pod}` | The desired number of successfully finished pods the job should be run with. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.job`](/docs/registry/entities/k8s.md#k8s-job) |

**[1]:** This metric aligns with the `completions` field of the
[K8s JobSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobspec-v1-batch)..

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.job.pod.max_parallel`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.job.pod.max_parallel -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.job.pod.max_parallel` | UpDownCounter | `{pod}` | The max desired number of pods the job should run at any given time. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.job`](/docs/registry/entities/k8s.md#k8s-job) |

**[1]:** This metric aligns with the `parallelism` field of the
[K8s JobSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#jobspec-v1-batch).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## CronJob metrics

**Description:** CronJob level metrics captured under the namespace `k8s.cronjob`.

### Metric: `k8s.cronjob.job.active`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.cronjob.job.active -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.cronjob.job.active` | UpDownCounter | `{job}` | The number of actively running jobs for a cronjob. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.cronjob`](/docs/registry/entities/k8s.md#k8s-cronjob) |

**[1]:** This metric aligns with the `active` field of the
[K8s CronJobStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#cronjobstatus-v1-batch).

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

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.namespace.phase` | UpDownCounter | `{namespace}` | Describes number of K8s namespaces that are currently in a given phase. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.namespace`](/docs/registry/entities/k8s.md#k8s-namespace) |

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.namespace.phase`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The phase of the K8s namespace. [1] | `active`; `terminating` |

**[1] `k8s.namespace.phase`:** This attribute aligns with the `phase` field of the
[K8s NamespaceStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#namespacestatus-v1-core)

---

`k8s.namespace.phase` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `active` | Active namespace phase as described by [K8s API](https://pkg.go.dev/k8s.io/api@v0.31.3/core/v1#NamespacePhase) | ![Development](https://img.shields.io/badge/-development-blue) |
| `terminating` | Terminating namespace phase as described by [K8s API](https://pkg.go.dev/k8s.io/api@v0.31.3/core/v1#NamespacePhase) | ![Development](https://img.shields.io/badge/-development-blue) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## K8s Container metrics

**Description:** K8s Container level metrics captured under the namespace `k8s.container`.

### Metric: `k8s.container.cpu.limit_utilization`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.cpu.limit_utilization -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.cpu.limit_utilization` | Gauge | `1` | The ratio of container CPU usage to its CPU limit. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** The value range is [0.0,1.0]. A value of 1.0 means the container is using 100% of its CPU limit. If the CPU limit is not set, this metric SHOULD NOT be emitted for that container.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.cpu.request_utilization`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.cpu.request_utilization -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.cpu.request_utilization` | Gauge | `1` | The ratio of container CPU usage to its CPU request. | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.cpu.limit`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.container.cpu.limit -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.cpu.limit` | UpDownCounter | `{cpu}` | Maximum CPU resource limit set for the container. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.container.cpu.request`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.container.cpu.request -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.cpu.request` | UpDownCounter | `{cpu}` | CPU resource requested for the container. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.container.memory.limit`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.container.memory.limit -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.memory.limit` | UpDownCounter | `By` | Maximum memory resource limit set for the container. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.container.memory.request`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.container.memory.request -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.memory.request` | UpDownCounter | `By` | Memory resource requested for the container. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.container.storage.limit`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.container.storage.limit -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.storage.limit` | UpDownCounter | `By` | Maximum storage resource limit set for the container. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.container.storage.request`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.container.storage.request -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.storage.request` | UpDownCounter | `By` | Storage resource requested for the container. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.container.ephemeral_storage.limit`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.container.ephemeral_storage.limit -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.ephemeral_storage.limit` | UpDownCounter | `By` | Maximum ephemeral storage resource limit set for the container. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.container.ephemeral_storage.request`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.container.ephemeral_storage.request -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.ephemeral_storage.request` | UpDownCounter | `By` | Ephemeral storage resource requested for the container. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** See https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#resourcerequirements-v1-core for details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.container.restart.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.restart.count -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.restart.count` | UpDownCounter | `{restart}` | Describes how many times the container has restarted (since the last counter reset). [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** This value is pulled directly from the K8s API and the value can go indefinitely high and be reset to 0
at any time depending on how your kubelet is configured to prune dead containers.
It is best to not depend too much on the exact value but rather look at it as
either == 0, in which case you can conclude there were no restarts in the recent past, or > 0, in which case
you can conclude there were restarts in the recent past, and not try and analyze the value beyond that.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Metric: `k8s.container.ready`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.k8s.container.ready -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.container.ready` | UpDownCounter | `{container}` | Indicates whether the container is currently marked as ready to accept traffic, based on its readiness probe (1 = ready, 0 = not ready). [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.container`](/docs/registry/entities/k8s.md#k8s-container) |

**[1]:** This metric SHOULD reflect the value of the `ready` field in the
[K8s ContainerStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#containerstatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Resource Quota metrics

**Description:** Resource Quota level metrics captured under the namespace `k8s.resourcequota`.

### Metric: `k8s.resourcequota.cpu.limit.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.cpu.limit.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.cpu.limit.hard` | UpDownCounter | `{cpu}` | The CPU limits in a specific namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.cpu.limit.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.cpu.limit.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.cpu.limit.used` | UpDownCounter | `{cpu}` | The CPU limits in a specific namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.cpu.request.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.cpu.request.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.cpu.request.hard` | UpDownCounter | `{cpu}` | The CPU requests in a specific namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.cpu.request.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.cpu.request.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.cpu.request.used` | UpDownCounter | `{cpu}` | The CPU requests in a specific namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.memory.limit.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.memory.limit.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.memory.limit.hard` | UpDownCounter | `By` | The memory limits in a specific namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.memory.limit.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.memory.limit.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.memory.limit.used` | UpDownCounter | `By` | The memory limits in a specific namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.memory.request.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.memory.request.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.memory.request.hard` | UpDownCounter | `By` | The memory requests in a specific namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.memory.request.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.memory.request.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.memory.request.used` | UpDownCounter | `By` | The memory requests in a specific namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.hugepage_count.request.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.hugepage_count.request.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.hugepage_count.request.hard` | UpDownCounter | `{hugepage}` | The huge page requests in a specific namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.hugepage.size`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The size (identifier) of the K8s huge page. | `2Mi` |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.hugepage_count.request.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.hugepage_count.request.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.hugepage_count.request.used` | UpDownCounter | `{hugepage}` | The huge page requests in a specific namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.hugepage.size`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The size (identifier) of the K8s huge page. | `2Mi` |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.storage.request.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.storage.request.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.storage.request.hard` | UpDownCounter | `By` | The storage requests in a specific namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

The `k8s.storageclass.name` should be required when a resource quota is defined for a specific
storage class.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.storageclass.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [1] | string | The name of K8s [StorageClass](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#storageclass-v1-storage-k8s-io) object. | `gold.storageclass.storage.k8s.io` |

**[1] `k8s.storageclass.name`:** The `k8s.storageclass.name` should be required when a resource quota is defined for a specific
storage class.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.storage.request.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.storage.request.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.storage.request.used` | UpDownCounter | `By` | The storage requests in a specific namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

The `k8s.storageclass.name` should be required when a resource quota is defined for a specific
storage class.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.storageclass.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [1] | string | The name of K8s [StorageClass](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#storageclass-v1-storage-k8s-io) object. | `gold.storageclass.storage.k8s.io` |

**[1] `k8s.storageclass.name`:** The `k8s.storageclass.name` should be required when a resource quota is defined for a specific
storage class.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.persistentvolumeclaim_count.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.persistentvolumeclaim_count.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.persistentvolumeclaim_count.hard` | UpDownCounter | `{persistentvolumeclaim}` | The total number of PersistentVolumeClaims that can exist in the namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

The `k8s.storageclass.name` should be required when a resource quota is defined for a specific
storage class.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.storageclass.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [1] | string | The name of K8s [StorageClass](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#storageclass-v1-storage-k8s-io) object. | `gold.storageclass.storage.k8s.io` |

**[1] `k8s.storageclass.name`:** The `k8s.storageclass.name` should be required when a resource quota is defined for a specific
storage class.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.persistentvolumeclaim_count.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.persistentvolumeclaim_count.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.persistentvolumeclaim_count.used` | UpDownCounter | `{persistentvolumeclaim}` | The total number of PersistentVolumeClaims that can exist in the namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

The `k8s.storageclass.name` should be required when a resource quota is defined for a specific
storage class.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.storageclass.name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [1] | string | The name of K8s [StorageClass](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#storageclass-v1-storage-k8s-io) object. | `gold.storageclass.storage.k8s.io` |

**[1] `k8s.storageclass.name`:** The `k8s.storageclass.name` should be required when a resource quota is defined for a specific
storage class.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.ephemeral_storage.request.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.ephemeral_storage.request.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.ephemeral_storage.request.hard` | UpDownCounter | `By` | The sum of local ephemeral storage requests in the namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.ephemeral_storage.request.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.ephemeral_storage.request.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.ephemeral_storage.request.used` | UpDownCounter | `By` | The sum of local ephemeral storage requests in the namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.ephemeral_storage.limit.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.ephemeral_storage.limit.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.ephemeral_storage.limit.hard` | UpDownCounter | `By` | The sum of local ephemeral storage limits in the namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.ephemeral_storage.limit.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.ephemeral_storage.limit.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.ephemeral_storage.limit.used` | UpDownCounter | `By` | The sum of local ephemeral storage limits in the namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.object_count.hard`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.object_count.hard -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.object_count.hard` | UpDownCounter | `{object}` | The object count limits in a specific namespace.
The value represents the configured quota limit of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `hard` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.resourcequota.resource_name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the K8s resource a resource quota defines. [1] | `count/replicationcontrollers` |

**[1] `k8s.resourcequota.resource_name`:** The value for this attribute can be either the full `count/<resource>[.<group>]` string (e.g., count/deployments.apps, count/pods), or, for certain core Kubernetes resources, just the resource name (e.g., pods, services, configmaps). Both forms are supported by Kubernetes for object count quotas. See [Kubernetes Resource Quotas documentation](https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-on-object-count) for more details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

### Metric: `k8s.resourcequota.object_count.used`

This metric is [recommended][MetricRecommended].

<!-- markdownlint-disable -->
<!-- semconv metric.k8s.resourcequota.object_count.used -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

| Name | Instrument Type | Unit (UCUM) | Description | Stability | Entity Associations |
| -------- | --------------- | ----------- | -------------- | --------- | ------ |
| `k8s.resourcequota.object_count.used` | UpDownCounter | `{object}` | The object count limits in a specific namespace.
The value represents the current observed total usage of the resource in the namespace. [1] | ![Development](https://img.shields.io/badge/-development-blue) | [`k8s.resourcequota`](/docs/registry/entities/k8s.md#k8s-resourcequota) |

**[1]:** This metric is retrieved from the `used` field of the
[K8s ResourceQuotaStatus](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.32/#resourcequotastatus-v1-core).

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`k8s.resourcequota.resource_name`](/docs/registry/attributes/k8s.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the K8s resource a resource quota defines. [1] | `count/replicationcontrollers` |

**[1] `k8s.resourcequota.resource_name`:** The value for this attribute can be either the full `count/<resource>[.<group>]` string (e.g., count/deployments.apps, count/pods), or, for certain core Kubernetes resources, just the resource name (e.g., pods, services, configmaps). Both forms are supported by Kubernetes for object count quotas. See [Kubernetes Resource Quotas documentation](https://kubernetes.io/docs/concepts/policy/resource-quotas/#quota-on-object-count) for more details.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->
<!-- markdownlint-restore-->

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
[MetricOptIn]: /docs/general/metric-requirement-level.md#opt-in
