# YAML Model for Semantic Conventions

The YAML descriptions of semantic convention contained in this directory are intended to
be used by the various OpenTelemetry language implementations to aid in automatic
generation of semantics-related code.

⚠ If you want to read the semantic conventions and not edit them, please see
the generated markdown output in the [docs](../docs/README.md) folder.

## Writing semantic conventions

Semantic conventions for the spec MUST adhere to the
[attribute naming](../docs/general/attribute-naming.md),
[attribute requirement level](../docs/general/attribute-requirement-level.md),
and [metric requirement level](../docs/general/metric-requirement-level.md) conventions.

Refer to the [syntax](https://github.com/open-telemetry/build-tools/tree/v0.24.0/semantic-conventions/syntax.md)
for how to write the YAML files for semantic conventions and what the YAML properties mean.

A schema file for VS code is configured in the `/.vscode/settings.json` of this
repository, enabling auto-completion and additional checks. Refer to
[the generator README](https://github.com/open-telemetry/build-tools/tree/v0.24.0/semantic-conventions/README.md) for what extension you need.

## Generating markdown

These YAML files are used by the make target `table-generation` to generate consistently
formatted Markdown tables for all semantic conventions in the specification. Run it from the root of this repository using the command

```
make table-generation
```

For more information, see the [Weaver](https://github.com/open-telemetry/weaver)
as our code generations tool.
Using Weaver, it is also possible to generate code for use in OpenTelemetry
language projects, in addition to build-tools.

See also:

* [Markdown Templates](https://github.com/open-telemetry/semantic-conventions/tree/main/templates/registry/markdown)
* [Weaver Template Documentation](https://github.com/open-telemetry/weaver/blob/main/crates/weaver_forge/README.md)
* [Weaver Usage Documentation](https://github.com/open-telemetry/weaver/blob/main/docs/usage.md#registry-generate)
* [Build Tools - Code Generator](https://github.com/open-telemetry/build-tools/tree/main/semantic-conventions#code-generator)
