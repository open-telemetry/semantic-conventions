---
applyTo: ".chloggen/**"
---

# Reviewing changelog entries

Changelog entries are `.chloggen/*.yaml` files transcribed into `CHANGELOG.md` at
release time. See [changelog](/CONTRIBUTING.md#5-changelog) and
[TEMPLATE.yaml](/.chloggen/TEMPLATE.yaml). `make chlog-validate` checks that the
fields are present and well-formed, so do not comment on that. Review whether
the content is correct for this PR.

- `issues` lists the tracking issue(s) for this change (usually the one the PR
  closes), or this PR's own number when there is no issue. Flag `0`, template placeholders, and numbers of unrelated or
  earlier PRs.
- `component` must match one or more folder names under `model/` for the areas
  whose YAML the PR changes. Docs-only or cross-cutting entries may use `docs`,
  `general`, or `all`; don't flag those.
- `change_type` matches the change; see
  [choosing a change type](/CONTRIBUTING.md#choosing-a-change-type).
- `note` must match the final diff: attribute, metric, and signal names exist in
  the changed YAML with the same spelling, and claims such as opt-in, deprecated,
  renamed, or a stability level match the model.
- `note` is one short, specific sentence that names the affected attributes or
  signals in backticks, when applicable; rationale belongs in the PR description.
- The entry covers every user-visible change in the PR listed in
  [when to add a changelog entry](/CONTRIBUTING.md#when-to-add-a-changelog-entry),
  such as requirement level changes, new or removed enum members, and changes to
  normative text.
