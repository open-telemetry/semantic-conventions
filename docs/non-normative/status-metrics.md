<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Status Metrics
aliases: [status-metrics]
--->

# State Metrics

**Status**: [Development][DocumentStatus]

<!-- toc -->

- [Definition](#definition)
- [Design](#design)
  - [Naming](#naming)
  - [Instrument](#instrument)
  - [Why not Resource Attributes?](#why-not-resource-attributes)

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

### Naming

This pattern represents a unique naming challenge. You could reasonably call the
metric and attribute both "status" or "state" as the two words are relatively
interchangeable in common parlance.

This problem necessitates choosing words to represent two things:

* The noun representing one of the set of possible values (the attribute name)
* The adjective describing which of the values is currently active (the metric
  name)

The general recommendation is to use the word "state" for the attribute and
"status" for the metric. This is derived from common turns of phrase for each
word, respectively:  
"What **state** is X in?"  
"What is the **current status** of X?"  

The english-language semantics of this are heavily debatable, thus it is
recommended for the sake of consistency that this pattern be adopted to avoid
inconsistent naming across similarly designed metrics.

The exception to this would be if a particular system has only one word that
would be used for both the noun and the adjective in question. An example would
be in Kubernetes, where the word "phase" equally represents both and there
is no acceptable alternative. In this case, using a metric name suffix is
recommended to avoid the naming clash, i.e. naming the attribute `k8s.phase` and
the metric `k8s.phase.current`.

### Instrument

The metric is instrumented as an `UpDownCounter` rather than a `Gauge`. This is
a deliberate choice, as it is a reasonable use case to count objects that are
in a particular state. Since the metric value is either `0` or `1` for a given
state attribute value, this means you can do a simple sum aggregation to count
instances of particular states.

### Why not Resource Attributes?

It is a common mistake to attach a "state" as a Resource Attribute. This is
not recommended for two reasons:

* Resource is intended to be immutable, thus adding an attribute like "state"
  that will almost certainly change during the resource's lifetime breaks the
  immutability and will create what are essentially new timeseries each time the
  attribute would update.
* Making the "state" an attribute on Resource would make it impossible to track
  changes in state over time.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
