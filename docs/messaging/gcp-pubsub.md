<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Google Cloud Pub/Sub
--->

# Semantic Conventions for Google Cloud Pub/Sub

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [Google Cloud Pub/Sub](https://cloud.google.com/pubsub) extend and override the [Messaging Semantic Conventions](README.md) that describe common messaging operations attributes in addition to the Semantic Conventions described on this page.

`messaging.system` MUST be set to `"gcp_pubsub"`.

## Span attributes

For Google Cloud Pub/Sub, the following additional attributes are defined:
<!-- semconv messaging.gcp_pubsub(full,tag=tech-specific-gcp-pubsub) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`messaging.gcp_pubsub.message.link`](../attributes-registry/messaging.md) | int | An identifier for the link. This is *not* the message id. The number will be in between 0 and the max batch size. | `1` | Recommended |
| [`messaging.gcp_pubsub.message.ordering_key`](../attributes-registry/messaging.md) | string | The ordering key for a given message. If the attribute is not present, the message does not have an ordering key. | `ordering_key` | Conditionally Required: If the message type has an ordering key set. |
<!-- endsemconv -->

## Examples

### Asynchronous Batch Publish Example

Given is a process P that asynchronously publishes 2 messages in a batch to a topic T on Pub/Sub.

```mermaid
flowchart LR;
  subgraph PRODUCER
  direction LR
  CA[Span Create A]
  CB[Span Create B]
  P[Span Publish]
  end
  CA-. link .-P;
  CB-. link .-P;

  classDef normal fill:green
  class PA,PB,D1 normal
  linkStyle 0,1 color:green,stroke:green
```

| Field or Attribute | Span Create A | Span Create B | Span Publish A B |
|-|-|-|-|
| Span name | `T create` | `T create` | `publish` |
| Parent |  |  |  |
| Links |  |  | Span Create A, Span Create B |
| Link attributes [1]|  |  | Span Create A: `messaging.gcp_pubsub.message.link`: `1`  |
|                 |  |  | Span Create B: `messaging.gcp_pubsub.message.link`: `2`  |
| SpanKind | `PRODUCER` | `PRODUCER` | `PRODUCER` |
| Status | `Ok` | `Ok` | `Ok` |
| `messaging.batch.message_count` |  |  | 2 |
| `messaging.destination.name` | `"T"` | `"T"` |  |
| `messaging.destination.template` | `"topic"` | `"topic"` |  |
| `messaging.operation` | `"create"` | `"create"` | `"publish"` |
| `messaging.message.id` | `"a1"` | `"a2"` | |
| `messaging.message.total_size_bytes` | `1` | `1` | |
| `messaging.system` | `"gcp_pubsub"` | `"gcp_pubsub"` | |

**[1]:** A message receives its id after the publish span completes. The message link attribute represenets

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
