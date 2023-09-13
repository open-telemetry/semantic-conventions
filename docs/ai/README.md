<!--- Hugo front matter used to generate the website version of this page:
linkTitle: AI
path_base_for_github_subdir:
  from: content/en/docs/specs/semconv/ai/_index.md
  to: database/README.md
--->

# Semantic Conventions for AI systems

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for the following kind of AI systems:

* LLMs
* Vector Embeddings (todo)
* Vector Databases (todo)

Semantic conventions for LLM operations are defined for the following signals:

* [LLM Spans](llm-spans.md): Semantic Conventions for LLM requests.
* [LLM chains](llm-chains.md): Semantic Conventions for LLM chains.

Technology specific semantic conventions are defined for the following databases:

* [OpenAI](openai.md): Semantic Conventions for *OpenAI*.
* [Anthropic](anthropic.md): Semantic Conventions for *Anthropic*.
* [Cohere](cohere.md): Semantic Conventions for *Cohere*.
* [Replicate](replicate.md): Semantic Conventions for *Replicate*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
