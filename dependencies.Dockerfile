# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.16.1@sha256:5ca4901b460217604ddb83feaca05238e2b016a226ecfb9b87a95555918a03af AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.6.0@sha256:72220208128e960b6620c155630566a38b76de2d4f230c3ca9442aaaf6626077 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-2aa22f8@sha256:2e3786630482c41f9f2dd081e06d7da1c36d66996e8cf6573409b8bc418d48c4 AS lychee