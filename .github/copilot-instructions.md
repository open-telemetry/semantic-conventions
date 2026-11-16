# Copilot instructions

This repository defines OpenTelemetry semantic conventions. Attributes and
telemetry signals are defined in the YAML model under `model/`, which is the
source of truth. Docs under `docs/` are free-form prose with generated tables
inside `<!-- semconv ... -->` blocks, except `docs/registry/`, which is fully
generated. See [CONTRIBUTING.md](../CONTRIBUTING.md) and
[how to write conventions](../docs/how-to-write-conventions/README.md).

Scoped, path-specific instructions provide the detailed review guidance:

- [model-yaml.instructions.md](instructions/model-yaml.instructions.md) —
  reviewing semantic convention YAML models (`model/**/*.yaml`).
- [docs-markdown.instructions.md](instructions/docs-markdown.instructions.md) —
  reviewing semantic convention docs (`docs/**/*.md`).
- [chloggen.instructions.md](instructions/chloggen.instructions.md) —
  reviewing changelog entries (`.chloggen/**`).

Formatting, spelling, links, schema validity, generated tables, and the checks in
[policies](../policies/README.md) are enforced by CI; don't comment on them.

## Pull request checklist

Apply these checks to the PR as a whole:

- PRs that add conventions or change their semantics should link the relevant
  instrumentation and any applicable prototypes in the PR description
  ([how to contribute](../CONTRIBUTING.md#how-to-contribute),
  [prototyping](../docs/how-to-write-conventions/README.md#prototyping)).
  If none is linked, ask for it.
- Flag changes unrelated to the purpose stated in the PR title and description
  (for example a stability change, a breaking change, or edits to another area)
  and suggest moving them to a separate PR.
- Refactoring, migration guide, tooling, and `[chore]` PRs should not change
  attribute or signal semantics, stability, or generated documentation beyond
  what the change requires. Flag any such change.
- When a PR renames, deprecates, or changes the meaning of a convention, check
  that other references are updated: related signals, sibling system
  definitions, hand-written docs, and migration guides.
- PRs with user-facing changes need a changelog entry
  ([when to add a changelog entry](../CONTRIBUTING.md#when-to-add-a-changelog-entry)).
  Flag `[chore]` titles on PRs that change conventions or normative text.

Before running build, lint, or validation commands, follow
[CONTRIBUTING.md](../CONTRIBUTING.md); most checks run via `make check`,
`make check-policies`, and `make generate-all`.
