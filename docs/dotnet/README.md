<!--- Hugo front matter used to generate the website version of this page:
linkTitle: .NET
--->

# Semantic conventions for .NET

This article documents semantic conventions for metrics and traces emitted by the .NET runtime and individual components in the .NET ecosystem.

The following span are currently supported:

- [HTTP client, DNS, and TLS](dotnet-network-traces.md): Semantic Conventions for HTTP client and connection-related _spans_.

The following metrics are currently supported:

- [ASP.NET Core](dotnet-aspnetcore-metrics.md): Semantic Conventions for ASP.NET Core routing, exceptions, and rate-limiting _metrics_.
- [DNS](dotnet-dns-metrics.md): Semantic Conventions for client-side DNS lookups associated with _metrics_.
- [HTTP](dotnet-http-metrics.md): Semantic Conventions for HTTP client and server _metrics_.
- [Kestrel](dotnet-kestrel-metrics.md): Semantic Conventions for Kestrel web server _metrics_.
- [SignalR](dotnet-signalr-metrics.md): Semantic Conventions for SignalR server _metrics_.
- [Runtime](/docs/runtime/dotnet-metrics.md): Semantic conventions for .NET Runtime _metrics_.
