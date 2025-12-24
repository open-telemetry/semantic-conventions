# Recommended vs Opt-In CPU Metrics

The [**Instrument Naming**](/docs/general/naming.md#instrument-naming) section
defines the `*.usage`, `*.limit`, `*.utilization`, and `*.time` metrics, but it
does **not** specify their
[**requirement levels**](/docs/general/metric-requirement-level.md)
(`required`,`recommended`, `opt-in`). Because these metrics convey overlapping
information in different forms, implementations may become inconsistent without
explicit guidance.

This document provides guidance regarding the requirement level of the CPU
metrics across the different areas of the Semantic Conventions.

## Policy

* **recommended**: `*.cpu.time`
* **opt-in** (optional): `*.cpu.utilization`, `*.cpu.usage`,
  `*.cpu.limit_utilization`, `*.cpu.request_utilization`

## Rationale

`*.cpu.time` metrics are unambiguous, as they are measured directly from the
operating system or runtime. They aggregate cleanly across CPUs and resources,
support spatial aggregation, and form a consistent base for deriving usage and
utilization in backends or at the time of collection for convenience when
possible.

By contrast, `*.cpu.usage` and `*.cpu.utilization` are derived or
presentation-focused metrics. Their definitions may vary across implementations,
especially in containerized and Kubernetes environments where CPU limits are
defined per container or Pod. This leads to ambiguity and inconsistencies in how
these metrics should be calculated and reported. While they can be convenient
for dashboards and alerts, they should remain optional and only implemented when
specific environments explicitly provide them. For example
[Kubelet's stats endpoint](https://github.com/kubernetes/kubernetes/blob/dbc7fe1b7fec4a76562d5e1565072a447fec5439/staging/src/k8s.io/kubelet/pkg/apis/stats/v1alpha1/types.go#L230-L233)
provides an opinionated metrics for `*.cpu.usage` that can be used directly, yet
should be optional since it is derived from the `.cpu.time` metrics and is not
uniquely implemented in other systems like the
[Docker stats API](https://docs.docker.com/reference/api/engine/version/v1.52/#tag/Container/operation/ContainerStats).

## Implementation Guidance

* SHOULD emit `*.cpu.time` by default for system, process container, and k8s
  resources.
* SHOULD gate `*.cpu.*utilization` and `*.cpu.usage` metrics behind explicit
  configuration.

## Backend Guidance

* SHOULD provide transforms or views to derive utilization/usage from
  `*.cpu.time` when helpful.
* SHOULD treat `*.cpu.time` as the canonical source of truth across system,
  container, and k8s resources.

## Using CPU Time

The cumulative CPU time values can be used to derive the utilization or usage
metrics.

**Usage** metric can be computed using a `rate()` function with a given window,
dividing by the window size. CPU usage usually is measured in core-seconds.

**Utilization** can be computed using the above result divided by the given CPU
limit and is usually in the range of [0, 1].

Examples of how the CPU time can be used to derive usage or utilization metrics,
can be found bellow:

### CPU Time to Usage

`rate(system.cpu.time[5m])/(5*60)` measured in core-seconds.

This is the PromQL equivalent. The rate() function is equivalent to the
subtraction of the current to the previous value, while the denominator is the
elapsed time in seconds.

### CPU Time to Utilization

`rate(system.cpu.time[5m])/(5*60)` measured in [0, 1] per core (limit equals to
1 core)

`rate(k8s.pod.cpu.time[5m])/(5*60)/k8s.pod.cpu.limit`

The above will give the `k8s.pod.cpu.limit_utilization` derived metric.

### Utilization excluding non-`idle` states

To represent the utilization as an expression of the percentage of time the
system spent in non-`idle` states, the following can be used:

`sum(rate(system.cpu.time{cpu.mode!="idle"}[5m]) without (cpu.mode))/(5*60))`
measured in [0, 1] per core.

### Total utilization of the whole system

To get the utilization of the whole system, an average across all cores can be
used:

`avg(sum(rate(system.cpu.time{cpu.mode!="idle"}[5m])) by (cpu.logical_number))/(5*60)`

Note that the above formulas can be ambigous and hence they are not standardized
as part of the Semantic Conventions project. They are only provided as examples.

Projects like
[Prometheus Node Exporter](https://github.com/prometheus/node_exporter/blob/b959d48df950d5c446660eca3354c26eb997ca44/docs/node-mixin/lib/prom-mixin.libsonnet#L85-L87)
come with their own formula for calculating System's utilization.

The standardization of `k8s.*.cpu.usage` is an exception since it is collected
directly from the Kubelet's Stats API and is K8s specific.

## References

1. [System CPU Utilization gist](https://gist.github.com/braydonk/b2381da98dc3c4fd5ac064045d556634)
   by Braydon Kains (@braydonk)
2. Attempt to introduce an
   [optional normalized total CPU utilization metric](https://github.com/open-telemetry/semantic-conventions/issues/1873)
