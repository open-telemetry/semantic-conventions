<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
--->

# Semantic conventions for CI/CD span lifecycle events

**Status**: [Development][DocumentStatus]

This document defines lifecycle events for CI/CD spans that may run for a long time.
They make these spans visible while they run, and let consumers rebuild a span
that the process which started it can no longer end, for example after the
CI/CD controller restarted.

<!-- START doctoc -->

- [Overview](#overview)
- [Merge rules](#merge-rules)
- [Export and duplicates](#export-and-duplicates)
- [Pipeline run events](#pipeline-run-events)
  - [Pipeline run started](#pipeline-run-started)
  - [Pipeline run progress](#pipeline-run-progress)
  - [Pipeline run ended](#pipeline-run-ended)
- [Pipeline task run events](#pipeline-task-run-events)
  - [Pipeline task run started](#pipeline-task-run-started)
  - [Pipeline task run progress](#pipeline-task-run-progress)
  - [Pipeline task run ended](#pipeline-task-run-ended)
- [Open questions](#open-questions)

<!-- END doctoc -->

## Overview

The [pipeline run and pipeline task run spans](cicd-spans.md) may run for a long time.
Instrumentation MAY emit the following lifecycle events for them:

| Span type | Started | Progress | Ended |
| --- | --- | --- | --- |
| `cicd.server.pipeline.run` | `cicd.server.pipeline.run.started` | `cicd.server.pipeline.run.progress` | `cicd.server.pipeline.run.ended` |
| `cicd.pipeline.task` | `cicd.pipeline.task.started` | `cicd.pipeline.task.progress` | `cicd.pipeline.task.ended` |

- `started` is emitted when the span starts. It carries the span's name, parent,
  TraceState and the span attributes known at that time.
- `progress` is emitted while the span runs, periodically (a heartbeat) and/or
  when the span changes. It carries only what changed since the previous
  lifecycle event for the same span.
- `ended` is emitted when the span ends. It carries the complete span, so that a
  consumer can build the span from it alone.

The lifecycle events supplement the span, they don't replace it:

- Instrumentation creates the span as usual. The sampler decides about the span,
  the SDK assigns its IDs, and its children use it as their parent.
- The lifecycle events are emitted in addition, with the span's trace context
  (TraceId, SpanId and TraceFlags).
- The lifecycle events SHOULD only be emitted for sampled spans, so that the
  events and the span are sampled consistently.

A producer that doesn't hold the SDK span, for example a CI/CD controller that
restarted while a pipeline run was running, emits the `progress` and `ended`
events itself, using the trace ID, span ID and trace flags it stored for the
span. Such a producer MUST provide a complete `ended` event.

The span type and the span kind are given by the event name: `SERVER` for
pipeline runs and `INTERNAL` for pipeline task runs. The pipeline run's identity
(`cicd.pipeline.name`, `cicd.pipeline.run.id`) comes from the Resource, through
the `cicd.pipeline` and `cicd.pipeline.run` entities, as it does for the span.

Example: a pipeline run where the controller restarts while the run is executing.

```text
t0  cicd.server.pipeline.run.started   trace=T span=S cicd.span.name="RUN build" cicd.span.parent.id=P
t1  cicd.server.pipeline.run.progress  trace=T span=S                                   (heartbeat)
t2  cicd.server.pipeline.run.progress  trace=T span=S cicd.pipeline.run.state=executing
    ... the controller restarts ...
t9  cicd.server.pipeline.run.ended     trace=T span=S cicd.span.name="RUN build" cicd.span.parent.id=P
                                       cicd.span.start_time=t0 cicd.pipeline.result=timeout
                                       otel.status_code=ERROR
```

A consumer that received all events builds a span from `t0` to `t9` with the
attributes of the `ended` event, plus `cicd.pipeline.run.state=executing` from
the `progress` event at `t2`. A consumer that received only the `ended` event
builds the same span without `cicd.pipeline.run.state`.

## Merge rules

A consumer builds a span by merging all lifecycle events that share a trace ID
and span ID.

1. **Fixed fields** are set when the span starts and can't change: trace ID,
   span ID, parent span ID (`cicd.span.parent.id`), span kind and span type
   (given by the event name), start time and TraceState
   (`cicd.span.trace_state`). Every event that carries one of them MUST carry
   the same value.
2. **Changeable fields** are the span name (`cicd.span.name`) and the span
   attributes. They are merged per key: the value from the event with the later
   timestamp wins.
3. **Nothing is removed.** A key missing from an event means "unchanged or
   unknown", never "removed".
4. **`ended` is final.** Its values win over those of any earlier event,
   regardless of the order in which the events arrive. The span's status and end
   time come only from `ended`.
5. **Merging is idempotent.** Receiving the same event twice, for example after
   an export retry, doesn't change the result.

Events that arrive after the consumer has emitted the span are dropped.

| `ended` compared to earlier events | Result |
| --- | --- |
| carries more attributes | they are added |
| carries fewer attributes | the earlier ones are kept |
| carries a different value | the value from `ended` is used |
| carries a different fixed field | the value from `ended` is used, and the consumer SHOULD report the inconsistency |

Building a span from `ended` alone and building it from all events give the same
span, except for attributes that only earlier events carried. That only happens
when the process ending the span is not the one that started it.

## Export and duplicates

Because the span is still exported as usual, a deployment that also rebuilds
spans from the lifecycle events gets each of these spans twice. Deployments that
rebuild spans from the lifecycle events SHOULD drop the normally exported span of
the same span type. The trace SDK specification has no built-in span filter, so
this is a configuration choice, for example:

- a custom `SpanProcessor` in the SDK that doesn't forward `OnEnd` to the
  exporting span processor for these spans;
- the [Collector `filter` processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor),
  dropping these spans from the trace pipeline.

Deployments that don't rebuild spans keep the exported span, and can use the
lifecycle events as the live status of running pipeline runs and task runs.

## Pipeline run events

### Pipeline run started

<!-- semconv event.cicd.server.pipeline.run.started -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

The event name MUST be `cicd.server.pipeline.run.started`.

Reports that a CI/CD pipeline run span has started.

The event's trace context (TraceId, SpanId and TraceFlags) MUST be the
span's. Its timestamp MUST be the span's start time.

The event SHOULD only be emitted for sampled spans.

Besides the attributes listed below, the event MAY carry the span's other
attributes, with unchanged keys and values.

The pipeline run's identity comes from the Resource (the `cicd.pipeline`
and `cicd.pipeline.run` entities), as it does for the span.

See [CI/CD span lifecycle events](/docs/cicd/cicd-events.md) for how
consumers combine the lifecycle events of a span.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`cicd.span.name`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the span that a CI/CD span lifecycle event reports on. [1] | `RUN Build and Test` |
| [`cicd.span.parent.id`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` If the span has a parent. | string | The span ID of the parent of the span that a CI/CD span lifecycle event reports on, as 16 lowercase hex characters. [2] | `b7ad6b7169203331` |
| [`cicd.span.trace_state`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` If the span's TraceState is not empty. | string | The W3C `tracestate` of the span that a CI/CD span lifecycle event reports on, in header format. [3] | `ot=th:8` |
| [`cicd.pipeline.action.name`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Opt-In` | string | The kind of action a pipeline run is performing. | `BUILD`; `RUN`; `SYNC` [(see more)](#cicd-pipeline-action-name-values) |

**[1] `cicd.span.name`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[2] `cicd.span.parent.id`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[3] `cicd.span.trace_state`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

---

<a id="cicd-pipeline-action-name-values"></a>

`cicd.pipeline.action.name` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `BUILD` | The pipeline run is executing a build. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `RUN` | The pipeline run is executing. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `SYNC` | The pipeline run is executing a sync. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Pipeline run progress

<!-- semconv event.cicd.server.pipeline.run.progress -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

The event name MUST be `cicd.server.pipeline.run.progress`.

Reports that a CI/CD pipeline run span is still running, and what changed since the previous lifecycle event for the same span.

The event's trace context (TraceId, SpanId and TraceFlags) MUST be the
span's. Its timestamp is the time the event was emitted.

The event SHOULD only be emitted for sampled spans.

The event carries only what changed since the previous lifecycle event for
the same span, including span attributes not listed below. A heartbeat
carries no attributes. A missing attribute means unchanged or unknown,
never removed.

The pipeline run's identity comes from the Resource (the `cicd.pipeline`
and `cicd.pipeline.run` entities), as it does for the span.

See [CI/CD span lifecycle events](/docs/cicd/cicd-events.md) for how
consumers combine the lifecycle events of a span.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`cicd.pipeline.run.state`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Conditionally Required` [1] | string | The pipeline run goes through these states during its lifecycle. | `pending`; `executing`; `finalizing` [(see more)](#cicd-pipeline-run-state-values) |
| [`cicd.span.name`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [2] | string | The name of the span that a CI/CD span lifecycle event reports on. [3] | `RUN Build and Test` |

**[1] `cicd.pipeline.run.state`:** If the pipeline run state changed since the previous lifecycle event for the same span.

**[2] `cicd.span.name`:** If the span name changed since the previous lifecycle event for the same span.

**[3] `cicd.span.name`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

---

<a id="cicd-pipeline-run-state-values"></a>

`cicd.pipeline.run.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `executing` | The executing state spans the execution of any run tasks (eg. build, test). | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `finalizing` | The finalizing state spans from when the run has finished executing (eg. cleanup of run resources). | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `pending` | The run pending state spans from the event triggering the pipeline run until the execution of the run starts (eg. time spent in a queue, provisioning agents, creating run resources). | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Pipeline run ended

<!-- semconv event.cicd.server.pipeline.run.ended -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

The event name MUST be `cicd.server.pipeline.run.ended`.

Reports that a CI/CD pipeline run span has ended, and carries the complete span.

The event's trace context (TraceId, SpanId and TraceFlags) MUST be the
span's. Its timestamp MUST be the span's end time.

The event SHOULD only be emitted for sampled spans.

The event MUST carry all of the span's attributes, with unchanged keys and
values, and a consumer MUST be able to build the span from this event
alone. A producer that doesn't hold the SDK span (for example, a CI/CD
controller that restarted while the pipeline run was running) MUST still
provide a complete event.

The pipeline run's identity comes from the Resource (the `cicd.pipeline`
and `cicd.pipeline.run` entities), as it does for the span.

See [CI/CD span lifecycle events](/docs/cicd/cicd-events.md) for how
consumers combine the lifecycle events of a span.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`cicd.pipeline.result`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Required` | string | The result of a pipeline run. | `success`; `failure`; `timeout`; `skip` [(see more)](#cicd-pipeline-result-values) |
| [`cicd.span.name`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the span that a CI/CD span lifecycle event reports on. [1] | `RUN Build and Test` |
| [`cicd.span.start_time`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | int | The start time of the span that a CI/CD span lifecycle event reports on, in nanoseconds since the UNIX epoch. [2] | `1763000000000000000` |
| [`cicd.span.parent.id`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` If the span has a parent. | string | The span ID of the parent of the span that a CI/CD span lifecycle event reports on, as 16 lowercase hex characters. [3] | `b7ad6b7169203331` |
| [`cicd.span.trace_state`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` If the span's TraceState is not empty. | string | The W3C `tracestate` of the span that a CI/CD span lifecycle event reports on, in header format. [4] | `ot=th:8` |
| [`error.type`](/docs/registry/attributes/error.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` if the pipeline result is `failure` or `error` | string | Describes a class of error the operation ended with. [5] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` |
| [`otel.status_code`](/docs/registry/attributes/otel.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If the span status is not `UNSET`. | string | Name of the code, either "OK" or "ERROR". MUST NOT be set if the status code is UNSET. | `OK`; `ERROR` [(see more)](#otel-status-code-values) |
| [`otel.status_description`](/docs/registry/attributes/otel.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [6] | string | Description of the Status if it has a value, otherwise not set. | `resource not found` |
| [`cicd.pipeline.action.name`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Opt-In` | string | The kind of action a pipeline run is performing. | `BUILD`; `RUN`; `SYNC` [(see more)](#cicd-pipeline-action-name-values) |

**[1] `cicd.span.name`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[2] `cicd.span.start_time`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[3] `cicd.span.parent.id`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[4] `cicd.span.trace_state`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[5] `error.type`:** The `error.type` SHOULD be predictable, and SHOULD have low cardinality.

When `error.type` is set to a type (e.g., an exception type), its
canonical class name identifying the type within the artifact SHOULD be used.

If the recorded error type is a wrapper that is not meaningful for
failure classification, instrumentation MAY use the type of the inner
error instead. For example, in Go, errors created with `fmt.Errorf`
using `%w` MAY be unwrapped when the wrapper type does not help
classify the failure.

Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low.
Telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

If a specific domain defines its own set of error identifiers (such as HTTP or RPC status codes),
it's RECOMMENDED to:

- Use a domain-specific attribute
- Set `error.type` to capture all errors, regardless of whether they are defined within the domain-specific set or not.

**[6] `otel.status_description`:** If the span status code is `ERROR` and the status has a description.

---

<a id="cicd-pipeline-action-name-values"></a>

`cicd.pipeline.action.name` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `BUILD` | The pipeline run is executing a build. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `RUN` | The pipeline run is executing. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `SYNC` | The pipeline run is executing a sync. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |

---

<a id="cicd-pipeline-result-values"></a>

`cicd.pipeline.result` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `cancellation` | The pipeline run was cancelled, eg. by a user manually cancelling the pipeline run. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `error` | The pipeline run failed due to an error in the CI/CD system, eg. due to the worker being killed. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `failure` | The pipeline run did not finish successfully, eg. due to a compile error or a failing test. Such failures are usually detected by non-zero exit codes of the tools executed in the pipeline run. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `skip` | The pipeline run was skipped, eg. due to a precondition not being met. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `success` | The pipeline run finished successfully. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `timeout` | A timeout caused the pipeline run to be interrupted. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |

---

<a id="otel-status-code-values"></a>

`otel.status_code` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `ERROR` | The operation contains an error. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `OK` | The operation has been validated by an Application developer or Operator to have completed successfully. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Pipeline task run events

### Pipeline task run started

<!-- semconv event.cicd.pipeline.task.started -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

The event name MUST be `cicd.pipeline.task.started`.

Reports that a CI/CD pipeline task run span has started.

The event's trace context (TraceId, SpanId and TraceFlags) MUST be the
span's. Its timestamp MUST be the span's start time.

The event SHOULD only be emitted for sampled spans.

Besides the attributes listed below, the event MAY carry the span's other
attributes, with unchanged keys and values.

See [CI/CD span lifecycle events](/docs/cicd/cicd-events.md) for how
consumers combine the lifecycle events of a span.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`cicd.pipeline.task.name`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Required` | string | The human readable name of a task within a pipeline. Task here most closely aligns with a [computing process](https://wikipedia.org/wiki/Pipeline_(computing)) in a pipeline. Other terms for tasks include commands, steps, and procedures. | `Run GoLang Linter`; `Go Build`; `go-test`; `deploy_binary` |
| [`cicd.pipeline.task.run.id`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Required` | string | The unique identifier of a task run within a pipeline. [1] | `12097` |
| [`cicd.pipeline.task.run.url.full`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Required` | string | The [URL](https://wikipedia.org/wiki/URL) of the pipeline task run, providing the complete address in order to locate and identify the pipeline task run. | `https://github.com/open-telemetry/semantic-conventions/actions/runs/9753949763/job/26920038674?pr=1075` |
| [`cicd.span.name`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the span that a CI/CD span lifecycle event reports on. [2] | `RUN Build and Test` |
| [`cicd.span.parent.id`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` If the span has a parent. | string | The span ID of the parent of the span that a CI/CD span lifecycle event reports on, as 16 lowercase hex characters. [3] | `b7ad6b7169203331` |
| [`cicd.span.trace_state`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` If the span's TraceState is not empty. | string | The W3C `tracestate` of the span that a CI/CD span lifecycle event reports on, in header format. [4] | `ot=th:8` |

**[1] `cicd.pipeline.task.run.id`:** For a given pipeline run and task, the `cicd.pipeline.task.run.id` MUST be unique within that run. For the same task across different runs of the same pipeline, the `cicd.pipeline.task.run.id` MAY remain the same, enabling correlation of `cicd.pipeline.task.run.result` values across multiple pipeline runs.

**[2] `cicd.span.name`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[3] `cicd.span.parent.id`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[4] `cicd.span.trace_state`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Pipeline task run progress

<!-- semconv event.cicd.pipeline.task.progress -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

The event name MUST be `cicd.pipeline.task.progress`.

Reports that a CI/CD pipeline task run span is still running, and what changed since the previous lifecycle event for the same span.

The event's trace context (TraceId, SpanId and TraceFlags) MUST be the
span's. Its timestamp is the time the event was emitted.

The event SHOULD only be emitted for sampled spans.

The event carries only what changed since the previous lifecycle event for
the same span, including span attributes not listed below. A heartbeat
carries no attributes. A missing attribute means unchanged or unknown,
never removed.

See [CI/CD span lifecycle events](/docs/cicd/cicd-events.md) for how
consumers combine the lifecycle events of a span.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`cicd.span.name`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` [1] | string | The name of the span that a CI/CD span lifecycle event reports on. [2] | `RUN Build and Test` |

**[1] `cicd.span.name`:** If the span name changed since the previous lifecycle event for the same span.

**[2] `cicd.span.name`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Pipeline task run ended

<!-- semconv event.cicd.pipeline.task.ended -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

The event name MUST be `cicd.pipeline.task.ended`.

Reports that a CI/CD pipeline task run span has ended, and carries the complete span.

The event's trace context (TraceId, SpanId and TraceFlags) MUST be the
span's. Its timestamp MUST be the span's end time.

The event SHOULD only be emitted for sampled spans.

The event MUST carry all of the span's attributes, with unchanged keys and
values, and a consumer MUST be able to build the span from this event
alone. A producer that doesn't hold the SDK span (for example, a CI/CD
controller that restarted while the task run was running) MUST still
provide a complete event.

See [CI/CD span lifecycle events](/docs/cicd/cicd-events.md) for how
consumers combine the lifecycle events of a span.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`cicd.pipeline.task.name`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Required` | string | The human readable name of a task within a pipeline. Task here most closely aligns with a [computing process](https://wikipedia.org/wiki/Pipeline_(computing)) in a pipeline. Other terms for tasks include commands, steps, and procedures. | `Run GoLang Linter`; `Go Build`; `go-test`; `deploy_binary` |
| [`cicd.pipeline.task.run.id`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Required` | string | The unique identifier of a task run within a pipeline. [1] | `12097` |
| [`cicd.pipeline.task.run.result`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Required` | string | The result of a task run. | `success`; `failure`; `timeout`; `skip` [(see more)](#cicd-pipeline-task-run-result-values) |
| [`cicd.pipeline.task.run.url.full`](/docs/registry/attributes/cicd.md) | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) | `Required` | string | The [URL](https://wikipedia.org/wiki/URL) of the pipeline task run, providing the complete address in order to locate and identify the pipeline task run. | `https://github.com/open-telemetry/semantic-conventions/actions/runs/9753949763/job/26920038674?pr=1075` |
| [`cicd.span.name`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | string | The name of the span that a CI/CD span lifecycle event reports on. [2] | `RUN Build and Test` |
| [`cicd.span.start_time`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Required` | int | The start time of the span that a CI/CD span lifecycle event reports on, in nanoseconds since the UNIX epoch. [3] | `1763000000000000000` |
| [`cicd.span.parent.id`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` If the span has a parent. | string | The span ID of the parent of the span that a CI/CD span lifecycle event reports on, as 16 lowercase hex characters. [4] | `b7ad6b7169203331` |
| [`cicd.span.trace_state`](/docs/registry/attributes/cicd.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Conditionally Required` If the span's TraceState is not empty. | string | The W3C `tracestate` of the span that a CI/CD span lifecycle event reports on, in header format. [5] | `ot=th:8` |
| [`error.type`](/docs/registry/attributes/error.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` if the task result is `failure` or `error` | string | Describes a class of error the operation ended with. [6] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` |
| [`otel.status_code`](/docs/registry/attributes/otel.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` If the span status is not `UNSET`. | string | Name of the code, either "OK" or "ERROR". MUST NOT be set if the status code is UNSET. | `OK`; `ERROR` [(see more)](#otel-status-code-values) |
| [`otel.status_description`](/docs/registry/attributes/otel.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Conditionally Required` [7] | string | Description of the Status if it has a value, otherwise not set. | `resource not found` |

**[1] `cicd.pipeline.task.run.id`:** For a given pipeline run and task, the `cicd.pipeline.task.run.id` MUST be unique within that run. For the same task across different runs of the same pipeline, the `cicd.pipeline.task.run.id` MAY remain the same, enabling correlation of `cicd.pipeline.task.run.result` values across multiple pipeline runs.

**[2] `cicd.span.name`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[3] `cicd.span.start_time`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[4] `cicd.span.parent.id`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[5] `cicd.span.trace_state`:** This attribute is only meant for CI/CD span lifecycle events, not for spans.

**[6] `error.type`:** The `error.type` SHOULD be predictable, and SHOULD have low cardinality.

When `error.type` is set to a type (e.g., an exception type), its
canonical class name identifying the type within the artifact SHOULD be used.

If the recorded error type is a wrapper that is not meaningful for
failure classification, instrumentation MAY use the type of the inner
error instead. For example, in Go, errors created with `fmt.Errorf`
using `%w` MAY be unwrapped when the wrapper type does not help
classify the failure.

Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low.
Telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

If a specific domain defines its own set of error identifiers (such as HTTP or RPC status codes),
it's RECOMMENDED to:

- Use a domain-specific attribute
- Set `error.type` to capture all errors, regardless of whether they are defined within the domain-specific set or not.

**[7] `otel.status_description`:** If the span status code is `ERROR` and the status has a description.

---

<a id="cicd-pipeline-task-run-result-values"></a>

`cicd.pipeline.task.run.result` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `cancellation` | The task run was cancelled, eg. by a user manually cancelling the task run. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `error` | The task run failed due to an error in the CI/CD system, eg. due to the worker being killed. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `failure` | The task run did not finish successfully, eg. due to a compile error or a failing test. Such failures are usually detected by non-zero exit codes of the tools executed in the task run. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `skip` | The task run was skipped, eg. due to a precondition not being met. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `success` | The task run finished successfully. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |
| `timeout` | A timeout caused the task run to be interrupted. | ![Release Candidate](https://img.shields.io/badge/-rc-mediumorchid) |

---

<a id="otel-status-code-values"></a>

`otel.status_code` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value | Description | Stability |
| --- | --- | --- |
| `ERROR` | The operation contains an error. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `OK` | The operation has been validated by an Application developer or Operator to have completed successfully. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

## Open questions

These lifecycle events are a prototype for the
[span lifecycle events](https://github.com/open-telemetry/semantic-conventions/issues/2133)
discussion. Still open:

- How links are carried.
- Which Resource a rebuilt span gets when `ended` comes from a different process
  than `started`, for example after a restart.
- How long a consumer waits for `ended` before it treats a span as abandoned, and
  whether `started` should announce the heartbeat interval.
- Whether `ended` remains needed.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status/
