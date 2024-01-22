# Kubernetes

## Kubernetes Resource Attributes

<!-- semconv registry.k8s(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `k8s.cluster.name` | string | The name of the cluster. | `opentelemetry-cluster` |
| `k8s.cluster.uid` | string | A pseudo-ID for the cluster, set to the UID of the `kube-system` namespace. [1] | `218fc5a9-a5f1-4b54-aa05-46717d0ab26d` |
| `k8s.container.name` | string | The name of the Container from Pod specification, must be unique within a Pod. Container runtime usually uses different globally unique name (`container.name`). | `redis` |
| `k8s.container.restart_count` | int | Number of times the container was restarted. This attribute can be used to identify a particular container (running or stopped) within a container spec. | `0`; `2` |
| `k8s.cronjob.name` | string | The name of the CronJob. | `opentelemetry` |
| `k8s.cronjob.uid` | string | The UID of the CronJob. | `275ecb36-5aa8-4c2a-9c47-d8bb681b9aff` |
| `k8s.daemonset.name` | string | The name of the DaemonSet. | `opentelemetry` |
| `k8s.daemonset.uid` | string | The UID of the DaemonSet. | `275ecb36-5aa8-4c2a-9c47-d8bb681b9aff` |
| `k8s.deployment.name` | string | The name of the Deployment. | `opentelemetry` |
| `k8s.deployment.uid` | string | The UID of the Deployment. | `275ecb36-5aa8-4c2a-9c47-d8bb681b9aff` |
| `k8s.job.name` | string | The name of the Job. | `opentelemetry` |
| `k8s.job.uid` | string | The UID of the Job. | `275ecb36-5aa8-4c2a-9c47-d8bb681b9aff` |
| `k8s.namespace.name` | string | The name of the namespace that the pod is running in. | `default` |
| `k8s.node.name` | string | The name of the Node. | `node-1` |
| `k8s.node.uid` | string | The UID of the Node. | `1eb3a0c6-0477-4080-a9cb-0cb7db65c6a2` |
| `k8s.pod.annotation.<key>` | string | The annotation key-value pairs placed on the Pod, the `<key>` being the annotation name, the value being the annotation value. | `k8s.pod.annotation.kubernetes.io/enforce-mountable-secrets=true`; `k8s.pod.annotation.mycompany.io/arch=x64`; `k8s.pod.annotation.data=` |
| `k8s.pod.label.<key>` | string | The label key-value pairs placed on the Pod, the `<key>` being the label name, the value being the label value. | `k8s.pod.label.app=my-app`; `k8s.pod.label.mycompany.io/arch=x64`; `k8s.pod.label.data=` |
| `k8s.pod.name` | string | The name of the Pod. | `opentelemetry-pod-autoconf` |
| `k8s.pod.uid` | string | The UID of the Pod. | `275ecb36-5aa8-4c2a-9c47-d8bb681b9aff` |
| `k8s.replicaset.name` | string | The name of the ReplicaSet. | `opentelemetry` |
| `k8s.replicaset.uid` | string | The UID of the ReplicaSet. | `275ecb36-5aa8-4c2a-9c47-d8bb681b9aff` |
| `k8s.statefulset.name` | string | The name of the StatefulSet. | `opentelemetry` |
| `k8s.statefulset.uid` | string | The UID of the StatefulSet. | `275ecb36-5aa8-4c2a-9c47-d8bb681b9aff` |

**[1]:** K8s doesn't have support for obtaining a cluster ID. If this is ever
added, we will recommend collecting the `k8s.cluster.uid` through the
official APIs. In the meantime, we are able to use the `uid` of the
`kube-system` namespace as a proxy for cluster ID. Read on for the
rationale.

Every object created in a K8s cluster is assigned a distinct UID. The
`kube-system` namespace is used by Kubernetes itself and will exist
for the lifetime of the cluster. Using the `uid` of the `kube-system`
namespace is a reasonable proxy for the K8s ClusterID as it will only
change if the cluster is rebuilt. Furthermore, Kubernetes UIDs are
UUIDs as standardized by
[ISO/IEC 9834-8 and ITU-T X.667](https://www.itu.int/ITU-T/studygroups/com17/oid.html).
Which states:

> If generated according to one of the mechanisms defined in Rec.
  ITU-T X.667 | ISO/IEC 9834-8, a UUID is either guaranteed to be
  different from all other UUIDs generated before 3603 A.D., or is
  extremely likely to be different (depending on the mechanism chosen).

Therefore, UIDs between clusters should be extremely unlikely to
conflict.
<!-- endsemconv -->
