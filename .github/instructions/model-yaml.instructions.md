---
applyTo: "model/**/*.yaml"
---

# Reviewing semantic convention YAML models

These files are the source of truth for all attributes, metrics, spans, events,
and entities. Review for design and semantic quality. CI (`make check-policies`
and other checks) already enforces the presence and format of these, so do not
comment on them — only on their correctness and appropriateness: name formatting,
namespace/constant collisions, backward compatibility, stability ordering,
`brief` presence, and entity associations.

Flag violations of the guidance below with a short rationale and a doc link.

## File formats

Two definition formats are supported and both are valid: files starting with
`file_format: definition/2` follow
[schema v2](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv.schema.v2.json),
all others follow
[v1](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md).
Schema is validated by the CI job. Review only the design and semantics described below.

## New attributes

Follow [defining attributes](/docs/how-to-write-conventions/README.md#defining-attributes).

- Prefer reusing an existing attribute; a new one needs a clear end-user benefit
  and a plan to emit it. See [common attributes](/docs/general/attributes.md).
- Confirm each new attribute is referenced by a signal; flag unused ones.
- New attributes should start at `development` stability.
- `brief`/`note` should clearly explain the attribute and link to standards
  (RFCs, specs) when relevant.
- If a value may contain PII/sensitive data, `note` should include a
  `> [!WARNING]` callout.

## Attribute type choices

See the [type syntax](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md#type).

- Use `enum` for short, well-known value sets; ISO 8601 strings for timestamps.
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
- Attributes should capture only the operation's own important details.
- For status, reference [recording errors](/docs/general/recording-errors.md);
  avoid strict rules for ambiguous cases (cancellations, 404s).

## Metrics

Follow [metrics general guidelines](/docs/general/metrics.md).

- Check the instrument type fits the measurement (`Counter`, `UpDownCounter`,
  gauge, histogram).
- `unit` should follow [UCUM](https://ucum.org/ucum): `1` for utilization, `s`
  for durations, non-prefixed units (`By` not `MiBy`), `{request}`-style
  annotations for counts; don't repeat the unit in the metric name.
- Metric attributes must be low-cardinality unless `opt_in`; flag unbounded
  values (ids, URLs, user input) as non-`opt_in` attributes.
- For `UpDownCounter`, increments and decrements must use the same attribute set.

## Events

Follow [events](/docs/general/events.md).

- Events are for named point-in-time occurrences; flag events for operations with
  duration (use a span) or whole-operation properties (use span attributes).
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

## Error handling

Follow [recording errors](/docs/general/recording-errors.md).

- Operations that can fail should populate `error.type`, with consistent values
  across the spans and metrics for the same operation.
