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

Before running build, lint, or validation commands, follow
[CONTRIBUTING.md](../CONTRIBUTING.md); most checks run via `make check`,
`make check-policies`, and `make generate-all`.
