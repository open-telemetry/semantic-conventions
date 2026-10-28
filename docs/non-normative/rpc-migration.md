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

The following recommendations summarize the migration guidance in
[Semantic conventions for RPC](../rpc/README.md).
When existing RPC instrumentations published by OpenTelemetry are
updated to the stable RPC semantic conventions, they:

- SHOULD NOT change the version of the RPC conventions that they emit by
  default in their existing major version. Conventions include (but are not
  limited to) attributes, metric and span names, span kind, and unit of measure.
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
  - `rpc/dup` takes precedence over `rpc` if both values are present.
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

### Common RPC attribute changes

The following changes apply to RPC spans and call duration metrics:

<!-- disable markdownlint requirement for tables to be aligned -->
<!-- markdownlint-disable-file MD060 -->
<!-- prettier-ignore-start -->
| Change                                                         | PR                                                                                                                                                   | Comments                                                                                                                          |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name`                          | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | See [below](#rpcsystemname-values) for changes to the values |
| `rpc.method`                                                   | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Now the fully-qualified logical name of the method from the RPC interface perspective. See [method and span name changes](#rpc-methods-and-span-names). |
| `rpc.service`                                                  | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)                                                                            | Deprecated, use fully-qualified `rpc.method` instead. |
| `network.transport`                                            | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350)                                                                            | Removed                                                                                                                           |
| `network.type`                                                 | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857)                                                                            | Removed                                                                                                                           |
| New: `error.type`                                              | [#2852](https://github.com/open-telemetry/semantic-conventions/pull/2852)                                                                            |                                                                                                                                   |
<!-- prettier-ignore-end -->

### RPC span attributes

In addition to the [common attribute changes](#common-rpc-attribute-changes):

<!-- prettier-ignore-start -->
| Change | PR | Comments |
| --- | --- | --- |
| `rpc.system.name`, `rpc.method` | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203) | Now marked as sampling-relevant |
| `rpc.grpc.status_code` &rarr; `rpc.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921)                                                                            | Changed from int to string (e.g., `0` &rarr; `"OK"`)                                                                              |
| `rpc.connect_rpc.error_code` &rarr; `rpc.status_code` | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921)                                                                            |                                                                                                                                   |
| `rpc.grpc.request.metadata.<key>`                              | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Replaced by `rpc.request.header.<key>`                                                                                            |
| `rpc.grpc.response.metadata.<key>`                             | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Split into `rpc.response.header.<key>` (sent before the response payload) and `rpc.response.trailer.<key>` (sent after it) |
| `rpc.connect_rpc.request.metadata.<key>`                       | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Replaced by `rpc.request.header.<key>`                                                                                            |
| `rpc.connect_rpc.response.metadata.<key>`                      | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Split into `rpc.response.header.<key>` (sent before the response payload) and `rpc.response.trailer.<key>` (sent after it) |
| `server.address`                                               | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203), [#3317](https://github.com/open-telemetry/semantic-conventions/pull/3317), [#3257](https://github.com/open-telemetry/semantic-conventions/pull/3257), [#3919](https://github.com/open-telemetry/semantic-conventions/pull/3919) | Now sampling-relevant. Required &rarr; Conditionally Required if available on client spans; Required &rarr; Recommended when available on server spans. |
| `server.port`                                                  | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203), [#3317](https://github.com/open-telemetry/semantic-conventions/pull/3317), [#3919](https://github.com/open-telemetry/semantic-conventions/pull/3919) | Now sampling-relevant. Still Conditionally Required, but the condition changed from the transport supporting ports to the port being applicable and `server.address` being set. |
| New: `rpc.method_original`                                     | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)                                                                            | The original name of the method used by the client. See [method and span name changes](#rpc-methods-and-span-names). |
| `client.address`                                               | [#3488](https://github.com/open-telemetry/semantic-conventions/pull/3488)                                                                            | Removed                                                                                                                           |
| `client.port`                                                  | [#3488](https://github.com/open-telemetry/semantic-conventions/pull/3488)                                                                            | Removed                                                                                                                           |

<!-- prettier-ignore-end -->

For client spans, `server.address` identifies a group of RPC server instances.
It may contain a DNS name, a service-registry target, a local socket name, or an
IP address.

For server spans, `server.address` and `server.port` describe the address the
client used to reach this server, as reported by the transport or RPC
framework. Instrumentations SHOULD NOT use actual network-level
connection information to populate these attributes. If the address
used by the client is unavailable, instrumentations SHOULD NOT set
these attributes.

Individual RPC systems can override the general requirement levels in the
table. See [RPC system-specific changes](#rpc-system-specific-changes) for
overrides and address sourcing.

References:

- [RPC spans v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-spans.md)
- [RPC spans (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md)

### RPC methods and span names

On spans and metrics, methods that are unrecognized or
cannot reliably be identified as predefined MUST be recorded as `_OTHER`.
Instrumentations SHOULD support configuring recognized methods if valid
methods could otherwise become `_OTHER`. See the
[method cardinality rules](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md#rpc-client-span).

On spans, `rpc.method_original` is Conditionally Required if and only if it's
different than `rpc.method`.

In v1.37.0, the span name MUST be the full RPC method name. It now SHOULD be
`{rpc.method}`, falling back to `{rpc.system.name}` when the method is unavailable
or `_OTHER`. Individual RPC systems MAY override these
[span naming rules](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md#name)
([#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)).

JSON-RPC overrides the common method guidance for spans, as described
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

### RPC call duration metrics

Both duration metrics were renamed in
[#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961):

| v1.37.0 | TODO (latest) |
| --- | --- |
| `rpc.server.duration` | `rpc.server.call.duration` |
| `rpc.client.duration` | `rpc.client.call.duration` |

Shared changes:

- **Unit**: `ms` &rarr; `s` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961)).
- **Descriptions**: Now `Measures the duration of an incoming Remote Procedure Call (RPC).`
  for the server metric and `Measures the duration of an outgoing Remote Procedure Call (RPC).`
  for the client metric ([#3328](https://github.com/open-telemetry/semantic-conventions/pull/3328)).
- **Histogram buckets**: Explicit boundaries are now recommended, in seconds,
  ranging from `0.0001` to `100`. See the
  [general RPC boundaries](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-metrics.md#metric-rpcservercallduration)
  ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961), [#4185](https://github.com/open-telemetry/semantic-conventions/pull/4185)).
  [gRPC uses a different set](#grpc).

Both metrics remain Recommended, as in v1.37.0.

In addition to the [common attribute changes](#common-rpc-attribute-changes),
both metrics add `rpc.status_code`
([#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921)).

Address attributes were Recommended on both metrics in v1.37.0:

<!-- prettier-ignore-start -->
| Attribute | Client metric requirement (TODO) | Server metric requirement (TODO) | PR |
| --- | --- | --- | --- |
| `server.address` | Conditionally Required if available | Opt-In | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197), [#3257](https://github.com/open-telemetry/semantic-conventions/pull/3257) |
| `server.port` | Conditionally Required if applicable and `server.address` is set | Opt-In | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) |
<!-- prettier-ignore-end -->

See [RPC system-specific changes](#rpc-system-specific-changes) for overrides
and target port availability rules.

References:

- [Metric `rpc.server.duration` v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-metrics.md#metric-rpcserverduration)
- [Metric `rpc.server.call.duration` (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-metrics.md#metric-rpcservercallduration)
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
Client address attributes SHOULD come from the
[configured channel target](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/grpc.md#client),
not the network connection. Server span address attributes SHOULD come from
[HTTP/2 `:authority`](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/grpc.md#server).

Both duration metrics SHOULD use the
[gRPC-specific bucket boundaries](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/grpc.md#metrics)
instead of the general RPC boundaries. These match gRPC's existing
OpenTelemetry metrics
([#4185](https://github.com/open-telemetry/semantic-conventions/pull/4185)).

References:

- [gRPC v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/grpc.md)
- [gRPC (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/grpc.md)

#### Apache Dubbo

Client address attributes SHOULD come from the configured Dubbo target, not the
network connection. For service discovery, `server.address` SHOULD contain the
discovery target and `server.port` SHOULD NOT be set, since the registry port is
not the RPC server port.

See [Dubbo client conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/dubbo.md#client)
for target parsing and port requirements
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

JSON-RPC allows arbitrary method names, so general-purpose tracing
instrumentations SHOULD NOT set `rpc.method` by default and SHOULD provide
a way to configure recognized methods.

References:

- [JSON-RPC v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/json-rpc.md)
- [JSON-RPC (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/json-rpc.md)
