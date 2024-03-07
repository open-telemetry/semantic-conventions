<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Sampling
--->

# Sampling

## Sampling attributes

The following attributes are recognized for telemetry in general.

<!-- semconv registry.sampling(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `sampling.priority` | int | Allows users and instrumentations to prioritize collection of reported telemetry items. [1] | `10`; `1`; `0` |
| `sampling.randomness` | string | The source of randomness for making probability sampling decisions, when it is not otherwise recorded. [2] | `ce929d0e0e4736` |
| `sampling.threshold` | string | Sampling probability as specified by OpenTelemetry. [3] | `c`; `ff8` |

**[1]:** If greater than 0, a hint to the Tracer to do its best to capture the trace. If 0, a hint to the Tracer to not-capture the trace. If absent, the Tracer should use its default sampling mechanism.

**[2]:** This attribute is an optional way to express trace randomness, especially for cases where the TraceID is missing or known to be not random.  Sampler components set and consume this value.  The value is a hex-coded string containing 14 hex digits (56 bits) of randomness.  Setting this attribute indicates the source of randomness that was used (and may be used again) for probability sampling.  This field is taken to have the same meaning as the OpenTelemetry tracestate "R-value" for probability sampling, which is an alternative to deriving trace randomness from the TraceID specified in OTEP 235.

**[3]:** This attribute is set to convey sampling probability. Sampler components set and consume this value, which is taken to have the same meaning as the OpenTelemetry tracestate "T-value" for probability sampling.  This attribute contains a hexadecimal-coded value containing 1 to 14 hex digits of precision, defining the threshold used to reject, depending on the random variable.  This value can be converted into sampling probability as specified in OTEP 235.

The following attributes can be important for making sampling decisions and SHOULD be provided **at span creation time** (if provided at all):

* `sampling.priority`
<!-- endsemconv -->
