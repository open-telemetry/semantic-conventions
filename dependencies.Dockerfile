# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.20.0@sha256:fa4f1c6954ecea78ab1a4e865bd6f5b4aaba80c1896f9f4a11e2c361d04e197e AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.12.3@sha256:d051ffbd818b36e46cfaaa3fd4770e0a2103813877bb77234f025e7e7f73a316 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-0a96dc2@sha256:2d397eb32e4add073deb5af328f7d644538cd62c007892c57b57551b073b6a12 AS lychee
