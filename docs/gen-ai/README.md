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

This document defines semantic conventions for the following kind of Generative AI systems:

* LLMs

Semantic conventions for Generative AI operations are defined for the following signals:

* [Metrics](gen-ai-metrics.md): Semantic Conventions for Generative AI operations - *metrics*.

Semantic conventions for LLM operations are defined for the following signals:

* [LLM Spans](llm-spans.md): Semantic Conventions for LLM requests - *spans*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
