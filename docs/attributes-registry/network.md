<!--- Hugo front matter used to generate the website version of this page:
--->

# Network

These attributes may be used for any network related operation.

## Network Attributes

<!-- semconv registry.network(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `network.carrier.icc` | string | The ISO 3166-1 alpha-2 2-character country code associated with the mobile carrier network. | `DE` |
| `network.carrier.mcc` | string | The mobile carrier country code. | `310` |
| `network.carrier.mnc` | string | The mobile carrier network code. | `001` |
| `network.carrier.name` | string | The name of the mobile carrier. | `sprint` |
| `network.connection.subtype` | string | This describes more details regarding the connection.type. It may be the type of cell technology connection, but it could be used for describing details about a wifi connection. | `LTE` |
| `network.connection.type` | string | The internet connection type. | `wifi` |
| `network.io.direction` | string | The network IO operation direction | `transmit` |
| `network.local.address` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Local address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` |
| `network.local.port` | int | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Local port number of the network connection. | `65123` |
| `network.peer.address` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Peer address of the network connection - IP address or Unix domain socket name. | `10.1.2.80`; `/tmp/my.sock` |
| `network.peer.port` | int | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Peer port number of the network connection. | `65123` |
| `network.protocol.name` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>[OSI application layer](https://osi-model.com/application-layer/) or non-OSI equivalent. [1] | `amqp`; `http`; `mqtt` |
| `network.protocol.version` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Version of the protocol specified in `network.protocol.name`. [2] | `3.1.1` |
| `network.transport` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>[OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [3] | `tcp`; `udp` |
| `network.type` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>[OSI network layer](https://osi-model.com/network-layer/) or non-OSI equivalent. [4] | `ipv4`; `ipv6` |

**[1]:** The value SHOULD be normalized to lowercase.

**[2]:** `network.protocol.version` refers to the version of the protocol used and might be different from the protocol client's version. If the HTTP client has a version of `0.27.2`, but sends HTTP version `1.1`, this attribute should be set to `1.1`.

**[3]:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[4]:** The value SHOULD be normalized to lowercase.

`network.connection.subtype` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `gprs` | GPRS |
| `edge` | EDGE |
| `umts` | UMTS |
| `cdma` | CDMA |
| `evdo_0` | EVDO Rel. 0 |
| `evdo_a` | EVDO Rev. A |
| `cdma2000_1xrtt` | CDMA2000 1XRTT |
| `hsdpa` | HSDPA |
| `hsupa` | HSUPA |
| `hspa` | HSPA |
| `iden` | IDEN |
| `evdo_b` | EVDO Rev. B |
| `lte` | LTE |
| `ehrpd` | EHRPD |
| `hspap` | HSPAP |
| `gsm` | GSM |
| `td_scdma` | TD-SCDMA |
| `iwlan` | IWLAN |
| `nr` | 5G NR (New Radio) |
| `nrnsa` | 5G NRNSA (New Radio Non-Standalone) |
| `lte_ca` | LTE CA |

`network.connection.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `wifi` | wifi |
| `wired` | wired |
| `cell` | cell |
| `unavailable` | unavailable |
| `unknown` | unknown |

`network.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `transmit` | transmit |
| `receive` | receive |

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
<!-- endsemconv -->

## Deprecated Network Attributes

<!-- semconv network-deprecated(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `net.host.name` | string | Deprecated, use `server.address`. | `example.com` |
| `net.host.port` | int | Deprecated, use `server.port`. | `8080` |
| `net.peer.name` | string | Deprecated, use `server.address` on client spans and `client.address` on server spans. | `example.com` |
| `net.peer.port` | int | Deprecated, use `server.port` on client spans and `client.port` on server spans. | `8080` |
| `net.protocol.name` | string | Deprecated, use `network.protocol.name`. | `amqp`; `http`; `mqtt` |
| `net.protocol.version` | string | Deprecated, use `network.protocol.version`. | `3.1.1` |
| `net.sock.family` | string | Deprecated, use `network.transport` and `network.type`. | `inet` |
| `net.sock.host.addr` | string | Deprecated, use `network.local.address`. | `/var/my.sock` |
| `net.sock.host.port` | int | Deprecated, use `network.local.port`. | `8080` |
| `net.sock.peer.addr` | string | Deprecated, use `network.peer.address`. | `192.168.0.1` |
| `net.sock.peer.name` | string | Deprecated, no replacement at this time. | `/var/my.sock` |
| `net.sock.peer.port` | int | Deprecated, use `network.peer.port`. | `65531` |
| `net.transport` | string | Deprecated, use `network.transport`. | `ip_tcp` |

`net.sock.family` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `inet` | IPv4 address |
| `inet6` | IPv6 address |
| `unix` | Unix domain socket path |

`net.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `ip_tcp` | ip_tcp |
| `ip_udp` | ip_udp |
| `pipe` | Named or anonymous pipe. |
| `inproc` | In-process communication. [1] |
| `other` | Something else (non IP-based). |

**[1]:** Signals that there is only in-process communication not using a "real" network protocol in cases where network attributes would normally be expected. Usually all other network attributes can be left out in that case.
<!-- endsemconv -->
