<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Semantic Conventions
# no_list: true
cascade:
  body_class: otel-docs-spec
  github_repo: &repo https://github.com/open-telemetry/semantic-conventions
  github_subdir: docs
  path_base_for_github_subdir: content/en/docs/specs/semconv/
  github_project_repo: *repo
path_base_for_github_subdir:
  from: content/en/docs/specs/semconv/_index.md
  to: README.md
--->

# OpenTelemetry Semantic Conventions

The Semantic Conventions define a common set of (semantic) attributes which provide meaning to data when collecting, producing and consuming it.
The Semantic Conventions specify among other things span names and kind, metric instruments and units as well as attribute names, types, meaning and valid values. For a detailed definition of the Semantic Conventions' scope see [Semantic Conventions Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability).
The benefit to using Semantic Conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms. This allows easier correlation and consumption of data.

Semantic Conventions are defined for the following areas:

* **[General](general/README.md): General Semantic Conventions**.
* [Cloud Providers](cloud-providers/README.md): Semantic Conventions for cloud providers libraries.
* [CloudEvents](cloudevents/README.md): Semantic Conventions for the CloudEvents specification.
* [Database](database/README.md): Semantic Conventions for database operations.
* [Exceptions](exceptions/README.md): Semantic Conventions for exceptions.
* [FaaS](faas/README.md): Semantic Conventions for Function as a Service (FaaS) operations.
* [Feature Flags](feature-flags/README.md): Semantic Conventions for feature flag evaluations.
* [HTTP](http/README.md): Semantic Conventions for HTTP client and server operations.
* [Messaging](messaging/README.md): Semantic Conventions for messaging operations and systems.
* [Object Stores](object-stores/README.md): Semantic Conventions for object stores operations.
* [RPC](rpc/README.md): Semantic Conventions for RPC client and server operations.
* [System](system/README.md): System Semantic Conventions.

Semantic Conventions by signals:

* [Events](general/events.md): Semantic Conventions for event data.
* [Logs](general/logs.md): Semantic Conventions for logs data.
* [Metrics](general/metrics.md): Semantic Conventions for metrics.
* [Resource](resource/README.md): Semantic Conventions for resources.
* [Trace](general/trace.md): Semantic Conventions for traces and spans.
