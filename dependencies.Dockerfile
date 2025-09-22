# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.18.0@sha256:5425ade81dc22ddd840902b0638b4b6a9186fb654c5b50c1d1ccd31299437390 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.8.0@sha256:0917dda453560b65798d3c78caed0376c4db0708f1e4df5724058a5dfd412948 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-2aa22f8@sha256:2e3786630482c41f9f2dd081e06d7da1c36d66996e8cf6573409b8bc418d48c4 AS lychee