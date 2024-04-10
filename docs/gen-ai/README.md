<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Generative AI
path_base_for_github_subdir:
  from: tmp/semconv/docs/gen-ai/_index.md
  to: gen-ai/README.md
--->

# Semantic Conventions for Generative AI systems

**Status**: [Experimental][DocumentStatus]

**Warning**:
The semantic conventions for GenAI and LLM are currently in development.
We encourage instrumentation libraries and telemetry consumers developers to
use the conventions in limited non-critical workloads and share the feedback

Semantic conventions for Generative AI operations are defined for the following signals:

* [Events](gen-ai-events.md): Semantic Conventions for Generative AI inputs and outputs - *events*.
* [Metrics](gen-ai-metrics.md): Semantic Conventions for Generative AI operations - *metrics*.
* [Spans](gen-ai-spans.md): Semantic Conventions for Generative AI requests - *spans*.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
