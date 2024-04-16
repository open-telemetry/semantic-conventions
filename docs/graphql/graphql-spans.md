<!--- Hugo front matter used to generate the website version of this page:
linkTitle: GraphQL Server
--->

# Semantic Conventions for GraphQL Server

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions to apply when instrumenting the GraphQL implementation. They map GraphQL
operations to attributes on a Span.

The **span name** MUST be of the format `<graphql.operation.type> <graphql.operation.name>` provided that
`graphql.operation.type` and `graphql.operation.name` are available. If `graphql.operation.name` is not available, the
span SHOULD be named `<graphql.operation.type>`. When `<graphql.operation.type>` is not available, `GraphQL Operation`
MAY be used as span name.

<!-- semconv graphql(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`graphql.document`](../attributes-registry/graphql.md) | string | The GraphQL document being executed. [1] | `query findBookById { bookById(id: ?) { name } }` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`graphql.operation.name`](../attributes-registry/graphql.md) | string | The name of the operation being executed. | `findBookById` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`graphql.operation.type`](../attributes-registry/graphql.md) | string | The type of the operation being executed. | `query`; `mutation`; `subscription` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The value may be sanitized to exclude sensitive information.

`graphql.operation.type` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `query` | GraphQL query | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mutation` | GraphQL mutation | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `subscription` | GraphQL subscription | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
