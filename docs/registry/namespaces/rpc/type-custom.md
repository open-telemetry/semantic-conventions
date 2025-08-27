# RPC

**Summary:** This document defines how to describe remote procedure calls (also called “remote method invocations” / “RMI”) with spans.

> [!IMPORTANT]  Namespace was stablised in v1.20
>
> When migrating from an earlier version of semantic conventions, the migration document should be followed. [Migration Guide](#rpc)

**Description:** The conventions described in this section are RPC specific. When RPC operations occur, measurements about those operations are recorded to instruments. The measurements are aggregated and exported as metrics, which provide insight into those operations. By including RPC properties as attributes on measurements, the metrics can be filtered for finer grain analysis.

---------------------------------

## Type: RPC System

**Status:** ![Development](https://img.shields.io/badge/-development-blue)

**Namespace:** [`rpc`](README.md)

**Summary:** A string identifying the remoting system. See below for a list of well-known identifiers.

**Signal Type:** Custom Type

**Type Name:** `rpc.system`

**Description:** An RPC System is.....

**Values:**

| Value  | Description | Stability |
|---|---|---|
| `apache_dubbo` | Apache Dubbo | ![Development](https://img.shields.io/badge/-development-blue) |
| `connect_rpc` | Connect RPC | ![Development](https://img.shields.io/badge/-development-blue) |
| `dotnet_wcf` | .NET WCF | ![Development](https://img.shields.io/badge/-development-blue) |
| `grpc` | gRPC | ![Development](https://img.shields.io/badge/-development-blue) |
| `java_rmi` | Java RMI | ![Development](https://img.shields.io/badge/-development-blue) |
