<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Sampling
--->

# Semantic Conventions for Sampling

**Status**: [Experimental][DocumentStatus]

<!-- toc -->

- [Probability sampling](#probability-sampling)
  - [Overriding sampling decisions](#overriding-sampling-decisions)
  - [Overriding sampling randomness](#overriding-sampling-randomness)
  - [Sampling threshold](#sampling-threshold)
  - [Sampling randomness](#sampling-randomness)
  - [No definition for Scope and Resource attributes](#no-definition-for-scope-and-resource-attributes)
- [Span sampling attributes](#span-sampling-attributes)
- [Logs sampling attributes](#logs-sampling-attributes)
- [Examples](#examples)
  - [Head sampling](#head-sampling)
  - [Tail sampling](#tail-sampling)

<!-- tocstop -->

These attributes reflect the effect of sampling in a telemetry
collection pipeline.  These attributes describe how items of telemetry
were collected, making it possible for Span-to-Metrics pipelines
and Logs-to-Metrics pipelines to accurately count Spans and Log
Records of telemetry, before sampling, in a probabilistic sense.

These attributes MAY be modified by components in a collection
pipeline to convey successive sampling that has been carried out for a
particular item of telemetry, using the conventions for consistent
sampling described here.  In that sense, telemetry consumers
should see these attributes as telemetry metadata.

## Probability sampling

The OpenTelemetry sampling decision is defined in terms of a Threshold
value and a Randomness value, each containing 56 bits of information.

A constant known as _maximum adjusted count_ (`MaxAdjustedCount`),
with value `0x100000000000000`, (which can also be expressed
`0x1p+56`, `math.Pow(2, 56)`, or `math.Ldexp(1, 56)`), defines the
exclusive upper limit of these values.

Logically, both Threshold (`T`) and Randomness (`R`) are represented
as unsigned integers in the range `0` through `0xffffffffffffff` or
`MaxAdjustedCount - 1`.  Items of telemetry are selected (i.e.,
"sampled") when their Threshold value is less than or equal to their
Randomness value, or `T <= R`.

Sampling probability is defined by the following expression:

```
Probability = (MaxAdjustedCount - Threshold) / MaxAdjustedCount
```

In a Span-to-Metrics or Logs-to-Metrics pipeline, each item of
telemetry is representative of an _adjusted count_ number of items in
the original population.  Adjusted count is the inverse of sampling
probability, and `MaxAdjustedCount` (defined above) is the inverse of
the smallest supported sampling probability (which can also be
represented as `0x1p-56`, `math.Pow(2, -56)`, or `math.Ldexp(1,
-56)`).

For the tracing signal, Threshold and Randomness propagate via W3C
Trace Context `tracestate`.  When they appear in the `tracestate`, the
Threshold and Randomness properties are called "T-value" and
"R-value"; they are represented in the OpenTelemetry section of the
`tracestate` (having vendor tag `ot`), using properties named `th` and
`rv`, respectively.

For the logs signal, which generally does not record the W3C Trace
Context `tracestate`, sampling attributes are meant to be expressed
using log record attributes with the same definition as T-value and
R-value.

For more information on how to perform and interpret probability
sampling based on these properties, [consult OTEP 235][OTEP235].

### Overriding sampling decisions

Samplers and sampler delgates are encouraged to force a sampling
decision by configuring a 100% sampling threshold, rather than bypass
sampling logic.  Forced sampling decisions will have T-value "0",
indicating 100% sampling.

To force sampling decisions in the other direction, a threshold
corresponding with zero probability can be used.  However, since the
"do not sample" threshold indicates a record should not be exported,
there is no specified way to encode "zero probability".  Ultimately,
the decision not to sample is not a probabilistic decision.

### Overriding sampling randomness

Sampling system designers are able to override sampling randomness,
which may be done for several reasons, including situations where
there is no TraceID defined.

When a tracing system purposely uses TraceIDs that do not follow the
W3C Trace Context Level 2 specification for TraceID randomness, and
they wish to use OpenTelemetry sampling components, they can insert
explicit randomness to prevent erroneously taking randomness from the
TraceID.

Another use for overriding sampling randomness is to configure a
different unit of sampling consistency.  For example, multiple traces
can be given the same randomness value to ensure that either all or
none of them are sampled consistently.

In the tracing signal, sampling randomness can be overridden by
setting an R-value in the tracestate, however the R-value should not
be modified, once set, in a Context.  In the logging signal, sampling
randomness can be overridden by setting the `sampling.randomness`
attribute.

### Sampling threshold

When determining the Threshold value from an item of telemetry,
sampler implementations SHOULD evaluate the following in order:

- use the OpenTelemetry T-value field (`th`) in `tracestate` from a live SpanContext (in context)
- use the OpenTelemetry T-value field (`th`) in `tracestate` from a Span tracestate (spans data)
- use the `sampling.threshold` attribute value, if present in the record attributes (logs data)

In both cases, the Threshold value is represented by one to 14
hexadecimal digits, allowing the use of variable-precision sampling
probability.  When fewer than 14 digits are input, the string is
padded with trailing zeros to make the correct number of bits (56).

The zero Threshold value (encoded by a single `0`) corresponds with
100% sampling.

When Threshold is not provided, no information about probability
sampling is available.

### Sampling randomness

When determining the Randomness value from an item of telemetry,
sampler implementations SHOULD:

- use the OpenTelemetry R-value field (`rv`) in `tracestate` from a live SpanContext (in context)
- use the OpenTelemetry R-value field (`rv`) in `tracestate` from a Span tracestate (spans data)
- use the `sampling.randomness` attribute value if it is present (logs data), or
- use the least significant 56 bits of the W3C Trace Context TraceID, as described in the W3C Trace Context Level 2 specification (in context, spans data, and logs data)

In the first two cases, where Randomness is explicitly encoded, the
value is represented by exactly 14 hexadecimal digits.

Sampler implementations SHOULD NOT require trace flags to have the Trace
Context Level 2 Random flag set, in case the Trace ID is used as the
source of randomness.  Because the Random flag is not widely available
at this time, and because the W3C Trace Context Level 2 specification
was designed for widespread compliance with existing systems, it is
recommended to assume there are 56 bits of randomness.

In case a system knowingly uses TraceIDs that do not conform to the
W3C Trace Context Level 2 specification and they wish to perform
sampling with OpenTelemetry components, they SHOULD synthesize a
random R-value and store it in the `tracestate` (Spans) or the
`sampling.randomness` (Log Records) attribute value.

### No definition for Scope and Resource attributes

We recognize that in some configurations, sampling probability and
even sampling randomness may be set to a constant value.

The `sampling.threshold` and `sampling.randomness` attributes are not
defined for use as Scope or Resource attributes in the present
specification, because there is an existing need to encode per-item
sampling probability, stemming from prioritization schemes.

## Span sampling attributes

No attributes are recognized for Spans.  The `tracestate` fields should
be used to convey sampling for Span data.

## Logs sampling attributes

The following attributes are recognized for Logs.

<!-- semconv logs.sampling(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`sampling.randomness`](../attributes-registry/sampling.md) | string | The source of randomness for making probability sampling decisions, when it is not otherwise recorded. [1] | `ce929d0e0e4736` | Conditionally Required: [2] |
| [`sampling.threshold`](../attributes-registry/sampling.md) | string | Sampling probability as specified by OpenTelemetry. [3] | `c`; `ff8` | Conditionally Required: [4] |

**[1]:** This attribute is an optional way to express trace randomness, especially for cases where the TraceID is missing or known to be not random.  Sampler components set and consume this value.  The value is a hex-coded string containing 14 hex digits (56 bits) of randomness.  Setting this attribute indicates the source of randomness that was used (and may be used again) for probability sampling.  This field is taken to have the same meaning as the OpenTelemetry tracestate "R-value" for probability sampling, which is an alternative to deriving trace randomness from the TraceID. For details, see OTEP 235.

**[2]:** When a `sampling.threshold` is provided, the corresponding 56-bit randomness value is also recorded.

**[3]:** This attribute is set to convey sampling probability. Sampler components set and consume this value, which is taken to have the same meaning as the OpenTelemetry tracestate "T-value" for probability sampling.  This attribute contains a hexadecimal-coded value containing 1 to 14 hex digits of precision, defining the threshold used to reject, depending on the random variable.  This value can be converted into sampling probability.  For details, see OTEP 235.

**[4]:** When a 56-bit consistent probability sampler is used.
<!-- endsemconv -->

## Examples

### Head sampling

For example, a span that was selected by a 25% probability sampler
using randomness from the TraceID, has selected field values like:

```
  trace_id: 4bf92f3577b34da6a3ce929d0e0e4736
  tracestate: ot=th:c
```

We can verify that the sampling decision was made correctly as follows.

The trailing 14 hex-digits of randomness are extracted from the
TraceID, forming the Randomness value `0xce929d0e0e4736`.  The T-value
`c` is extended with 13 zeros, forming the Threshold value
`0xc0000000000000`.  Since `T <= R` is true, the span was correctly sampled.

For a log record, which does not include the `tracestate` field, the
same can be expressed as:

```
  trace_id: 4bf92f3577b34da6a3ce929d0e0e4736
  attributes:
    sampling.threshold: c
```

A log record that does not define the trace_id and was sampled by a
probability sampler requires explicit randomness.  For example:

```
  attributes:
    sampling.threshold: c
    sampling.randomness: ce929d0e0e4736
```

### Tail sampling

A span is received with no sampling information (i.e., no `tracestate`
field) is selected by a tail sampler at 10% probability.  A
`tracestate` entry is created.

```
  trace_id: 4bf92f3577b34da6a3fe929d0e0e4736
  tracestate: ot=th:e66
```

A log record containing a TraceID is received with no sampling
attributes and is selected by a tail sampler at 10% probability.  A
sampling threshold is inserted:

```
  trace_id: 4bf92f3577b34da6a3fe929d0e0e4736
  attributes:
    sampling.threshold: e66
```

In both cases, the Threshold value e66 corresponds with rejecting a
fraction equal to `0xe66 / 0x1000` or 0.10009765625.  Had 5 digits of
precision been used (`e6666`), the exact sampling probability would be
0.10000038147.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[OTEP235]: https://github.com/open-telemetry/oteps/blob/main/text/trace/0235-sampling-threshold-in-trace-state.md
