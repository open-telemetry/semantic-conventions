<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Hardware
--->

# Semantic conventions for hardware metrics

**Status**: [Development][DocumentStatus]

This document describes instruments and attributes for common hardware level
metrics in OpenTelemetry. Consider the [general metric semantic conventions](/docs/general/metrics.md#general-guidelines)
when creating instruments not explicitly defined in the specification.

This document is being converted to specific hardware metrics, parts of this document that have already been
converted are now located in the [Hardware](/docs/hardware/README.md) folder and are no longer present in this file.

Please note that this is an [ongoing process](https://github.com/open-telemetry/semantic-conventions/issues/1309) and may take some time to complete.

<!-- Toc is maintained manually due to ongoing conversion -->

- [Common hardware attributes](/docs/registry/attributes/hardware.md)
- [Metric Instruments](#metric-instruments)
  - [`hw.` - Common hardware metrics](/docs/hardware/common.md)
  - [`hw.host.` - Physical host metrics](/docs/hardware/host.md)
  - [`hw.battery.` - Battery metrics](#hwbattery---battery-metrics)
  - [`hw.cpu.` - Physical processor metrics](#hwcpu---physical-processor-metrics)
  - [`hw.disk_controller.` - Disk controller metrics](#hwdisk_controller---disk-controller-metrics)
  - [`hw.enclosure.` - Enclosure metrics](#hwenclosure---enclosure-metrics)
  - [`hw.fan.` - Fan metrics](#hwfan---fan-metrics)
  - [`hw.gpu.` - GPU metrics](#hwgpu---gpu-metrics)
  - [`hw.logical_disk.`- Logical disk metrics](#hwlogical_disk--logical-disk-metrics)
  - [`hw.memory.` - Memory module metrics](#hwmemory---memory-module-metrics)
  - [`hw.network.` - Network adapter metrics](#hwnetwork---network-adapter-metrics)
  - [`hw.physical_disk.`- Physical disk metrics](#hwphysical_disk--physical-disk-metrics)
  - [`hw.power_supply.` - Power supply metrics](#hwpower_supply---power-supply-metrics)
  - [`hw.tape_drive.` - Tape drive metrics](#hwtape_drive---tape-drive-metrics)
  - [`hw.temperature.` - Temperature sensor metrics](#hwtemperature---temperature-sensor-metrics)
  - [`hw.voltage.` - Voltage sensor metrics](#hwvoltage---voltage-sensor-metrics)

> **Warning**
> Existing instrumentations and collector that are using
> [v1.21.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.21.0/docs/system/hardware-metrics.md)
> (or prior):
>
> * SHOULD NOT adopt any breaking changes from document until the system
>   semantic conventions are marked stable. Conventions include, but are not
>   limited to, attributes, metric names, and unit of measure.
> * SHOULD introduce a control mechanism to allow users to opt-in to the new
>   conventions once the migration plan is finalized.

## Metric instruments

### `hw.battery.` - Battery metrics

**Description:** A battery in a computer system or an UPS.

| Name                      | Description                                                                   | Units | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key(s)                                                            | Attribute Values                                      |
| ------------------------- | ----------------------------------------------------------------------------- | ----- | ------------------------------------------------- | ---------- | --------------------------------------------------------------------------- | ----------------------------------------------------- |
| `hw.battery.charge`       | Remaining fraction of battery charge                                          | 1     | Gauge                                             | Double     |                                                                             |                                                       |
| `hw.battery.charge.limit` | Lower limit of battery charge fraction to ensure proper operation             | 1     | Gauge                                             | Double     | `limit_type` (Recommended)                                                  | `critical`, `throttled`, `degraded`                   |
| `hw.battery.time_left`    | Time left before battery is completely charged or discharged                  | s     | Gauge                                             | Int        | `state` (Conditionally Required, if the battery is charging or discharging) | `charging`, `discharging`                             |
| `hw.status`               | Operational status: `1` (true) or `0` (false) for each of the possible states |       | UpDownCounter                                     | Int        | `state` (**Required**)                                                      | `ok`, `degraded`, `failed`, `charging`, `discharging` |
|                           |                                                                               |       |                                                   |            | `hw.type`                                                                   | `battery`                                             |

All `hw.battery.` metrics may include the below **Recommended** attributes to
describe the characteristics of the monitored battery:

| Attribute Key | Description                                   | Example                     |
| ------------- | --------------------------------------------- | --------------------------- |
| `chemistry`   | Chemistry of the battery                      | Nickel-Cadmium, Lithium-ion |
| `capacity`    | Design capacity in Watts-hours or Amper-hours | 9.3Ah                       |
| `model`       | Descriptive model name                        |                             |
| `vendor`      | Vendor name                                   |                             |

### `hw.cpu.` - Physical processor metrics

**Description:** Physical processor (as opposed to the logical processor seen by
the operating system for multi-core systems). A physical processor may include
many individual cores.

| Name                 | Description                                                                   | Units   | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key              | Attribute Values                                |
| -------------------- | ----------------------------------------------------------------------------- | ------- | ------------------------------------------------- | ---------- | -------------------------- | ----------------------------------------------- |
| `hw.errors`          | Total number of errors encountered and corrected by the CPU                   | {error} | Counter                                           | Int64      | `hw.type` (**Required**)   | `cpu`                                           |
| `hw.cpu.speed`       | CPU current frequency                                                         | Hz      | Gauge                                             | Int64      |                            |                                                 |
| `hw.cpu.speed.limit` | CPU maximum frequency                                                         | Hz      | Gauge                                             | Int64      | `limit_type` (Recommended) | `throttled`, `max`, `turbo`                     |
| `hw.status`          | Operational status: `1` (true) or `0` (false) for each of the possible states |         | UpDownCounter                                     | Int        | `state` (**Required**)     | `ok`, `degraded`, `failed`, `predicted_failure` |
|                      |                                                                               |         |                                                   |            | `hw.type` (**Required**)   | `cpu`                                           |

Additional **Recommended** attributes:

| Attribute Key | Description            | Example |
| ------------- | ---------------------- | ------- |
| `model`       | Descriptive model name |         |
| `vendor`      | Vendor name            |         |

### `hw.disk_controller.` - Disk controller metrics

**Description:** Controller that controls the physical disks and organize
them in RAID sets and logical disks that are exposed to the operating system.

| Name        | Description                                                                   | Units | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key            | Attribute Values           |
| ----------- | ----------------------------------------------------------------------------- | ----- | ------------------------------------------------- | ---------- | ------------------------ | -------------------------- |
| `hw.status` | Operational status: `1` (true) or `0` (false) for each of the possible states |       | UpDownCounter                                     | Int        | `state` (**Required**)   | `ok`, `degraded`, `failed` |
|             |                                                                               |       |                                                   |            | `hw.type` (**Required**) | `disk_controller`          |

Additional **Recommended** attributes:

| Attribute Key      | Description               | Example |
| ------------------ | ------------------------- | ------- |
| `bios_version`     | BIOS version              |         |
| `driver_version`   | Driver for the controller |         |
| `firmware_version` | Firmware version          |         |
| `model`            | Descriptive model name    |         |
| `serial_number`    | Serial number             |         |
| `vendor`           | Vendor name               |         |

### `hw.enclosure.` - Enclosure metrics

**Description:** Computer chassis (can be an expansion enclosure)

| Name        | Description                                                                   | Units | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key            | Attribute Values                   |
| ----------- | ----------------------------------------------------------------------------- | ----- | ------------------------------------------------- | ---------- | ------------------------ | ---------------------------------- |
| `hw.status` | Operational status: `1` (true) or `0` (false) for each of the possible states |       | UpDownCounter                                     | Int        | `state` (**Required**)   | `ok`, `degraded`, `failed`, `open` |
|             |                                                                               |       |                                                   |            | `hw.type` (**Required**) | `enclosure`                        |

Additional **Recommended** attributes:

| Attribute Key   | Description                                        | Example                   |
| --------------- | -------------------------------------------------- | ------------------------- |
| `bios_version`  | BIOS version                                       |                           |
| `model`         | Descriptive model name                             |                           |
| `serial_number` | Serial number                                      |                           |
| `type`          | Type of the enclosure (useful for modular systems) | Computer, Storage, Switch |
| `vendor`        | Vendor name                                        |                           |

### `hw.fan.` - Fan metrics

**Description:** Fan that keeps the air flowing to maintain the internal
temperature of a computer

| Name                 | Description                                                                   | Units | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key                  | Attribute Values                      |
| -------------------- | ----------------------------------------------------------------------------- | ----- | ------------------------------------------------- | ---------- | ------------------------------ | ------------------------------------- |
| `hw.fan.speed`       | Fan speed in revolutions per minute                                           | rpm   | Gauge                                             | Int        |                                |                                       |
| `hw.fan.speed.limit` | Speed limit in rpm                                                            | rpm   | Gauge                                             | Int        | `limit_type` (**Recommended**) | `low.critical`, `low.degraded`, `max` |
| `hw.fan.speed_ratio` | Fan speed expressed as a fraction of its maximum speed                        | 1     | Gauge                                             | Double     |                                |                                       |
| `hw.status`          | Operational status: `1` (true) or `0` (false) for each of the possible states |       | UpDownCounter                                     | Int        | `state` (**Required**)         | `ok`, `degraded`, `failed`            |
|                      |                                                                               |       |                                                   |            | `hw.type` (**Required**)       | `fan`                                 |

Additional **Recommended** attributes:

| Attribute Key     | Description                                   | Example          |
| ----------------- | --------------------------------------------- | ---------------- |
| `sensor_location` | Location of the fan in the computer enclosure | cpu0, ps1, INLET |

### `hw.gpu.` - GPU metrics

**Description:** Graphics Processing Unit (discrete)

| Name                        | Description                                                                   | Units   | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key                 | Attribute Values                                |
| --------------------------- | ----------------------------------------------------------------------------- | ------- | ------------------------------------------------- | ---------- | ----------------------------- | ----------------------------------------------- |
| `hw.errors`                 | Number of errors encountered by the GPU                                       | {error} | Counter                                           | Int64      | `hw.error.type` (Recommended) | `corrected`, `uncorrected`                      |
|                             |                                                                               |         |                                                   |            | `hw.type` (**Required**)      | `gpu`                                           |
| `hw.gpu.io`                 | Received and transmitted bytes by the GPU                                     | By      | Counter                                           | Int64      | `direction` (**Required**)    | `receive`, `transmit`                           |
| `hw.gpu.memory.limit`       | Size of the GPU memory                                                        | By      | UpDownCounter                                     | Int64      |                               |                                                 |
| `hw.gpu.memory.utilization` | Fraction of GPU memory used                                                   | 1       | Gauge                                             | Double     |                               |                                                 |
| `hw.gpu.memory.usage`       | GPU memory used                                                               | By      | UpDownCounter                                     | Int64      |                               |                                                 |
| `hw.gpu.power`              | GPU instantaneous power consumption in Watts                                  | W       | Gauge                                             | Double     |                               |                                                 |
| `hw.gpu.utilization`        | Fraction of time spent in a specific task                                     | 1       | Gauge                                             | Double     | `task` (Recommended)          | `decoder`, `encoder`, `general`                 |
| `hw.status`                 | Operational status: `1` (true) or `0` (false) for each of the possible states |         | UpDownCounter                                     | Int        | `state` (**Required**)        | `ok`, `degraded`, `failed`, `predicted_failure` |
|                             |                                                                               |         |                                                   |            | `hw.type` (**Required**)      | `gpu`                                           |

Additional **Recommended** attributes:

| Attribute Key      | Description               | Example |
| ------------------ | ------------------------- | ------- |
| `driver_version`   | Driver for the controller |         |
| `firmware_version` | Firmware version          |         |
| `model`            | Descriptive model name    |         |
| `serial_number`    | Serial number             |         |
| `vendor`           | Vendor name               |         |

### `hw.logical_disk.`- Logical disk metrics

**Description:** Storage extent presented as a physical disk by a disk
controller to the operating system (e.g. a RAID 1 set made of 2 disks, and exposed
as /dev/hdd0 by the controller).

| Name                          | Description                                                                   | Units   | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key            | Attribute Values           |
| ----------------------------- | ----------------------------------------------------------------------------- | ------- | ------------------------------------------------- | ---------- | ------------------------ | -------------------------- |
| `hw.errors`                   | Number of errors encountered on this logical disk                             | {error} | Counter                                           | Int64      | `hw.type` (**Required**) | `logical_disk`             |
| `hw.logical_disk.limit`       | Size of the logical disk                                                      | By      | UpDownCounter                                     | Int64      |                          |                            |
| `hw.logical_disk.usage`       | Logical disk space usage                                                      | By      | UpDownCounter                                     | Int64      | `state` (**Required**)   | `used`, `free`             |
| `hw.logical_disk.utilization` | Logical disk space utilization as a fraction                                  | 1       | Gauge                                             | Double     | `state` (**Required**)   | `used`, `free`             |
| `hw.status`                   | Operational status: `1` (true) or `0` (false) for each of the possible states |         | UpDownCounter                                     | Int        | `state` (**Required**)   | `ok`, `degraded`, `failed` |
|                               |                                                                               |         |                                                   |            | `hw.type` (**Required**) | `logical_disk`             |

Additional **Recommended** attributes:

| Attribute Key | Description | Example   |
| ------------- | ----------- | --------- |
| `raid_level`  | RAID Level  | `RAID0+1` |

### `hw.memory.` - Memory module metrics

**Description:** A memory module in a computer system.

| Name             | Description                                                                   | Units   | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key            | Attribute Values                                |
| ---------------- | ----------------------------------------------------------------------------- | ------- | ------------------------------------------------- | ---------- | ------------------------ | ----------------------------------------------- |
| `hw.errors`      | Number of errors encountered on this memory module                            | {error} | Counter                                           | Int64      | `hw.type` (**Required**) | `memory`                                        |
| `hw.memory.size` | Size of the memory module                                                     | By      | UpDownCounter                                     | Int64      |                          |                                                 |
| `hw.status`      | Operational status: `1` (true) or `0` (false) for each of the possible states |         | UpDownCounter                                     | Int        | `state` (**Required**)   | `ok`, `degraded`, `failed`, `predicted_failure` |
|                  |                                                                               |         |                                                   |            | `hw.type` (**Required**) | `memory`                                        |

Additional **Recommended** attributes:

| Attribute Key   | Description               | Example |
| --------------- | ------------------------- | ------- |
| `model`         | Descriptive model name    |         |
| `serial_number` | Serial number             |         |
| `type`          | Type of the memory module | `DDR5`  |
| `vendor`        | Vendor name               |         |

### `hw.network.` - Network adapter metrics

**Description:** A physical network interface, or a network interface controller
(NIC), excluding software-based virtual adapters and loopbacks. For example, a
physical network interface on a server, switch, router or firewall, an HBA, a
fiber channel port or a Wi-Fi adapter.

| Name                               | Description                                                                                                  | Units    | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key                 | Attribute Values                  |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------- | ---------- | ----------------------------- | --------------------------------- |
| `hw.errors`                        | Number of errors encountered by the network adapter                                                          | {error}  | Counter                                           | Int64      | `hw.error.type` (Recommended) | `zero_buffer_credit`, `crc`, etc. |
|                                    |                                                                                                              |          |                                                   |            | `hw.type` (**Required**)      | `network`                         |
|                                    |                                                                                                              |          |                                                   |            | `direction` (Recommended)     | `receive`, `transmit`             |
| `hw.network.bandwidth.limit`       | Link speed                                                                                                   | By/s     | UpDownCounter                                     | Int64      |                               |                                   |
| `hw.network.bandwidth.utilization` | Utilization of the network bandwidth as a fraction                                                           | 1        | Gauge                                             | Double     |                               |                                   |
| `hw.network.io`                    | Received and transmitted network traffic in bytes                                                            | By       | Counter                                           | Int64      | `direction` (**Required**)    | `receive`, `transmit`             |
| `hw.network.packets`               | Received and transmitted network traffic in packets (or frames)                                              | {packet} | Counter                                           | Int64      | `direction` (**Required**)    | `receive`, `transmit`             |
| `hw.network.up`                    | Link status: `1` (up) or `0` (down)                                                                          |          | UpDownCounter                                     | Int        |                               |                                   |
| `hw.status`                        | Operational status, regardless of the link status: `1` (true) or `0` (false) for each of the possible states |          | UpDownCounter                                     | Int        | `state` (**Required**)        | `ok`, `degraded`, `failed`        |
|                                    |                                                                                                              |          |                                                   |            | `hw.type` (**Required**)      | `network`                         |

Additional **Recommended** attributes:

| Attribute Key       | Description                                                 | Example                     |
| ------------------- | ----------------------------------------------------------- | --------------------------- |
| `model`             | Descriptive model name                                      |                             |
| `logical_addresses` | Logical addresses of the adapter (e.g. IP address, or WWPN) | `172.16.8.21, 57.11.193.42` |
| `physical_address`  | Physical address of the adapter (e.g. MAC address, or WWNN) | `00-90-F5-E9-7B-36`         |
| `serial_number`     | Serial number                                               |                             |
| `vendor`            | Vendor name                                                 |                             |

### `hw.physical_disk.`- Physical disk metrics

**Description:** Physical hard drive (HDD or SDD)

| Name                                     | Description                                                                                 | Units   | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key                   | Attribute Values                                |
| ---------------------------------------- | ------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------- | ---------- | ------------------------------- | ----------------------------------------------- |
| `hw.errors`                              | Number of errors encountered on this disk                                                   | {error} | Counter                                           | Int64      | `hw.error.type` (Recommended)   | `bad_sector`, `write`, etc.                     |
|                                          |                                                                                             |         |                                                   |            | `hw.type` (**Required**)        | `physical_disk`                                 |
| `hw.physical_disk.endurance_utilization` | Endurance remaining for this SSD disk                                                       | 1       | Gauge                                             | Double     | `state` (**Required**)          | `remaining`                                     |
| `hw.physical_disk.size`                  | Size of the disk                                                                            | By      | UpDownCounter                                     | Int64      |                                 |                                                 |
| `hw.physical_disk.smart`                 | Value of the corresponding [S.M.A.R.T.](https://wikipedia.org/wiki/S.M.A.R.T.) attribute | 1       | Gauge                                             | Int        | `smart_attribute` (Recommended) | `Seek Error Rate`, `Spin Retry Count`, etc.     |
| `hw.status`                              | Operational status: `1` (true) or `0` (false) for each of the possible states               |         | UpDownCounter                                     | Int        | `state` (**Required**)          | `ok`, `degraded`, `failed`, `predicted_failure` |
|                                          |                                                                                             |         |                                                   |            | `hw.type` (**Required**)        | `physical_disk`                                 |

Additional **Recommended** attributes:

| Attribute Key      | Description            | Example             |
| ------------------ | ---------------------- | ------------------- |
| `firmware_version` | Firmware version       |                     |
| `model`            | Descriptive model name |                     |
| `serial_number`    | Serial number          |                     |
| `type`             | Type of the disk       | `HDD`, `SSD`, `10K` |
| `vendor`           | Vendor name            |                     |

### `hw.power_supply.` - Power supply metrics

**Description:** Power supply converting AC current to DC used by the
motherboard and the GPUs

| Name                          | Description                                                                   | Units | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key              | Attribute Values               |
| ----------------------------- | ----------------------------------------------------------------------------- | ----- | ------------------------------------------------- | ---------- | -------------------------- | ------------------------------ |
| `hw.power_supply.limit`       | Maximum power output of the power supply                                      | W     | UpDownCounter                                     | Int64      | `limit_type` (Recommended) | `max`, `critical`, `throttled` |
| `hw.power_supply.utilization` | Utilization of the power supply as a fraction of its maximum output           | 1     | Gauge                                             | Double     |                            |                                |
| `hw.status`                   | Operational status: `1` (true) or `0` (false) for each of the possible states |       | UpDownCounter                                     | Int        | `state` (**Required**)     | `ok`, `degraded`, `failed`     |
|                               |                                                                               |       |                                                   |            | `hw.type` (**Required**)   | `power_supply`                 |

Additional **Recommended** attributes:

| Attribute Key   | Description            | Example |
| --------------- | ---------------------- | ------- |
| `model`         | Descriptive model name |         |
| `serial_number` | Serial number          |         |
| `vendor`        | Vendor name            |         |

### `hw.tape_drive.` - Tape drive metrics

**Description:** A tape drive in a computer or in a tape library (excluding
virtual tape libraries)

| Name                       | Description                                                                   | Units       | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key            | Attribute Values                             |
| -------------------------- | ----------------------------------------------------------------------------- | ----------- | ------------------------------------------------- | ---------- | ------------------------ | -------------------------------------------- |
| `hw.errors`                | Number of errors encountered by the tape drive                                | {error}     | Counter                                           | Int64      | `hw.error.type`          | `read`, `write`, `mount`, etc.               |
|                            |                                                                               |             |                                                   |            | `hw.type` (**Required**) | `tape_drive`                                 |
| `hw.tape_drive.operations` | Operations performed by the tape drive                                        | {operation} | Counter                                           | Int64      | `type` (Recommended)     | `mount`, `unmount`, `clean`                  |
| `hw.status`                | Operational status: `1` (true) or `0` (false) for each of the possible states |             | UpDownCounter                                     | Int        | `state` (**Required**)   | `ok`, `degraded`, `failed`, `needs_cleaning` |
|                            |                                                                               |             |                                                   |            | `hw.type` (**Required**) | `tape_drive`                                 |

Additional **Recommended** attributes:

| Attribute Key   | Description            | Example |
| --------------- | ---------------------- | ------- |
| `model`         | Descriptive model name |         |
| `serial_number` | Serial number          |         |
| `vendor`        | Vendor name            |         |

### `hw.temperature.` - Temperature sensor metrics

**Description:** A temperature sensor, either numeric or discrete

| Name                   | Description                                                                                               | Units | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key              | Attribute Values                                                 |
| ---------------------- | --------------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------- | ---------- | -------------------------- | ---------------------------------------------------------------- |
| `hw.temperature`       | Temperature in degrees Celsius                                                                            | Cel   | Gauge                                             | Double     |                            |                                                                  |
| `hw.temperature.limit` | Temperature limit in degrees Celsius                                                                      | Cel   | Gauge                                             | Double     | `limit_type` (Recommended) | `low.critical`, `low.degraded`, `high.degraded`, `high.critical` |
| `hw.status`            | Whether the temperature is within normal range: `1` (true) or `0` (false) for each of the possible states |       | UpDownCounter                                     | Int        | `state` (**Required**)     | `ok`, `degraded`, `failed`                                       |
|                        |                                                                                                           |       |                                                   |            | `hw.type` (**Required**)   | `temperature`                                                    |

Additional **Recommended** attributes:

| Attribute Key     | Description            | Example    |
| ----------------- | ---------------------- | ---------- |
| `sensor_location` | Location of the sensor | `CPU0_DIE` |

### `hw.voltage.` - Voltage sensor metrics

**Description:** A voltage sensor, either numeric or discrete

| Name                 | Description                                                                                           | Units | Instrument Type ([*](/docs/general/metrics.md#instrument-types)) | Value Type | Attribute Key              | Attribute Values                                                 |
| -------------------- | ----------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------- | ---------- | -------------------------- | ---------------------------------------------------------------- |
| `hw.voltage.limit`   | Voltage limit in Volts                                                                                | V     | Gauge                                             | Double     | `limit_type` (Recommended) | `low.critical`, `low.degraded`, `high.degraded`, `high.critical` |
| `hw.voltage.nominal` | Nominal (expected) voltage                                                                            | V     | Gauge                                             | Double     |                            |                                                                  |
| `hw.voltage`         | Voltage measured by the sensor                                                                        | V     | Gauge                                             | Double     |                            |                                                                  |
| `hw.status`          | Whether the voltage is within normal range: `1` (true) or `0` (false) for each of the possible states |       | UpDownCounter                                     | Int        | `state` (**Required**)     | `ok`, `degraded`, `failed`                                       |
|                      |                                                                                                       |       |                                                   |            | `hw.type` (**Required**)   | `voltage`                                                        |

Additional **Recommended** attributes:

| Attribute Key     | Description            | Example    |
| ----------------- | ---------------------- | ---------- |
| `sensor_location` | Location of the sensor | `PS0 V3_3` |

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
