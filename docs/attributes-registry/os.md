<!--- Hugo front matter used to generate the website version of this page:
linkTitle: OS
--->
# OS

## Operating system Attributes

<!-- semconv registry.os(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `os.build_id` | string | Unique identifier for a particular build or compilation of the operating system. | `TQ3C.230805.001.B2`; `20E247`; `22621` |
| `os.description` | string | Human readable (not intended to be parsed) OS version information, like e.g. reported by `ver` or `lsb_release -a` commands. | `Microsoft Windows [Version 10.0.18363.778]`; `Ubuntu 18.04.1 LTS` |
| `os.name` | string | Human readable operating system name. | `iOS`; `Android`; `Ubuntu` |
| `os.type` | string | The operating system type. | `windows` |
| `os.version` | string | The version string of the operating system as defined in [Version Attributes](/docs/resource/README.md#version-attributes). | `14.2.1`; `18.04.1` |

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