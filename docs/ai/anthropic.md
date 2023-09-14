<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Anthropic
--->

# Semantic Conventions for Anthropic

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Anthropic](https://docs.anthropic.com/claude/docs) extend the [LLM Semantic Conventions](llm-spans.md)
that describe common LLM request attributes in addition to the Semantic Conventions
described on this page.

## Anthropic LLM request attributes

These are additional attributes when instrumenting Anthropic LLM requests.

<!-- semconv llm.anthropic(tag=llm-request-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.anthropic.top_k` | int | If present, represents the value used to only sample from the top K options for each subsequent token. | `5` | Required |
| `llm.anthropic.metadata.user_id` | string | If present, the `user_id` used in an Anthropic request. | `bob` | Required |

## Anthropic LLM response attributes

These are additional attributes when instrumenting Anthropic LLM responses.

### Chat completion attributes

These are the attributes for a full chat completion (no streaming).

<!-- semconv llm.anthropic(tag=llm-response-tech-specific) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.anthropic.stop_reason` | string | The reason why the model stopped sampling. | `stop_sequence` | Required |
| `llm.ahtropic.model` | string | The name of the model used for the completion. | `claude-instant-1` | Recommended |
