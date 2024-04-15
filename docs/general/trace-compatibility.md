<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Tracing Compatibility
--->

# Semantic Conventions for Tracing Compatibility Components

**Status**: [Experimental][DocumentStatus]

This document defines trace semantic conventions used by the
compatibility components, e.g. OpenTracing Shim layer.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [OpenTracing](#opentracing)

<!-- tocstop -->

## OpenTracing

`Link`s created by the OpenTracing Shim MUST set `opentracing.ref_type`
with one of the accepted values, describing the direct causal relationships
between a child Span and a parent Span, as defined by
[OpenTracing](https://github.com/opentracing/specification/blob/master/specification.md).

<!-- semconv opentracing(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`opentracing.ref_type`](../attributes-registry/opentracing.md) | string | Parent-child Reference type [1] | `child_of` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The causal relationship between a child Span and a parent Span.

`opentracing.ref_type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `child_of` | The parent Span depends on the child Span in some capacity | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `follows_from` | The parent Span doesn't depend in any way on the result of the child Span | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
