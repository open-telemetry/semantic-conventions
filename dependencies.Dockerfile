# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.22.0@sha256:0e08b9e1a88f4202234db10d4b973828fd7ecbc37370d12f3fd2d8f5d22b70e4 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.14.1@sha256:d94bd6ac314a57aceeb6dacc3f27bc59f9083b49f365aa79105abb345f94e573 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-0a96dc2@sha256:2d397eb32e4add073deb5af328f7d644538cd62c007892c57b57551b073b6a12 AS lychee
