# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.13.2 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.1.0 AS opa

# Semconv gen is used for backwards compatibility checks.
# TODO(jsuereth): Remove this when no longer used.
FROM otel/semconvgen:0.25.0 AS semconvgen
