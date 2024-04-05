# Operating System

**Status**: [Experimental][DocumentStatus]

**type:** `os`

**Description**: The operating system (OS) on which the process represented by this resource is running.

In case of virtualized environments, this is the operating system as it is observed by the process, i.e., the virtualized guest rather than the underlying host.

<!-- semconv os(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`os.type`](../attributes-registry/os.md) | string | The operating system type. | `windows` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`os.build_id`](../attributes-registry/os.md) | string | Unique identifier for a particular build or compilation of the operating system. | `TQ3C.230805.001.B2`; `20E247`; `22621` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`os.description`](../attributes-registry/os.md) | string | Human readable (not intended to be parsed) OS version information, like e.g. reported by `ver` or `lsb_release -a` commands. | `Microsoft Windows [Version 10.0.18363.778]`; `Ubuntu 18.04.1 LTS` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`os.name`](../attributes-registry/os.md) | string | Human readable operating system name. | `iOS`; `Android`; `Ubuntu` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`os.version`](../attributes-registry/os.md) | string | The version string of the operating system as defined in [Version Attributes](/docs/resource/README.md#version-attributes). | `14.2.1`; `18.04.1` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`os.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `windows` | Microsoft Windows | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `linux` | Linux | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `darwin` | Apple Darwin | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `freebsd` | FreeBSD | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `netbsd` | NetBSD | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `openbsd` | OpenBSD | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `dragonflybsd` | DragonFly BSD | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hpux` | HP-UX (Hewlett Packard Unix) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aix` | AIX (Advanced Interactive eXecutive) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `solaris` | SunOS, Oracle Solaris | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `z_os` | IBM z/OS | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
