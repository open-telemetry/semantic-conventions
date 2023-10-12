# Semantic Conventions for DNS metrics emitted by .NET

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This document defines semantic conventions for DNS metrics emitted by .NET.

<!-- toc -->

- [DNS metrics](#dns-metrics)
  * [Metric: `dns.lookup.duration`](#metric-dnslookupduration)

<!-- tocstop -->

## DNS metrics

### Metric: `dns.lookup.duration`

<!-- semconv metric.dotnet.dns.lookup.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `dns.lookup.duration` | Histogram | `s` | Measures the time taken to perform a DNS lookup. [1] |

**[1]:** Meter name: `System.Net.NameResolution`; Added in: .NET 8.0
<!-- endsemconv -->

<!-- semconv metric.dotnet.dns.lookup.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `dns.question.name` | string | The name being queried. [1] | `www.example.com`; `dot.net` | Required |
| `error.type` | string | One of the resolution errors or the full name of exception type. [2] | `host_not_found`; `no_recovery`; `System.Net.Sockets.SocketException` | Conditionally Required: if and only if an error has occurred. |

**[1]:** The name being queried.

If the name field contains non-printable
characters (below 32 or above 126), those characters should be represented
as escaped base 10 integers (\DDD). Back slashes and quotes should be escaped.
Tabs, carriage returns, and line feeds should be converted to \t, \r, and
\n respectively.

**[2]:** Following errors code are reported:

- "host_not_found"
- "try_again"
- "address_family_not_supported"
- "no_recovery"

See [SocketError](https://learn.microsoft.com/dotnet/api/system.net.sockets.socketerror)
documentation for more details.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation does not define a custom value for it. |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
