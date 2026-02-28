<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Version selection
--->

# Semantic convention version selection

**Status**: [Development][DocumentStatus]

This document defines declarative configuration for semantic convention
version selection.

<!-- toc -->

- [Declarative configuration](#declarative-configuration)
  - [Unsupported configuration](#unsupported-configuration)
- [Additional rules for stable instrumentations](#additional-rules-for-stable-instrumentations)
- [Relationship with `OTEL_SEMCONV_STABILITY_OPT_IN`](#relationship-with-otel_semconv_stability_opt_in)

<!-- tocstop -->

## Declarative configuration

If semantic convention version selection is done via declarative configuration,
it SHOULD be under the path:

```
.instrumentation/development.general.<domain>.semconv
```

where `<domain>` is one of the following:

- `code`
- `db`
- `gen_ai`
- `http`
- `k8s`
- `messaging`
- `rpc`

The following properties SHOULD be supported:

| Property       | Type    | Required | Default |
| -------------- | ------- | -------- | ------- |
| `version`      | integer | Yes      | (none)  |
| `experimental` | boolean | No       | `false` |
| `dual_emit`    | boolean | No       | `false` |

**`version`**

The target semantic convention version for this domain (e.g., `1`).

**`experimental`**

When `true`, include development-stage conventions for the selected
`version`, regardless of whether that version is pre-stable or already
stable.

**`dual_emit`**

When `true`, also emit the previous stable major version alongside the
target version (e.g., `version=2, dual_emit=true` emits both v2 and v1).
Enables dual-emit for phased migration between major versions.

When conflicts arise between versions, the target (new) version SHOULD be
prioritized. Non-overlapping attributes from both versions SHOULD be merged,
so consumers can access attributes from both the previous and target versions.

Note: the `experimental` flag only applies to the selected version, not to the
previous version emitted via `dual_emit`.

### Unsupported configuration

A single configuration block is often shared across multiple
instrumentations with differing stability levels. Instrumentations
SHOULD NOT emit warnings for unsupported configuration and SHOULD
fall back gracefully by applying the following rules to the requested
(`version`, `experimental`, `dual_emit`) triplet, in order:

1. **`version`**: If the requested version is not supported, fall back
   to the nearest prior supported version. When `experimental` is
   `false`, only versions with stable support are candidates.
2. **`experimental`**: If `true` is requested but only stable
   conventions exist for the resolved version, treat as `false`.
3. **`dual_emit`**: If `true` is requested but dual-emit is not supported
   for the resolved version, treat as `false`.

If no supported version matches after applying these rules, use the
instrumentation's default behavior.

## Additional rules for stable instrumentations

Stable instrumentations MUST NOT break existing telemetry when operating
under the stable flag (`experimental: false`). See
[Semantic Conventions Stability][SemConvStability] for the
definition of stability guarantees and breaking changes.

When adding support for a new stable semantic convention version
(e.g., v1) to a stable instrumentation, the instrumentation SHOULD only
support the new conventions under `experimental: true` (even though the
convention itself is stable) until the implementation is complete and
validated. Once confident that the new version is fully supported, it
SHOULD then begin supporting `experimental: false` for that version. This
ensures users are not exposed to incomplete or changing telemetry when
using the stable configuration (`experimental: false`).

## Relationship with `OTEL_SEMCONV_STABILITY_OPT_IN`

When an instrumentation supports both declarative configuration and the
`OTEL_SEMCONV_STABILITY_OPT_IN` environment variable,
the declarative configuration MUST take precedence.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
[SemConvStability]: https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability
