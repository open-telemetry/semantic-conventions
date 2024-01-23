<!--- Hugo front matter used to generate the website version of this page:
--->
# Host

## Host Attributes

<!-- semconv registry.host(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `host.arch` | string | The CPU architecture the host system is running on. | `amd64` |
| `host.cpu.cache.l2.size` | int | The amount of level 2 memory cache available to the processor (in Bytes). | `12288000` |
| `host.cpu.family` | string | Family or generation of the CPU. | `6`; `PA-RISC 1.1e` |
| `host.cpu.model.id` | string | Model identifier. It provides more granular information about the CPU, distinguishing it from other CPUs within the same family. | `6`; `9000/778/B180L` |
| `host.cpu.model.name` | string | Model designation of the processor. | `11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz` |
| `host.cpu.stepping` | string | Stepping or core revisions. | `1`; `r1p1` |
| `host.cpu.vendor.id` | string | Processor manufacturer identifier. A maximum 12-character string. [1] | `GenuineIntel` |
| `host.id` | string | Unique host ID. For Cloud, this must be the instance_id assigned by the cloud provider. For non-containerized systems, this should be the `machine-id`. See the table below for the sources to use to determine the `machine-id` based on operating system. | `fdbf79e8af94cb7f9e8df36789187052` |
| `host.image.id` | string | VM image ID or host OS image ID. For Cloud, this value is from the provider. | `ami-07b06b442921831e5` |
| `host.image.name` | string | Name of the VM image or OS install the host was instantiated from. | `infra-ami-eks-worker-node-7d4ec78312`; `CentOS-8-x86_64-1905` |
| `host.image.version` | string | The version string of the VM image or host OS as defined in [Version Attributes](/docs/resource/README.md#version-attributes). | `0.1` |
| `host.ip` | string[] | Available IP addresses of the host, excluding loopback interfaces. [2] | `[192.168.1.140, fe80::abc2:4a28:737a:609e]` |
| `host.mac` | string[] | Available MAC addresses of the host, excluding loopback interfaces. [3] | `[AC-DE-48-23-45-67, AC-DE-48-23-45-67-01-9F]` |
| `host.name` | string | Name of the host. On Unix systems, it may contain what the hostname command returns, or the fully qualified hostname, or another name specified by the user. | `opentelemetry-test` |
| `host.type` | string | Type of host. For Cloud, this must be the machine type. | `n1-standard-1` |

**[1]:** [CPUID](https://wiki.osdev.org/CPUID) command returns the vendor ID string in EBX, EDX and ECX registers. Writing these to memory in this order results in a 12-character string.

**[2]:** IPv4 Addresses MUST be specified in dotted-quad notation. IPv6 addresses MUST be specified in the [RFC 5952](https://www.rfc-editor.org/rfc/rfc5952.html) format.

**[3]:** MAC Addresses MUST be represented in [IEEE RA hexadecimal form](https://standards.ieee.org/wp-content/uploads/import/documents/tutorials/eui.pdf): as hyphen-separated octets in uppercase hexadecimal form from most to least significant.

`host.arch` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `amd64` | AMD64 |
| `arm32` | ARM32 |
| `arm64` | ARM64 |
| `ia64` | Itanium |
| `ppc32` | 32-bit PowerPC |
| `ppc64` | 64-bit PowerPC |
| `s390x` | IBM z/Architecture |
| `x86` | 32-bit x86 |
<!-- endsemconv -->