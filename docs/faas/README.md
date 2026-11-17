<!--- Hugo front matter used to generate the website version of this page:
linkTitle: FaaS
--->

# Semantic conventions for Function-as-a-Service

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for Function as a Service (FaaS) spans, metrics and logs.

> [!IMPORTANT]
> Existing FaaS instrumentations that are using
> [v1.44.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.44.0/docs/faas/faas-spans.md)
> (or prior):
>
> * SHOULD NOT change the version of the FaaS conventions that they emit by
>   default in their existing major version. Conventions include (but are not
>   limited to) attributes, metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in their existing major version as a comma-separated list of category-specific values
>   (e.g., `http`, `database`, `faas`). The list of values includes:
>   * `faas` - emit the stable FaaS conventions, and stop emitting
>     the experimental FaaS conventions that the instrumentation emitted
>     previously.
>   * `faas/dup` - emit both the experimental and stable FaaS conventions,
>     allowing for a phased rollout of the stable semantic conventions.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental FaaS conventions
>     the instrumentation was emitting previously.
>   * Note: `faas/dup` has higher precedence than `faas` in case both values are present
> * SHOULD maintain (security patching at a minimum) their existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * MAY drop the environment variable in their next major version and emit only
>   the stable FaaS conventions.

Semantic conventions for FaaS are defined for the following signals:

* [FaaS Spans](faas-spans.md): Semantic Conventions for FaaS *spans*.
* [FaaS Metrics](faas-metrics.md): Semantic Conventions for FaaS *metrics*.
* [FaaS Exceptions](faas-exceptions.md): Semantic Conventions for FaaS *exceptions*.

Technology specific semantic conventions are defined for the following FaaS services:

* [AWS Lambda](aws-lambda.md): Semantic Conventions for *AWS Lambda*.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status/
