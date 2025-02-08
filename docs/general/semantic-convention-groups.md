<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Semantic convention groups
aliases: [group-stability]
--->

# Semantic convention groups

**Status**: [Development][DocumentStatus]

Spans, metrics, events, and resources are defined in semantic convention groups in YAML schema.
Each group has a `type` property that could be one of the following:

- `span` - defines semantic convention for a specific type of span, such as HTTP `CLIENT`
- `metric` - defines semantic convention for a specific metric, such as HTTP client request duration
- `event` - defines semantic conventions for a specific event, such as exception.
- `resource` - defines semantic conventions for a specific entity the telemetry is collected within,
  such as `service`.

Groups that have `attribute_group` type do not describe semantic convention and
are used for auxiliary purposes.

All semantic convention groups have the following common properties:

- `id` - identifies specific span type, metric instrument, or event
  among other spans, instruments, or events.
- `brief` and `note` provide human-readable description of the convention
- `stability` describes the maturity level of the convention
- `deprecated` property marks convention as deprecated and provides information about
  replacement or other details.
- `attributes` lists references to applicable attributes in the [registry](../attributes-registry/README.md)

In addition to common properties, semantic convention groups have type-specific properties, see
[Schema documentation](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md)
for the details.

## Group Stability

Semantic Convention groups can have the following [stability levels][MaturityLevel]:
`development`, `alpha`, `beta`, `release_candidate`, and `stable`.

Stability level is required on groups of all types except `attribute_group`.
If stability level is not specified, it's assumed to be `development`.

Group stability MUST NOT change from `stable` to any other level.

Semantic convention group of any stability level MUST NOT be removed
to preserve code generation and documentation for legacy instrumentations.

When group is renamed or no longer recommended, it SHOULD be deprecated.

See [Versioning and Stability][Stability] for the details on stability guarantees
provided for semantic convention groups of different types.

Stability guarantees **do not** apply to groups with `attribute_group` type as they
don't describe telemetry items.

### Groups with mixed stability

Stability guarantees on a group apply to the group properties (such as type, id and
signal-specific properties) as well as overridden properties of stable attributes
referenced by this group.

Stability guarantees on a group level **do not** apply to unstable attribute references.

**Unstable groups:**

- MAY add or remove references to stable or unstable attributes
- MAY change requirement level and other properties of attribute references

**Stable groups:**

- MAY add or remove references to unstable attributes with `opt_in`
  requirement level.
- SHOULD NOT have references to unstable attributes with requirement level
  other than `opt_in`.
  The requirement level of an unstable attribute reference
  MAY be changed when this attribute becomes stable in cases allowed by the
  [Versioning and Stability][Stability].
- MUST NOT remove references to stable attributes.

Stable instrumentations MUST NOT report telemetry following the unstable part
of semantic conventions by default. They MAY support unstable part and allow
users to opt into it.

<!-- TODO: SchemaURL needs to contain some indication of stability level, e.g. as a suffix -->
<!-- https://github.com/open-telemetry/semantic-conventions/issues/1511 -->

[Stability]: https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability
[MaturityLevel]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.41.0/oteps/0232-maturity-of-otel.md
[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
