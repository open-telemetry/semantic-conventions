<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Choosing network address and port attributes
--->

# Choosing network address and port attributes

**Status**: [Development][DocumentStatus]

The address you record depends on where you observe the exchange:

- An **endpoint** sees its own socket and the socket it is directly connected to. That peer may be
  the other party, or an intermediary.
- An **intermediary** (proxy, load balancer, or NAT) rewrites addresses, so the inbound side and the
  outbound side differ.
- A **pass-through observer** (switch, router, tap, or flow exporter) has no socket. It only sees
  the addresses on the packets crossing that point.

The logical service a client intended to reach, the address observed at a given point, and the
directly connected socket can all be different. OpenTelemetry defines a separate address/port pair
for each, and more than one pair MAY apply to the same telemetry. The
[Attribute reference](#attribute-reference) lists the attributes in each family.

<!-- START doctoc -->

- [Address and port attributes](#address-and-port-attributes)
- [Decision guide](#decision-guide)
- [How they coexist](#how-they-coexist)
  - [`client.*` / `server.*` and the socket](#client--server-and-the-socket)
    - [Logical service and concrete node](#logical-service-and-concrete-node)
    - [Simple client/server example](#simple-clientserver-example)
    - [Client/server example with reverse proxy](#clientserver-example-with-reverse-proxy)
    - [Client/server example with forward proxy](#clientserver-example-with-forward-proxy)
  - [`source.*` / `destination.*` and the socket](#source--destination-and-the-socket)
    - [One endpoint, both directions](#one-endpoint-both-directions)
    - [Router before NAT](#router-before-nat)
    - [Broadcast, multicast, and anycast](#broadcast-multicast-and-anycast)
- [Attribute reference](#attribute-reference)
  - [Server](#server)
  - [Client](#client)
  - [Source](#source)
  - [Destination](#destination)
  - [Network peer](#network-peer)
  - [Network local](#network-local)

<!-- END doctoc -->

## Address and port attributes

Each pair covers one of the three addresses above: the logical service, the address observed at this
point, and the directly connected socket.

| Attribute pair | Question answered | Layer | Address form | Typical source |
| --- | --- | --- | --- | --- |
| [`client.*`](/docs/registry/attributes/client.md) / [`server.*`](/docs/registry/attributes/server.md) | Who initiated vs. accepted the connection? (protocol roles) | Application (L7) | Logical / de-proxied when available (e.g. `X-Forwarded-For`, `Forwarded`, PROXY protocol) | Protocol or instrumentation library |
| [`source.*`](/docs/registry/attributes/source.md) / [`destination.*`](/docs/registry/attributes/destination.md) | Who sent vs. received this exchange? (direction) | Flow / packet (L4), or any exchange with no clear client/server role (L7) | As observed at the point of instrumentation | Packet headers or socket addresses |
| [`network.local.*`](/docs/registry/attributes/network.md) / [`network.peer.*`](/docs/registry/attributes/network.md) | Which end is mine vs. the directly connected peer? (vantage) | Direct connection / socket | Physical socket endpoints | `getsockname` / `getpeername` |

## Decision guide

```text
   What are you instrumenting?
   │
   ├─ L7 application / protocol role
   │   ├─ clear initiator and acceptor (HTTP, gRPC, DB protocols, …)
   │   │     → client / server
   │   │         note: logical, de-proxied when that address is available
   │   │     → network.local / network.peer
   │   └─ symmetric peers, no clear client/server (gossip, BitTorrent, blockchain, WebRTC)
   │         → source / destination
   │              note: as observed at this point; do not resolve past intermediaries
   │         → network.local / network.peer
   │
   ├─ L4 flow or packet (NetFlow, IPFIX, eBPF flows, pcap)
   │     → source / destination
   │         note: a host and a mid-path observer both use this pair,
   │               recording the address seen at that point;
   │               do not resolve past intermediaries
   │     → network.local / network.peer
   │         note: only when this observer has a socket;
   │               not a substitute for source / destination
   │
   └─ L2 / L3 adjacency, routing, or neighbor discovery
         → not covered by these semantic conventions
```

When an area's semantic convention uses `client` / `server`, an operation whose initiator
cannot be determined still uses `client` / `server`. That convention MAY say how to assign
the role.

## How they coexist

### `client.*` / `server.*` and the socket

For `client.*` / `server.*` and `network.peer.*`: when instrumenting the client, `server.address`
answers "who did I intend to talk to?" and `network.peer.address` answers "which host did this
connection land on?". When instrumenting the server, that flips: `network.peer.address` is the
directly connected client or proxy, and `client.address` is the logical client. Folding the concrete
peer into the logical role, in either direction, loses node-level diagnosis under load balancers,
connection pools, and replicas. See the
[`network.*` registry](/docs/registry/attributes/network.md) for socket-level details.

| Instrumentation perspective | Remote endpoint (logical vs. concrete) | Local endpoint (logical vs. concrete) |
| --- | --- | --- |
| Client | `server.*` vs. `network.peer.*` | `client.*` vs. `network.local.*` |
| Server | `client.*` vs. `network.peer.*` | `server.*` vs. `network.local.*` |

#### Logical service and concrete node

`server.address` is the service the client intended to reach. `network.peer.address` is the node
that accepted this connection.

```text
  ┌─────────────────────┐       ┌─────────────────────┐
  │ app                 │       │ replica B           │
  │ ip: 10.0.0.20       │ ────> │ ip: 10.0.0.8        │
  └─────────────────────┘       │ db.example.com:5432 │
                                └─────────────────────┘

  Reported on the app's DB client span:
    server.address       = db.example.com
    server.port          = 5432
    network.peer.address = 10.0.0.8
    network.peer.port    = 5432
```

The following examples show how the logical role (`server.*` / `client.*`) and the concrete socket
(`network.peer.*`) differ across proxy topologies. `network.local.*` is usually omitted;
area-specific conventions mark it Opt-In. The reverse-proxy server example includes it so the listen
socket is visible next to the external `server.*`.

#### Simple client/server example

```text
  ────> public connection (the client-server connection)

  ┌┄ logical client ┄┄┄┄┄┄┄┄┐       ┌┄ logical server ┄┄┄┄┄┄┄┄┐
  ┆                         ┆       ┆                         ┆
  ┆ ┌─────────────────────┐ ┆       ┆ ┌─────────────────────┐ ┆
  ┆ │ client              │ ┆       ┆ │ server              │ ┆
  ┆ │ ip: 101.102.103.104 │ ┆ ────> ┆ │ ip: 201.202.203.204 │ ┆
  ┆ │ port: 50101         │ ┆       ┆ │ port: 9876          │ ┆
  ┆ │ hostname: client.io │ ┆       ┆ │ hostname: server.io │ ┆
  ┆ └─────────────────────┘ ┆       ┆ └─────────────────────┘ ┆
  ┆                         ┆       ┆                         ┆
  └┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘       └┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘

  Reported by the client:                         Reported by the server:
    client.address       = 101.102.103.104          client.address       = 101.102.103.104
    client.port          = 50101                    client.port          = 50101
    server.address       = server.io                server.address       = server.io
    server.port          = 9876                     server.port          = 9876
    network.peer.address = 201.202.203.204          network.peer.address = 101.102.103.104
    network.peer.port    = 9876                     network.peer.port    = 50101
```

#### Client/server example with reverse proxy

`server.*` is the external host (`server.io:9876`), from `Host` or `X-Forwarded-Host`, not the
listen socket `the-server:5678`. That socket is `network.local.*` on the server report. This
picture gives the proxy one address. `client.port` is set only when the intermediary forwarded
that port. `X-Forwarded-For` carries the address and not the port, so
the server report omits `client.port`. `network.peer.port` is the proxy's port on the accepted
connection (`52323`).

```text
  ────> public connection (the client-server connection)
  ····> local connection (the connection behind the proxy)

  ┌┄ logical client ┄┄┄┄┄┄┄┄┐       ┌┄ logical server ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┐
  ┆                         ┆       ┆                                                       ┆
  ┆ ┌─────────────────────┐ ┆       ┆ ┌─────────────────────┐       ┌─────────────────────┐ ┆
  ┆ │ client              │ ┆       ┆ │ reverse proxy       │       │ server              │ ┆
  ┆ │ ip: 101.102.103.104 │ ┆ ────> ┆ │ ip: 201.202.203.204 │ ····> │ ip: 10.11.12.13     │ ┆
  ┆ │ port: 50101         │ ┆       ┆ │ port: 9876          │       │ port: 5678          │ ┆
  ┆ │ hostname: client.io │ ┆       ┆ │ hostname: server.io │       │ hostname: the-server│ ┆
  ┆ └─────────────────────┘ ┆       ┆ └─────────────────────┘       └─────────────────────┘ ┆
  ┆                         ┆       ┆                                                       ┆
  └┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘       └┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘

  Reported by the client:                         Reported by the server:
    client.address       = 101.102.103.104          client.address        = 101.102.103.104
    client.port          = 50101
    server.address       = server.io                server.address        = server.io
    server.port          = 9876                     server.port           = 9876
    network.peer.address = 201.202.203.204          network.peer.address  = 201.202.203.204
    network.peer.port    = 9876                     network.peer.port     = 52323
                                                    network.local.address = 10.11.12.13
                                                    network.local.port    = 5678
```

#### Client/server example with forward proxy

The server knows the original client, so `client.address` is `101.102.103.104` and
`network.peer.address` is the proxy `1.2.3.4`. `client.port` is omitted, as in the reverse proxy.
When the original client was not forwarded, `client.address` is the immediate peer and matches
`network.peer.address`.

```text
  ────> public connection (the client-server connection)
  ····> local connection (the connection behind the proxy)

  ┌┄ logical client ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┐       ┌┄ logical server ┄┄┄┄┄┄┄┄┐
  ┆                                                       ┆       ┆                         ┆
  ┆ ┌─────────────────────┐       ┌─────────────────────┐ ┆       ┆ ┌─────────────────────┐ ┆
  ┆ │ client              │       │ forward proxy       │ ┆       ┆ │ server              │ ┆
  ┆ │ ip: 101.102.103.104 │ ····> │ ip: 1.2.3.4         │ ┆ ────> ┆ │ ip: 201.202.203.204 │ ┆
  ┆ │ port: 50101         │       │ port: 4321          │ ┆       ┆ │ port: 5678          │ ┆
  ┆ │ hostname: client.io │       │ hostname: proxy.io  │ ┆       ┆ │ hostname: server.io │ ┆
  ┆ └─────────────────────┘       └─────────────────────┘ ┆       ┆ └─────────────────────┘ ┆
  ┆                                                       ┆       ┆                         ┆
  └┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘       └┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘

  Reported by the client:                         Reported by the server:
    client.address       = 101.102.103.104          client.address        = 101.102.103.104
    client.port          = 50101
    server.address       = server.io                server.address        = server.io
    server.port          = 5678                     server.port           = 5678
    network.peer.address = 1.2.3.4                  network.peer.address  = 1.2.3.4
    network.peer.port    = 4321                     network.peer.port     = 52323
```

### `source.*` / `destination.*` and the socket

`network.peer` is not `source` or `destination`. On an endpoint the vantage is fixed while the
direction of each exchange flips:

```text
   transmit :  local → source        peer  → destination
   receive  :  peer  → source        local → destination
```

A mid-path observer such as a router often has no local socket, so `network.local` /
`network.peer` do not apply. `source` / `destination` remain well-defined from the packet headers.

#### One endpoint, both directions

```text
  ────> transmit    <──── receive

  ┌─────────────────────┐       ┌─────────────────────┐
  │ host A              │       │ host B              │
  │ ip: 101.102.103.104 │ ────> │ ip: 201.202.203.204 │
  │ port: 50101         │ <──── │ port: 9876          │
  └─────────────────────┘       └─────────────────────┘

  Reported by A, transmit:                          Reported by A, receive:
    source.address         = 101.102.103.104          source.address         = 201.202.203.204
    source.port            = 50101                    source.port            = 9876
    destination.address    = 201.202.203.204          destination.address    = 101.102.103.104
    destination.port       = 9876                     destination.port       = 50101
    network.local.address  = 101.102.103.104          network.local.address  = 101.102.103.104
    network.local.port     = 50101                    network.local.port     = 50101
    network.peer.address   = 201.202.203.204          network.peer.address   = 201.202.203.204
    network.peer.port      = 9876                     network.peer.port      = 9876
```

`source` / `destination` name one sender and one receiver.
A single packet, a one-way flow, or one peer-to-peer message fits.
A record that sums both directions does not.
Split that record by direction, or pick a stable orientation, such as `source` = the initiator.
There is no standard orientation yet
([opentelemetry-ebpf-instrumentation#1659](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/issues/1659),
[#3828](https://github.com/open-telemetry/semantic-conventions/pull/3828)).

#### Router before NAT

A NAT between the router and host B rewrites host A's source to `101.102.103.104:40000`.
The router is before that translation and has no socket for this flow.

```text
  ────> packet

  ┌─────────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
  │ host A              │       │ router              │       │ NAT                 │       │ host B              │
  │ ip: 10.1.2.80       │ ────> │ no socket           │ ────> │ src 101.102.103.104 │ ────> │ ip: 201.202.203.204 │
  │ port: 50101         │       │                     │       │ port: 40000         │       │ port: 9876          │
  └─────────────────────┘       └─────────────────────┘       └─────────────────────┘       └─────────────────────┘

  Reported by the router, before NAT:            Reported by host B, after NAT:
    source.address      = 10.1.2.80                source.address         = 101.102.103.104
    source.port         = 50101                    source.port            = 40000
    destination.address = 201.202.203.204          destination.address    = 201.202.203.204
    destination.port    = 9876                     destination.port       = 9876
                                                   network.local.address  = 201.202.203.204
                                                   network.local.port     = 9876
                                                   network.peer.address   = 101.102.103.104
                                                   network.peer.port      = 40000
```

Two observers of the same flow can disagree, and both can be right.
Each records the address it sees.
This guide does not say how to name which point a record came from.

#### Broadcast, multicast, and anycast

For broadcast and multicast, `destination.*` is the group address on the packet, not each host that
received a copy. Host B below receives a copy of host A's packet. A group is not a connected peer,
so `network.peer` does not apply. `network.local.*` is the socket on the host that sends or receives.

```text
  ────> packet addressed to 239.1.1.1:9876

  ┌─────────────────────┐       ┌─────────────────────┐
  │ host A              │       │ host B              │
  │ ip: 101.102.103.104 │ ────> │ ip: 201.202.203.204 │
  │ port: 50101         │       │ port: 9876          │
  └─────────────────────┘       └─────────────────────┘

  Reported by host A:                           Reported by host B:
    source.address         = 101.102.103.104      source.address         = 101.102.103.104
    source.port            = 50101                source.port            = 50101
    destination.address    = 239.1.1.1            destination.address    = 239.1.1.1
    destination.port       = 9876                 destination.port       = 9876
    network.local.address  = 101.102.103.104      network.local.address  = 201.202.203.204
    network.local.port     = 50101                network.local.port     = 9876
```

For anycast, `destination.*` is the VIP on the packet, not the replica's own address.
`network.local.*` is the replica's socket. `network.peer` is host A, the peer connected to that
socket.

```text
  ────> packet addressed to the VIP 201.202.203.204:9876

  ┌─────────────────────┐       ┌─────────────────────┐
  │ host A              │       │ replica             │
  │ ip: 101.102.103.104 │ ────> │ ip: 10.11.12.13     │
  │ port: 50101         │       │ port: 9876          │
  └─────────────────────┘       └─────────────────────┘

  Reported by the replica:
    source.address         = 101.102.103.104
    source.port            = 50101
    destination.address    = 201.202.203.204
    destination.port       = 9876
    network.local.address  = 10.11.12.13
    network.local.port     = 9876
    network.peer.address   = 101.102.103.104
    network.peer.port      = 50101
```

Naming each host that receives a copy is out of scope
([#4121](https://github.com/open-telemetry/semantic-conventions/issues/4121)).

## Attribute reference

The address and port attribute families are summarized below. Full definitions live in the registry:
[`client`](/docs/registry/attributes/client.md), [`server`](/docs/registry/attributes/server.md),
[`source`](/docs/registry/attributes/source.md),
[`destination`](/docs/registry/attributes/destination.md), and
[`network`](/docs/registry/attributes/network.md).

### Server

<!-- semconv server -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Stable](https://img.shields.io/badge/-stable-lightgreen)

`server.*` attributes describe the server in a connection-based network interaction: the side that accepts the connection (the client is the side that initiates it). They identify the logical server the client intended to reach, which - behind proxies or load balancers - can differ from the concrete socket endpoint.

Use them for interactions with a clear initiator and acceptor. This covers common TCP interactions, connection-oriented UDP such as QUIC (HTTP/3), and request/response protocols such as DNS and SNMP polling. It does not cover peer-to-peer communication where the protocol or API exposes no clear notion of client and server (even over TCP).

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`server.address`](/docs/registry/attributes/server.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or UNIX domain socket name. [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` |
| [`server.port`](/docs/registry/attributes/server.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | int | Server port number. [2] | `80`; `8080`; `443` |

**[1] `server.address`:** On the client side, `server.address` is the remote service name; on the server side, it is the local service name as seen externally by clients. These normally match - for example, for the URL `https://example.com/foo` it is `"example.com"` on both sides. When a client reaches the server through an intermediary such as a proxy, `server.address` SHOULD represent the server behind the intermediary, if available.

For IP-based communication, prefer a DNS hostname of the service. Instrumentation is often given the address as a URL, connection string, or hostname, so `server.address` SHOULD be set to the known hostname available to it, which may be a DNS name or an IP address (for example `"127.0.0.1"` for `https://127.0.0.1/foo`). If only an IP address is available, populate `server.address` with it; a reverse DNS lookup SHOULD NOT be used to obtain a name.

If `network.transport` is `"pipe"`, use the absolute path to the file representing it; for an anonymous pipe with no such file, set `server.address` to an empty string to distinguish it from an unknown or uninstrumented value.

For a UNIX domain socket, `server.address` is the remote endpoint address on the client side and the local endpoint address on the server side.

**[2] `server.port`:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Client

<!-- semconv client -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Stable](https://img.shields.io/badge/-stable-lightgreen)

`client.*` attributes describe the client in a connection-based network interaction: the side that initiates the connection (the server is the side that accepts it). They identify the logical client, which - behind proxies or load balancers - can differ from the concrete socket endpoint and is typically recovered from headers such as `X-Forwarded-For`.

Use them for interactions with a clear initiator and acceptor. This covers common TCP interactions, connection-oriented UDP such as QUIC (HTTP/3), and request/response protocols such as DNS and SNMP polling. It does not cover peer-to-peer communication where the protocol or API exposes no clear notion of client and server (even over TCP).

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`client.address`](/docs/registry/attributes/client.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or UNIX domain socket name. [1] | `client.example.com`; `10.1.2.80`; `/tmp/my.sock` |
| [`client.port`](/docs/registry/attributes/client.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | int | Client port number. [2] | `65123` |

**[1] `client.address`:** When observed from the server side, and when communicating through an intermediary, `client.address` SHOULD represent the client address behind any intermediaries, for example proxies, if it's available.

**[2] `client.port`:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries, for example proxies, if it's available.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Source

<!-- semconv source -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

`source.*` attributes describe the sender of a network exchange or packet. They capture the address available at the point of instrumentation and do not try to resolve the address behind intermediaries such as proxies.

Use them when there is no client/server relationship between the two sides, or when that relationship is unknown - for example, packet-level telemetry and peer-to-peer protocols.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`source.address`](/docs/registry/attributes/source.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | Source address as observed at the point of instrumentation - typically an IP address, or a UNIX domain socket name; a domain name only when the sender was addressed by name (for example a peer-to-peer node dialed by hostname), never obtained via reverse DNS lookup. [1] | `10.1.2.80`; `source.example.com`; `/tmp/my.sock` |
| [`source.port`](/docs/registry/attributes/source.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | int | Source port number | `3389`; `2888` |

**[1] `source.address`:** `source.address` SHOULD be the sender address as observed at the point of instrumentation, for example the source of the packet, flow, or exchange seen on the wire or socket. Instrumentation SHOULD capture the available address and SHOULD NOT try to resolve the address behind intermediaries such as proxies or load balancers, or perform a reverse DNS lookup to obtain a domain name.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Destination

<!-- semconv destination -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

`destination.*` attributes describe the receiver of a network exchange or packet. They capture the address available at the point of instrumentation and do not try to resolve the address behind intermediaries such as proxies.

Use them when there is no client/server relationship between the two sides, or when that relationship is unknown - for example, packet-level telemetry and peer-to-peer protocols.

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`destination.address`](/docs/registry/attributes/destination.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | string | Destination address as observed at the point of instrumentation - typically an IP address, or a UNIX domain socket name; a domain name only when the receiver was addressed by name (for example a peer-to-peer node dialed by hostname), never obtained via reverse DNS lookup. [1] | `10.1.2.80`; `destination.example.com`; `/tmp/my.sock` |
| [`destination.port`](/docs/registry/attributes/destination.md) | ![Development](https://img.shields.io/badge/-development-blue) | `Recommended` | int | Destination port number | `3389`; `2888` |

**[1] `destination.address`:** `destination.address` SHOULD be the receiver address as observed at the point of instrumentation, for example the destination of the packet, flow, or exchange seen on the wire or socket. Instrumentation SHOULD capture the available address and SHOULD NOT try to resolve the address behind intermediaries such as proxies or load balancers, or perform a reverse DNS lookup to obtain a domain name.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Network peer

<!-- semconv network.peer -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Stable](https://img.shields.io/badge/-stable-lightgreen)

These attributes identify the network peer that is directly connected to the local endpoint.

> [!NOTE]
> Specific structures and methods to obtain socket-level attributes are mentioned here only as examples.
> Instrumentations would usually use the socket API provided by their environment or socket implementations.

When connecting using `connect(2)` ([Linux or other POSIX systems](https://man7.org/linux/man-pages/man2/connect.2.html) /
[Windows](https://docs.microsoft.com/windows/win32/api/winsock2/nf-winsock2-connect)) with the `AF_INET` address family,
`network.peer.address` and `network.peer.port` represent the `sin_addr` and `sin_port` fields of the `sockaddr_in` structure.

`network.peer.address` and `network.peer.port` can be obtained by calling `getpeername` ([Linux or other POSIX systems](https://man7.org/linux/man-pages/man2/getpeername.2.html) /
[Windows](https://docs.microsoft.com/windows/win32/api/winsock2/nf-winsock2-getpeername)).

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`network.peer.address`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Peer address of the network connection - IP address or UNIX domain socket name. [1] | `10.1.2.80`; `/tmp/my.sock` |
| [`network.peer.port`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | int | Peer port number of the network connection. | `65123` |

**[1] `network.peer.address`:** This SHOULD be an IP address, UNIX domain socket name, or other address specific to the network type.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

### Network local

<!-- semconv network.local -->
<!-- NOTE: THIS TEXT IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/snippet.md.j2 -->
<!-- prettier-ignore-start -->

**Status:** ![Stable](https://img.shields.io/badge/-stable-lightgreen)

These attributes identify the local endpoint of a network connection.

> [!NOTE]
> Specific structures and methods to obtain socket-level attributes are mentioned here only as examples.
> Instrumentations would usually use the socket API provided by their environment or socket implementations.

When binding using `bind(2)` ([Linux or other POSIX systems](https://man7.org/linux/man-pages/man2/bind.2.html) /
[Windows](https://docs.microsoft.com/windows/win32/api/winsock2/nf-winsock2-bind)) with the `AF_INET` address family,
`network.local.address` and `network.local.port` represent the `sin_addr` and `sin_port` fields of the `sockaddr_in` structure.

`network.local.address` and `network.local.port` can be obtained by calling `getsockname` ([Linux or other POSIX systems](https://man7.org/linux/man-pages/man2/getsockname.2.html) /
[Windows](https://docs.microsoft.com/windows/win32/api/winsock2/nf-winsock2-getsockname)).

**Attributes:**

| Key | Stability | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| [`network.local.address`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | string | Local address of the network connection - IP address or UNIX domain socket name. [1] | `10.1.2.80`; `/tmp/my.sock` |
| [`network.local.port`](/docs/registry/attributes/network.md) | ![Stable](https://img.shields.io/badge/-stable-lightgreen) | `Recommended` | int | Local port number of the network connection. | `65123` |

**[1] `network.local.address`:** This SHOULD be an IP address, UNIX domain socket name, or other address specific to the network type.

<!-- prettier-ignore-end -->
<!-- END AUTOGENERATED TEXT -->
<!-- endsemconv -->

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status/
