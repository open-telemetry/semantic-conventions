# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.17.1@sha256:32523b5e44fb44418786347e9f7dde187d8797adb6d57a2ee99c245346c3cdfe AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.7.1@sha256:e14c54bddfd680d051db44eab44d4b7ec96609a60d4359e04273b9a1457ce3c4 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-2aa22f8@sha256:2e3786630482c41f9f2dd081e06d7da1c36d66996e8cf6573409b8bc418d48c4 AS lychee