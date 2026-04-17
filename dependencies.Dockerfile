# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.22.1@sha256:33ae522ae4b71c1c562563c1d81f46aa0f79f088a0873199143a1f11ac30e5c9 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.15.2@sha256:4750afa83e85a1b0a4964ea5700e9caa1c1e61b508435e09fd77f038747340e6 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-0a96dc2@sha256:2d397eb32e4add073deb5af328f7d644538cd62c007892c57b57551b073b6a12 AS lychee
