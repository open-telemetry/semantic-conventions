# System

<!-- toc -->

- [CPU attributes](#cpu-attributes)
- [Memory attributes](#memory-attributes)
- [Paging attributes](#paging-attributes)
- [Filesystem attributes](#filesystem-attributes)
- [Network attributes](#network-attributes)
- [Process attributes](#process-attributes)
- [Deprecated System Attributes](#deprecated-system-attributes)

<!-- tocstop -->

<!-- semconv registry.system(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.device` | string | The device identifier | `(identifier)` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## CPU attributes

<!-- semconv registry.system.cpu(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.cpu.logical_number` | int | The logical CPU number [0..n-1] | `1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `system.cpu.state` | string | The state of the CPU | `idle`; `interrupt` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.cpu.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `user` | user | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `system` | system | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `nice` | nice | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `idle` | idle | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `iowait` | iowait | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `interrupt` | interrupt | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `steal` | steal | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Memory attributes

<!-- semconv registry.system.memory(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.memory.state` | string | The memory state | `free`; `cached` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.memory.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `used` | used | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `free` | free | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `buffers` | buffers | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cached` | cached | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `shared` | shared | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Removed, report shared memory usage with `metric.system.memory.shared` metric |
<!-- endsemconv -->

## Paging attributes

<!-- semconv registry.system.paging(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.paging.direction` | string | The paging access direction | `in` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `system.paging.state` | string | The memory paging state | `free` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `system.paging.type` | string | The memory paging type | `minor` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.paging.direction` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `in` | in | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `out` | out | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.paging.state` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `used` | used | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `free` | free | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.paging.type` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `major` | major | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `minor` | minor | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Filesystem attributes

<!-- semconv registry.system.filesystem(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.filesystem.mode` | string | The filesystem mode | `rw, ro` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `system.filesystem.mountpoint` | string | The filesystem mount path | `/mnt/data` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `system.filesystem.state` | string | The filesystem state | `used` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `system.filesystem.type` | string | The filesystem type | `ext4` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.filesystem.state` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `used` | used | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `free` | free | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `reserved` | reserved | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.filesystem.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `fat32` | fat32 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `exfat` | exfat | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ntfs` | ntfs | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `refs` | refs | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `hfsplus` | hfsplus | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ext4` | ext4 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Network attributes

<!-- semconv registry.system.network(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.network.state` | string | A stateless protocol MUST NOT set this attribute | `close_wait` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.network.state` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `close` | close | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `close_wait` | close_wait | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `closing` | closing | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `delete` | delete | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `established` | established | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fin_wait_1` | fin_wait_1 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fin_wait_2` | fin_wait_2 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `last_ack` | last_ack | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `listen` | listen | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `syn_recv` | syn_recv | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `syn_sent` | syn_sent | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `time_wait` | time_wait | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Process attributes

<!-- semconv registry.system.process(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.process.status` | string | The process state, e.g., [Linux Process State Codes](https://man7.org/linux/man-pages/man1/ps.1.html#PROCESS_STATE_CODES) | `running` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`system.process.status` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `running` | running | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `sleeping` | sleeping | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `stopped` | stopped | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `defunct` | defunct | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Deprecated System Attributes

<!-- semconv registry.system.deprecated(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.processes.status` | string | Deprecated, use `system.process.status` instead. | `running` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Replaced by `system.process.status`. |

`system.processes.status` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `running` | running | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `sleeping` | sleeping | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `stopped` | stopped | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `defunct` | defunct | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->
