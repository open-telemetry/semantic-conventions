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
YAML (e.g. a `note` on a metric), not as free-form prose in the Markdown.

- When prose next to a semconv block explains how one attribute is used by one
  signal, suggest moving it to the `note` of that attribute's reference in the
  signal definition. When it describes the signal itself, suggest the signal's
  `note`.
- Flag prose that repeats a `brief` or `note` already rendered in a nearby
  semconv block, and suggest deleting it.

## Clarity

- Flag terms and jargon that the document doesn't define or link, pronouns with
  more than one possible referent, and lists of conditions that don't say
  whether all or any must apply. Ask for a definition, a link, or an example.
- Flag sentences that give the reader no information, such as "additional
  conventions may be added in the future", and references to signals or
  attributes that the conventions don't define. Suggest deleting them.
- Flag guidance repeated from another section or from
  [general docs](/docs/general/); suggest linking to the original section
  instead.
- Use OpenTelemetry terms precisely: "entity", "span", "event", and "resource"
  have specific meanings; flag loose use. In guidance that applies to more than
  one signal, flag wording tied to a single signal, for example "span" when the
  guidance also applies to logs or metrics; the same applies to any other signal.
- Keep the document to what semantic conventions and instrumentation control;
  flag requirements on SDK internals, backends, or vendor behavior and suggest
  linking to the relevant specification instead.

## Content quality

- Normative statements should use RFC 2119 keywords (MUST, SHOULD, MAY)
  correctly, be unambiguous, and make clear who must act. In signal and area docs
  that is usually instrumentation, and statements should only require what
  instrumentation can observe and control; in `docs/general/` and
  `docs/how-to-write-conventions/` it is usually the convention author.
- Prose must match the corresponding YAML (requirement levels, stability) and
  [general docs](/docs/general/). A section describing a signal should sit under
  a heading whose `**Status**` matches the signal's stability. Flag
  contradictions between prose and models.
- Descriptions and examples should be accurate and realistic; flag placeholder or
  misleading examples.
- Don't present deprecated attributes, metrics, or values as current in
  hand-written prose; use the replacement.
- Link to external standards (RFCs, specs) when describing documented concepts.
- Call out missing PII/sensitive-data warnings where relevant.
- Error-recording guidance should match
  [recording errors](/docs/general/recording-errors.md).

## Hugo frontmatter

- When a `<!--- Hugo front matter ... --->` block is present, `linkTitle` should
  be the short sub-area name (e.g. `Spans`, `Metrics`) and omitted when it would
  duplicate the title. See [Hugo frontmatter](/CONTRIBUTING.md#hugo-frontmatter).
