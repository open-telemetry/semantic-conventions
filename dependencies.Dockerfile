# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.14.0@sha256:bea89bc5544ad760db2fd906c5285c2a3769c61fb04f660f9c31e7e44f11804b AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.3.0@sha256:e02dc1957f7a4195f0724762269dfe3309f13344629e0c926316a7cf72233af5 AS opa

# Semconv gen is used for backwards compatibility checks.
# TODO(jsuereth): Remove this when no longer used.
FROM otel/semconvgen:0.25.0@sha256:9df7b8cbaa732277d64d0c0a8604d96bb6f5a36d0e96338cba5dced720c16485 AS semconvgen
