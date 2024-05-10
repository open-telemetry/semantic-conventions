<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Hardware Common Metrics
--->

# Semantic Conventions for Hardware Common Metrics

**Status**: [Experimental][DocumentStatus]

All metrics in `hw.` instruments should be attached to a [Host Resource](/docs/resource/host.md)
and therefore inherit its attributes, like `host.id` and `host.name`.

Additionally, all metrics in `hw.` instruments have the following attributes:

<!-- semconv hardware.attributes.common -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`hw.id`](/docs/attributes-registry/hw.md) | string | An identifier for the hardware component, unique within the monitored host | `win32battery_battery_testsysa33_1` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.name`](/docs/attributes-registry/hw.md) | string | An easily-recognizable name for the hardware component | `eth0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.parent`](/docs/attributes-registry/hw.md) | string | Unique identifier of the parent component (typically the `id` attribute of the enclosure, or disk controller) | `dellStorage_perc_0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Common hardware metrics

The below metrics apply to any type of hardware component.

These common `hw.` metrics include the below attributes to describe the
monitored component:
<!-- semconv metric.hardware.attributes(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`hw.id`](/docs/attributes-registry/hw.md) | string | An identifier for the hardware component, unique within the monitored host | `win32battery_battery_testsysa33_1` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.type`](/docs/attributes-registry/hw.md) | string | Type of the component | `battery`; `cpu`; `disk_controller` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.name`](/docs/attributes-registry/hw.md) | string | An easily-recognizable name for the hardware component | `eth0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.parent`](/docs/attributes-registry/hw.md) | string | Unique identifier of the parent component (typically the `id` attribute of the enclosure, or disk controller) | `dellStorage_perc_0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`hw.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `battery` | Battery | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cpu` | CPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `disk_controller` | Disk controller | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `enclosure` | Enclosure | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fan` | Fan | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gpu` | GPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `logical_disk` | Logical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `memory` | Memory | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network` | Network | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `physical_disk` | Physical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `power_supply` | Power supply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tape_drive` | Tape drive | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `temperature` | Temperature | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `voltage` | Voltage | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `hw.energy`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.hardware.energy(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `hw.energy` | Counter | `J` | Energy consumed by the component, in joules | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.hardware.energy(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`hw.id`](/docs/attributes-registry/hw.md) | string | An identifier for the hardware component, unique within the monitored host | `win32battery_battery_testsysa33_1` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.type`](/docs/attributes-registry/hw.md) | string | Type of the component | `battery`; `cpu`; `disk_controller` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.name`](/docs/attributes-registry/hw.md) | string | An easily-recognizable name for the hardware component | `eth0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.parent`](/docs/attributes-registry/hw.md) | string | Unique identifier of the parent component (typically the `id` attribute of the enclosure, or disk controller) | `dellStorage_perc_0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`hw.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `battery` | Battery | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cpu` | CPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `disk_controller` | Disk controller | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `enclosure` | Enclosure | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fan` | Fan | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gpu` | GPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `logical_disk` | Logical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `memory` | Memory | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network` | Network | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `physical_disk` | Physical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `power_supply` | Power supply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tape_drive` | Tape drive | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `temperature` | Temperature | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `voltage` | Voltage | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `hw.errors`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.hardware.errors(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `hw.errors` | Counter | `{errors}` | Number of errors encountered by the component | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

<!-- semconv metric.hardware.errors(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`hw.id`](/docs/attributes-registry/hw.md) | string | An identifier for the hardware component, unique within the monitored host | `win32battery_battery_testsysa33_1` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.type`](/docs/attributes-registry/hw.md) | string | Type of the component | `battery`; `cpu`; `disk_controller` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.error.type`](/docs/attributes-registry/hw.md) | string | The type of error encountered by the component | `` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.name`](/docs/attributes-registry/hw.md) | string | An easily-recognizable name for the hardware component | `eth0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.parent`](/docs/attributes-registry/hw.md) | string | Unique identifier of the parent component (typically the `id` attribute of the enclosure, or disk controller) | `dellStorage_perc_0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`hw.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `battery` | Battery | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cpu` | CPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `disk_controller` | Disk controller | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `enclosure` | Enclosure | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fan` | Fan | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gpu` | GPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `logical_disk` | Logical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `memory` | Memory | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network` | Network | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `physical_disk` | Physical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `power_supply` | Power supply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tape_drive` | Tape drive | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `temperature` | Temperature | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `voltage` | Voltage | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `hw.power`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.hardware.power(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `hw.power` | Gauge | `W` | Instantaneous power consumed by the component, in Watts [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** `hw.energy` is preferred
<!-- endsemconv -->

<!-- semconv metric.hardware.power(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`hw.id`](/docs/attributes-registry/hw.md) | string | An identifier for the hardware component, unique within the monitored host | `win32battery_battery_testsysa33_1` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.type`](/docs/attributes-registry/hw.md) | string | Type of the component | `battery`; `cpu`; `disk_controller` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.name`](/docs/attributes-registry/hw.md) | string | An easily-recognizable name for the hardware component | `eth0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.parent`](/docs/attributes-registry/hw.md) | string | Unique identifier of the parent component (typically the `id` attribute of the enclosure, or disk controller) | `dellStorage_perc_0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`hw.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `battery` | Battery | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cpu` | CPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `disk_controller` | Disk controller | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `enclosure` | Enclosure | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fan` | Fan | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gpu` | GPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `logical_disk` | Logical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `memory` | Memory | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network` | Network | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `physical_disk` | Physical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `power_supply` | Power supply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tape_drive` | Tape drive | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `temperature` | Temperature | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `voltage` | Voltage | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Metric: `hw.status`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.hardware.status(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    | Stability |
| -------- | --------------- | ----------- | -------------- | --------- |
| `hw.status` | UpDownCounter | `1` | Operational status: `1` (true) or `0` (false) for each of the possible states [1] | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** `hw.status` is currently specified as an *UpDownCounter* but would ideally be represented using a [*StateSet* as defined in OpenMetrics](https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md#stateset). This semantic convention will be updated once *StateSet* is specified in OpenTelemetry. This planned change  is not expected to have any consequence on the way users query their timeseries backend to retrieve the  values of `hw.status` over time.
<!-- endsemconv -->

<!-- semconv metric.hardware.status(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`hw.id`](/docs/attributes-registry/hw.md) | string | An identifier for the hardware component, unique within the monitored host | `win32battery_battery_testsysa33_1` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.state`](/docs/attributes-registry/hw.md) | string | The current state of the component | `ok`; `degraded`; `failed` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.type`](/docs/attributes-registry/hw.md) | string | Type of the component | `battery`; `cpu`; `disk_controller` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.name`](/docs/attributes-registry/hw.md) | string | An easily-recognizable name for the hardware component | `eth0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`hw.parent`](/docs/attributes-registry/hw.md) | string | Unique identifier of the parent component (typically the `id` attribute of the enclosure, or disk controller) | `dellStorage_perc_0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`hw.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `ok` | Ok | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `degraded` | Degraded | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `failed` | Failed | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`hw.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `battery` | Battery | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `cpu` | CPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `disk_controller` | Disk controller | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `enclosure` | Enclosure | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fan` | Fan | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `gpu` | GPU | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `logical_disk` | Logical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `memory` | Memory | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `network` | Network | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `physical_disk` | Physical disk | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `power_supply` | Power supply | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tape_drive` | Tape drive | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `temperature` | Temperature | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `voltage` | Voltage | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
[MetricRecommended]: /docs/general/metric-requirement-level.md#recommended
