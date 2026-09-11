<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Network
--->

# Semantic conventions for Network

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for network-centric observability:
telemetry taken from the network itself, not only from an application's view of
its own connections. That includes traditional methods such as NetFlow, IPFIX,
and SNMP, as well as eBPF and other on-path observers, and the shared address
and protocol attributes that application instrumentations also reuse.

Semantic conventions for Network will be defined for the following signals,
and will be added as they are defined:

- **Spans** - for example flow traces
- **Metrics** - for example protocol, flow, and SNMP metrics
- **Events** - for example SNMP traps and routing updates
- **Entities** - network entities across the OSI model (interfaces, peers,
  sessions, flows)

This page documents how to choose among the shared address and port families
those signals use. The attribute definitions themselves live in
[General network attributes](/docs/general/attributes.md#general-network-attributes)
and the [attribute registry](/docs/registry/attributes/network.md).

<!-- START doctoc -->

- [Choosing address and port attributes](#choosing-address-and-port-attributes)
  - [Why these pairs are not interchangeable](#why-these-pairs-are-not-interchangeable)
  - [How they coexist](#how-they-coexist)
  - [Decision guide](#decision-guide)
  - [Flow direction vs. socket vantage](#flow-direction-vs-socket-vantage)
  - [What flow exporters observe](#what-flow-exporters-observe)
- [See also](#see-also)

<!-- END doctoc -->

Attributing an address to a communication is harder than it first appears, because the same
exchange looks different depending on where it is observed:

- At a communicating **endpoint**, a process sees its own socket and the socket of whatever it is
  directly connected to - which may be the other party, or an intermediary.
- At an **intermediary** such as a proxy, load balancer, or NAT gateway, addresses are frequently
  rewritten, so the addresses on the inbound side differ from those on the outbound side.
- At a **pass-through observer** such as a switch or router interface, a network tap, or a flow
  exporter, there may be no socket at all - only the addresses carried in the packets crossing
  that point.

Because of this, no single address/port pair can answer every question. The address of the
_logical_ service a client intended to reach, the address _actually observed on the wire_ at a
given point, and the address of the _directly connected_ node can all differ - especially when
intermediaries are involved. OpenTelemetry therefore defines several address/port pairs, each
answering a distinct question, and more than one pair MAY apply to the same telemetry. See
[Choosing address and port attributes](#choosing-address-and-port-attributes) for how to pick the
right one(s).

## Choosing address and port attributes

OpenTelemetry defines three pairs of address/port attributes for the two sides of a network
interaction. They answer different questions and are not synonyms; more than one pair MAY apply
to the same telemetry.

| Attribute pair | Question answered | Layer | Address form | Typical source |
| --- | --- | --- | --- | --- |
| [`client.*`](/docs/registry/attributes/client.md) / [`server.*`](/docs/registry/attributes/server.md) | Who initiated vs. accepted the connection? (protocol roles) | Application (L7) | Logical / de-proxied when available (e.g. `X-Forwarded-For`, `Forwarded`, PROXY protocol) | Protocol or instrumentation library |
| [`source.*`](/docs/registry/attributes/source.md) / [`destination.*`](/docs/registry/attributes/destination.md) | Who sent vs. received this exchange? (direction) | Flow / packet (L4), or any exchange with no clear client/server role | As observed at the point of instrumentation | The 5-tuple seen on the wire or socket at the meter |
| [`network.local.*`](/docs/registry/attributes/network.md) / [`network.peer.*`](/docs/registry/attributes/network.md) | Which end is mine vs. the directly connected peer? (vantage) | Direct connection / socket | Physical socket endpoints | `getsockname` / `getpeername` |

The pairs map roughly onto observation layers:

```text
   L7  Application / protocol roles                client / server
       (HTTP, gRPC, DB wire protocols, …)          (+ network.local/peer = concrete socket node)
       symmetric peers, no clear roles             source / destination
       (gossip, BitTorrent, blockchain, WebRTC)
   ─────────────────────────────────────────────────────────────────────────────────────────────────
   L4  Transport flow / packet direction           source / destination
       (NetFlow, IPFIX, eBPF flows, pcap)          (same family at endpoint or mid-path)
   ─────────────────────────────────────────────────────────────────────────────────────────────────
   L3  Network routing / forwarding                (not covered by these pairs today)
   L2  Link / neighbor discovery                   (not covered by these pairs today)
```

### Why these pairs are not interchangeable

Each pair answers a different question, and only some pin down _which_ address to record:

```text
   ROLE (who initiated?)                              [client / server]
     client ●───────────────────────────────────────────● server

   DIRECTION (who sent THIS exchange?)                [source / destination]
     source ●───────────────────────────────────────────● destination

   VANTAGE (my end vs directly wired other)           [network.local / network.peer]
     local  ●───────────────────────────────────────────● peer
```

| Pair | What the label means | Which address is recorded |
| --- | --- | --- |
| `client` / `server` | who initiated vs. accepted | Logical / de-proxied |
| `source` / `destination` | who sent vs. received this exchange | As observed at the observation point |
| `network.local` / `network.peer` | this end vs. the directly connected other | Physical (`getsockname` / `getpeername`) |

`network.peer` is not simply `source` or `destination`: on an endpoint the vantage is fixed while
packet direction flips.

```text
   Server viewpoint (network.peer = client or proxy, fixed):

     request  :  peer ──▶ local     peer plays SOURCE
     response :  local ──▶ peer     peer plays DESTINATION
```

Mid-path observers (routers, taps) often have no local socket at all, so `network.local` /
`network.peer` do not apply, while `source` / `destination` remain well-defined from packet headers.

### How they coexist

At L7, logical role and concrete adjacency are independent dimensions. Emitting both is correct,
not redundant: emit `server.address` (logical) and `network.peer.address` (concrete node) when they
differ.

```text
   External client → reverse proxy / LB → app → DB cluster (this query → node B)

   ┌──────────┐      ┌────────────┐      ┌──────────┐      ┌─────────────────────┐
   │  CLIENT  │─────▶│ PROXY / LB │─────▶│   APP    │─────▶│  db.example.com     │
   │203.0.113 │      │  10.0.0.9  │      │10.0.0.20 │      │  ┌ A ┐ ┌ B ┐ ┌ C ┐  │
   └──────────┘      └────────────┘      └──────────┘      │  │.7 │ │.8 │ │.9 │  │
                                                           └─────────────────────┘

   On the APP's outbound DB client span:
     server.address        = db.example.com   ← logical destination
     network.peer.address  = 10.0.0.8         ← concrete node B (getpeername)
     network.local.address = 10.0.0.20        ← app's socket (often opt-in)

   On the APP's inbound HTTP server span:
     client.address        = 203.0.113.x      ← logical client (XFF), if available
     server.address        = api.example.com
     network.peer.address  = 10.0.0.9         ← concrete: the proxy's IP
     network.local.address = 10.0.0.20        ← app's accepting socket (opt-in)

   If the same path is also observed as L4 flows (eBPF / NetFlow):
     source / destination  = as-observed 5-tuple at that metering point
     (may be proxy, node, or post-NAT addresses — not the same as L7 client/server)
```

Which logical role maps to the concrete socket depends on the span's perspective: logical
identity and physical adjacency are recorded from whichever side emits the telemetry.

| Span perspective | Remote endpoint (logical vs. concrete) | Local endpoint (logical vs. concrete) |
| --- | --- | --- |
| Client span | `server.*` vs. `network.peer.*` | `client.*` vs. `network.local.*` |
| Server span | `client.*` vs. `network.peer.*` | `server.*` vs. `network.local.*` |

On a client span, `server.address` answers "who did I intend to talk to?" while
`network.peer.address` answers "which specific box did this connection land on?". On a server span
the roles invert: `network.peer.address` is the directly connected client or proxy, while
`client.address` is the logical (de-proxied) client. Folding the concrete peer into the logical
role - in either direction - would lose node-level diagnosis under load balancers, connection
pools, and replicas. See
[`network.peer.*` and `network.local.*` attributes](/docs/general/attributes.md#networkpeer-and-networklocal-attributes)
for socket-level details and proxy examples.

### Decision guide

```text
   What are you instrumenting?
   │
   ├─ L7 protocol / application API
   │   ├─ clear initiator and acceptor
   │   │     → client / server  (roles; logical / de-proxied)
   │   │     → also network.local / network.peer for the concrete socket
   │   └─ symmetric peers, no clear client/server role
   │         (gossip, BitTorrent, blockchain, WebRTC)
   │         → source / destination
   │
   ├─ L4 flow, packet, or mid-path metering (no / unknown app roles)
   │     → source / destination  (direction of this exchange, as observed)
   │       used consistently whether observed at an endpoint or mid-path
   │       (network.local / network.peer are for connection/socket-level telemetry,
   │        not a substitute encoding for a flow record's endpoints)
   │
   └─ L2 / L3 adjacency, routing, or neighbor discovery
         → not covered by these pairs today
```

| If you know… | Prefer |
| --- | --- |
| Protocol initiator / acceptor (L7) | `client` / `server` |
| Packet or flow direction (L4) | `source` / `destination` |
| Symmetric peers with no clear client/server role | `source` / `destination` |
| Concrete socket endpoint (L4/L7; also BGP TCP) | `network.local` / `network.peer` |
| Logical service name _and_ concrete node | `server.*` **and** `network.peer.*` together |

> [!NOTE]
> The `client` / `server` roles come from protocol or connection semantics - who initiated the
> connection and who accepted it - which at L7 is almost always known. In the rare case where the
> initiator cannot be determined, a best-effort heuristic MAY be used as a last resort, for example
> treating the well-known / lower port as the server and the ephemeral / higher port as the client.
> Such a heuristic is best-effort only and can be wrong (ephemeral port ranges vary by platform,
> both ends may use registered ports, and peer-to-peer protocols have no roles), so fall back to
> `source` / `destination` when it would not be reliable.

<!-- -->

> [!NOTE]
> Choosing `source` / `destination` requires more than the absence of a client/server role: each
> telemetry record must have a well-defined direction, identifying who sent and who received _that_
> exchange. This holds naturally for a single packet, a unidirectional flow, or one peer-to-peer
> message. A bidirectional aggregate (for example a flow record that sums both directions of a
> connection) has no single sender, so `source` / `destination` are ambiguous for it. Such telemetry
> should either be split into per-direction records, or adopt a stable forward/reverse orientation
> (for example, keying `source` to the flow initiator). A standard orientation semantic
> convention is out of scope for this guidance and is a work in progress (see
> [open-telemetry/opentelemetry-ebpf-instrumentation#1659](https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/issues/1659)
> and [#3828](https://github.com/open-telemetry/semantic-conventions/pull/3828)).

### Flow direction vs. socket vantage

Flow and packet telemetry uses `source` / `destination` consistently, whether observed at an
endpoint (host IPFIX, eBPF) or mid-path (router/switch NetFlow/IPFIX), so that the same flow is
represented the same way regardless of vantage. `network.local` / `network.peer` are not an
alternative encoding for a flow's endpoints: they describe the concrete socket of a
connection-oriented interaction and belong on connection/socket-level telemetry (for example a
`client` / `server` span, or a BGP TCP session).

The two families are related but not synonymous. On an endpoint the vantage
(`network.local` / `network.peer`) is fixed while the direction (`source` / `destination`) flips
per exchange:

```text
   transmit :  local → source        peer  → destination
   receive  :  peer  → source        local → destination
```

Use this correspondence to reason about telemetry that already carries both families (such as a
connection span that also reports direction); it is not a license to move a flow record onto
`network.local` / `network.peer`.

### What flow exporters observe

L3/L4 observers generally cannot see behind an L7 proxy or SNAT, so in flow telemetry
`source` / `destination` hold the addresses actually present at the metering point:

| Path to backend | Typical L4 `source` at the backend |
| --- | --- |
| L7 proxy / ingress that terminates the connection | Proxy IP (real client only in `X-Forwarded-For` / PROXY protocol) |
| L4 load balancer with SNAT (e.g. K8s `externalTrafficPolicy: Cluster`) | Load balancer / node IP |
| L4 load balancer with client-IP preservation / DSR (`externalTrafficPolicy: Local`) | Real client IP |
| Pod to pod, no intermediary | Pod IP |

This is why L4 `source` / `destination` are recorded as observed and are not resolved behind
intermediaries; use `client.*` / `server.*` when the logical, de-proxied identity is needed.

## See also

- [General network attributes](/docs/general/attributes.md#general-network-attributes) -
  the address, port, transport, and protocol attribute reference tables.
- [`network.*` registry](/docs/registry/attributes/network.md)
- [`source.*` registry](/docs/registry/attributes/source.md)
- [`destination.*` registry](/docs/registry/attributes/destination.md)

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status/
