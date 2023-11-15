<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Destination
--->

# Destination Attributes

These attributes may be used to describe the receiver of a network exchange/packet. These should be used
when there is no client/server relationship between the two sides, or when that relationship is unknown.
This covers low-level network interactions (e.g. packet tracing) where you don't know if
there was a connection or which side initiated it.
This also covers unidirectional UDP flows and peer-to-peer communication where the
"user-facing" surface of the protocol / API does not expose a clear notion of client and server.

<!-- semconv destination(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `destination.address` | string | Destination address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `destination.example.com`; `10.1.2.80`; `/tmp/my.sock` |
| `destination.port` | int | Destination port number | `3389`; `2888` |

**[1]:** When observed from the source side, and when communicating through an intermediary, `destination.address` SHOULD represent the destination address behind any intermediaries, for example proxies, if it's available.
<!-- endsemconv -->
