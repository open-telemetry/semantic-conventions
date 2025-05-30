<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Generative AI
--->

# Semantic conventions for generative AI systems

**Status**: [Development][DocumentStatus]

> [!Warning]
>
> Existing GenAI instrumentations that are using
> [v1.34.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.34.0/docs/gen-ai/README.md)
> (or prior):
>
> * SHOULD NOT change the version of the GenAI conventions that they emit by default.
>   Conventions include, but are not limited to, attributes, metric and span names,
>   span kind and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_UPDATE_OPT_IN`
>   in the existing major version as a comma-separated list of category-specific values
>   (e.g., http, databases, messaging, gen-ai). The list of values includes:
>   * `gen-ai` - emit the newer GenAI conventions and stop emitting the old
>     GenAI conventions (v1.34.0 or prior).
>   * `gen-ai/dup` - emit both the old and the new GenAI conventions, allowing
>     for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the GenAI conventions the instrumentation
>     was emitting prior to 1.34.0.
>   * Note: `gen-ai/dup` has higher precedence than `gen-ai` in case both values are present
> * SHOULD emit the new values for span name, span kind and similar "single"
>   valued concepts when `gen-ai/dup` is present in the list.

Semantic conventions for Generative AI operations are defined for the following signals:

* [Events](gen-ai-events.md): Semantic Conventions for Generative AI inputs and outputs - *events*.
* [Metrics](gen-ai-metrics.md): Semantic Conventions for Generative AI operations - *metrics*.
* [Model spans](gen-ai-spans.md): Semantic Conventions for Generative AI model operations - *spans*.
* [Agent spans](gen-ai-agent-spans.md): Semantic Conventions for Generative AI agent operations - *spans*.

Technology specific semantic conventions are defined for the following GenAI system:

* [Azure AI Inference](./azure-ai-inference.md): Semantic Conventions for Azure AI Inference.
* [OpenAI](./openai.md): Semantic Conventions for OpenAI.
* [AWS Bedrock](./aws-bedrock.md): Semantic Conventions for AWS Bedrock.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
