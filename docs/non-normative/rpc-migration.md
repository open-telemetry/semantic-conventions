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
- SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN` in
  their existing major version, which accepts:
  - `rpc` - emit the stable RPC conventions, and stop emitting
    the old RPC conventions that the instrumentation emitted previously.
  - `rpc/dup` - emit both the old and the stable RPC conventions,
    allowing for a phased rollout of the stable semantic conventions.
  - The default behavior (in the absence of one of these values) is to continue
    emitting whatever version of the old RPC conventions the
    instrumentation was emitting previously.
- Need to maintain (security patching at a minimum) their existing major version
  for at least six months after it starts emitting both sets of conventions.
- May drop the environment variable in their next major version and emit only
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
| `rpc.method`                                                   | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223), [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203) | Now contains fully-qualified method name (e.g., `com.example.ExampleService/exampleMethod`) or `_OTHER`, also now marked as sampling-relevant. See [method and span name changes](#rpc-methods-and-span-names). |
| `rpc.service`                                                  | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)                                                                            | Removed, integrated into `rpc.method`                                                                                             |
| `network.transport`                                            | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350)                                                                            | Removed                                                                                                                           |
| `network.type`                                                 | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857)                                                                            | Removed                                                                                                                           |
| `rpc.grpc.status_code` &rarr; `rpc.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921)                                                                            | Changed from int to string (e.g., `0` &rarr; `"OK"`)                                                                              |
| `rpc.connect_rpc.error_code` &rarr; `rpc.status_code` | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921)                                                                            |                                                                                                                                   |
| `rpc.grpc.request.metadata.<key>`                              | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Replaced by `rpc.request.header.<key>`                                                                                            |
| `rpc.grpc.response.metadata.<key>`                             | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Split into `rpc.response.header.<key>` (sent before the response payload) and `rpc.response.trailer.<key>` (sent after it) |
| `rpc.connect_rpc.request.metadata.<key>`                       | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Replaced by `rpc.request.header.<key>`                                                                                            |
| `rpc.connect_rpc.response.metadata.<key>`                      | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169), [#3924](https://github.com/open-telemetry/semantic-conventions/issues/3924) | Split into `rpc.response.header.<key>` (sent before the response payload) and `rpc.response.trailer.<key>` (sent after it) |
| `server.address`                                               | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203), [#3317](https://github.com/open-telemetry/semantic-conventions/pull/3317), [#3919](https://github.com/open-telemetry/semantic-conventions/pull/3919) | Now marked as sampling-relevant. For client spans, identifies a group of server instances according to framework-specific rules. For server spans, identifies the address the client used, as exposed by the transport or RPC framework, not the actual network connection. |
| `server.port`                                                  | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203), [#3317](https://github.com/open-telemetry/semantic-conventions/pull/3317), [#3919](https://github.com/open-telemetry/semantic-conventions/pull/3919) | Now marked as sampling-relevant. For client spans, identifies the server port according to framework-specific rules. For server spans, identifies the port the client used, as exposed by the transport or RPC framework, not the actual network connection. |
| New: `error.type`                                              | [#2852](https://github.com/open-telemetry/semantic-conventions/pull/2852)                                                                            |                                                                                                                                   |
| New: `rpc.method_original`                                     | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)                                                                            | Original method name, conditionally required if and only if it differs from `rpc.method`, including when `rpc.method` is `_OTHER` |
| `client.address`                                               | [#3488](https://github.com/open-telemetry/semantic-conventions/pull/3488)                                                                            | Removed                                                                                                                           |
| `client.port`                                                  | [#3488](https://github.com/open-telemetry/semantic-conventions/pull/3488)                                                                            | Removed                                                                                                                           |

<!-- prettier-ignore-end -->

For gRPC server spans, `server.address` and `server.port` come from the host
and port components of the HTTP/2 `:authority` pseudo-header. If the address
used by the client is unavailable, server instrumentations SHOULD NOT set
these attributes.

References:

- [RPC spans v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-spans.md)
- [RPC spans (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md)

### RPC methods and span names

`rpc.method` now includes the service name, where applicable, rather than
containing only the method name. For frameworks with a fixed set of recognized
methods, instrumentations MUST use `_OTHER` when the method is unrecognized or
when they cannot reliably determine whether it is predefined. Instrumentations
that could convert valid methods to `_OTHER` SHOULD support configuring the
list of recognized methods. These rules apply to spans and metrics.
On spans, `rpc.method_original` preserves the original method name when it
differs from `rpc.method`.

In v1.37.0, the span name MUST be the full RPC method name. The current
[span naming rules](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md#name)
instead say the name SHOULD be `{rpc.method}` when it is available and not
`_OTHER`. Otherwise, the name SHOULD be `{rpc.system.name}`. Individual RPC
systems MAY specify a different format
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

### JSON-RPC

JSON-RPC conventions remain in development. The system identifier `jsonrpc`
is unchanged from v1.37.0, but the attribute names and error reporting have
changed.

<!-- prettier-ignore-start -->
| Attribute change | PR | Comments |
| ---------------- | --- | -------- |
| `rpc.jsonrpc.version` &rarr; `jsonrpc.protocol.version` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | Still conditionally required if the version is not the default `1.0` |
| `rpc.jsonrpc.request_id` &rarr; `jsonrpc.request.id` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | Still recommended. Previously, a `null` ID was recorded as an empty string. Instrumentations now SHOULD NOT capture the attribute when the ID is `null` or omitted. |
| `rpc.jsonrpc.error_code` &rarr; `rpc.status_code` | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921) | Changed from int to string (e.g., `-32602` &rarr; `"-32602"`) |
| `rpc.jsonrpc.error_message` | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3308](https://github.com/open-telemetry/semantic-conventions/pull/3308) | Replaced by the span status description |
| `rpc.method` | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Changed from Required to Opt-In on JSON-RPC spans |
<!-- prettier-ignore-end -->

General-purpose JSON-RPC instrumentations SHOULD NOT set `rpc.method` by default
because JSON-RPC allows arbitrary method names. They SHOULD provide a way to
configure the list of recognized methods. When tracing instrumentation converts
a method to `_OTHER`, it MUST also record the original value in
`rpc.method_original`.

References:

- [JSON-RPC v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/json-rpc.md)
- [JSON-RPC (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/json-rpc.md)

### RPC server call duration metric

Metric changes:

- **Name**: `rpc.server.duration` &rarr; `rpc.server.call.duration` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Unit**: `ms` &rarr; `s` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Description**: `Measures the duration of inbound RPC.` &rarr;
  `Measures the duration of an incoming Remote Procedure Call (RPC).` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961), [#3328](https://github.com/open-telemetry/semantic-conventions/pull/3328))
- **Histogram buckets**: boundaries updated to reflect change from milliseconds
  to seconds ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961)).
  [General RPC boundaries](/docs/rpc/rpc-metrics.md#metric-rpcservercallduration)
  cover 0.1 ms to 100 s, with a [gRPC-specific recommendation](/docs/rpc/grpc.md#metrics)
  matching native gRPC latency boundaries ([#4185](https://github.com/open-telemetry/semantic-conventions/pull/4185)).
- **Requirement level**: Remains recommended, as in v1.37.0. The intermediate
  change to required in [#3284](https://github.com/open-telemetry/semantic-conventions/pull/3284)
  was superseded by [#3810](https://github.com/open-telemetry/semantic-conventions/pull/3810).
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                      | PR                                                                        | Comments                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | See [above](#rpcsystemname-values) for changes to the values                                |
| `rpc.method`                          | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Now contains fully-qualified method name (e.g., `com.example.ExampleService/exampleMethod`) or `_OTHER`. See [method and span name changes](#rpc-methods-and-span-names). |
| `rpc.service`                         | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Removed, integrated into `rpc.method`                                                       |
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
- **Histogram buckets**: boundaries updated to reflect change from milliseconds
  to seconds ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961)).
  [General RPC boundaries](/docs/rpc/rpc-metrics.md#metric-rpcclientcallduration)
  cover 0.1 ms to 100 s, with a [gRPC-specific recommendation](/docs/rpc/grpc.md#metrics)
  matching native gRPC latency boundaries.
- **Requirement level**: Remains recommended, as in v1.37.0. The intermediate
  change to required in [#3284](https://github.com/open-telemetry/semantic-conventions/pull/3284)
  was superseded by [#3810](https://github.com/open-telemetry/semantic-conventions/pull/3810).
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                      | PR                                                                        | Comments                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | See [above](#rpcsystemname-values) for changes to the values                                |
| `rpc.method`                          | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Now contains fully-qualified method name (e.g., `com.example.ExampleService/exampleMethod`) or `_OTHER`. See [method and span name changes](#rpc-methods-and-span-names). |
| `rpc.service`                         | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Removed, integrated into `rpc.method`                                                       |
| `network.transport`                   | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350) | Removed                                                                                     |
| `network.type`                        | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857) | Removed                                                                                     |
| `server.address`                      | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197), [#3257](https://github.com/open-telemetry/semantic-conventions/pull/3257) | Changed from Recommended to Conditionally Required if available in the common conventions and Dubbo. Required for gRPC. |
| `server.port`                         | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) | Changed from Recommended to Conditionally Required if applicable and `server.address` is set. See framework-specific rules for target port availability. |
| New: `rpc.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920), [#3921](https://github.com/open-telemetry/semantic-conventions/pull/3921) |                                                                                             |
| New: `error.type`                     | [#2852](https://github.com/open-telemetry/semantic-conventions/pull/2852) |                                                                                             |
<!-- prettier-ignore-end -->

References:

- [Metric `rpc.client.duration` v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-metrics.md#metric-rpcclientduration)
- [Metric `rpc.client.call.duration` (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-metrics.md#metric-rpcclientcallduration)

### RPC exception events

Exceptions that prevent the call from completing successfully are recorded as
[`rpc.client.call.exception` and `rpc.server.call.exception` log-based events](/docs/rpc/rpc-exceptions.md) ([#3426](https://github.com/open-telemetry/semantic-conventions/pull/3426)).

### Deprecated events

The `rpc.message` event and its associated attributes have been deprecated with no replacement:

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

The following metrics have been deprecated with no replacement:

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
