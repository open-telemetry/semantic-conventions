<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
--->

# Semantic conventions for generative AI events

**Status**: [Development][DocumentStatus]

> [!Warning]
>
> Existing GenAI instrumentations that are using
> [v1.36.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.36.0/docs/gen-ai/README.md)
> (or prior):
>
> * SHOULD NOT change the version of the GenAI conventions that they emit by default.
>   Conventions include, but are not limited to, attributes, metric, span and event names,
>   span kind and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   as a comma-separated list of category-specific values. The list of values
>   includes:
>   * `gen_ai_latest_experimental` - emit the latest experimental version of
>     GenAI conventions (supported by the instrumentation) and do not emit the
>     old one (v1.36.0 or prior).
>   * The default behavior is to continue emitting whatever version of the GenAI
>     conventions the instrumentation was emitting (1.36.0 or prior).
>
> This transition plan will be updated to include stable version before the
> GenAI conventions are marked as stable.

GenAI instrumentations MAY capture user inputs sent to the model and responses received from it as [events](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#events).

> Note:
> Events are in-development and not yet available in some languages. Check [spec-compliance matrix](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/spec-compliance-matrix.md#logs) to see the implementation status in corresponding language.

Instrumentations MAY capture inputs and outputs if and only if application has enabled the collection of this data.
This is for three primary reasons:

1. Data privacy concerns. End users of GenAI applications may input sensitive information or personally identifiable information (PII) that they do not wish to be sent to a telemetry backend.
2. Data size concerns. Although there is no specified limit to sizes, there are practical limitations in programming languages and telemetry systems. Some GenAI systems allow for extremely large context windows that end users may take full advantage of.
3. Performance concerns. Sending large amounts of data to a telemetry backend may cause performance issues for the application.

Body fields that contain user input, model output, or other potentially sensitive and verbose data
SHOULD NOT be captured by default.

Semantic conventions for individual systems which extend content events SHOULD document all additional body fields and specify whether they
should be captured by default or need application to opt into capturing them.

Telemetry consumers SHOULD expect to receive unknown body fields.

Instrumentations SHOULD NOT capture undocumented body fields and MUST follow the documented defaults for known fields.
Instrumentations MAY offer configuration options allowing to disable events or allowing to capture all fields.

## Events

Is now described in the namespace registry.

To see usage of the events defined in the registry refer to the [Gen-AI implementations](gen-ai-implementations.md) documentation.

## Custom events

System-specific events that are not covered in this document SHOULD be documented in corresponding Semantic Conventions extensions and
SHOULD follow `{gen_ai.provider.name}.*` naming pattern.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
