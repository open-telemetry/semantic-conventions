<!--- Hugo front matter used to generate the website version of this page:
linkTitle: K8s naming
--->

# Kubernetes Naming Guidance

Kubernetes users are accustomed to the single-word resource names used in the Kubernetes API (e.g., `replicaset`, `statefulset`, `daemonset`, `replicationcontroller`, `resourcequota`). Using these same names in telemetry data makes it easier for users to map the data to familiar Kubernetes concepts and commands (e.g., `kubectl get replicaset`). 

This naming style avoids ambiguity, and reduces the need to decide when to split or join words with underscores, which can lead to inconsistencies.

When naming resources, attributes, or metrics related to Kubernetes objects, prioritize consistency with Kubernetes API naming over the [general naming considerations](../general/naming.md), as long as the resulting name adheres to the general naming rules.

## Naming Recommendations

- **Use single-word forms**: Follow the single-word naming style used in the Kubernetes API.
- **Avoid short-form abbreviations**: Use abbreviations only if they are widely recognized in the Kubernetes community (e.g., `hpa` for HorizontalPodAutoscaler, which is also a valid short form in `kubectl`).

### Examples

```text
Use:    k8s.replicaset.uid      (not k8s.replica_set.uid)
Use:    k8s.resourcequota.uid   (not k8s.resource_quota.uid)
```
