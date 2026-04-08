# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.22.1 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.15.1@sha256:c3e940a236811f34a9bdf1b98e1a441db7f1ef81151a0bb4a9706467a11c8cd9 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-0a96dc2@sha256:2d397eb32e4add073deb5af328f7d644538cd62c007892c57b57551b073b6a12 AS lychee
