---
applyTo: "docs/**/*.md"
---

# Reviewing semantic convention Markdown docs

Review the substance of the prose. Formatting, spelling, link validity, tables of
contents, and whether generated tables are up to date are enforced by CI,
so do not comment on those.

Flag issues below with a short rationale and a doc link.

## Keep signal details in YAML

Content between `<!-- semconv ... -->` and `<!-- endsemconv -->` is generated from
`model/**/*.yaml`. Don't flag issues inside these blocks, but review their
consistency with the surrounding free-form prose. Anything that belongs to a
specific attribute, metric, span, event, or entity definition should live in the
YAML (e.g. a `note` on a metric), not as free-form prose in the Markdown. Flag
prose that documents a specific signal's semantics and should instead be a
`brief`/`note` inside the model.

## Content quality

- Normative statements should use RFC 2119 keywords (MUST, SHOULD, MAY)
  correctly, be unambiguous, and match the corresponding YAML (requirement
  levels, stability). Flag contradictions between prose and models.
- Descriptions and examples should be accurate and realistic; flag placeholder or
  misleading examples.
- Link to external standards (RFCs, specs) when describing documented concepts.
- Call out missing PII/sensitive-data warnings where relevant.
- Error-recording guidance should match
  [recording errors](/docs/general/recording-errors.md).

## Hugo frontmatter

- When a `<!--- Hugo front matter ... --->` block is present, `linkTitle` should
  be the short sub-area name (e.g. `Spans`, `Metrics`) and omitted when it would
  duplicate the title. See [Hugo frontmatter](/CONTRIBUTING.md#hugo-frontmatter).
