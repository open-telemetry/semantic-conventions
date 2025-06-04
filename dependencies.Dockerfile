# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.15.1@sha256:95c0aaa493d84ac72a1188756bd46eec1ead8e82004e7778ff5779736be8d578 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.5.0@sha256:09a86c8bb25e68603fe011cdb8ee8909b37f479eac95c0f3f1053d48fa9521eb AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-2aa22f8@sha256:2e3786630482c41f9f2dd081e06d7da1c36d66996e8cf6573409b8bc418d48c4 AS lychee