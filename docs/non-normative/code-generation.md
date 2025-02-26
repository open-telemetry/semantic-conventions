# Generating semantic convention libraries

<!-- toc -->

- [Stability and Versioning](#stability-and-versioning)
  - [Deprecated Conventions](#deprecated-conventions)
- [Semantic Conventions Artifact Structure](#semantic-conventions-artifact-structure)
- [Generating semantic conventions](#generating-semantic-conventions)
  - [Migrating from build-tools](#migrating-from-build-tools)
    - [Weaver config](#weaver-config)
    - [Jinja templates](#jinja-templates)

<!-- tocstop -->

The code for OpenTelemetry Semantic Conventions defined in this repository can be auto-generated.

OpenTelemetry Language SIGs can generate Semantic Conventions code in the form that's idiomatic for
their language and may (or may not) ship it as a stand-alone library.

This document outlines common patterns and provides non-normative guidance on how to structure semantic conventions artifacts
and generate the code.

## Stability and Versioning

Semantic Conventions contain a mix of stability levels.
Language SIGs that ship semantic conventions library may decide to ship a stable artifact with stable part of the Semantic Conventions, a preview artifact with all Semantic Conventions, or other combination that's idiomatic for this language and provides [SemVer 2.0](https://semver.org/) stability guarantees.

Possible solutions include:

- Generate all Semantic Conventions for a given version in specific folder while keeping old versions intact. It is used by [opentelemetry-go](https://github.com/open-telemetry/opentelemetry-go/tree/main/semconv/) but could be problematic if the artifact size is a concern.
- Follow language-specific conventions to annotate unstable parts. For example, Semantic Conventions in Python puts unstable attributes in `opentelemetry.semconv._incubating` import path which is considered (following Python underscore convention) to be internal and subject to change.
- Ship two different artifacts: one that contains stable Semantic Conventions and another one with all available conventions. For example, [semantic-conventions in Java](https://github.com/open-telemetry/semantic-conventions-java) are shipped in two artifacts: `opentelemetry-semconv` and `opentelemetry-semconv-incubating`.

> Note:
> Shipping two versions of the same artifact (stable and preview) could be problematic due to diamond-dependency problems.
> For example, if user application depends on the `semconv v1.0.0-preview` and some library brings transitive dependency on `semconv v1.1.0` that does not contain
> experimental conventions, the latter would be resolved leading to compilation or runtime issues in the application.

Instrumentation libraries should depend on the stable (part of) semantic convention artifact or copy relevant definitions into their own code base.
Unstable semantic conventions artifact is intended for end-user applications.

### Deprecated Conventions

It's recommended to generate code for deprecated attributes, metrics, and other conventions. Use appropriate annotations to mark them as deprecated.
Conventions have a `stability` property which provide the stability level at the deprecation time (`development`, `alpha`, `beta`, `release_candidate` or `stable`) and
the `deprecated` property that describes deprecation reason which can be used to generate documentation.

- Deprecated conventions that reached stability should not be removed without major version update according to SemVer.
- Conventions that were deprecated while being unstable should still be generated and kept in the preview (part of) semantic conventions artifact. It minimizes runtime issues
  and breaking changes in user applications.

Keep stable convention definitions inside the preview (part of) semantic conversions artifact. It prevents user code from breaking when semantic convention stabilizes. Deprecate stable definitions inside the preview artifact and point users to the stable location in generated documentation.
For example, in Java, the attribute `http.request.method` is defined as deprecated in both stable and preview artifacts (e.g., `io.opentelemetry.semconv.incubating.HttpIncubatingAttributes.HTTP_REQUEST_METHOD`, `io.opentelemetry.semconv.HttpAttributes.HTTP_REQUEST_METHOD`).

## Semantic Conventions Artifact Structure

This section contains suggestions on how to structure semantic convention artifact(s).

- Artifact name:
  - `opentelemetry-semconv` - stable conventions
  - `opentelemetry-semconv-incubating` - (if applicable) the preview artifact containing all (stable and unstable) conventions
- Namespace: `opentelemetry.semconv` and `opentelemetry.semconv.incubating`
- All supported Schema URLs should be listed to allow different instrumentations in the same application to provide the exact version of conventions they follow.
- Attributes, metrics, and other convention definitions should be grouped by the convention type and the root namespace. See the example below:

```
├── SchemaUrls.code
├── attributes
│   ├── ClientAttributes.code
│   ├── HttpAttributes.code
│   └── ...
├── metrics
│   ├── HttpMetrics.code
│   └── ...
└── events
    └── ...
```

## Generating semantic conventions

This section describes how to do code-generation with weaver.

> [!IMPORTANT]
> We're transitioning away from [build-tools](https://github.com/open-telemetry/build-tools/blob/main/semantic-conventions/README.md#code-generator)
> to [opentelemetry-weaver](https://github.com/open-telemetry/weaver/blob/main/crates/weaver_forge/README.md) to generate code for semantic conventions.
> All new code-generation should be done using weaver, build-tools may become incompatible with future version of semantic conventions.
> Weaver supports Semantic Conventions version starting from [1.26.0](https://github.com/open-telemetry/semantic-conventions/tree/v1.26.0).

Code-generation is based on YAML definitions in the specific version of semantic conventions.
Usually, it involves several steps where some can be semi-automated:
involves several steps which could be semi-automated:

1. Manually update the Semantic Conventions version in config
2. Add the new Schema URL to the list of supported versions
   - If it's not automated, then it can, at least, be automatically checked.
3. Check out (or download) the new version of Semantic Conventions
4. Run code-generation script (see below for the details)
5. Fix lint violations in the auto-generated code (if any)
6. Send the PR with new code to the corresponding repository

Here are examples of how steps 2-5 are implemented for [Python](https://github.com/open-telemetry/opentelemetry-python/pull/4091) and [Erlang](https://github.com/open-telemetry/opentelemetry-erlang/pull/733).

Step 4 (running code generation) depends on language-specific customizations. It's also the only step that's affected by tooling migration.

Check out [weaver code-generation documentation for more details](https://github.com/open-telemetry/weaver/blob/main/crates/weaver_forge/README.md)

### Migrating from build-tools

Migration from build-tools involves changing Jinja templates and adding a [weaver config file](https://github.com/open-telemetry/weaver/blob/main/crates/weaver_forge/README.md#configuration-file---weaveryaml).

#### Weaver config

Here's a simplified example of this file that generates all attributes.

```yaml
params:
  excluded_namespaces: [ios, aspnetcore, signalr, android, dotnet, jvm, kestrel]

templates:
  - pattern: semantic_attributes.j2
    filter: >
      semconv_grouped_attributes({
        "exclude_root_namespace": $excluded_namespaces
      })
      | map({
          root_namespace: .root_namespace,
          attributes: .attributes,
          output: $output + "attributes/"
        })
    application_mode: each
```

You can configure language-specific parameters in the `params` section of the config or pass them with `-DparamName=value` arguments when
running weaver command from the code generation script (similarly to build-tools).

Weaver is able to run code-generation for multiple templates (defined in the corresponding section) at once.

Before executing Jinja, weaver allows to filter or process semantic convention definitions in the `filter` section for each template.
In this example, it uses `semconv_grouped_attributes` filter - a helper method that groups attribute definitions by root namespace and excludes
attributes not relevant to this language. You can write alternative or additional filters and massage semantic conventions data using [JQ](https://jqlang.github.io/jq/manual/).

In certain cases, calling `semconv_grouped_attributes` with namespace exclusion and stability filters may be enough and post-processing is not necessary.

The `application_mode: each` configures weaver to run code generation for each semantic convention group and, as a consequence,
generate code for each group in a different file. The application mode `single` is also supported to apply the template to all groups at once.

See
[weaver code-generation docs](https://github.com/open-telemetry/weaver/blob/main/crates/weaver_forge/README.md)
for the details on the config, data schema, JQ filters, and more.

#### Jinja templates

Jinja templates need to be changed to leverage (better) data structure and helper methods.
The first key difference is that each jinja template can define how to name the corresponding file(s). If you
don't specify the name of the output file via the method `set_file_name`, Weaver will use the relative path
and the name of the template itself to determine the output file.

E.g. here's an example that uses root namespace in a subfolder provided in the `output` parameter.

```jinja
{% set file_name = ctx.output + (ctx.root_namespace | snake_case ) ~ "_attributes.py" -%}
{{- template.set_file_name(file_name) -}}
```

Notable changes on data structure:

- `attributes_and_templates` -> `ctx.attributes`
- `enum_attributes` -> `ctx.attributes | select("enum")`
- `metrics` -> `ctx.metrics`
- `root_namespace` -> `ctx.root_namespace` (only available if using `semconv_grouped_attributes` or similar filter)'
- all custom parameters are provided as properties under `ctx` variable.
- `attribute.fqn` -> `attribute.name`
- `attribute.type | instantiated_type` (gets underlying type of enum values)
- `attribute.attr_type.members` -> `attribute.type.members` (gets members of enum type)
- `member.member_id` -> `member.id` (gets id of the enum member)

Notable changes on helper methods:

- `attr.fqn | to_const_name` -> `attr.name | screaming_snake_case`
- `attr.fqn | to_camelcase(True)` -> `attr.name | pascal_case`
- `attr.brief | to_doc_brief | indent` -> `attr.brief | comment(indent=4)`, check out extensive [comment formatting configuration](https://github.com/open-telemetry/weaver/blob/main/crates/weaver_forge/README.md#comment-filter)
- stability/deprecation checks:
  - `attribute is stable` if checking one attribute, `attributes | select("stable")` to filter stable attributes
  - `attribute is deprecated` if checking one attribute, `attributes | select("deprecated")` to filter deprecated attributes
- check if attribute is a template: `attribute.type is template_type`
- new way to simplify switch-like logic: `key | map_text("map_name")`. Maps can be defined in the weaver config.
  It can be very useful to convert semantic convention attribute types to language-specific types.
