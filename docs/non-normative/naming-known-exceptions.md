<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Naming known exceptions 
--->

# Kubernetes naming exceptions

Kubernetes users are accustomed to the single-word resource names used in the Kubernetes API (e.g., `replicaset`, `statefulset`, `daemonset`, `replicationcontroller`, `resourcequota`). Using these same names in telemetry data makes it easier for users to map the data to familiar Kubernetes concepts and commands (e.g., `kubectl get replicaset`).

When naming entities, attributes, or metrics related to Kubernetes objects, prioritize using the exact single-word form from the official Kubernetes API object names (i.e., borrow the existing single-word term from the API when there is a 1:1 mapping). The official list of API object names can be found in the [Kubernetes API reference documentation](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.33/). For new terms or fields, follow the [general naming considerations](../general/naming.md).

## Naming Recommendations

- For resources that map 1:1 to Kubernetes API object names, use the exact single-word form from the Kubernetes API (no underscores, words concatenated as in the API).

### Examples

```text
Use:    k8s.replicaset.uid      (not k8s.replica_set.uid)
Use:    k8s.resourcequota.uid   (not k8s.resource_quota.uid)
```
