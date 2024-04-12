<!--- Hugo front matter used to generate the website version of this page:
--->

# Feature Flag

- [Feature Flag](#feature_flag)

## Feature Flag Attributes

| Attribute                    | Type   | Description                                                                                                             | Examples            | Stability                                                        |
| ---------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------- | ---------------------------------------------------------------- |
| `feature_flag.key`           | string | The unique identifier of the feature flag.                                                                              | `logo-color`        | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `feature_flag.provider_name` | string | The name of the service provider that performs the flag evaluation.                                                     | `Flag Manager`      | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `feature_flag.variant`       | string | SHOULD be a semantic identifier for a value. If one is unavailable, a stringified version of the value can be used. [1] | `red`; `true`; `on` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** A semantic identifier, commonly referred to as a variant, provides a means
for referring to a value without including the value itself. This can
provide additional context for understanding the meaning behind a value.
For example, the variant `red` maybe be used for the value `#c05543`.

A stringified version of the value can be used in situations where a
semantic identifier is unavailable. String representation of the value
should be determined by the implementer.
