<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Client
--->

# Client Attributes

These attributes may be used to describe the client in a connection-based network interaction
where there is one side that initiates the connection (the client is the side that initiates the connection).
This covers all TCP network interactions since TCP is connection-based and one side initiates the
connection (an exception is made for peer-to-peer communication over TCP where the "user-facing" surface of the
protocol / API does not expose a clear notion of client and server).
This also covers UDP network interactions where one side initiates the interaction, e.g. QUIC (HTTP/3) and DNS.

<!-- semconv registry.client(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `client.address` | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `client.example.com`; `10.1.2.80`; `/tmp/my.sock` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `client.port` | int | Client port number. [2] | `65123` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** When observed from the server side, and when communicating through an intermediary, `client.address` SHOULD represent the client address behind any intermediaries,  for example proxies, if it's available.

**[2]:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries,  for example proxies, if it's available.
<!-- endsemconv -->
