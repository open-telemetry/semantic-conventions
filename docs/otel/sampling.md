<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Sampling
--->

# Semantic Conventions for Sampling

**Status**: [Experimental][DocumentStatus]

<!-- toc -->
<!-- tocstop -->

These attributes may be modified by components in a collection
pipeline to convey the amount of sampling that has been carried out
for a particular item of telemetry.

## Span attributes

The following attributes are recognized for Spans.

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
