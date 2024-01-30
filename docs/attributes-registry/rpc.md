<!--- Hugo front matter used to generate the website version of this page:
--->

# RPC

## RPC Attributes

RPC attributes are intended to be used in the context of events related to remote procedure calls (RPC).

<!-- semconv registry.rpc(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `rpc.connect_rpc.error_code` | string | The [error codes](https://connect.build/docs/protocol/#error-codes) of the Connect request. Error codes are always string values. | `cancelled` |
| `rpc.connect_rpc.request.metadata.<key>` | string[] | Connect request metadata, `<key>` being the normalized Connect Metadata key (lowercase), the value being the metadata values. [1] | `rpc.request.metadata.my-custom-metadata-attribute=["1.2.3.4", "1.2.3.5"]` |
| `rpc.connect_rpc.response.metadata.<key>` | string[] | Connect response metadata, `<key>` being the normalized Connect Metadata key (lowercase), the value being the metadata values. [2] | `rpc.response.metadata.my-custom-metadata-attribute=["attribute_value"]` |
| `rpc.grpc.request.metadata.<key>` | string[] | gRPC request metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. [3] | `rpc.grpc.request.metadata.my-custom-metadata-attribute=["1.2.3.4", "1.2.3.5"]` |
| `rpc.grpc.response.metadata.<key>` | string[] | gRPC response metadata, `<key>` being the normalized gRPC Metadata key (lowercase), the value being the metadata values. [4] | `rpc.grpc.response.metadata.my-custom-metadata-attribute=["attribute_value"]` |
| `rpc.grpc.status_code` | int | The [numeric status code](https://github.com/grpc/grpc/blob/v1.33.2/doc/statuscodes.md) of the gRPC request. | `0` |
| `rpc.jsonrpc.error_code` | int | `error.code` property of response if it is an error response. | `-32700`; `100` |
| `rpc.jsonrpc.error_message` | string | `error.message` property of response if it is an error response. | `Parse error`; `User already exists` |
| `rpc.jsonrpc.request_id` | string | `id` property of request or response. Since protocol allows id to be int, string, `null` or missing (for notifications), value is expected to be cast to string for simplicity. Use empty string in case of `null` value. Omit entirely if this is a notification. | `10`; `request-7`; `` |
| `rpc.jsonrpc.version` | string | Protocol version as in `jsonrpc` property of request/response. Since JSON-RPC 1.0 doesn't specify this, the value can be omitted. | `2.0`; `1.0` |
| `rpc.method` | string | The name of the (logical) method being called, must be equal to the $method part in the span name. [5] | `exampleMethod` |
| `rpc.service` | string | The full (logical) name of the service being called, including its package name, if applicable. [6] | `myservice.EchoService` |
| `rpc.system` | string | A string identifying the remoting system. See below for a list of well-known identifiers. | `java_rmi` |

**[1]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all request metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

**[2]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all response metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

**[3]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all request metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

**[4]:** Instrumentations SHOULD require an explicit configuration of which metadata values are to be captured. Including all response metadata values can be a security risk - explicit configuration helps avoid leaking sensitive information.

**[5]:** This is the logical name of the method from the RPC interface perspective, which can be different from the name of any implementing method/function. The `code.function` attribute may be used to store the latter (e.g., method actually executing the call on the server side, RPC client stub method on the client side).

**[6]:** This is the logical name of the service from the RPC interface perspective, which can be different from the name of any implementing class. The `code.namespace` attribute may be used to store the latter (despite the attribute name, it may include a class name; e.g., class with method actually executing the call on the server side, RPC client stub class on the client side).

`rpc.connect_rpc.error_code` MUST be one of the following:

| Value  | Description |
|---|---|
| `cancelled` | cancelled |
| `unknown` | unknown |
| `invalid_argument` | invalid_argument |
| `deadline_exceeded` | deadline_exceeded |
| `not_found` | not_found |
| `already_exists` | already_exists |
| `permission_denied` | permission_denied |
| `resource_exhausted` | resource_exhausted |
| `failed_precondition` | failed_precondition |
| `aborted` | aborted |
| `out_of_range` | out_of_range |
| `unimplemented` | unimplemented |
| `internal` | internal |
| `unavailable` | unavailable |
| `data_loss` | data_loss |
| `unauthenticated` | unauthenticated |

`rpc.grpc.status_code` MUST be one of the following:

| Value  | Description |
|---|---|
| `0` | OK |
| `1` | CANCELLED |
| `2` | UNKNOWN |
| `3` | INVALID_ARGUMENT |
| `4` | DEADLINE_EXCEEDED |
| `5` | NOT_FOUND |
| `6` | ALREADY_EXISTS |
| `7` | PERMISSION_DENIED |
| `8` | RESOURCE_EXHAUSTED |
| `9` | FAILED_PRECONDITION |
| `10` | ABORTED |
| `11` | OUT_OF_RANGE |
| `12` | UNIMPLEMENTED |
| `13` | INTERNAL |
| `14` | UNAVAILABLE |
| `15` | DATA_LOSS |
| `16` | UNAUTHENTICATED |

`rpc.system` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `java_rmi` | Java RMI |
| `dotnet_wcf` | .NET WCF |
| `apache_dubbo` | Apache Dubbo |
| `connect_rpc` | Connect RPC |
<!-- endsemconv -->
