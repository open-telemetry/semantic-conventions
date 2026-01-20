<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Generative AI
--->

# Semantic conventions for generative AI systems

**Status**: [Development][DocumentStatus]

> [!IMPORTANT]
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

Semantic conventions for Generative AI operations are defined for the following signals:

* [Events](gen-ai-events.md): Semantic Conventions for Generative AI inputs and outputs - *events*.
* [Metrics](gen-ai-metrics.md): Semantic Conventions for Generative AI operations - *metrics*.
* [Model spans](gen-ai-spans.md): Semantic Conventions for Generative AI model operations - *spans*.
* [Agent spans](gen-ai-agent-spans.md): Semantic Conventions for Generative AI agent operations - *spans*.

Technology specific semantic conventions are defined for the following GenAI system:

* [Azure AI Inference](./azure-ai-inference.md): Semantic Conventions for Azure AI Inference.
* [OpenAI](./openai.md): Semantic Conventions for OpenAI.
* [AWS Bedrock](./aws-bedrock.md): Semantic Conventions for AWS Bedrock.

See also:

* [Model Context Protocol](./mcp.md): Semantic Conventions for [MCP](https://modelcontextprotocol.io)

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
