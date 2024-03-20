<!--- Hugo front matter used to generate the website version of this page:
linkTitle: DNS
--->

# Semantic Conventions for DNS queries

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions to apply when instrumenting DNS queries.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Metrics](#metrics)
  - [Metric: `dns.lookup.duration`](#metric-dnslookupduration)

<!-- tocstop -->

## Metrics

### Metric: `dns.lookup.duration`

**Status**: [Experimental][DocumentStatus]

This metric is optional.

This metric SHOULD be specified with
[`ExplicitBucketBoundaries`](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/api.md#instrument-advisory-parameters)
of `[ 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10 ]`.

<!-- semconv metric.dns.lookup.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `dns.lookup.duration` | Histogram | `s` | Measures the time taken to perform a DNS lookup. |
<!-- endsemconv -->

<!-- semconv metric.dns.lookup.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`dns.question.name`](../attributes-registry/dns.md) | string | The name being queried. [1] | `www.example.com`; `dot.net` | Required |
| [`error.type`](../attributes-registry/error.md) | string | Describes the error the DNS lookup failed with. [2] | `host_not_found`; `no_recovery`; `java.net.UnknownHostException` | Conditionally Required: if and only if an error has occurred. |

**[1]:** If the name field contains non-printable characters (below 32 or above 126), those characters should be represented as escaped base 10 integers (\DDD). Back slashes and quotes should be escaped. Tabs, carriage returns, and line feeds should be converted to \t, \r, and \n respectively.

**[2]:** Instrumentations SHOULD use error code such as one of errors reported by `getaddrinfo`([Linux or other POSIX systems](https://man7.org/linux/man-pages/man3/getaddrinfo.3.html) / [Windows](https://learn.microsoft.com/windows/win32/api/ws2tcpip/nf-ws2tcpip-getaddrinfo)) or one reported by the runtime or client library. If error code is not available, the full name of exception type SHOULD be used.

`error.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `_OTHER` | A fallback error value to be used when the instrumentation doesn't define a custom value. |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
