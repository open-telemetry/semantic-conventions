<!--- Hugo front matter used to generate the website version of this page:
linkTitle: HTTP migration
aliases: [../http/migration-guide]
--->

# HTTP semantic convention stability migration

Due to the significant number of modifications and the extensive user base
affected by them, existing HTTP instrumentations published by
OpenTelemetry are required to implement a migration plan that will assist users in
transitioning to the stable HTTP semantic conventions.

Specifically, when existing HTTP instrumentations published by OpenTelemetry are
updated to the stable HTTP semantic conventions, they:

- SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN` in
  their existing major version, which accepts:
  - `http` - emit the stable HTTP and networking conventions, and stop emitting
    the old HTTP and networking conventions that the instrumentation emitted
    previously.
  - `http/dup` - emit both the old and the stable HTTP and networking
    conventions, allowing for a phased rollout of the stable semantic
    conventions.
  - The default behavior (in the absence of one of these values) is to continue
    emitting whatever version of the old HTTP and networking conventions the
    instrumentation was emitting previously.
- Need to maintain (security patching at a minimum) their existing major version
  for at least six months after it starts emitting both sets of conventions.
- May drop the environment variable in their next major version and emit only
  the stable HTTP and networking conventions.

> [!NOTE]
> `OTEL_SEMCONV_STABILITY_OPT_IN` is only intended to be used when migrating
> from an experimental semantic convention to its initial stable version.

## Summary of changes

This section summarizes the changes made to the HTTP semantic conventions
from
[v1.20.0](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md)
to
[v1.23.1 (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.23.1/README.md).

### Common attributes across HTTP client and server spans

<!-- prettier-ignore-start -->
| Change | Comments |
| --- | --- |
| `http.method` &rarr; `http.request.method` | Now captures only 9 common HTTP methods by default (configurable) plus `_OTHER` |
| `http.status_code` &rarr; `http.response.status_code` | |
| `http.request.header.<key>` | &bullet; Dash (`"-"`) to underscore (`"_"`) normalization in `<key>` has been removed<br>&bullet; On HTTP server spans: now must be provided to sampler |
| `http.response.header.<key>` | Dash (`"-"`) to underscore (`"_"`) normalization in `<key>` has been removed |
| `http.request_content_length` &rarr; `http.request.body.size` | &bullet; Recommended &rarr; Opt-In<br>&bullet; _Not marked stable yet_ |
| `http.response_content_length` &rarr; `http.response.body.size` | &bullet; Recommended &rarr; Opt-In<br>&bullet; _Not marked stable yet_ |
| `user_agent.original` | &bullet; On HTTP client spans: Recommended &rarr; Opt-In<br>&bullet; On HTTP server spans: now must be provided to sampler<br>&bullet; See note if [migrating from <= v1.18.0](#migrating-from--v1180) |
| `net.protocol.name` &rarr; `network.protocol.name` | Recommended &rarr; Conditionally required if not `http` and `network.protocol.version` is set |
| `net.protocol.version` &rarr; `network.protocol.version` | &bullet; Examples fixed: `2.0` &rarr; `2` and `3.0` &rarr; `3`<br>&bullet; See note if [migrating from <= v1.19.0](#migrating-from--v1190) |
| `net.sock.family` | Removed |
| `net.sock.peer.addr` &rarr; `network.peer.address` | On HTTP server spans: if `http.client_ip` was unknown, then also `net.sock.peer.addr` &rarr; `client.address`; `client.address` must be provided to sampler |
| `net.sock.peer.port` &rarr; `network.peer.port` | Now captured even if same as `server.port` |
| `net.sock.peer.name` | Removed |
| New: `http.request.method_original` | Only captured when `http.request.method` is `_OTHER` |
| New: `error.type` | |
<!-- prettier-ignore-end -->

References:

- [Common attributes v1.20.0](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md#common-attributes)
- [Common attributes v1.23.1 (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.23.1/docs/http/http-spans.md#common-attributes)

### HTTP client span attributes

<!-- prettier-ignore-start -->
| Change | Comments |
| --- | --- |
| `http.url` &rarr; `url.full` | |
| `http.resend_count` &rarr; `http.request.resend_count` | |
| `net.peer.name` &rarr; `server.address` | |
| `net.peer.port` &rarr; `server.port` | Now captured even when same as default port for scheme |
<!-- prettier-ignore-end -->

References:

- [HTTP client span attributes v1.20.0](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md#http-client)
- [HTTP client span attributes v1.23.1 (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.23.1/docs/http/http-metrics.md#metric-httpserverrequestduration)

### HTTP server span attributes

<!-- prettier-ignore-start -->
| Change | Comments |
| --- | --- |
| `http.route` | No change |
| `http.target` &rarr; `url.path` and `url.query` | Split into two separate attributes |
| `http.scheme` &rarr; `url.scheme` | Now factors in [X-Forwarded-Proto][], [Forwarded#proto][] headers |
| `http.client_ip` &rarr; `client.address` | If `http.client_ip` was unknown (i.e., no [X-Forwarded-For][], [Forwarded#for][] headers), then `net.sock.peer.addr` &rarr; `client.address`; now must be provided to sampler |
| `net.host.name` &rarr; `server.address` | Now based only on [Host][Host header], [:authority][HTTP/2 authority], [X-Forwarded-Host][], [Forwarded#host][] headers |
| `net.host.port` &rarr; `server.port` | &bullet; Now based only on [Host][Host header], [:authority][HTTP/2 authority], [X-Forwarded-Host][X-Forwarded-Host], [Forwarded#host][] headers<br>&bullet; Now captured even when same as default port for scheme |
| `net.sock.host.addr` &rarr; `network.local.address` | |
| `net.sock.host.port` &rarr; `network.local.port` | No longer defaults to `server.port` when `network.local.address` is set. |
<!-- prettier-ignore-end -->

References:

- [HTTP server span attributes v1.20.0](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md#http-server)
- [HTTP server span attributes v1.23.1 (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.23.1/docs/http/http-metrics.md#metric-httpserverrequestduration)

### HTTP client and server span names

The `{http.method}` portion of span names is replace by `HTTP` when
`{http.method}` is `_OTHER`.

See note if [migrating from `<= v1.17.0`](#migrating-from--v1170).

References:

- [HTTP client and server span names v1.20.0](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md#name)
- [HTTP client and server span names v1.23.1 (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.23.1/docs/http/http-metrics.md#metric-httpserverrequestduration)

### HTTP client duration metric

Metric changes:

- **Name**: `http.client.duration` &rarr; `http.client.request.duration`
- **Unit**: `ms` &rarr; `s`
- **Description**: `Measures the duration of outbound HTTP requests.` &rarr;
  `Duration of HTTP client requests.`
- **Histogram buckets**: boundaries updated to reflect change from milliseconds
  to seconds, and zero bucket boundary removed
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| --- | --- |
| `http.method` &rarr; `http.request.method` | Now captures only 9 common HTTP methods by default plus `_OTHER` |
| `http.status_code` &rarr; `http.response.status_code` | |
| `net.peer.name` &rarr; `server.address` | |
| `net.peer.port` &rarr; `server.port` | Now captured even when same as default port for scheme |
| `net.sock.peer.addr` | Removed |
| `net.protocol.name` &rarr; `network.protocol.name` | Recommended &rarr; Conditionally required if not `http` and `network.protocol.version` is set |
| `net.protocol.version` &rarr; `network.protocol.version` | Examples fixed: `2.0` &rarr; `2` and `3.0` &rarr; `3`; see note if [migrating from `<= v1.19.0`](#migrating-from--v1190) |
| New: `error.type` | |
<!-- prettier-ignore-end -->

References:

- [Metric `http.client.duration` v1.20.0](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/metrics/semantic_conventions/http-metrics.md#metric-httpclientduration)
- [Metric `http.client.request.duration` v1.23.1 (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.23.1/docs/http/http-metrics.md#metric-httpserverrequestduration)

### HTTP server duration metric

Metric changes:

- **Name**: `http.server.duration` &rarr; `http.server.request.duration`
- **Unit**: `ms` &rarr; `s`
- **Description**: `Measures the duration of inbound HTTP requests.` &rarr;
  `Duration of HTTP server requests.`
- **Histogram buckets**: boundaries updated to reflect change from milliseconds
  to seconds, and zero bucket boundary removed
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change | Comments |
| --- | --- |
| `http.route` | No change |
| `http.method` → `http.request.method` | Now captures only 9 common HTTP methods by default plus `_OTHER` |
| `http.status_code` → `http.response.status_code` | |
| `http.scheme` → `url.scheme` | Now factors in [`X-Forwarded-Proto` span][X-Forwarded-Proto], [`Forwarded#proto` span][Forwarded#proto] headers |
| `net.protocol.name` → `network.protocol.name` | Recommended → Conditionally required if not `http` and `network.protocol.version` is set |
| `net.protocol.version` → `network.protocol.version` | Examples fixed: `2.0` → `2` and `3.0` → `3`; see note if [migrating from `<= v1.19.0`](#migrating-from--v1190) |
| `net.host.name` → `server.address` | &bullet; Recommended → Opt-In (due to high-cardinality vulnerability since based on HTTP headers)<br>&bullet; Now based only on [`Host` span][Host header], [`:authority` span][HTTP/2 authority], [`X-Forwarded-Host` span][X-Forwarded-Host], [`Forwarded#host` span][Forwarded#host] headers |
| `net.host.port` → `server.port` | &bullet; Recommended → Opt-In (due to high-cardinality vulnerability since based on HTTP headers)<br>&bullet; Now based only on [`Host` span][Host header], [`:authority` span][HTTP/2 authority], [`X-Forwarded-Host` span][X-Forwarded-Host], [`Forwarded#host` span][Forwarded#host] headers |
| New: `error.type` | |
<!-- prettier-ignore-end -->

References:

- [Metric `http.server.duration` v1.20.0](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/metrics/semantic_conventions/http-metrics.md#metric-httpserverduration)
- [Metric `http.server.request.duration` v1.23.1 (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.23.1/docs/http/http-metrics.md#metric-httpserverrequestduration)

## Migrating from a version prior to v1.20.0?

In addition to the changes made to the HTTP semantic conventions
from
[v1.20.0](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/trace/semantic_conventions/http.md)
to
[v1.23.1 (stable)](https://github.com/open-telemetry/semantic-conventions/blob/v1.23.1/README.md),
there are additional changes if you are migrating to v1.23.1 from a version prior to v1.20.0.

### Migrating from `<= v1.19.0`

- `http.flavor` &rarr; `network.protocol.version`
  - Examples fixed: `2.0` &rarr; `2` and `3.0` &rarr; `3`

### Migrating from `<= v1.18.0`

- `http.user_agent` &rarr; `user_agent.original`

### Migrating from `<= v1.17.0`

#### HTTP server span name

- When `http.route` is available:<br> `{http.route}` &rarr;
  `{summary} {http.route}`
- When `http.route` is not available:<br> `HTTP {http.method}` &rarr;
  `{summary}`

Where `{summary}` is `{http.method}`, unless `{http.method}` is `_OTHER`, in
which case `{summary}` is `HTTP`.

#### HTTP client span name

- `HTTP {http.method}` &rarr; `{summary}`

Where `{summary}` is `{http.method}`, unless `{http.method}` is `_OTHER`, in
which case `{summary}` is `HTTP`.

### Migrating from `<= v1.16.0`

This page does not cover these versions.

[Host header]: https://tools.ietf.org/html/rfc7230#section-5.4
[HTTP/2 authority]: https://tools.ietf.org/html/rfc9113#section-8.3.1
[Forwarded#for]: https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#for
[Forwarded#proto]: https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#proto
[Forwarded#host]: https://developer.mozilla.org/docs/Web/HTTP/Headers/Forwarded#host
[X-Forwarded-For]: https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-For
[X-Forwarded-Proto]: https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-Proto
[X-Forwarded-Host]: https://developer.mozilla.org/docs/Web/HTTP/Headers/X-Forwarded-Host
