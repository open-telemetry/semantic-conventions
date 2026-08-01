# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.25.1@sha256:9ad46ca9cd4fa5974b121f886aa3e9946a8ef8ea905001a96c018d21f9db87ca AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.18.2@sha256:cba27d3c6af2feba1e4d6e6b5e24df5b53db332420d4148a90acccd12efae6ed AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-0a96dc2@sha256:2d397eb32e4add073deb5af328f7d644538cd62c007892c57b57551b073b6a12 AS lychee
