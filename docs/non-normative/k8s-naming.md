<!--- Hugo front matter used to generate the website version of this page:
linkTitle: K8s naming
--->

# Kubernetes Naming Guidance

When naming resource, attributes, or metrics related to Kubernetes objects, **prioritize consistency with Kubernetes API naming** over certain Opentelemetry's naming conventions, as long as the resulting name is valid per the general naming rules.

**Rationale:**  
Kubernetes users are accustomed to the single-word resource names used in the Kubernetes API (e.g., `replicaset`, `statefulset`, `daemonset`, `replicationcontroller`, `resourcequota`).  
Using the same names as the Kubernetes API makes it easier for users to map telemetry data to familiar Kubernetes concepts and commands (e.g., `kubectl get replicaset`).  
This approach avoids ambiguity and reduces the need to decide when to split or join words with underscores, which can be inconsistent.

- For new attributes, **prefer the single-word form** as used in the Kubernetes API.
- **Short-form names (abbreviations) should be avoided** unless they are widely recognized in the Kubernetes community (e.g., `hpa` for HorizontalPodAutoscaler).

**Examples:**

```text
Use:    k8s.replicaset.uid           (not k8s.replica_set.uid)
Use:    k8s.resourcequota.uid         (not k8s.resource_quota.uid)
```
