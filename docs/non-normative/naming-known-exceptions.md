<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Kubernetes naming examples
--->

# Kubernetes naming examples

Kubernetes users are accustomed to the single-word resource names used in the Kubernetes API (e.g., `replicaset`, `statefulset`, `daemonset`, `replicationcontroller`, `resourcequota`). Using these same names in telemetry data makes it easier for users to map the data to familiar Kubernetes concepts and commands (e.g., `kubectl get replicaset`).

These resource names are examples of established concatenated forms under the
[general naming considerations](../general/naming.md#general-naming-considerations),
not a separate Kubernetes-specific exception. When naming entities, attributes,
or metrics that map 1:1 to Kubernetes resources, use the same concatenated forms.
The official list of API object names can be found in the
[Kubernetes API reference documentation](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.33/).
For new terms or fields, follow the general naming considerations. CamelCase or
PascalCase in an individual API field does not, by itself, justify concatenation.

## Naming Recommendations

- For resources that map 1:1 to Kubernetes API object names, use the exact single-word form from the Kubernetes API (no underscores, words concatenated as in the API).

### Examples

```text
Use:    k8s.replicaset.uid      (not k8s.replica_set.uid)
Use:    k8s.resourcequota.uid   (not k8s.resource_quota.uid)
```
