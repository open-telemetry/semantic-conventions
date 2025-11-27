<!--- Hugo front matter used to generate the website version of this page:
cascade:
  body_class: otel-docs-spec
  github_repo: &repo https://github.com/open-telemetry/semantic-conventions
  github_subdir: docs
  path_base_for_github_subdir: tmp/semconv/docs/
  github_project_repo: *repo
redirects:
  - { from: 'attributes-registry/*', to: 'registry/attributes/:splat' }
  - { from: 'database/*', to: 'db/:splat' }
cSpell:ignore: semconv CICD
auto_gen: below
linkTitle: Semantic conventions
--->

# OpenTelemetry semantic conventions

The Semantic Conventions define a common set of (semantic) attributes which provide meaning to data when collecting, producing and consuming it.
The Semantic Conventions specify among other things span names and kind, metric instruments and units as well as attribute names, types, meaning and valid values. For a detailed definition of the Semantic Conventions' scope see [Semantic Conventions Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability).
The benefit to using Semantic Conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms. This allows easier correlation and consumption of data.

Semantic Conventions are defined for the following areas:

* **[General](general/README.md): General Semantic Conventions**.
* [CICD](cicd/README.md): Semantic Conventions for CICD systems.
* [Cloud Providers](cloud-providers/README.md): Semantic Conventions for cloud providers libraries.
* [CloudEvents](cloudevents/README.md): Semantic Conventions for the CloudEvents specification.
* [Database](db/README.md): Semantic Conventions for database operations.
* [Exceptions](exceptions/README.md): Semantic Conventions for exceptions.
* [FaaS](faas/README.md): Semantic Conventions for Function as a Service (FaaS) operations.
* [Feature Flags](feature-flags/README.md): Semantic Conventions for feature flag evaluations.
* [Generative AI](gen-ai/README.md): Semantic Conventions for generative AI (LLM, etc.) operations.
* [GraphQL](graphql/README.md): Semantic Conventions for GraphQL implementations.
* [HTTP](http/README.md): Semantic Conventions for HTTP client and server operations.
* [Messaging](messaging/README.md): Semantic Conventions for messaging operations and systems.
* [Object Stores](object-stores/README.md): Semantic Conventions for object stores operations.
* [RPC](rpc/README.md): Semantic Conventions for RPC client and server operations.
* [System](system/README.md): System Semantic Conventions.

Semantic Conventions by signals:

* [Events](general/events.md): Semantic Conventions for event data.
* [Logs](general/logs.md): Semantic Conventions for logs data.
* [Metrics](general/metrics.md): Semantic Conventions for metrics.
* [Profiles](general/profiles.md): Semantic Conventions for profiles.
* [Resource](resource/README.md): Semantic Conventions for resources.
* [Trace](general/trace.md): Semantic Conventions for traces and spans.

Also see:

* [How to write semantic conventions](how-to-write-conventions/README.md)
* [Non-normative supplementary information](non-normative/README.md)
