<!--- Hugo front matter used to generate the website version of this page:
linkTitle: RPC migration
--->

# RPC semantic convention stability migration guide

> [!WARNING]
> This document is a work in progress as the RPC semantic conventions
> have not been marked stable yet and changes are still being made.

Due to the significant number of modifications and the extensive user base
affected by them, existing RPC instrumentations published by
OpenTelemetry are required to implement a migration plan that will assist users in
transitioning to the stable RPC semantic conventions.

Specifically, when existing RPC instrumentations published by OpenTelemetry are
updated to the stable RPC semantic conventions, they:

- SHOULD NOT change the version of the RPC conventions that they emit by
  default in their existing major version. Conventions include (but are not
  limited to) attributes, metric and span names, and unit of measure.
- SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
  in their existing major version as a comma-separated list of category-specific
  values. The list of values includes:
  - `rpc` - emit the stable RPC conventions, and stop emitting
    the experimental RPC conventions that the instrumentation emitted
    previously.
  - `rpc/dup` - emit both the experimental and stable RPC conventions,
    allowing for a phased rollout of the stable semantic conventions.
  - The default behavior (in the absence of one of these values) is to continue
    emitting whatever version of the old experimental RPC conventions the
    instrumentation was emitting previously.
  - `rpc/dup` has higher precedence than `rpc` in case both values are present.
- SHOULD maintain (security patching at a minimum) their existing major version
  for at least six months after it starts emitting both sets of conventions.
- MAY drop the environment variable in their next major version and emit only
  the stable RPC conventions.

> [!NOTE]
> `OTEL_SEMCONV_STABILITY_OPT_IN` is only intended to be used when migrating
> from an experimental semantic convention to its initial stable version.

## Summary of changes

This section summarizes the changes made to the RPC semantic conventions
from
[v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/README.md)
to
TODO (latest).

### RPC span attributes

<!-- disable markdownlint requirement for tables to be aligned -->
<!-- markdownlint-disable-file MD060 -->
<!-- prettier-ignore-start -->
| Change                                                         | PR                                                                                                                                                   | Comments                                                                                                                          |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name`                          | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176), [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203) | See [below](#rpcsystemname-values) for changes to the values, also now marked as sampling-relevant                                |
| `rpc.method`                                                   | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223), [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203) | Now the fully-qualified logical name of the method from the RPC interface perspective, also now marked as sampling-relevant. See [method and span name changes](#rpc-methods-and-span-names). |
| `rpc.service`                                                  | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)                                                                            | Deprecated, use fully-qualified `rpc.method` instead. |
| `network.transport`                                            | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350)                                                                            | Removed                                                                                                                           |
| `network.type`                                                 | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857)                                                                            | Removed                                                                                                                           |
| `rpc.grpc.status_code` &rarr; `rpc.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921)                                                                            | Changed from int to string (e.g., `0` &rarr; `"OK"`)                                                                              |
| `rpc.connect_rpc.error_code` &rarr; `rpc.status_code` | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921)                                                                            |                                                                                                                                   |
| `rpc.grpc.request.metadata.<key>`                              | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Replaced by `rpc.request.header.<key>`                                                                                            |
| `rpc.grpc.response.metadata.<key>`                             | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Split into `rpc.response.header.<key>` (sent before the response payload) and `rpc.response.trailer.<key>` (sent after it) |
| `rpc.connect_rpc.request.metadata.<key>`                       | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Replaced by `rpc.request.header.<key>`                                                                                            |
| `rpc.connect_rpc.response.metadata.<key>`                      | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Split into `rpc.response.header.<key>` (sent before the response payload) and `rpc.response.trailer.<key>` (sent after it) |
| `server.address`                                               | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203), [#3317](https://github.com/open-telemetry/semantic-conventions/pull/3317), [#3919](https://github.com/open-telemetry/semantic-conventions/pull/3919) | Now marked as sampling-relevant. For client spans, identifies a group of RPC server instances the request is sent to. May contain a DNS name, an endpoint and path in the service registry, local socket name or an IP address. See below for server spans. |
| `server.port`                                                  | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203), [#3317](https://github.com/open-telemetry/semantic-conventions/pull/3317), [#3919](https://github.com/open-telemetry/semantic-conventions/pull/3919) | Now marked as sampling-relevant. See below for server spans. |
| New: `error.type`                                              | [#2852](https://github.com/open-telemetry/semantic-conventions/pull/2852)                                                                            |                                                                                                                                   |
| New: `rpc.method_original`                                     | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)                                                                            | The original name of the method used by the client. See [method and span name changes](#rpc-methods-and-span-names). |
| `client.address`                                               | [#3488](https://github.com/open-telemetry/semantic-conventions/pull/3488)                                                                            | Removed                                                                                                                           |
| `client.port`                                                  | [#3488](https://github.com/open-telemetry/semantic-conventions/pull/3488)                                                                            | Removed                                                                                                                           |

<!-- prettier-ignore-end -->

For server spans, `server.address` and `server.port` describe the address the
client used to reach this server, as reported by the transport or RPC
framework. Instrumentations SHOULD NOT use actual network-level
connection information to populate these attributes. If the address
used by the client is unavailable, instrumentations SHOULD NOT set
these attributes. See
[RPC system-specific changes](#rpc-system-specific-changes) for address and
port sourcing details.

References:

- [RPC spans v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-spans.md)
- [RPC spans (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md)

### RPC methods and span names

`rpc.method` is now the fully-qualified logical name of the method from the RPC
interface perspective, rather than containing only the method name.
Instrumentations for frameworks or libraries with a fixed set of recognized
methods MUST set this attribute to the original method name only when the
method is recognized by the framework or library.

When the method is not recognized, or when instrumentation is not able to
reliably detect if the method is predefined, the attribute MUST be set to
`_OTHER`. If the RPC instrumentation could end up converting valid RPC methods
to `_OTHER`, then it SHOULD provide a way to configure the list of recognized
RPC methods. These rules apply to spans and metrics.

On spans, `rpc.method_original` is Conditionally Required if and only if it's
different than `rpc.method`.

In v1.37.0, the span name MUST be the full RPC method name. The current
[span naming rules](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md#name)
state that the span name SHOULD be `{rpc.method}` if it is available and not
set to `_OTHER`. If `rpc.method` is unavailable or set to `_OTHER`, the span
name SHOULD be `{rpc.system.name}`. Semantic conventions for individual RPC
systems MAY specify different span name format
([#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)).

JSON-RPC overrides the common method guidance, as described
[below](#json-rpc).

### `rpc.system.name` values

<!-- prettier-ignore-start -->
| Change                            | PR                                                                        | Comments                                         |
| --------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------ |
| `apache_dubbo` &rarr; `dubbo`     | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) |                                                  |
| `connect_rpc` &rarr; `connectrpc` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) |                                                  |
| `java_rmi`                        | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | Removed, but can still be used as a custom value |
| `dotnet_wcf`                      | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | Removed, but can still be used as a custom value |
<!-- prettier-ignore-end -->

References:

- [RPC spans v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-spans.md)
- [RPC spans (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md)

### RPC server call duration metric

Metric changes:

- **Name**: `rpc.server.duration` &rarr; `rpc.server.call.duration` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Unit**: `ms` &rarr; `s` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Description**: `Measures the duration of inbound RPC.` &rarr;
  `Measures the duration of an incoming Remote Procedure Call (RPC).` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961), [#3328](https://github.com/open-telemetry/semantic-conventions/pull/3328))
- **Histogram buckets**: Explicit histogram bucket boundaries are now recommended,
  in seconds, ranging from `0.0001` to `100`
  ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961), [#4185](https://github.com/open-telemetry/semantic-conventions/pull/4185)).
  See [general RPC boundaries](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-metrics.md#metric-rpcservercallduration).
  [gRPC uses a different set](#grpc).
- **Requirement level**: Remains recommended, as in v1.37.0. The intermediate
  change to required in [#3284](https://github.com/open-telemetry/semantic-conventions/pull/3284)
  was superseded by [#3810](https://github.com/open-telemetry/semantic-conventions/pull/3810).
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                      | PR                                                                        | Comments                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | See [above](#rpcsystemname-values) for changes to the values                                |
| `rpc.method`                          | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Now the fully-qualified logical name of the method from the RPC interface perspective. See [method and span name changes](#rpc-methods-and-span-names). |
| `rpc.service`                         | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Deprecated, use fully-qualified `rpc.method` instead. |
| `network.transport`                   | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350) | Removed                                                                                     |
| `network.type`                        | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857) | Removed                                                                                     |
| `server.address`                      | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) | Changed from Recommended to Opt-In                                                          |
| `server.port`                         | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) | Changed from Recommended to Opt-In                                                          |
| New: `rpc.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921) |                                                                                             |
| New: `error.type`                     | [#2852](https://github.com/open-telemetry/semantic-conventions/pull/2852) |                                                                                             |
<!-- prettier-ignore-end -->

References:

- [Metric `rpc.server.duration` v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-metrics.md#metric-rpcserverduration)
- [Metric `rpc.server.call.duration` (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-metrics.md#metric-rpcservercallduration)

### RPC client call duration metric

Metric changes:

- **Name**: `rpc.client.duration` &rarr; `rpc.client.call.duration` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Unit**: `ms` &rarr; `s` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Description**: `Measures the duration of outbound RPC.` &rarr;
  `Measures the duration of an outgoing Remote Procedure Call (RPC).` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961), [#3328](https://github.com/open-telemetry/semantic-conventions/pull/3328))
- **Histogram buckets**: Explicit histogram bucket boundaries are now recommended,
  in seconds, ranging from `0.0001` to `100`
  ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961), [#4185](https://github.com/open-telemetry/semantic-conventions/pull/4185)).
  See [general RPC boundaries](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-metrics.md#metric-rpcclientcallduration).
  [gRPC uses a different set](#grpc).
- **Requirement level**: Remains recommended, as in v1.37.0. The intermediate
  change to required in [#3284](https://github.com/open-telemetry/semantic-conventions/pull/3284)
  was superseded by [#3810](https://github.com/open-telemetry/semantic-conventions/pull/3810).
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                      | PR                                                                        | Comments                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | See [above](#rpcsystemname-values) for changes to the values                                |
| `rpc.method`                          | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Now the fully-qualified logical name of the method from the RPC interface perspective. See [method and span name changes](#rpc-methods-and-span-names). |
| `rpc.service`                         | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Deprecated, use fully-qualified `rpc.method` instead. |
| `network.transport`                   | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350) | Removed                                                                                     |
| `network.type`                        | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857) | Removed                                                                                     |
| `server.address`                      | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197), [#3257](https://github.com/open-telemetry/semantic-conventions/pull/3257) | Changed from Recommended to Conditionally Required if available. See [RPC system-specific changes](#rpc-system-specific-changes) for overrides. |
| `server.port`                         | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) | Changed from Recommended to Conditionally Required if applicable and `server.address` is set. See [RPC system-specific changes](#rpc-system-specific-changes) for target port availability rules. |
| New: `rpc.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921) |                                                                                             |
| New: `error.type`                     | [#2852](https://github.com/open-telemetry/semantic-conventions/pull/2852) |                                                                                             |
<!-- prettier-ignore-end -->

References:

- [Metric `rpc.client.duration` v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-metrics.md#metric-rpcclientduration)
- [Metric `rpc.client.call.duration` (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-metrics.md#metric-rpcclientcallduration)

### RPC exception events

New [`rpc.client.call.exception` and `rpc.server.call.exception` log-based events](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-exceptions.md)
represent exceptions that occurred during an outgoing RPC call or incoming RPC
call processing, respectively
([#3426](https://github.com/open-telemetry/semantic-conventions/pull/3426)).

### Deprecated events

The `rpc.message` event and its associated attributes have been deprecated with no replacement at this time:

<!-- prettier-ignore-start -->
| Deprecated Event/Attribute     | PR                                                                        |
| ------------------------------ | ------------------------------------------------------------------------- |
| `rpc.message` event            | [#3283](https://github.com/open-telemetry/semantic-conventions/pull/3283) |
| `rpc.message.type`             | [#3283](https://github.com/open-telemetry/semantic-conventions/pull/3283) |
| `rpc.message.id`               | [#3283](https://github.com/open-telemetry/semantic-conventions/pull/3283) |
| `rpc.message.compressed_size`  | [#3283](https://github.com/open-telemetry/semantic-conventions/pull/3283) |
| `rpc.message.uncompressed_size`| [#3283](https://github.com/open-telemetry/semantic-conventions/pull/3283) |
<!-- prettier-ignore-end -->

### Deprecated metrics

The following metrics have been deprecated with no replacement at this time:

<!-- prettier-ignore-start -->
| Deprecated Metric              | PR                                                                        |
| ------------------------------ | ------------------------------------------------------------------------- |
| `rpc.server.requests_per_rpc`  | [#2846](https://github.com/open-telemetry/semantic-conventions/pull/2846) |
| `rpc.server.responses_per_rpc` | [#2846](https://github.com/open-telemetry/semantic-conventions/pull/2846) |
| `rpc.client.requests_per_rpc`  | [#2846](https://github.com/open-telemetry/semantic-conventions/pull/2846) |
| `rpc.client.responses_per_rpc` | [#2846](https://github.com/open-telemetry/semantic-conventions/pull/2846) |
| `rpc.server.request.size`      | [#3267](https://github.com/open-telemetry/semantic-conventions/pull/3267) |
| `rpc.server.response.size`     | [#3267](https://github.com/open-telemetry/semantic-conventions/pull/3267) |
| `rpc.client.request.size`      | [#3267](https://github.com/open-telemetry/semantic-conventions/pull/3267) |
| `rpc.client.response.size`     | [#3267](https://github.com/open-telemetry/semantic-conventions/pull/3267) |
<!-- prettier-ignore-end -->

### RPC system-specific changes

#### gRPC

For client spans and `rpc.client.call.duration`, `server.address` is Required.
Instrumentations SHOULD populate `server.address` (along with `server.port`)
based on the configuration used when creating the gRPC channel and
SHOULD NOT use actual network-level connection information for this purpose
to ensure low cardinality.
See [gRPC client conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/grpc.md#client)
for target-string parsing and fallback rules.

For server spans, instrumentations SHOULD populate `server.address` from the
host component of the HTTP/2 `:authority` pseudo-header the client used to
reach this server. Instrumentations SHOULD populate `server.port` from the
port component of the HTTP/2 `:authority` pseudo-header the client used to
reach this server. `server.port` is
Conditionally Required if `server.address` is set and a port is present in
`:authority`.

Both client and server call-duration metrics SHOULD be specified with the
[gRPC-specific `ExplicitBucketBoundaries`](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/grpc.md#metrics)
in seconds, instead of the general RPC bucket boundaries.
The call-duration bucket recommendations match those used by gRPC's existing
OpenTelemetry metrics. The boundaries include `0` and finer-grained values from
`0.00001` to `100` seconds
([#4185](https://github.com/open-telemetry/semantic-conventions/pull/4185)).

References:

- [gRPC v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/grpc.md)
- [gRPC (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/grpc.md)

#### Apache Dubbo

For client spans and `rpc.client.call.duration`, `server.address` is
Conditionally Required if available.
Instrumentations SHOULD populate `server.address` (and `server.port`, when applicable)
based on the configuration used when creating the Dubbo client and
SHOULD NOT use actual network-level connection information for this purpose
to ensure low cardinality.

For direct connection, when the consumer is configured with an explicit
provider target URL, instrumentations SHOULD parse `server.address` and
`server.port` from that URL. `server.port` is Conditionally Required
if `server.address` is set and a port is specified in that URL.

For service discovery through a registry, instrumentations SHOULD set
`server.address` to the service-discovery target and SHOULD NOT set
`server.port`. The `{registry-port}` component is part of the registry endpoint
in the service-discovery target and SHOULD NOT be recorded as `server.port`.
See [Dubbo client conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/dubbo.md#client)
for the target format and examples
([#4120](https://github.com/open-telemetry/semantic-conventions/pull/4120)).

References:

- [Apache Dubbo (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/dubbo.md)

#### JSON-RPC

JSON-RPC conventions remain in development. The system identifier `jsonrpc`
is unchanged from v1.37.0, but the attribute names and error reporting have
changed.

<!-- prettier-ignore-start -->
| Attribute change | PR | Comments |
| ---------------- | --- | -------- |
| `rpc.jsonrpc.version` &rarr; `jsonrpc.protocol.version` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | Still Conditionally Required if other than the default version (`1.0`) |
| `rpc.jsonrpc.request_id` &rarr; `jsonrpc.request.id` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | Still Recommended. Previously, a `null` ID was recorded as an empty string. Instrumentations SHOULD NOT capture this attribute when the `id` is `null` or omitted. |
| `rpc.jsonrpc.error_code` &rarr; `rpc.status_code` | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921) | Changed from int to string (e.g., `-32602` &rarr; `"-32602"`) |
| `rpc.jsonrpc.error_message` | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3308](https://github.com/open-telemetry/semantic-conventions/pull/3308) | Deprecated, use the span status description when reporting JSON-RPC spans. |
| `rpc.method` | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Changed from Required to Opt-In on JSON-RPC spans |
<!-- prettier-ignore-end -->

JSON-RPC supports sending and receiving arbitrary method names without prior
registration or definition. General-purpose JSON-RPC instrumentations therefore
SHOULD NOT set `rpc.method` by default and SHOULD provide a way to configure
the list of recognized RPC methods. When tracing instrumentation converts
RPC method to `_OTHER`, it MUST also set `rpc.method_original` span attribute
to the original value.

References:

- [JSON-RPC v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/json-rpc.md)
- [JSON-RPC (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/json-rpc.md)
