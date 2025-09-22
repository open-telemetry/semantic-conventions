<!--- Hugo front matter used to generate the website version of this page:
linkTitle: K8s attributes
--->

# Specify resource attributes using Kubernetes annotations

All annotations with the `resource.opentelemetry.io/` prefix should be translated into the corresponding resource
attributes.

For example, the annotation `resource.opentelemetry.io/service.name` should be translated into the `service.name`
attribute.

## Service attributes

The following [service resource attributes](../registry/attributes/service.md) are recommended for Kubernetes services.

There are different ways to calculate the service attributes.

1. [Well-Known Labels](https://kubernetes.io/docs/reference/labels-annotations-taints/)
2. Annotations on the pod template that have the `resource.opentelemetry.io/`
   prefix as described in this page.
3. A function of the Kubernetes resource attributes defined above

This translation can typically be done by an OpenTelemetry Collector component like the
[Kubernetes Attribute Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/k8sattributesprocessor).

Tools offering this functionality should provide an opt-in flag for the use of well-known labels,
since users may not be aware that their labels are being used for this purpose.

Each attribute has a priority order for how it should be calculated as described below.

### How `service.namespace` should be calculated

Choose the first value found:

1. `pod.annotation[resource.opentelemetry.io/service.namespace]`
2. `k8s.namespace.name`

### How `service.name` should be calculated

Choose the first value found:

- `pod.annotation[resource.opentelemetry.io/service.name]`
- `pod.label[app.kubernetes.io/instance]` (well-known label
  [app.kubernetes.io/instance](https://kubernetes.io/docs/reference/labels-annotations-taints/#app-kubernetes-io-instance))
- `pod.label[app.kubernetes.io/name]` (well-known label
  [app.kubernetes.io/name](https://kubernetes.io/docs/reference/labels-annotations-taints/#app-kubernetes-io-name))
- `k8s.deployment.name`
- `k8s.replicaset.name`
- `k8s.statefulset.name`
- `k8s.daemonset.name`
- `k8s.cronjob.name`
- `k8s.job.name`
- `k8s.pod.name`
- `k8s.container.name`

The rationale is to go from the ancestor to the descendant in the Kubernetes resource hierarchy, e.g. from `deployment`
to `pod` - see [Kubernetes Object Hierarchy](https://gist.github.com/fardjad/ea3c38d566c845e0b353237d3959e365).

### How `service.version` should be calculated

Choose the first value found:

- `pod.annotation[resource.opentelemetry.io/service.version]`
- `pod.label[app.kubernetes.io/version]` (well-known label
  [app.kubernetes.io/version](https://kubernetes.io/docs/reference/labels-annotations-taints/#app-kubernetes-io-version))
- calculate the version using algorithm described below

1. calculate tag and digest using the algorithm described in the
   [reference library](https://github.com/distribution/reference/blob/main/reference.go)
2. choose the first value found:
   - `<tag>@<digest>`
   - `<digest>`
   - `<tag>`

### How `service.instance.id` should be calculated

Choose the first value found:

- `pod.annotation[resource.opentelemetry.io/service.instance.id]`
- `concat([k8s.namespace.name, k8s.pod.name, k8s.container.name], '.')`

Note that the container restart count is not included in the `service.instance.id` calculation, because it makes
troubleshooting harder when the ID changes on every restart, e.g. in a crash loop.
