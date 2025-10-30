<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Status Metrics
--->

# State Metrics

**Status**: [Development][DocumentStatus]

<!-- toc -->

- [Definition](#definition)
- [Design](#design)
  - [Instrument](#instrument)
  - [Should it be an Entity Attribute?](#should-it-be-an-entity-attribute)
  - [Naming](#naming)

<!-- tocstop -->

## Definition

For the purposes of this document, a "status metric" is a metric used to
represent something being in a particular state at a given time from a closed
set of distinct possible state values.

## Design

To represent a metric of this nature, the design will look like the following:

```yaml
id: metric.example.status
type: metric
metric_name: example.status
stability: development
brief: "The current state."
note: |
  A timeseries is produced for every possible value of `example.state`. The
  value of this metric is 1 for a state if it is currently in said state, and
  is 0 for all other states.
instrument: updowncounter
unit: "1"
attributes:
  - ref: example.state
```

### Instrument

The metric is
[instrumented as an `UpDownCounter`](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/metrics.md#consistent-updowncounter-timeseries)
rather than a `Gauge`. This is a deliberate choice, as it is a reasonable use
case to count objects that are in a particular state. Since the metric value is
either `0` or `1` for a given state attribute value, this means you can do a
simple sum aggregation to count instances of particular states.

### Should it be an Entity Attribute?

It is possible to make the status a descriptive attribute on an entity (**not**
an identifying attribute). Tracking entity state changes is a known use case
for entities. However, it is still recommended to also define a status metric
as it helps metric-centric solutions understand how to interact with entities.

### Naming

If there is already well-known naming conventions within the instrumentation
context, i.e. `k8s` having words like `phase` or `status`, those words should
always be chosen.

If there are not any naming options immediately available, you may use this
recommended naming scheme.  
This naming scheme necessitates choosing words to represent two things:

* The noun representing one of the set of possible values (the attribute name)
* The adjective describing which of the values is currently active (the metric
  name)

The general recommendation is to use the word "state" for the attribute and
"status" for the metric. This is derived from common turns of phrase for each
word, respectively:

"What **state** is X in?"
"What is the **current status** of X?"

The english-language semantics of this are heavily debatable, thus for the sake
of consistency it is recommended to adopt this naming scheme if there is no
obvious verbiage available.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
