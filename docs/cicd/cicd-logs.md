<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Logs
--->

# Semantic conventions for CICD logs

**Status**: [Development][DocumentStatus]

CI/CD systems emit logs as part of pipeline runs, usually consisting of the stdout/stderr
of any processes launched as part of the pipeline run.

The controller of any CI/CD system may also emit logs (e.g. "Starting pipeline run").

Any logs emitted by CI/CD systems SHOULD follow the [General Semantic Conventions for logs](/docs/general/logs.md).

When a trace context is available (cf. [CICD Spans](cicd-spans.md)) then emitted logs SHOULD be correlated to the execution context as defined in the [logs specification](https://opentelemetry.io/docs/specs/otel/logs/#log-correlation).

Any resources of the [CICD and VCS resource conventions][cicdres] that apply SHOULD be used.

[cicdres]: /docs/resource/cicd.md "CICD and VCS resource conventions"
[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
