
<!--- Hugo front matter used to generate the website version of this page:
--->

# NETWORK

- [network](#network)
- [network deprecated](#network deprecated)


## network Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `network.carrier.icc` | string | The ISO 3166-1 alpha-2 2-character country code associated with the mobile carrier network.  |
DE | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network.carrier.mcc` | string | The mobile carrier country code.  |
310 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network.carrier.mnc` | string | The mobile carrier network code.  |
001 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network.carrier.name` | string | The name of the mobile carrier.  |
sprint | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network.connection.subtype` | string | This describes more details regarding the connection.type. It may be the type of cell technology connection, but it could be used for describing details about a wifi connection.  |`gprs`; `edge`; `umts`; `cdma`; `evdo_0`; `evdo_a`; `cdma2000_1xrtt`; `hsdpa`; `hsupa`; `hspa`; `iden`; `evdo_b`; `lte`; `ehrpd`; `hspap`; `gsm`; `td_scdma`; `iwlan`; `nr`; `nrnsa`; `lte_ca` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network.connection.type` | string | The internet connection type.  |`wifi`; `wired`; `cell`; `unavailable`; `unknown` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network.local.address` | string | Local address of the network connection - IP address or Unix domain socket name.  |`10.1.2.80`; `/tmp/my.sock` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `network.local.port` | int | Local port number of the network connection.  |`65123` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `network.peer.address` | string | Peer address of the network connection - IP address or Unix domain socket name.  |`10.1.2.80`; `/tmp/my.sock` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `network.peer.port` | int | Peer port number of the network connection.  |`65123` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `network.protocol.name` | string | [OSI application layer](https://osi-model.com/application-layer/) or non-OSI equivalent. [1] |`amqp`; `http`; `mqtt` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `network.protocol.version` | string | The actual version of the protocol used for network communication. [2] |`1.1`; `2` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `network.transport` | string | [OSI transport layer](https://osi-model.com/transport-layer/) or [inter-process communication method](https://wikipedia.org/wiki/Inter-process_communication). [3] |`tcp`; `udp`; `pipe`; `unix` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `network.type` | string | [OSI network layer](https://osi-model.com/network-layer/) or non-OSI equivalent. [4] |`ipv4`; `ipv6` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `network.io.direction` | string | The network IO operation direction.  |`transmit`; `receive` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|

**[1]:** The value SHOULD be normalized to lowercase.
**[2]:** If protocol version is subject to negotiation (for example using [ALPN](https://www.rfc-editor.org/rfc/rfc7301.html)), this attribute SHOULD be set to the negotiated version. If the actual protocol version is not known, this attribute SHOULD NOT be set.

**[3]:** The value SHOULD be normalized to lowercase.

Consider always setting the transport when setting a port number, since
a port number is ambiguous without knowing the transport. For example
different processes could be listening on TCP port 12345 and UDP port 12345.

**[4]:** The value SHOULD be normalized to lowercase.

`network.connection.subtype` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `gprs` | GPRS |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `edge` | EDGE |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `umts` | UMTS |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cdma` | CDMA |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `evdo_0` | EVDO Rel. 0 |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `evdo_a` | EVDO Rev. A |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cdma2000_1xrtt` | CDMA2000 1XRTT |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hsdpa` | HSDPA |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hsupa` | HSUPA |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hspa` | HSPA |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `iden` | IDEN |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `evdo_b` | EVDO Rev. B |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `lte` | LTE |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ehrpd` | EHRPD |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hspap` | HSPAP |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gsm` | GSM |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `td_scdma` | TD-SCDMA |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `iwlan` | IWLAN |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `nr` | 5G NR (New Radio) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `nrnsa` | 5G NRNSA (New Radio Non-Standalone) |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `lte_ca` | LTE CA |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`network.connection.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `wifi` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `wired` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cell` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `unavailable` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `unknown` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`network.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `tcp` | TCP |  ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `udp` | UDP |  ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `pipe` | Named or anonymous pipe. |  ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unix` | Unix domain socket |  ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`network.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `ipv4` | IPv4 |  ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `ipv6` | IPv6 |  ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`network.io.direction` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `transmit` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `receive` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |


## network deprecated Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `net.sock.peer.name` | string | Deprecated, no replacement at this time. [5] |`/var/my.sock` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.sock.peer.addr` | string | Deprecated, use `network.peer.address`. [6] |`192.168.0.1` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.sock.peer.port` | int | Deprecated, use `network.peer.port`. [7] |`65531` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.peer.name` | string | Deprecated, use `server.address` on client spans and `client.address` on server spans. [8] |`example.com` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.peer.port` | int | Deprecated, use `server.port` on client spans and `client.port` on server spans. [9] |`8080` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.host.name` | string | Deprecated, use `server.address`. [10] |`example.com` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.host.port` | int | Deprecated, use `server.port`. [11] |`8080` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.sock.host.addr` | string | Deprecated, use `network.local.address`. [12] |`/var/my.sock` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.sock.host.port` | int | Deprecated, use `network.local.port`. [13] |`8080` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.transport` | string | Deprecated, use `network.transport`. [14] |`ip_tcp`; `ip_udp`; `pipe`; `inproc`; `other` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.protocol.name` | string | Deprecated, use `network.protocol.name`. [15] |`amqp`; `http`; `mqtt` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.protocol.version` | string | Deprecated, use `network.protocol.version`. [16] |
3.1.1 | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `net.sock.family` | string | Deprecated, use `network.transport` and `network.type`. [17] |`inet`; `inet6`; `unix` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
|---|---|---|---|---|

**[5]:** Removed.
**[6]:** Replaced by `network.peer.address`.
**[7]:** Replaced by `network.peer.port`.
**[8]:** Replaced by `server.address` on client spans and `client.address` on server spans.
**[9]:** Replaced by `server.port` on client spans and `client.port` on server spans.
**[10]:** Replaced by `server.address`.
**[11]:** Replaced by `server.port`.
**[12]:** Replaced by `network.local.address`.
**[13]:** Replaced by `network.local.port`.
**[14]:** Replaced by `network.transport`.
**[15]:** Replaced by `network.protocol.name`.
**[16]:** Replaced by `network.protocol.version`.
**[17]:** Split to `network.transport` and `network.type`.

`net.transport` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `ip_tcp` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ip_udp` | none |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `pipe` | Named or anonymous pipe. |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `inproc` | In-process communication. |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `other` | Something else (non IP-based). |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`net.sock.family` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `inet` | IPv4 address |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `inet6` | IPv6 address |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `unix` | Unix domain socket path |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |

