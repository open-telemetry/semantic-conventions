# YAML model for semantic conventions

The YAML descriptions of semantic conventions contained in this directory are intended to
be used by the various OpenTelemetry language implementations to aid in automatic
generation of semantics-related code.

> [!NOTE]
>
> If you want to read the semantic conventions and not edit them, please see
> the generated markdown output in the [docs](../docs/README.md) folder.

## Writing semantic conventions

Semantic conventions for the spec MUST adhere to the
[naming](../docs/general/naming.md),
[attribute requirement level](../docs/general/attribute-requirement-level.md),
and [metric requirement level](../docs/general/metric-requirement-level.md) conventions.

Refer to the [syntax](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md)
for how to write the YAML files for semantic conventions and what the YAML properties mean.

A schema file for VS code is configured in the `/.vscode/settings.json` of this
repository, enabling auto-completion and additional checks. Refer to
[the generator README](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md) for what extension you need.

When defining semantic conventions, follow the [contributing guide](/CONTRIBUTING.md#1-modify-the-yaml-model):

- If new attributes are necessary, define them in the [attribute registry](/docs/registry/attributes/README.md).
  Attributes can only be defined inside groups with `attribute_group` type and with `id` starting with `registry.` prefix.
- Define new spans, metrics, events, resources, and other conventions using the appropriate group type. See
  [semantic convention groups](/docs/general/semantic-convention-groups.md) for more details.

## Generating markdown

These YAML files are used by the make targets `registry-generation` and `table-generation` to generate consistently
formatted Markdown tables for all semantic conventions in the specification. Run it from the root of this repository using the command

```bash
make registry-generation table-generation
```

Or, for convenience, run

```bash
make generate-all
```

which executes both targets along with other markdown generation targets that
update [areas](/AREAS.md) and GitHub area labels.

For more information, see [Weaver](https://github.com/open-telemetry/weaver)
as our code generation tool.

## Validating semantic conventions

Semantic conventions YAML files are validated by the `check-policies` make target for backward compatibility,
name formatting, and other policies.

You can run it with the following command:

```
make check-policies
```

See also:

* [Markdown Templates](../templates/registry/markdown)
* [Weaver Template Documentation](https://github.com/open-telemetry/weaver/blob/main/crates/weaver_forge/README.md)
* [Weaver Usage Documentation](https://github.com/open-telemetry/weaver/blob/main/docs/usage.md#weaver-registry-generate)
* [Code Generator Documentation](../docs/non-normative/code-generation.md)
