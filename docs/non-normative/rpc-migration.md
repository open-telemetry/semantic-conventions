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

<!-- disable mdlint requirement for tables to be aligned -->
<!-- markdownlint-disable-file MD060 -->
<!-- prettier-ignore-start -->
| Change                                                         | PR                                                                                                                                                   | Comments                                                                                                                          |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name`                          | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176), [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203) | See [below](#rpcsystemname-values) for changes to the values, also now marked as sampling-relevant                                |
| `rpc.method`                                                   | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223), [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203) | Now contains fully-qualified method name (e.g., `com.example.ExampleService/exampleMethod`), also now marked as sampling-relevant |
| `rpc.service`                                                  | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)                                                                            | Removed, integrated into `rpc.method`                                                                                             |
| `network.transport`                                            | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350)                                                                            | Removed                                                                                                                           |
| `network.type`                                                 | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857)                                                                            | Removed                                                                                                                           |
| `rpc.grpc.status_code` &rarr; `rpc.response.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920)                                                                            | Changed from int to string (e.g., `0` &rarr; `"OK"`)                                                                              |
| `rpc.connect_rpc.error_code` &rarr; `rpc.response.status_code` | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920)                                                                            |                                                                                                                                   |
| `rpc.grpc.request.metadata.<key>`                              | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169)                                                                            | Replaced by `rpc.request.metadata.<key>`                                                                                          |
| `rpc.grpc.response.metadata.<key>`                             | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169)                                                                            | Replaced by `rpc.response.metadata.<key>`                                                                                         |
| `rpc.connect_rpc.request.metadata.<key>`                       | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169)                                                                            | Replaced by `rpc.request.metadata.<key>`                                                                                          |
| `rpc.connect_rpc.response.metadata.<key>`                      | [#3169](https://github.com/open-telemetry/semantic-conventions/pull/3169)                                                                            | Replaced by `rpc.response.metadata.<key>`                                                                                         |
| `server.address`                                               | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203), [#3317](https://github.com/open-telemetry/semantic-conventions/pull/3317) | Now marked as sampling-relevant;<br>Now it’s taken from static configuration and can be any string identifying a group of server instances.  |
| `server.port`                                                  | [#3203](https://github.com/open-telemetry/semantic-conventions/pull/3203), [#3317](https://github.com/open-telemetry/semantic-conventions/pull/3317) | Now marked as sampling-relevant;<br>>Now it’s taken from static configuration.  |
| New: `error.type`                                              | [#2852](https://github.com/open-telemetry/semantic-conventions/pull/2852)                                                                            |                                                                                                                                   |
| New: `rpc.method_original`                                     | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223)                                                                            | Original method name when `rpc.method` is set to `_OTHER`                                                                         |
<!-- prettier-ignore-end -->

References:

- [RPC spans v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-spans.md)
- [RPC spans (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md)

### `rpc.system.name` values

<!-- prettier-ignore-start -->
| Change                            | PR                                                                        | Comments                                         |
| --------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------ |
| `apache_dubbo` &rarr; `dubbo`     | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) |                                                  |
| `connect_rpc` &rarr; `connectrpc` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) |                                                  |
| `java_rmi`                        | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | Removed, but can still be used as a custom value |
| `dotnet_wcf`                      | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | Removed, but can still be used as a custom value |
| New: `jsonrpc`                    | [#2503](https://github.com/open-telemetry/semantic-conventions/pull/2503) |                                                  |
<!-- prettier-ignore-end -->

References:

- [RPC spans v1.37.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/rpc/rpc-spans.md)
- [RPC spans (TODO)](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/rpc/rpc-spans.md)

### RPC server call duration metric

Metric changes:

- **Name**: `rpc.server.duration` &rarr; `rpc.server.call.duration` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Unit**: `ms` &rarr; `s` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Description**: `Measures the duration of inbound RPC.` &rarr;
  `Measures the duration of inbound remote procedure calls (RPC).` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Histogram buckets**: boundaries updated to reflect change from milliseconds
  to seconds ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Requirement level**: Made required ([#3284](https://github.com/open-telemetry/semantic-conventions/pull/3284))
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                      | PR                                                                        | Comments                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | See [above](#rpcsystemname-values) for changes to the values                                |
| `rpc.method`                          | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Now contains fully-qualified method name (e.g., `com.example.ExampleService/exampleMethod`) |
| `rpc.service`                         | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Removed, integrated into `rpc.method`                                                       |
| `network.transport`                   | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350) | Removed                                                                                     |
| `network.type`                        | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857) | Removed                                                                                     |
| `server.address`                      | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) | Changed from Recommended to Opt-In                                                          |
| `server.port`                         | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) | Changed from Recommended to Opt-In                                                          |
| New: `rpc.response.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920) |                                                                                             |
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
  `Measures the duration of outbound remote procedure calls (RPC).` ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Histogram buckets**: boundaries updated to reflect change from milliseconds
  to seconds ([#2961](https://github.com/open-telemetry/semantic-conventions/pull/2961))
- **Requirement level**: Made required ([#3284](https://github.com/open-telemetry/semantic-conventions/pull/3284))
- **Attributes**: see table below

<!-- prettier-ignore-start -->
| Attribute change                      | PR                                                                        | Comments                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `rpc.system` &rarr; `rpc.system.name` | [#3176](https://github.com/open-telemetry/semantic-conventions/pull/3176) | See [above](#rpcsystemname-values) for changes to the values                                |
| `rpc.method`                          | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Now contains fully-qualified method name (e.g., `com.example.ExampleService/exampleMethod`) |
| `rpc.service`                         | [#3223](https://github.com/open-telemetry/semantic-conventions/pull/3223) | Removed, integrated into `rpc.method`                                                       |
| `network.transport`                   | [#3350](https://github.com/open-telemetry/semantic-conventions/pull/3350) | Removed                                                                                     |
| `network.type`                        | [#2857](https://github.com/open-telemetry/semantic-conventions/pull/2857) | Removed                                                                                     |
| `server.address`                      | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) | Changed from Recommended to Required                                                        |
| `server.port`                         | [#3197](https://github.com/open-telemetry/semantic-conventions/pull/3197) | Changed from Recommended to Conditionally Required                                          |
| New: `rpc.response.status_code`       | [#2920](https://github.com/open-telemetry/semantic-conventions/pull/2920) |                                                                                             |
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
