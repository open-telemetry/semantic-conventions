---
applyTo: "model/**/*.yaml"
---

# Reviewing semantic convention YAML models

These files are the source of truth for all attributes, metrics, spans, events,
and entities. CI (`make check-policies`, schema validation, and other checks)
already enforces name formatting, namespace/constant collisions, backward
compatibility, stability ordering, `brief` presence, metric brief formatting, and
entity associations; don't comment on those. Review design and semantic quality
using the guidance below.

Flag violations with a short rationale and a doc link. Name the concrete existing
attribute, signal, or doc section you are comparing against instead of asking a
generic question.

Two definition formats are valid: files starting with `file_format: definition/2`
follow
[schema v2](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv.schema.v2.json),
all others follow
[v1](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md).

## Definitions: `brief`, `note`, `examples`

See [defining attributes](/docs/how-to-write-conventions/README.md#defining-attributes).

- When a value could be read in more than one way (which side of a call, which
  of several possible sources, which perspective), the note must say which one
  to report. When a signal references `server.*`, `client.*`, `source.*`, or
  `destination.*`, the ref note should say what they mean for that signal (see
  [defining spans: attributes](/docs/how-to-write-conventions/README.md#attributes)).
- A `note` must add information that the name, `brief`, type, or inherited
  definition does not already give. Flag notes that restate the brief.
- When a new attribute or metric is close to an existing one (`*.id` vs
  `*.name`, a detailed vs. a coarse variant, the same measurement on another
  signal), its brief or note should say how they differ.
- For metrics and for duration or count attributes, the definition must say what
  is measured: when the measurement starts and ends, which event increments a
  count, and how failures, cancellations, and retries are treated.
- New attributes should say where instrumentation gets the value (which API,
  field, or protocol element) and what to do when it is unavailable (see
  [prototyping](/docs/how-to-write-conventions/README.md#prototyping)).
- Normative text uses [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) keywords
  at the right strength, is addressed to instrumentation, and only requires
  things instrumentation can observe and control.
- Examples must be realistic values valid for the signal they appear on, never
  placeholders, and consistent with examples of sibling attributes.
- Keep wording consistent with sibling definitions in the same namespace; when a
  PR changes the wording of one definition, check whether its siblings need the
  same change.
- Link to the specific external standard or specification when the definition
  describes an externally defined concept.

## YAML structure

See [model README](/model/README.md) and
[span type](/docs/how-to-write-conventions/README.md#span-type).

- Put each statement on the element it constrains: requirements for one attribute
  in that attribute's ref `note`, per-value mappings in enum member briefs, and
  general semantics in the registry definition — not in the signal-level note.
- Don't restate in a signal `note` what the model already says (span kind, an
  attribute's requirement level, a fixed value).
- Override `brief`, `note`, `examples`, or `requirement_level` on an attribute
  ref only when the override changes the meaning for that signal; flag overrides
  identical to the inherited definition.
- Don't copy attribute lists between spans, metrics, and system-specific
  variants. Reuse a shared attribute group, or define a refinement of the base
  signal when specializing an existing operation for a system or library.

## Requirement levels

Follow [attribute requirement levels](/docs/general/attribute-requirement-level.md).

- `conditionally_required` and `recommended` conditions must be something the
  instrumentation can evaluate at runtime, and must agree with the attribute's
  note, examples, and any span name fallback.
- `required` is only for attributes that are essential and available to all
  instrumentations.
- Use `opt_in` for attributes that are expensive to obtain, may contain sensitive
  data, are verbose, or are high-cardinality on metrics. Question `opt_in` on
  cheap, low-cardinality, non-sensitive attributes.
- Compare the requirement level with the same attribute on counterpart signals
  (client vs. server, span vs. metric for the same operation, analogous systems
  in the area) and flag unexplained differences.

## New attributes and reuse

Follow [defining attributes](/docs/how-to-write-conventions/README.md#defining-attributes).

- Prefer reusing an existing attribute. Search the
  [attribute registry](/docs/registry/attributes/), the
  [common attributes](/docs/general/attributes.md) (`server.*`, `client.*`,
  `network.*`, `url.*`, `error.*`, `exception.*`) and the area's own namespace,
  and name the candidate in your comment. A new attribute needs a clear end user
  benefit and a plan to emit it.
- Flag pairs of attributes in the same proposal that carry the same information
  in a different form.
- Confirm each new attribute is referenced by a signal; flag unused ones.
- New attributes, enum members, and signals should start at `development`
  stability (see [defining new conventions](/docs/how-to-write-conventions/README.md#defining-new-conventions)).
- If a value may contain PII/sensitive data, `note` should include a
  `> [!WARNING]` callout.

## Naming

Follow [naming](/docs/general/naming.md). Check in particular:

- Names are precise: name the object and then the property (`file.owner.name`,
  not `file.owner`), using `{object}.{property}` rather than `{object}_{property}`
  when the object could have other properties
  ([general naming considerations](/docs/general/naming.md#general-naming-considerations)).
- Multi-word segments use snake_case unless an established concatenated form
  exists, determined by the evidence order in
  [general naming considerations](/docs/general/naming.md#general-naming-considerations).
- New names reuse the terms and suffixes of analogous existing names in the same
  and related areas (for example `*.operation.name`, `*.query.text`).
- Attributes and metrics specific to one system use the `{system}.*` namespace
  ([system-specific naming](/docs/general/naming.md#system-specific-naming)).
- Metric names follow [instrument naming](/docs/general/naming.md#instrument-naming)
  (`.limit`, `.usage`, `.utilization`; `.time` for a monotonic total time
  counter, `.duration` for a per-operation histogram) and the
  [counter and UpDownCounter rules](/docs/general/naming.md#naming-rules-for-counters-and-updowncounters).

## Attribute type choices

See the [type syntax](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md#type).

- Use `enum` for short, well-known value sets; ISO 8601 strings for timestamps.
- New enum members should match values used by real systems or standards; see
  [defining enum attribute members](/docs/how-to-write-conventions/README.md#defining-enum-attribute-members).
- Arrays should be homogeneous and represent one concept; split distinct concepts
  into separate attributes (e.g. `geo.lat`/`geo.lon`, not one array).
- Use `template[...]` only for dynamic names, and only the last segment may vary.
- Prefer flat attributes over complex/structured values.

## Spans

Follow [defining spans](/docs/how-to-write-conventions/README.md#defining-spans).

- Spans are for operations with duration worth observing (e.g. out-of-process
  calls); flag point-in-time occurrences (use events) or short in-process work.
- Flag a span duplicating an existing definition; distinct spans should differ in
  kind or attribute set.
- Names must be low-cardinality, follow `{action} {target}` using values also
  available as attributes; flag static prefixes or raw high-cardinality values.
  Each placeholder needs a fallback when its attribute may be unavailable or
  high-cardinality (see [naming pattern](/docs/how-to-write-conventions/README.md#naming-pattern)).
- Attributes should capture only the operation's own important details.
- For status, reference [recording errors](/docs/general/recording-errors.md);
  avoid strict rules for ambiguous cases (cancellations, 404s).

## Metrics

Follow [defining metrics](/docs/how-to-write-conventions/README.md#defining-metrics)
and [metrics general guidelines](/docs/general/metrics.md).

- Check the instrument choice (`Counter` for monotonic totals, `UpDownCounter`
  for additive values that can decrease, gauges only for non-additive values),
  that aggregation over all attributes is meaningful,
  and whether an existing metric split by an attribute already covers the new one.
- `unit` should follow [UCUM](https://ucum.org/ucum): `1` for utilization, `s`
  for durations, non-prefixed units (`By` not `MiBy`), `{request}`-style
  annotations for counts; don't repeat the unit in the metric name.
- Duration histogram bucket boundaries should follow
  [duration histogram bucket boundaries](/docs/general/metrics.md#duration-histogram-bucket-boundaries).
- Metric attributes must be low-cardinality unless `opt_in`; flag unbounded
  values (IDs, URLs, user input) as non-`opt_in` attributes.
- For `UpDownCounter`, increments and decrements must use the same attribute set.

## Events

Follow [events](/docs/general/events.md).

- Events are for named point-in-time occurrences; flag events for operations with
  duration (use a span) or whole-operation properties (use span attributes). Flag
  events whose attributes record start/end times or durations of an operation.
- `name` must uniquely identify the event and MUST NOT contain dynamic values.
- Don't define severity text, `body` (beyond a display message), or
  `ObservedTimestamp`.
- Reuse attributes shared with related signals; include `error.type` for
  failure/outcome events.

## Entities

Follow [resources and entities](/docs/how-to-write-conventions/resource-and-entities.md).

- A new entity is warranted when a signal needs a source and none fits; prefer an
  "is-a" relationship across domains (e.g. `k8s.container` is a `container`).
- Extend an entity with descriptive attributes only when it cannot own telemetry
  itself (e.g. `docker.container` reports against `container`).
- Each attribute must set `role: identifying` or `role: descriptive`.
- Identifying attributes should be minimally sufficient, immutable for the
  entity's lifespan, and resolvable consistently by multiple observers.
- Don't copy another entity's identifying attributes onto a new entity.

## Stability and deprecation

See [`deprecated` syntax](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md#semantic-convention)
and [code structure](/CONTRIBUTING.md#code-structure).

- Flag stability changes that the PR title and changelog do not mention.
- Put `deprecated` on the registry definition (not only on a ref). Place
  deprecated attributes and signals (not individual enum members) where the
  area already keeps its deprecations, or under
  `model/{root-namespace}/deprecated/` if it has none.
- Deprecation text (`deprecated.note`, or the brief in older definitions) must
  agree with `deprecated`: with `renamed_to`, name the replacement and never say
  there is no replacement. Don't otherwise rewrite the brief, note, enum member
  briefs, or stability of the deprecated definition.

## Error handling

Follow [recording errors](/docs/general/recording-errors.md).

- Operations that can fail should populate `error.type`, with consistent values
  across the spans, metrics, and events for the same operation.
