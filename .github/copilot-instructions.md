# Copilot instructions

This repository defines OpenTelemetry semantic conventions. The source of truth
is the YAML model under `model/`; the Markdown under `docs/` is generated from it
(see [CONTRIBUTING.md](../CONTRIBUTING.md) and
[how to write conventions](../docs/how-to-write-conventions/README.md)).

Scoped, path-specific instructions provide the detailed review guidance:

- [model-yaml.instructions.md](instructions/model-yaml.instructions.md) —
  reviewing semantic convention YAML models (`model/**/*.yaml`).
- [docs-markdown.instructions.md](instructions/docs-markdown.instructions.md) —
  reviewing semantic convention docs (`docs/**/*.md`).

Before running build, lint, or validation commands, follow
[CONTRIBUTING.md](../CONTRIBUTING.md); most checks run via `make check`,
`make check-policies`, and `make generate-all`.
