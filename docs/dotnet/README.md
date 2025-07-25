<!--- Hugo front matter used to generate the website version of this page:
linkTitle: .NET
--->

# Semantic conventions for .NET

This article documents semantic conventions for metrics and traces emitted by the .NET runtime and individual components in the .NET ecosystem.

The following span are currently supported:

- [HTTP client, DNS, and TLS](dotnet-network-traces.md): Semantic Conventions for HTTP client and connection-related *spans*.

The following metrics are currently supported:

* [ASP.NET Core](dotnet-aspnetcore-metrics.md): Semantic Conventions for ASP.NET Core routing, exceptions, and rate-limiting *metrics*.
* [DNS](dotnet-dns-metrics.md): Semantic Conventions for client-side DNS lookups associated with *metrics*.
* [HTTP](dotnet-http-metrics.md): Semantic Conventions for HTTP client and server *metrics*.
* [Kestrel](dotnet-kestrel-metrics.md): Semantic Conventions for Kestrel web server *metrics*.
* [SignalR](dotnet-signalr-metrics.md): Semantic Conventions for SignalR server *metrics*.
* [Runtime](/docs/runtime/dotnet-metrics.md): Semantic conventions for .NET Runtime *metrics*.
