<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Sampling
--->

# Semantic Conventions for Sampling

**Status**: [Experimental][DocumentStatus]

<!-- toc -->
<!-- tocstop -->

These attributes reflect the effect of sampling in a telemetry
collection pipeline.  These attributes describe how items of telemetry
was collected, making it possible to define Span-to-Metrics pipelines
and Logs-to-Metrics pipelines, which accurately count items of
telemetry, despite sampling.

These attributes MAY be modified by components in a collection pipeline
to convey the amount of sampling that has been carried out for a
particular item of telemetry.

## Probability sampling

For more information on how to perform and interpret probability
sampling based on these attributes, [consult OTEP
235](https://github.com/open-telemetry/oteps/blob/main/text/trace/0235-sampling-threshold-in-trace-state.md).

### Sampling threshold

The OpenTelemetry sampling decision is defined in terms in terms of a
threshold and a source of randomness.  The threshold expresses how
many traces out of `1<<56` (i.e., `math.Pow(2, 56)`) are rejected by
the sampler, and forms the basis of a rejection test defined by `T <=
R`.  An item is sampled when the item's sampling threshold is less or
equal to its randomness.

When determining sampling randomness from a span, implementations
SHOULD:

- use the `tracestate` OpenTelemetry T-value field (`rh`) if it is present, or
- use the `sampling.threshold` attribute value if it is present.

Otherwise, no information is available about what sampling was
performed.

### Sampling randomness

When determining sampling randomness from a span, implementations
SHOULD:

- use the `tracestate` OpenTelemetry R-value field (`rv`) if it is present, or
- use the `sampling.randomness` attribute value if it is present, or
- use the least significant 56 bits of the W3C Trace Context TraceID, as described in the W3C Trace Context Level 2 specification.

Callers SHOULD NOT require trace flags to have the Trace Context Level
2 Random flag set, in case the Trace ID is used as the source of
randomness, because it is not reliable information at this time.
Additionally, the W3C Trace Context Level 2 specification was based on
the widespread use of at least 56 bits of randomness.

In case the user knowingly creates TraceIDs that do not conform to the
W3C Trace Context Level 2 specification and they wish to perform
sampling, they SHOULD synthesize a random R-value and store it in the
`tracestate` (Spans) or the `sampling.randomness` (Log Records)
attribute value.

## Span attributes

The following attributes are recognized for Spans.  Since probability
sampling is tightly coordinated through Context propagation and
reflected in the W3C Trace Context `tracestate`, which is included in
the Span data model, it is not common to express sampling randomness
and threshold using attributes.

<!-- semconv sampling.common(full,tag=otel-span-attributes) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `sampling.priority` | int | Enables prioritizing and de-prioritizing collection of telemetry. [1] | `1`; `0` | Recommended |

**[1]:** This attribute is useful to express the user's desire to collect telemetry, despite the sampling configuration in place.  Non-zero values MAY prioritize the item for collection independent of probability sampling.  Zero values have the reverse effect and MAY cause telemetry not to be collected.  This convention derives from a conventional tag with the same name in the OpenTracing specification.
<!-- endsemconv -->

## Log Record attributes

The following attributes are recognized for Log Records.

<!-- semconv sampling.common(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `sampling.priority` | int | Enables prioritizing and de-prioritizing collection of telemetry. [1] | `1`; `0` | Recommended |
| `sampling.randomness` | string | The source of randomness for making probability sampling decisions, when it is not otherwise recorded. [2] | `ce929d0e0e4736` | Recommended |
| `sampling.threshold` | string | Sampling probability as specified by OpenTelemetry. [3] | `c`; `ff8` | Recommended |

**[1]:** This attribute is useful to express the user's desire to collect telemetry, despite the sampling configuration in place.  Non-zero values MAY prioritize the item for collection independent of probability sampling.  Zero values have the reverse effect and MAY cause telemetry not to be collected.  This convention derives from a conventional tag with the same name in the OpenTracing specification.

**[2]:** This attribute is an optional way to express trace randomness, especially for cases where the TraceID is missing or known to be not random.  This value is a hex-coded string containing 14 hex digits (56 bits) of randomness.  Setting this attribute indicates the source of randomness that was used (and may be used again) for probability sampling.  This field is taken to have the same meaning as the OpenTelemetry tracestate "R-value" for probability sampling, which is an alternative to deriving trace randomness from the TraceID [specified in OTEP 235](https://github.com/open-telemetry/oteps/blob/main/text/trace/0235-sampling-threshold-in-trace-state.md).

**[3]:** This attribute is set to convey sampling probability from samplers to consumers of spans and log records, taken to have the same meaning as the OpenTelemetry tracestate "T-value" for probability sampling.  This attribute contains a hexadecimal-coded value containing 1 to 14 hex digits of precision, defining the threshold used to reject, depending on the random variable.  This value can be converted into sampling probability as [specified in OTEP 235](https://github.com/open-telemetry/oteps/blob/main/text/trace/0235-sampling-threshold-in-trace-state.md).
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
