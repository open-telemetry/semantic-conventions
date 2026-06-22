# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.24.1@sha256:263964a7d444e77812f7a2d654e17683c4760a968c91278acdb7a44c20ccd572 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.17.1@sha256:dc009236137bb225a1ef09293bb32f2ee1861cc428870d297bf71412d50221c3 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-0a96dc2@sha256:2d397eb32e4add073deb5af328f7d644538cd62c007892c57b57551b073b6a12 AS lychee
