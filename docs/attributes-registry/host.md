
<!--- Hugo front matter used to generate the website version of this page:
--->

# HOST

- [host](#host)


## host Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `host.arch` | string | The CPU architecture the host system is running on.  | `amd64`; `arm32`; `arm64`; `ia64`; `ppc32`; `ppc64`; `s390x`; `x86` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.cpu.cache.l2.size` | int | The amount of level 2 memory cache available to the processor (in Bytes).  | `12288000` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.cpu.family` | string | Family or generation of the CPU.  | `6`; `PA-RISC 1.1e` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.cpu.model.id` | string | Model identifier. It provides more granular information about the CPU, distinguishing it from other CPUs within the same family.  | `6`; `9000/778/B180L` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.cpu.model.name` | string | Model designation of the processor.  | `11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.cpu.stepping` | string | Stepping or core revisions.  | `1`; `r1p1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.cpu.vendor.id` | string | Processor manufacturer identifier. A maximum 12-character string. [1] | `GenuineIntel` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.id` | string | Unique host ID. For Cloud, this must be the instance_id assigned by the cloud provider. For non-containerized systems, this should be the `machine-id`. See the table below for the sources to use to determine the `machine-id` based on operating system.  | `fdbf79e8af94cb7f9e8df36789187052` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.image.id` | string | VM image ID or host OS image ID. For Cloud, this value is from the provider.  | `ami-07b06b442921831e5` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.image.name` | string | Name of the VM image or OS install the host was instantiated from.  | `infra-ami-eks-worker-node-7d4ec78312`; `CentOS-8-x86_64-1905` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.image.version` | string | The version string of the VM image or host OS as defined in [Version Attributes](/docs/resource/README.md#version-attributes).  | `0.1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.ip` | string[] | Available IP addresses of the host, excluding loopback interfaces. [2] | `192.168.1.140`; `fe80::abc2:4a28:737a:609e` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.mac` | string[] | Available MAC addresses of the host, excluding loopback interfaces. [3] | `AC-DE-48-23-45-67`; `AC-DE-48-23-45-67-01-9F` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.name` | string | Name of the host. On Unix systems, it may contain what the hostname command returns, or the fully qualified hostname, or another name specified by the user.  | `opentelemetry-test` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `host.type` | string | Type of host. For Cloud, this must be the machine type.  | `n1-standard-1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|

**[1]:** [CPUID](https://wiki.osdev.org/CPUID) command returns the vendor ID string in EBX, EDX and ECX registers. Writing these to memory in this order results in a 12-character string.

**[2]:** IPv4 Addresses MUST be specified in dotted-quad notation. IPv6 addresses MUST be specified in the [RFC 5952](https://www.rfc-editor.org/rfc/rfc5952.html) format.

**[3]:** MAC Addresses MUST be represented in [IEEE RA hexadecimal form](https://standards.ieee.org/wp-content/uploads/import/documents/tutorials/eui.pdf): as hyphen-separated octets in uppercase hexadecimal form from most to least significant.


`host.arch` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `amd64` | AMD64 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `arm32` | ARM32 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `arm64` | ARM64 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ia64` | Itanium | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ppc32` | 32-bit PowerPC | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ppc64` | 64-bit PowerPC | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `s390x` | IBM z/Architecture | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `x86` | 32-bit x86 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

