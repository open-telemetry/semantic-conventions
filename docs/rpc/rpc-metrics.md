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
  - [RPC Server](#rpc-server)
    - [Metric: `rpc.server.duration`](#metric-rpcserverduration)
    - [Metric: `rpc.server.request.size`](#metric-rpcserverrequestsize)
    - [Metric: `rpc.server.response.size`](#metric-rpcserverresponsesize)
    - [Metric: `rpc.server.requests_per_rpc`](#metric-rpcserverrequests_per_rpc)
    - [Metric: `rpc.server.responses_per_rpc`](#metric-rpcserverresponses_per_rpc)
  - [RPC Client](#rpc-client)
    - [Metric: `rpc.client.duration`](#metric-rpcclientduration)
    - [Metric: `rpc.client.request.size`](#metric-rpcclientrequestsize)
    - [Metric: `rpc.client.response.size`](#metric-rpcclientresponsesize)
    - [Metric: `rpc.client.requests_per_rpc`](#metric-rpcclientrequests_per_rpc)
    - [Metric: `rpc.client.responses_per_rpc`](#metric-rpcclientresponses_per_rpc)
- [Attributes](#attributes)
  - [Service name](#service-name)
- [Semantic Conventions for specific RPC technologies](#semantic-conventions-for-specific-rpc-technologies)

<!-- tocstop -->

> **Warning**
> Existing RPC instrumentations that are using
> [v1.20.0 of this document](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/specification/metrics/semantic_conventions/rpc-metrics.md)
> (or prior):
>
> * SHOULD NOT change the version of the networking conventions that they emit
>   until the HTTP semantic conventions are marked stable (HTTP stabilization will
>   include stabilization of a core set of networking conventions which are also used
>   in RPC instrumentations). Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The only values defined so far are:
>   * `http` - emit the new, stable networking conventions,
>     and stop emitting the old experimental networking conventions
>     that the instrumentation emitted previously.
>   * `http/dup` - emit both the old and the stable networking conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental networking conventions
>     the instrumentation was emitting previously.
>   * Note: `http/dup` has higher precedence than `http` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version.

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
| `rpc.server.duration` | Histogram | `ms` | Measures the duration of inbound RPC. [1] |

**[1]:** While streaming RPCs may record this metric as start-of-batch
to end-of-batch, it's hard to interpret in practice.

**Streaming**: N/A.
<!-- endsemconv -->

#### Metric: `rpc.server.request.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.request.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.request.size` | Histogram | `By` | Measures the size of RPC request messages (uncompressed). [1] |

**[1]:** **Streaming**: Recorded per message in a streaming batch
<!-- endsemconv -->

#### Metric: `rpc.server.response.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.response.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.response.size` | Histogram | `By` | Measures the size of RPC response messages (uncompressed). [1] |

**[1]:** **Streaming**: Recorded per response in a streaming batch
<!-- endsemconv -->

#### Metric: `rpc.server.requests_per_rpc`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.requests_per_rpc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.requests_per_rpc` | Histogram | `{count}` | Measures the number of messages received per RPC. [1] |

**[1]:** Should be 1 for all non-streaming RPCs.

**Streaming** : This metric is required for server and client streaming RPCs
<!-- endsemconv -->

#### Metric: `rpc.server.responses_per_rpc`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.server.responses_per_rpc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.server.responses_per_rpc` | Histogram | `{count}` | Measures the number of messages sent per RPC. [1] |

**[1]:** Should be 1 for all non-streaming RPCs.

**Streaming**: This metric is required for server and client streaming RPCs
<!-- endsemconv -->

### RPC Client

Below is a list of RPC client metric instruments.
These apply to traditional RPC usage, not streaming RPCs.

#### Metric: `rpc.client.duration`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.duration` | Histogram | `ms` | Measures the duration of outbound RPC. [1] |

**[1]:** While streaming RPCs may record this metric as start-of-batch
to end-of-batch, it's hard to interpret in practice.

**Streaming**: N/A.
<!-- endsemconv -->

#### Metric: `rpc.client.request.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.request.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.request.size` | Histogram | `By` | Measures the size of RPC request messages (uncompressed). [1] |

**[1]:** **Streaming**: Recorded per message in a streaming batch
<!-- endsemconv -->

#### Metric: `rpc.client.response.size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.response.size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.response.size` | Histogram | `By` | Measures the size of RPC response messages (uncompressed). [1] |

**[1]:** **Streaming**: Recorded per response in a streaming batch
<!-- endsemconv -->

#### Metric: `rpc.client.requests_per_rpc`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.requests_per_rpc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.requests_per_rpc` | Histogram | `{count}` | Measures the number of messages received per RPC. [1] |

**[1]:** Should be 1 for all non-streaming RPCs.

**Streaming**: This metric is required for server and client streaming RPCs
<!-- endsemconv -->

#### Metric: `rpc.client.responses_per_rpc`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.rpc.client.responses_per_rpc(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `rpc.client.responses_per_rpc` | Histogram | `{count}` | Measures the number of messages sent per RPC. [1] |

**[1]:** Should be 1 for all non-streaming RPCs.

**Streaming**: This metric is required for server and client streaming RPCs
<!-- endsemconv -->

## Attributes

Below is a table of attributes that SHOULD be included on client and server RPC
measurements.

<!-- semconv attributes.metrics.rpc(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`network.transport`](../attributes-registry/network.md) | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [1] | `tcp`; `udp` | Recommended |
| [`network.type`](../attributes-registry/network.md) | string | [OSI network layer](https://osi-model.com/network-layer/) or non-OSI equivalent. [2] | `ipv4`; `ipv6` | Recommended |
| [`rpc.method`](../attributes-registry/rpc.md) | string | The name of the (logical) method being called, must be equal to the $method part in the span name. [3] | `exampleMethod` | Recommended |
| [`rpc.service`](../attributes-registry/rpc.md) | string | The full (logical) name of the service being called, including its package name, if applicable. [4] | `myservice.EchoService` | Recommended |
| [`rpc.system`](../attributes-registry/rpc.md) | string | A string identifying the remoting system. See below for a list of well-known identifiers. | `grpc` | Required |
| [`server.address`](../attributes-registry/server.md) | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [5] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | Recommended |
| [`server.port`](../attributes-registry/server.md) | int | Server port number. [6] | `80`; `8080`; `443` | Recommended |

**[1]:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[2]:** The value SHOULD be normalized to lowercase.

**[3]:** This is the logical name of the method from the RPC interface perspective, which can be different from the name of any implementing method/function. The `code.function` attribute may be used to store the latter (e.g., method actually executing the call on the server side, RPC client stub method on the client side).

**[4]:** This is the logical name of the service from the RPC interface perspective, which can be different from the name of any implementing class. The `code.namespace` attribute may be used to store the latter (despite the attribute name, it may include a class name; e.g., class with method actually executing the call on the server side, RPC client stub class on the client side).

**[5]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[6]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `tcp` | TCP |
| `udp` | UDP |
| `pipe` | Named or anonymous pipe. |
| `unix` | Unix domain socket |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ipv4` | IPv4 |
| `ipv6` | IPv6 |

`rpc.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `grpc` | gRPC |
| `java_rmi` | Java RMI |
| `dotnet_wcf` | .NET WCF |
| `apache_dubbo` | Apache Dubbo |
| `connect_rpc` | Connect RPC |
<!-- endsemconv -->

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

Specifications defined by maintainers of RPC systems:

* [gRPC](https://github.com/grpc/proposal/blob/master/A66-otel-stats.md): Semantic Conventions for *gRPC*.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
