<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic Conventions for OpenAI Spans

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for OpenAI client Spans.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Chat completions](#chat-completions)
- [Embeddings](#embeddings)
- [Image generations](#image-generations)

<!-- tocstop -->

## Chat completions

Span name should match TODO

The common attributes listed in this section apply to OpenAI [create chat completions calls](https://platform.openai.com/docs/api-reference/chat/create).

<!-- semconv trace.openai.chat_completions(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Recommended |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Recommended |
| `openai.azure.chat_completions.response.filter_results` | string[] | Array of results that were filtered out. | `[[1]: self_harm, [2]: violence, hate]` | Recommended |
| `openai.chat_completions.request.frequency_penalty` | double | Number between -2.0 and 2.0.Positive values penalize new tokens based on their existing frequency. | `0.0` | Recommended |
| `openai.chat_completions.request.max_tokens` | int | The maximum number of tokens to generate in the completion. | `1024` | Recommended |
| `openai.chat_completions.request.presence_penalty` | double | Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear. | `0.0` | Recommended |
| `openai.chat_completions.request.temperature` | double | Sampling temperature, between 0 and 2 | `0.7` | Recommended |
| `openai.chat_completions.request.top_p` | double | The nucleus sampling factor, between 0 and 1 | `0.1` | Recommended |
| `openai.chat_completions.response.completion_tokens` | int | Number of tokens in the generated completion. | `12` | Recommended |
| `openai.chat_completions.response.created_at` | int | The Unix timestamp (in seconds) of when the chat completion was created. | `1677652288` | Recommended |
| `openai.chat_completions.response.finish_reasons` | string[] | Finish reasons | `[stop, length, content_filter]` | Recommended |
| `openai.chat_completions.response.id` | string | A unique identifier for the chat completion. | `cmpl-7ykn0gf4r76hfDam5e7l0s05ZWSmA` | Recommended |
| `openai.chat_completions.response.prompt_tokens` | int | Number of tokens in the prompt. | `9` | Recommended |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Recommended |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

If a specific domain defines its own set of error codes (such as HTTP or gRPC status codes),
it's RECOMMENDED to use a domain-specific attribute and also set `error.type` to capture
all errors, regardless of whether they are defined within the domain-specific set or not.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

## Embeddings

Span name should match TODO

The common attributes listed in this section apply to OpenAI [create embedding calls](https://platform.openai.com/docs/api-reference/embeddings).

<!-- semconv trace.openai.embeddings(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Recommended |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Recommended |
| `openai.embeddings.request.input_size` | int | Size of input text to embed. | `1024` | Recommended |
| `openai.embeddings.response.index` | int | The index of the embedding in the list of embeddings. | `0` | Recommended |
| `openai.embeddings.response.prompt_tokens` | int | Number of tokens in the prompt. | `9` | Recommended |
| `openai.embeddings.response.vector_size` | int | The size of embedding vector | `1536` | Recommended |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Recommended |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

If a specific domain defines its own set of error codes (such as HTTP or gRPC status codes),
it's RECOMMENDED to use a domain-specific attribute and also set `error.type` to capture
all errors, regardless of whether they are defined within the domain-specific set or not.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

## Image generations

Span name should match TODO

The common attributes listed in this section apply to OpenAI [create image calls](https://platform.openai.com/docs/api-reference/images/create).

<!-- semconv trace.openai.image_generations(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `openai.model` | string | Model name | `text-davinci-003` | Recommended |
| `error.type` | string | Describes a class of error the operation ended with. [1] | `timeout`; `java.net.UnknownHostException`; `server_certificate_invalid`; `500` | Recommended |
| `openai.image_generations.request.image_count` | int | The number of images to generate. | `2` | Recommended |
| `openai.image_generations.request.image_format` | string | The format in which the generated images should be returned. | `b64_json` | Recommended |
| `openai.image_generations.request.image_size` | string | The size of the generated images. | `256x256` | Recommended |
| [`server.address`](../general/attributes.md) | string | Server address - domain name if available without reverse DNS lookup, otherwise IP address or Unix domain socket name. [2] | `example.com` | Recommended |

**[1]:** The `error.type` SHOULD be predictable and SHOULD have low cardinality.
Instrumentations SHOULD document the list of errors they report.

The cardinality of `error.type` within one instrumentation library SHOULD be low, but
telemetry consumers that aggregate data from multiple instrumentation libraries and applications
should be prepared for `error.type` to have high cardinality at query time, when no
additional filters are applied.

If the operation has completed successfully, instrumentations SHOULD NOT set `error.type`.

If a specific domain defines its own set of error codes (such as HTTP or gRPC status codes),
it's RECOMMENDED to use a domain-specific attribute and also set `error.type` to capture
all errors, regardless of whether they are defined within the domain-specific set or not.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent
the server address behind any intermediaries (e.g. proxies) if it's available.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
