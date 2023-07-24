<!--- Hugo front matter used to generate the website version of this page:
linkTitle: .NET
path_base_for_github_subdir:
  from: content/en/docs/specs/semconv/dotnet/_index.md
  to: dotnet/README.md
--->

# Semantic Conventions for .NET metrics

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This document documents semantic conventions for metrics emitted by .NET runtime and individual components in .NET ecosystem.

Following metrics are currently supported:

* [ASP.NET Core](dotnet-aspnetcore-metrics.md): Semantic Conventions for ASP.NET Core routing, exceptions, and rate-limiting *metrics*.
* [DNS](dotnet-dns-metrics.md): Semantic Conventions for client-side DNS lookups associated with *metrics*.
* [HTTP](dotnet-http-metrics.md): Semantic Conventions for HTTP client and server *metrics*.
* [Kestrel](dotnet-kestrel-metrics.md): Semantic Conventions for Kestrel web server *metrics*.
* [SignalR](dotnet-signalr-metrics.md): Semantic Conventions for SignalR server *metrics*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
