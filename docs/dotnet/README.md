<!--- Hugo front matter used to generate the website version of this page:
linkTitle: .NET
path_base_for_github_subdir:
  from: tmp/semconv/docs/dotnet/_index.md
  to: dotnet/README.md
--->

# Semantic Conventions for .NET metrics

**Status**: [Stable][DocumentStatus]

This article documents semantic conventions for metrics emitted by the .NET runtime and individual components in the .NET ecosystem.

The following metrics are currently supported:

* [ASP.NET Core](dotnet-aspnetcore-metrics.md): Semantic Conventions for ASP.NET Core routing, exceptions, and rate-limiting *metrics*.
* [DNS](dotnet-dns-metrics.md): Semantic Conventions for client-side DNS lookups associated with *metrics*.
* [HTTP](dotnet-http-metrics.md): Semantic Conventions for HTTP client and server *metrics*.
* [Kestrel](dotnet-kestrel-metrics.md): Semantic Conventions for Kestrel web server *metrics*.
* [SignalR](dotnet-signalr-metrics.md): Semantic Conventions for SignalR server *metrics*.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
