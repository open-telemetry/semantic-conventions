# Semantic convention libraries

The code for OpenTelemetry semantic conventions defined in this repository can be auto-generated.

OpenTelemetry Language SIGs can auto-generate semantic conventions code in the form that's idiomatic for
their language and may (or may not) ship semantic-conventions as a stand-alone library.

This document outlines common patters and provides non-normative guidance on how to implement auto-generation
and structure semantic conventions artifact.

## Generating semantic conventions

<!-- TODO: mention weaver -->
The generation is done using [build-tools code generator](https://github.com/open-telemetry/build-tools/blob/main/semantic-conventions/README.md#code-generator).
It's based on YAML definitions of the semantic conventions and uses [Jinja templates](https://palletsprojects.com/p/jinja/).

For example, this Jinja template can be used to generate Python constant for an attribute name along with the docstring.

```jinja
{{attribute.fqn | to_const_name}} = "{{attribute.fqn}}"
"""
{{attribute.brief | to_doc_brief}}.
{%- if attribute.note %}
Note: {{attribute.note | to_doc_brief | indent}}.
{%- endif %}
"""
```

It generates the following code:

```python
SERVER_ADDRESS = "server.address"
"""
Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name.
Note: When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.
"""
```

Language SIGs are expected to create Jinja templates specific to their language.
Code-generation usually involves several steps which could be semi-automated:

1. Manually update the Semantic Conventions version when necessary
2. Add the new Schema URL to the list of supported versions
   - If it's not automated, then it can, at least, be automatically checked.
4. Check out (or download) this version of Semantic Conventions
5. Run code-generation script for each template
6. Fix lint violations in the auto-generated code (if any)
7. Send the PR with new code to the corresponding repository

Here're the examples of how steps 2-5 are implemented for [Java](https://github.com/open-telemetry/semantic-conventions-java/blob/7da24068eea69dff11a78d59750b115dc4c5854d/build.gradle.kts#L55-L137) and [Python](https://github.com/open-telemetry/opentelemetry-python/blob/23f67971a4c147b8586c3fe6a68c9cfb0f5d7362/scripts/semconv/generate.sh).

## Stability and versioning

Semantic Conventions contain a mix of stability levels.
Language SIGs that ship semantic conventions library may decide to ship a stable artifact with stable part of the Semantic Conventions, a preview artifact with all Semantic Conventions, or other combination that's idiomatic for this language and provides [SemVer 2.0](https://semver.org/) stability guarantees.

> Note:
> Shipping two versions of the same artifact (stable and preview) could be problematic if dependency resolution mechanism is based on the latest version.
> For example, if user application depends on the `semconv v1.0.0-preview` and some library brings transitive dependency on `semconv v1.1.0`, the latter would be resolved leading
> to compile or runtime issues in the application.
> Shipping two artifacts with different names is recommended for the ecosystems that are prone to diamond-dependency conflicts.

Other possible solutions include:

- Generate all semantic conventions for a given version in specific folder while keeping old versions. It is used by [opentelemetry-go](https://github.com/open-telemetry/opentelemetry-go/tree/main/semconv/) but could be problematic if the artifact size is a concern.
- Follow language-specific conventions to annotate experimental parts. For example, Semantic Conventions in Python keeps experimental attributes in `opentelemetry.semconv._incubating` import path which is considered (following Python underscore convention) to be internal and subject to change.

### Recommendations

- Generate code for deprecated attributes, metrics, and other conventions (even if they never reached stability). It minimizes runtime issues and breaking changes in user applications. Use appropriate annotations to mark deprecated conventions. All deprecated conventions should have `deprecated` property describing new alternatives (when available) which can be used in auto-generated code documentation.
- Generate code for stable convention inside incubating artifact. It prevents user code from breaking when semantic convention stabilizes. Deprecate stable definitions inside incubating artifact and point users to the stable location.
- Instrumentation libraries should depend on the stable semantic convention artifact or copy relevant definitions and keep them in their code base. Incubating artifact is intended for the end-users.

## Semantic Conventions Artifact Structure

This section contains suggestion on structuring semantic convention artifact(s) which should be adjusted to the specific language.

- Artifact name: `opentelemetry-semconv` and `opentelemetry-semconv-incubating` (if shipping incubating artifact)
- Namespace: `opentelemetry.semconv` and `opentelemetry.semconv.incubating`
- All supported Schema URLs should be listed to allow different instrumentations in one process to provide the exact version of conventions they follow.
- Attributes, metrics, and other convention definitions should be grouped by the convention type and the root namespace. See the example below:

```
├── SchemaURLs.*
├── attributes
│   ├── ClientAttributes.*
│   ├── HttpAttributes.*
│   └── ...
├── metrics
│   ├── HttpMetrics.*
│   └── ...
└── events
    └── ...
```