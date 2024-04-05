<!--- Hugo front matter used to generate the website version of this page:
--->

# OpenTracing

## OpenTracing Attributes

<!-- semconv registry.opentracing(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `opentracing.ref_type` | string | Parent-child Reference type [1] | `child_of` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The causal relationship between a child Span and a parent Span.

`opentracing.ref_type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `child_of` | The parent Span depends on the child Span in some capacity | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `follows_from` | The parent Span doesn't depend in any way on the result of the child Span | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->
