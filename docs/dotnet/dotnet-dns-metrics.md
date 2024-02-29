<!--- Hugo front matter used to generate the website version of this page:
linkTitle: DNS
--->

# Semantic Conventions for DNS metrics emitted by .NET

**Status**: [Stable][DocumentStatus]

This article defines semantic conventions for DNS metrics emitted by .NET.

<!-- toc -->

- [DNS metrics](#dns-metrics)
  - [Metric: `dns.lookup.duration`](#metric-dnslookupduration)

<!-- tocstop -->

## DNS metrics

### Metric: `dns.lookup.duration`

DNS lookup duration measures the time taken to perform a DNS lookup.

This metric follows the common [dns.lookup.duration](../dns/dns-metrics.md#metric-dnslookupduration) definition.

Notes:

- Meter name is `System.Net.NameResolution`
- Metric added in .NET 8.0
- When the `error.type` attribute is reported, it contains one of [Socket Errors](https://learn.microsoft.com/dotnet/api/system.net.sockets.socketerror?view=net-8.0) in snake_case, or a full exception type.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
