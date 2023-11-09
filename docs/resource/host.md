# Host

**Status**: [Experimental][DocumentStatus]

**type:** `host`

**Description:** A host is defined as a computing instance. For example, physical servers, virtual machines, switches or disk array.

The `host.*` namespace SHOULD be exclusively used to capture resource attributes.
To report host metrics, the `system.*` namespace SHOULD be used.

<!-- semconv host -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`host.arch`](../attributes-registry/host.md) | string | The CPU architecture the host system is running on. | `amd64` | Recommended |
| [`host.id`](../attributes-registry/host.md) | string | Unique host ID. For Cloud, this must be the instance_id assigned by the cloud provider. For non-containerized systems, this should be the `machine-id`. See the table below for the sources to use to determine the `machine-id` based on operating system. | `fdbf79e8af94cb7f9e8df36789187052` | Recommended |
| [`host.image.id`](../attributes-registry/host.md) | string | VM image ID or host OS image ID. For Cloud, this value is from the provider. | `ami-07b06b442921831e5` | Recommended |
| [`host.image.name`](../attributes-registry/host.md) | string | Name of the VM image or OS install the host was instantiated from. | `infra-ami-eks-worker-node-7d4ec78312`; `CentOS-8-x86_64-1905` | Recommended |
| [`host.image.version`](../attributes-registry/host.md) | string | The version string of the VM image or host OS as defined in [Version Attributes](../resource/README.md#version-attributes). | `0.1` | Recommended |
| [`host.ip`](../attributes-registry/host.md) | string[] | Available IP addresses of the host, excluding loopback interfaces. [1] | `[192.168.1.140, fe80::abc2:4a28:737a:609e]` | Recommended |
| [`host.mac`](../attributes-registry/host.md) | string[] | Available MAC addresses of the host, excluding loopback interfaces. [2] | `[AC-DE-48-23-45-67, AC-DE-48-23-45-67-01-9F]` | Recommended |
| [`host.type`](../attributes-registry/host.md) | string | Type of host. For Cloud, this must be the machine type. | `n1-standard-1` | Recommended |

**[1]:** IPv4 Addresses MUST be specified in dotted-quad notation. IPv6 addresses MUST be specified in the [RFC 5952](https://www.rfc-editor.org/rfc/rfc5952.html) format.

**[2]:** MAC Addresses MUST be represented in [IEEE RA hexadecimal form](https://standards.ieee.org/wp-content/uploads/import/documents/tutorials/eui.pdf): as hyphen-separated octets in uppercase hexadecimal form from most to least significant.
<!-- endsemconv -->

**type:** `host.cpu`

<!-- semconv host.cpu -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`host.cache.l2.size`](../attributes-registry/host.md) | int | The amount of level 2 memory cache available to the processor (in Bytes). | `12288000` | Opt-In |
| [`host.family`](../attributes-registry/host.md) | int | Numeric value specifying the family or generation of the CPU. | `6` | Opt-In |
| [`host.model.id`](../attributes-registry/host.md) | int | Model identifier. It provides more granular information about the CPU, distinguishing it from other CPUs within the same family. | `6` | Opt-In |
| [`host.model.name`](../attributes-registry/host.md) | string | Model designation of the processor. | `11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz` | Opt-In |
| [`host.stepping`](../attributes-registry/host.md) | int | Stepping or core revisions. | `1` | Opt-In |
| [`host.vendor.id`](../attributes-registry/host.md) | string | Processor manufacturer identifier. A maximum 12-character string. [1] | `GenuineIntel` | Opt-In |

**[1]:** [CPUID](https://wiki.osdev.org/CPUID) command returns the vendor ID string in EBX, EDX and ECX registers. Writing these to memory in this order results in a 12-character string.
<!-- endsemconv -->

## Collecting host.id from non-containerized systems

### Non-privileged Machine ID Lookup

When collecting `host.id` for non-containerized systems non-privileged lookups
of the machine id are preferred. SDK detector implementations MUST use the
sources listed below to obtain the machine id.

| OS      | Primary                                                                             | Fallback                               |
|---------|-------------------------------------------------------------------------------------|----------------------------------------|
| Linux   | contents of `/etc/machine-id`                                                       | contents of `/var/lib/dbus/machine-id` |
| BSD     | contents of `/etc/hostid`                                                           | output of `kenv -q smbios.system.uuid` |
| MacOS   | `IOPlatformUUID` line from the output of `ioreg -rd1 -c "IOPlatformExpertDevice"`   | -                                      |
| Windows | `MachineGuid` from registry `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography` | -                                      |

### Privileged Machine ID Lookup

The `host.id` can be looked up using privileged sources. For example, Linux
systems can use the output of `dmidecode -t system`, `dmidecode -t baseboard`,
`dmidecode -t chassis`, or read the corresponding data from the filesystem
(e.g. `cat /sys/devices/virtual/dmi/id/product_id`,
`cat /sys/devices/virtual/dmi/id/product_uuid`, etc), however, SDK resource
detector implementations MUST not collect `host.id` from privileged sources. If
privileged lookup of `host.id` is required, the value should be injected via the
`OTEL_RESOURCE_ATTRIBUTES` environment variable.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
