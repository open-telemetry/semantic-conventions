<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Exceptions
--->

# Semantic conventions for exceptions

**Status**: [Stable][DocumentStatus]

> [!IMPORTANT]
>
> Existing instrumentations that record exceptions as span events:
>
> * SHOULD introduce an environment variable `OTEL_SEMCONV_EXCEPTION_SIGNAL_OPT_IN`
>   supporting the following values:
>   * `logs` - emit exceptions as logs only.
>   * `logs/dup` - emit both span events and logs, allowing for a phased rollout.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting exceptions as span events (existing behavior).
> * SHOULD maintain (security patching at a minimum) their existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * MAY drop the environment variable in their next major version and emit exceptions
>   as logs only.
>
> Even after instrumentations start emitting exceptions only as logs, users will
> still have the option to route those to span events at the SDK layer.

Semantic conventions for Exceptions are defined for the following signals:

* [Exceptions on spans](exceptions-spans.md): Semantic Conventions for Exceptions recorded on *spans* (deprecated).
* [Exceptions in logs](exceptions-logs.md): Semantic Conventions for Exceptions recorded in *logs*.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
