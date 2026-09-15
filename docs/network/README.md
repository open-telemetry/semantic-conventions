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

## Guidance

- [Choosing network address and port attributes](choosing-network-attributes.md): how to pick among
  the shared address and port families (`client.*` / `server.*`, `source.*` / `destination.*`,
  `network.local.*` / `network.peer.*`).

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status/
