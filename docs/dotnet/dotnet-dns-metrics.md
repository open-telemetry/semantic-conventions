<!--- Hugo front matter used to generate the website version of this page:
linkTitle: DNS
--->

# Semantic conventions for DNS metrics emitted by .NET

**Status**: [Stable][DocumentStatus]

This article defines semantic conventions for DNS metrics emitted by .NET.

<!-- toc -->

- [DNS metrics](#dns-metrics)
  - [Metric: `dns.lookup.duration`](#metric-dnslookupduration)

<!-- tocstop -->

## DNS metrics

### Metric: `dns.lookup.duration`

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.51.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- Tables in this document are not auto-generated and are intentionally frozen in time. From the .NET perspective this metric and its attributes are stable till the next major version. They are still experimental in the OpenTelemetry. -->
| Name | Instrument Type | Unit (UCUM) | Description |
| ---- | --------------- | ----------- | ----------- |
| `dns.lookup.duration` | Histogram | `s` | Measures the time taken to perform a DNS lookup. [1] |

**[1]:** Meter name: `System.Net.NameResolution`; Added in: .NET 8.0

| Attribute | Type | Description | Examples | Requirement Level |
| --- | --- | --- | --- | --- |
| `dns.question.name` | string | The name being queried. [1] | `www.example.com`; `dot.net` | Required |
| [`error.type`](../registry/attributes/error.md) | string | One of the resolution errors or the full name of exception type. [2] | `host_not_found`; `no_recovery`; `System.Net.Sockets.SocketException` | Conditionally Required: if and only if an error has occurred. |

**[1]:** The name being queried.
If the name field contains non-printable characters (below 32 or above 126), those characters should be represented as escaped base 10 integers (\DDD). Back slashes and quotes should be escaped. Tabs, carriage returns, and line feeds should be converted to \t, \r, and \n respectively.

**[2]:** The following errors codes are reported:

- "host_not_found"
- "try_again"
- "address_family_not_supported"
- "no_recovery"

See [SocketError](https://learn.microsoft.com/dotnet/api/system.net.sockets.socketerror)
for more details.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value | Description |
| --- | --- |
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. |

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
