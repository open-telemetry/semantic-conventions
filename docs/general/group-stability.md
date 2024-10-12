<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Semantic Convention Groups
aliases: [semantic-convention-groups]
--->

# Semantic Convention Groups

**Status**: [Experimental][DocumentStatus]

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

- identity - TODO - identifies span type, metric instrument name, or event name
  among other spans, instruments, or events.
  All telemetry items of this type and with this name are expected to follow this
  semantic convention.
- `brief` and `note` describe the convention
- `stability` describes the maturity level of the convention
- `deprecated` property marks convention as deprecated and provides information about
  replacement or other details.
- `attributes` lists references to applicable attributes in the [registry](../attributes-registry/README.md)

In addition to common properties, semantic convention groups have type-specific properties, see
[Schema documentation](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md)
for the details.

## Group Stability

TODO: adopt new maturity levels.

Semantic Convention groups can be `stable` (corresponds to
[Stable maturity level](https://github.com/open-telemetry/oteps/blob/main/text/0232-maturity-of-otel.md#stable))
or `experimental` (corresponds to [Development maturity level](https://github.com/open-telemetry/oteps/blob/main/text/0232-maturity-of-otel.md#alpha))
if stability level is not specified, it's assumed to be `experimental`.

Group stability MUST NOT change from `stable` to `experimental`.

Identifiable (TODO) semantic convention group MUST NOT be removed even if it's `experimental`
to allow code generation and preserve documentation for legacy instrumentations.

When group is no longer recommended or supported, it SHOULD be deprecated.
When group is renamed, the existing group SHOULD be deprecated in favor of a new convention.

See [Versioning and Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability)
for the details on stability guarantees provided for specific group types.

### Attribute vs group stability

Semantic convention groups MAY reference attributes with stability levels different
from a group level.

Stability guarantees on the group level apply to group properties (such as type, identity and
signal-specific properties) and a subset of stable attributes used within this group.

Experimental group of any type:
- MAY add or remove a reference to a stable or an experimental attribute
- MAY change attribute requirement levels and other properties (that can be changed
  when referencing an attribute)

Stable groups MAY
- add references to experimental attributes with `opt_in` requirement level. The level MAY
in some cases be changed to a different level when attribute becomes stable.
- add or remove reference to stable attributes with `opt_in` requirement level.
- span, event, or resources groups MAY add a reference to a stable attribute with  `recommended` level,
- change stable attribute brief, note, or examples without altering the meaning and purpose of the attribute
  that would result in breaking change on the instrumentation or consumer side
- change experimental attribute properties or remove references to them.


Stable group:
- MUST NOT add or remove attribute references with `required` level
- SHOULD NOT add or remove attribute references with `conditionally_required` level
- SHOULD NOT change requirement level on stable attribute references
- span groups SHOULD NOT change `sampling_relevant` values on stable attribute references
- stable attributes MUST NOT be removed from a stable group.
- requirement level of a stable attribute SHOULD NOT change

### Examples of allowed and not allowed changes

#### Stable group and **stable** attribute

| Change                                                  | Is change allowed?                     | Description |
| ------------------------------------------------------- | -------------------------------------- | ----------- |
| Adding or removing **required** attribute               | not allowed                            | Breaks instrumentations and consumers |
| Adding or removing **conditionally required** attribute | not allowed, there could be exceptions | Could be fine if condition was never satisfied (e.g. HTTP 4 comes out)|
| Removing **recommended** attribute from a span/event    | not allowed, there could be exceptions |  |
| Adding **recommended** attributes to a span/event       | yes                                    |  |
| Adding or removing **recommended** attributes to a metric | not allowed, there could be exceptions | Some attributes don't affect number of time series |
| Adding or removing **opt-in** attribute from a group    | yes                                    |  |
| Changing requirement level                              | not allowed, there could be exceptions | Some changes from conditionally required -> recommended could be justified |
| Changing sampling_relevant value on a span attribute    | not allowed, there could be exceptions | Depending on requirement level |
| Changing brief, description, examples                   | yes                                    | As long as it does not change the meaning of the attribute |

#### Stable group and **experimental** attribute

| Change                                                  | Is change allowed?                     | Description |
| ------------------------------------------------------- | -------------------------------------- | ----------- |
| Adding or removing **required** attribute               | not allowed                            |  |
| Adding or removing **conditionally required** attribute | not allowed                            |  |
| Adding or removing **recommended** attribute from a group | not allowed                          |  |
| Adding or removing **opt-in** attribute from a group    | yes                                    |  |
| Changing requirement level                              | not allowed                            | Experimental attributes can only be opt-in on stable groups |
| Changing sampling_relevant value on a span attribute    | yes                                    |  |
| Changing brief, description, examples                   | yes                                    |  |
