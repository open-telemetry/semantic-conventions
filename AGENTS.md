# AGENTS.md

Guidance for AI agents working in this repository.

## Repository layout

- `model/` — YAML definitions of attributes, metrics, spans, events, and
  entities. This is the source of truth.
- `docs/` — Markdown documentation. Tables between `<!-- semconv ... -->` and
  `<!-- endsemconv -->` are generated from `model/`; `docs/registry/` is fully
  generated. Don't edit generated content by hand.
- `.chloggen/` — changelog entries for user-facing changes.
- `policies/` — local weaver policies; most checks come from
  [opentelemetry-weaver-packages](https://github.com/open-telemetry/opentelemetry-weaver-packages).

## Commands

- `make generate-all` — regenerate Markdown tables and the registry after
  changing YAML.
- `make check` — lint, links, and policies; `make check-policies` runs only the
  weaver policies.
- `make chlog-new` / `make chlog-validate` — create and validate a changelog entry.

See [CONTRIBUTING.md](CONTRIBUTING.md) for prerequisites and details.

## Writing and reviewing conventions

Read before writing or reviewing conventions:

- [How to write conventions](docs/how-to-write-conventions/README.md), including
  [resources and entities](docs/how-to-write-conventions/resource-and-entities.md).
- [Naming](docs/general/naming.md), [metrics](docs/general/metrics.md),
  [events](docs/general/events.md),
  [attribute requirement levels](docs/general/attribute-requirement-level.md), and
  [recording errors](docs/general/recording-errors.md).

Review checklists, also used by Copilot code review:

- [.github/copilot-instructions.md](.github/copilot-instructions.md) — whole-PR
  checklist.
- [.github/instructions/model-yaml.instructions.md](.github/instructions/model-yaml.instructions.md)
  — `model/**/*.yaml`.
- [.github/instructions/docs-markdown.instructions.md](.github/instructions/docs-markdown.instructions.md)
  — `docs/**/*.md`.
- [.github/instructions/chloggen.instructions.md](.github/instructions/chloggen.instructions.md)
  — `.chloggen/**`.
