# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.18.0@sha256:5425ade81dc22ddd840902b0638b4b6a9186fb654c5b50c1d1ccd31299437390 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.10.0@sha256:c0814ce7811ecef8f1297a8e55774a1d5422e5c18b996b665acbc126124fab19 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-0a96dc2@sha256:2d397eb32e4add073deb5af328f7d644538cd62c007892c57b57551b073b6a12 AS lychee
