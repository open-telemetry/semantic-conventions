<!--- Hugo front matter used to generate the website version of this page:
linkTitle: RPC
path_base_for_github_subdir:
  from: tmp/semconv/docs/rpc/_index.md
  to: rpc/README.md
--->

# Semantic Conventions for RPC

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for remote procedure calls (RPC)
, also called "remote method invocations" (RMI).

Semantic conventions for RPC are defined for the following signals:

* [RPC Spans](rpc-spans.md): Semantic Conventions for RPC client and server *spans*.
* [RPC Metrics](rpc-metrics.md): Semantic Conventions for RPC *metrics*.

Technology specific semantic conventions are defined for the following RPC systems:

* [Connect](connect-rpc.md): Semantic Conventions for *Connect RPC*.
* [gRPC](grpc.md): Semantic Conventions for *gRPC*.
* [JSON-RPC](json-rpc.md): Semantic Conventions for *JSON-RPC*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
