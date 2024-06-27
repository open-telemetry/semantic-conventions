# Messaging semantic convention stability migration guide

Due to the significant number of modifications and the extensive user base
affected by them, existing messaging instrumentations published by
OpenTelemetry are required to implement a migration plan that will assist users in
transitioning to the stable messaging semantic conventions.

Specifically, when existing messaging instrumentations published by OpenTelemetry are
updated to the stable messaging semantic conventions, they:

- SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN` in
  their existing major version, which accepts:
  - `messaging` - emit the stable messaging conventions, and stop emitting
    the old messaging conventions that the instrumentation emitted previously.
  - `messaging/dup` - emit both the old and the stable messaging conventions,
    allowing for a phased rollout of the stable semantic conventions.
  - The default behavior (in the absence of one of these values) is to continue
    emitting whatever version of the old messaging conventions the
    instrumentation was emitting previously.
- Need to maintain (security patching at a minimum) their existing major version
  for at least six months after it starts emitting both sets of conventions.
- May drop the environment variable in their next major version and emit only
  the stable messaging conventions.

## Summary of changes

This section summarizes the changes made to the HTTP semantic conventions
from
[v1.24.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/messaging/README.md).
to
[v1.TODO (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.TODO/docs/messaging/README.md).

### Common messaging attributes

| Change | Comments |
| ------ | -------- |
