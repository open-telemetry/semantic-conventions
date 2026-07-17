# Local check policies

Most semantic-convention policy checks are provided by the shared
[opentelemetry-weaver-packages](https://github.com/open-telemetry/opentelemetry-weaver-packages/tree/main/policies/check)
repository and are consumed by `make check-policies` (see the `check-policies`
target in the [Makefile](../Makefile)). The following packages are delegated:

- `naming_conventions` — name formats, namespace/constant collisions (attributes,
  metrics, events, entities), enum-member uniqueness, complex-type restrictions,
  metric brief formatting.
- `stability` — deprecation (`renamed_to`) validity, stable entities must have
  identity, and the stability-ordering check (a signal may not claim a higher
  stability than any attribute it references unless the attribute is `opt_in`).
- `entity_associations` — `entity_associations` must resolve to known entities.
- `backwards-compatibility` — no breaking changes vs. the baseline registry.

Only checks that are **not** available upstream are kept here:

- `brief.rego` — requires a non-empty `brief` on every attribute and signal.
  This is a semantic-conventions editorial requirement rather than a general
  registry rule.

## Exceptions

Per-signal exceptions to the shared checks are declared in the model via
`annotations.<package>.policy_exceptions`, where the exception key is the
finding id with the package prefix dropped. For example:

```yaml
annotations:
  naming_conventions:
    policy_exceptions:
      - metric_namespace_collision
  stability:
    policy_exceptions:
      - metric_lower_stability_attribute
```

## Tests

Local policies are unit-tested with OPA under [`../policies_test`](../policies_test)
via `make test-policies`. The delegated packages carry their own tests in the
weaver-packages repository.
