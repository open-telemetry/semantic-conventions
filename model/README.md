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

Refer to the [syntax](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md)
for how to write the YAML files for semantic conventions and what the YAML properties mean.

A schema file for VS code is configured in the `/.vscode/settings.json` of this
repository, enabling auto-completion and additional checks. Refer to
[the generator README](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md) for what extension you need.

## Generating markdown

These YAML files are used by the make target `table-generation` to generate consistently
formatted Markdown tables for all semantic conventions in the specification. Run it from the root of this repository using the command

```
make table-generation
```

For more information, see the [Weaver](https://github.com/open-telemetry/weaver)
as our code generations tool.

See also:

* [Markdown Templates](../templates/registry/markdown)
* [Weaver Template Documentation](https://github.com/open-telemetry/weaver/blob/main/crates/weaver_forge/README.md)
* [Weaver Usage Documentation](https://github.com/open-telemetry/weaver/blob/main/docs/usage.md#registry-generate)
* [Code Generator Documentation](../docs/non-normative/code-generation.md)
