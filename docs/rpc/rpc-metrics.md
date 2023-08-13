<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Metrics
--->

# Semantic Conventions for RPC Metrics

**Status**: [Experimental][DocumentStatus]

The conventions described in this section are RPC specific. When RPC operations
occur, measurements about those operations are recorded to instruments. The
measurements are aggregated and exported as metrics, which provide insight into
those operations. By including RPC properties as attributes on measurements, the
metrics can be filtered for finer grain analysis.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Metric instruments](#metric-instruments)
  * [RPC Server](#rpc-server)
    + [Metric: `rpc.server.duration`](#metric-rpcserverduration)
    + [Metric: `rpc.server.request.size`](#metric-rpcserverrequestsize)
    + [Metric: `rpc.server.response.size`](#metric-rpcserverresponsesize)
    + [Metric: `rpc.server.requests_per_rpc`](#metric-rpcserverrequests_per_rpc)
    + [Metric: `rpc.server.responses_per_rpc`](#metric-rpcserverresponses_per_rpc)
  * [RPC Client](#rpc-client)
    + [Metric: `rpc.client.duration`](#metric-rpcclientduration)
    + [Metric: `rpc.client.request.size`](#metric-rpcclientrequestsize)
    + [Metric: `rpc.client.response.size`](#metric-rpcclientresponsesize)
    + [Metric: `rpc.client.requests_per_rpc`](#metric-rpcclientrequests_per_rpc)
    + [Metric: `rpc.client.responses_per_rpc`](#metric-rpcclientresponses_per_rpc)
- [Attributes](#attributes)
  * [Service name](#service-name)
- [Semantic Conventions for specific RPC technologies](#semantic-conventions-for-specific-rpc-technologies)

<!-- tocstop -->

> **Warning**
> Existing RPC instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/metrics/semantic_conventions/rpc-metrics.md)
> (or prior):
>
> * SHOULD NOT change the version of the networking attributes that they emit
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking attributes which are also used
>   in RPC instrumentations).
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The only values defined so far are:
>   * `http` - emit the new, stable networking attributes,
>     and stop emitting the old experimental networking attributes
>     that the instrumentation emitted previously.
>   * `http/dup` - emit both the old and the stable networking attributes,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental networking attributes
>     the instrumentation was emitting previously.
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of attributes.
> * SHOULD drop the environment variable in the next major version (stable
>   next major version SHOULD NOT be released prior to October 1, 2023).

## Metric instruments

The following metric instruments MUST be used to describe RPC operations. They
MUST be of the specified type and units.

*Note: RPC server and client metrics are split to allow correlation across client/server boundaries, e.g. Lining up an RPC method latency to determine if the server is responsible for latency the client is seeing.*

### RPC Server

Below is a list of RPC server metric instruments.

#### Metric: `rpc.server.duration`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.duration` | Histogram | `ms` | Measures the duration of inbound RPC. **Streaming**: N/A. [1] |

**[1]:** While streaming RPCs may record this metric as start-of-batch
to end-of-batch, it's hard to interpret in practice.
<!-- endsemconv -->

#### Metric: `rpc.server.request.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.request.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.request.size` | Histogram | `By` | Measures the size of RPC request messages (uncompressed). **Streaming**: Recorded per message in a streaming batch |
<!-- endsemconv -->

#### Metric: `rpc.server.response.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.response.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.response.size` | Histogram | `By` | Measures the size of RPC response messages (uncompressed). **Streaming**: Recorded per response in a streaming batch |
<!-- endsemconv -->

#### Metric: `rpc.server.requests_per_rpc`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.requests_per_rpc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.requests_per_rpc` | Histogram | `{count}` | Measures the number of messages received per RPC. Should be 1 for all non-streaming RPCs. **Streaming**: This metric is required for server and client streaming RPCs |
<!-- endsemconv -->

#### Metric: `rpc.server.responses_per_rpc`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.responses_per_rpc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.responses_per_rpc` | Histogram | `{count}` | Measures the number of messages sent per RPC. Should be 1 for all non-streaming RPCs. **Streaming**: This metric is required for server and client streaming RPCs |
<!-- endsemconv -->

### RPC Client

Below is a list of RPC client metric instruments.
These apply to traditional RPC usage, not streaming RPCs.

#### Metric: `rpc.client.duration`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.duration` | Histogram | `ms` | Measures the duration of outbound RPC **Streaming**: N/A. [1] |

**[1]:** While streaming RPCs may record this metric as start-of-batch
to end-of-batch, it's hard to interpret in practice.
<!-- endsemconv -->

#### Metric: `rpc.client.request.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.request.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.request.size` | Histogram | `By` | Measures the size of RPC request messages (uncompressed). **Streaming**: Recorded per message in a streaming batch |
<!-- endsemconv -->

#### Metric: `rpc.client.response.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.response.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.response.size` | Histogram | `By` | Measures the size of RPC response messages (uncompressed). **Streaming**: Recorded per response in a streaming batch |
<!-- endsemconv -->

#### Metric: `rpc.client.requests_per_rpc`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.requests_per_rpc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.requests_per_rpc` | Histogram | `{count}` | Measures the number of messages received per RPC. Should be 1 for all non-streaming RPCs. **Streaming**: This metric is required for server and client streaming RPCs |
<!-- endsemconv -->

#### Metric: `rpc.client.responses_per_rpc`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.responses_per_rpc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.responses_per_rpc` | Histogram | `{count}` | Measures the number of messages sent per RPC. Should be 1 for all non-streaming RPCs. **Streaming**: This metric is required for server and client streaming RPCs |
<!-- endsemconv -->

## Attributes

Below is a table of attributes that SHOULD be included on client and server RPC
measurements.

<!-- semconv rpc -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`rpc.system`](rpc-spans.md) | string | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc` | Required |
| [`rpc.service`](rpc-spans.md) | string | The full (logical) name of the service being called, including its package name, if applicable. [1] | `myservice.EchoService` | Recommended |
| [`rpc.method`](rpc-spans.md) | string | The name of the (logical) method being called, must be equal to the $method part in the span name. [2] | `exampleMethod` | Recommended |
| [`network.transport`](../general/attributes.md) | string | [OSI Transport Layer](https://osi-model.com/transport-layer/) or [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication). The value SHOULD be normalized to lowercase. | `tcp`; `udp` | Recommended |
| [`network.type`](../general/attributes.md) | string | [OSI Network Layer](https://osi-model.com/network-layer/) or non-OSI equivalent. The value SHOULD be normalized to lowercase. | `ipv4`; `ipv6` | Recommended |
| [`server.address`](../general/attributes.md) | string | RPC server [host name](https://grpc.github.io/grpc/core/md_doc_naming.html). [3] | `example.com` | Required |
| [`server.port`](../general/attributes.md) | int | Logical server port number | `80`; `8080`; `443` | Conditionally Required: See below |
| [`server.socket.address`](../general/attributes.md) | string | Physical server IP address or Unix socket address. If set from the client, should simply use the socket's peer address, and not attempt to find any actual server IP (i.e., if set from client, this may represent some proxy server instead of the logical server). | `10.5.3.2` | See below |
| [`server.socket.port`](../general/attributes.md) | int | Physical server port. | `16456` | Recommended: [4] |

**[1]:** This is the logical name of the service from the RPC interface perspective, which can be different from the name of any implementing class. The `code.namespace` attribute may be used to store the latter (despite the attribute name, it may include a class name; e.g., class with method actually executing the call on the server side, RPC client stub class on the client side).

**[2]:** This is the logical name of the method from the RPC interface perspective, which can be different from the name of any implementing method/function. The `code.function` attribute may be used to store the latter (e.g., method actually executing the call on the server side, RPC client stub method on the client side).

**[3]:** May contain server IP address, DNS name, or local socket name. When host component is an IP address, instrumentations SHOULD NOT do a reverse proxy lookup to obtain DNS name and SHOULD set `server.address` to the IP address provided in the host component.

**[4]:** If different than `server.port` and if `server.socket.address` is set.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* [`server.socket.address`](../general/attributes.md)
* [`server.address`](../general/attributes.md)

`rpc.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `grpc` | gRPC |
| `java_rmi` | Java RMI |
| `dotnet_wcf` | .NET WCF |
| `apache_dubbo` | Apache Dubbo |
| `connect_rpc` | Connect RPC |
<!-- endsemconv -->

To avoid high cardinality, implementations should prefer the most stable of `server.address` or
`server.socket.address`, depending on expected deployment profile.  For many cloud applications, this is likely
`server.address` as names can be recycled even across re-instantiation of a server with a different `ip`.

For client-side metrics `server.port` is required if the connection is IP-based and the port is available (it describes the server port they are connecting to).
For server-side spans `server.port` is optional (it describes the port the client is connecting from).

### Service name

On the server process receiving and handling the remote procedure call, the service name provided in `rpc.service` does not necessarily have to match the [`service.name`][] resource attribute.
One process can expose multiple RPC endpoints and thus have multiple RPC service names. From a deployment perspective, as expressed by the `service.*` resource attributes, it will be treated as one deployed service with one `service.name`.

[`service.name`]: /docs/resource/README.md#service

## Semantic Conventions for specific RPC technologies

More specific Semantic Conventions are defined for the following RPC technologies:

* [Connect](connect-rpc.md): Semantic Conventions for *Connect RPC*.
* [gRPC](grpc.md): Semantic Conventions for *gRPC*.
* [JSON-RPC](json-rpc.md): Semantic Conventions for *JSON-RPC*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.22.0/specification/document-status.md
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.22.0/specification/metrics/metric-requirement-level.md#recommended
