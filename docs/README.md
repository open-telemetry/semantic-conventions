<!--- Hugo front matter used to generate the website version of this page:
cascade:
  body_class: otel-docs-spec
  github_repo: &repo https://github.com/open-telemetry/semantic-conventions
  github_subdir: docs
  path_base_for_github_subdir: tmp/semconv/docs/
  github_project_repo: *repo
redirects: [{ from: 'attributes-registry/*', to: 'registry/attributes/:splat' }]
cSpell:ignore: semconv CICD
auto_gen: below
linkTitle: Semantic conventions
--->

# OpenTelemetry semantic conventions

The Semantic Conventions define a common set of (semantic) attributes which provide meaning to data when collecting, producing and consuming it.
The Semantic Conventions specify among other things span names and kind, metric instruments and units as well as attribute names, types, meaning and valid values. For a detailed definition of the Semantic Conventions' scope see [Semantic Conventions Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability).
The benefit to using Semantic Conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms. This allows easier correlation and consumption of data.

Also see:

* [General](general/README.md): General Semantic Convention information
* [How to write semantic conventions](how-to-write-conventions/README.md)
* [Non-normative supplementary information](non-normative/README.md)
