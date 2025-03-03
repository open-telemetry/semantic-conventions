<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Runtime environment
--->

# Semantic conventions for runtime environment

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for
runtime environment spans, metrics and logs.

<!-- toc -->

- [Metrics](#metrics)
  - [Attributes](#attributes)

<!-- tocstop -->

## Metrics

Runtime environments vary widely in their terminology, implementation, and
relative values for a given metric. For example, Go and Python are both
garbage collected languages, but comparing heap usage between the Go and
CPython runtimes directly is not meaningful. For this reason, this document
does not propose any standard top-level runtime metric instruments. See [OTEP
108](https://github.com/open-telemetry/oteps/pull/108/files) for additional
discussion.

Metrics specific to a certain runtime environment should be prefixed with
the runtime's top-level namespace `{environment}.*`, e.g., `jvm.*` and follow the
[general metric semantic convention guidelines](/docs/general/metrics.md#general-guidelines).

Authors of runtime instrumentations are responsible for the choice of
`{environment}` to avoid ambiguity when interpreting a metric's name or values.

For example, some programming languages have multiple runtime environments
that vary significantly in their implementation, like [Python which has many
implementations](https://wiki.python.org/moin/PythonImplementations). For
such languages, consider using specific `{environment}` prefixes to avoid
ambiguity, like `cpython.*` and `pypy.*`.

Also consider the
[general metrics](/docs/general/metrics.md#general-guidelines),
[system metrics](/docs/system/system-metrics.md) and
[OS process metrics](/docs/system/process-metrics.md)
semantic conventions when instrumenting runtime environments.

- [Go](go-metrics.md)
- [JVM](jvm-metrics.md)
- [Node.js](nodejs-metrics.md)
- [V8 JS Engine](v8js-metrics.md)
- [.NET](dotnet-metrics.md)

### Attributes

[`process.runtime`](/docs/resource/process.md#process-runtimes)
resource attributes SHOULD be included on runtime metric events as appropriate.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
