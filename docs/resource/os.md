# Operating System

**Status**: [Experimental][DocumentStatus]

**type:** `os`

**Description**: The operating system (OS) on which the process represented by this resource is running.

In case of virtualized environments, this is the operating system as it is observed by the process, i.e., the virtualized guest rather than the underlying host.

<!-- semconv os -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `os.type` | string | The operating system type. | `windows` | Required |
| `os.description` | string | Human readable (not intended to be parsed) OS version information, like e.g. reported by `ver` or `lsb_release -a` commands. | `Microsoft Windows [Version 10.0.18363.778]`; `Ubuntu 18.04.1 LTS` | Recommended |
| `os.name` | string | Human readable operating system name. | `iOS`; `Android`; `Ubuntu` | Recommended |
| `os.version` | string | The major version string of the operating system.  Additionally, build numbers can be added in os.build attribute. | `14.2.1`; `18.04.1` | Recommended |
| `os.build` | string | Unique identifier for a particular build or compilation of software. | `TQ3C.230805.001.B2`; `20E247` | Recommended |
| `os.sdk_version` | string | Identifies the set of development tools and APIs used for building the software. | `26`; `6.1.1` | Recommended |

`os.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `windows` | Microsoft Windows |
| `linux` | Linux |
| `darwin` | Apple Darwin |
| `freebsd` | FreeBSD |
| `netbsd` | NetBSD |
| `openbsd` | OpenBSD |
| `dragonflybsd` | DragonFly BSD |
| `hpux` | HP-UX (Hewlett Packard Unix) |
| `aix` | AIX (Advanced Interactive eXecutive) |
| `solaris` | SunOS, Oracle Solaris |
| `z_os` | IBM z/OS |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
