# DO NOT BUILD
# This file is just for tracking dependencies of the semantic convention build.
# Dependabot can keep this file up to date with latest containers.

# Weaver is used to generate markdown docs, and enforce policies on the model.
FROM otel/weaver:v0.19.0@sha256:3d20814cef548f1d31f27f054fb4cd6a05125641a9f7cc29fc7eb234e8052cd9 AS weaver

# OPA is used to test policies enforced by weaver.
FROM openpolicyagent/opa:1.11.0@sha256:322ff76e01139cc2cb4ab2d70e9037c528c2219bba9e1ccca9eaec19d52364c6 AS opa

# Lychee is used for checking links in documentation.
FROM lycheeverse/lychee:sha-0a96dc2@sha256:2d397eb32e4add073deb5af328f7d644538cd62c007892c57b57551b073b6a12 AS lychee
