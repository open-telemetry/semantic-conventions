<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Runtime Environment
--->

# Semantic Conventions for BEAM Metrics

**Status**: [Experimental][DocumentStatus]

This document describes semantic conventions for BEAM in OpenTelemetry.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [BEAM Atom](#beam-atom)
  - [Metric: `beam.atom.count`](#metric-beamatomcount)
  - [Metric: `beam.atom.limit`](#metric-beamatomlimit)
- [BEAM CPU](#beam-cpu)
  - [Metric: `beam.cpu.async.time`](#metric-beamcpuasynctime)
  - [Metric: `beam.cpu.aux.time`](#metric-beamcpuauxtime)
  - [Metric: `beam.cpu.dirty_cpu_scheduler.count`](#metric-beamcpudirty_cpu_schedulercount)
  - [Metric: `beam.cpu.dirty_cpu_scheduler.online`](#metric-beamcpudirty_cpu_scheduleronline)
  - [Metric: `beam.cpu.dirty_cpu_scheduler.run_queue_length`](#metric-beamcpudirty_cpu_schedulerrun_queue_length)
  - [Metric: `beam.cpu.dirty_cpu_scheduler.time`](#metric-beamcpudirty_cpu_schedulertime)
  - [Metric: `beam.cpu.dirty_io_scheduler.count`](#metric-beamcpudirty_io_schedulercount)
  - [Metric: `beam.cpu.dirty_io_scheduler.online`](#metric-beamcpudirty_io_scheduleronline)
  - [Metric: `beam.cpu.dirty_io_scheduler.run_queue_length`](#metric-beamcpudirty_io_schedulerrun_queue_length)
  - [Metric: `beam.cpu.dirty_io_scheduler.time`](#metric-beamcpudirty_io_schedulertime)
  - [Metric: `beam.cpu.logical_processors`](#metric-beamcpulogical_processors)
  - [Metric: `beam.cpu.logical_processors_available`](#metric-beamcpulogical_processors_available)
  - [Metric: `beam.cpu.logical_processors_online`](#metric-beamcpulogical_processors_online)
  - [Metric: `beam.cpu.poll.time`](#metric-beamcpupolltime)
  - [Metric: `beam.cpu.scheduler.count`](#metric-beamcpuschedulercount)
  - [Metric: `beam.cpu.scheduler.online`](#metric-beamcpuscheduleronline)
  - [Metric: `beam.cpu.scheduler.run_queues_length`](#metric-beamcpuschedulerrun_queues_length)
  - [Metric: `beam.cpu.scheduler.time`](#metric-beamcpuschedulertime)
  - [Metric: `beam.cpu.thread_pool_size`](#metric-beamcputhread_pool_size)
- [BEAM ETS](#beam-ets)
  - [Metric: `beam.ets.limit`](#metric-beametslimit)
- [BEAM Memory](#beam-memory)
  - [Metric: `beam.memory.allocated`](#metric-beammemoryallocated)
  - [Metric: `beam.memory.allocators`](#metric-beammemoryallocators)
  - [Metric: `beam.memory.atoms`](#metric-beammemoryatoms)
  - [Metric: `beam.memory.garbage_collection.bytes_reclaimed`](#metric-beammemorygarbage_collectionbytes_reclaimed)
  - [Metric: `beam.memory.garbage_collection.count`](#metric-beammemorygarbage_collectioncount)
  - [Metric: `beam.memory.garbage_collection.words_reclaimed`](#metric-beammemorygarbage_collectionwords_reclaimed)
  - [Metric: `beam.memory.processes`](#metric-beammemoryprocesses)
  - [Metric: `beam.memory.system`](#metric-beammemorysystem)
- [BEAM Port](#beam-port)
  - [Metric: `beam.port.count`](#metric-beamportcount)
  - [Metric: `beam.port.io`](#metric-beamportio)
  - [Metric: `beam.port.limit`](#metric-beamportlimit)
- [BEAM Process](#beam-process)
  - [Metric: `beam.process.context_switches`](#metric-beamprocesscontext_switches)
  - [Metric: `beam.process.count`](#metric-beamprocesscount)
  - [Metric: `beam.process.cpu.time`](#metric-beamprocesscputime)
  - [Metric: `beam.process.limit`](#metric-beamprocesslimit)
  - [Metric: `beam.process.reductions`](#metric-beamprocessreductions)
- [BEAM System](#beam-system)
  - [Metric: `beam.system.wordsize`](#metric-beamsystemwordsize)

<!-- tocstop -->

## BEAM Atom

**Status**: [Experimental][DocumentStatus]

**Description:** BEAM metrics captured under the namespace `beam.atom.*`

### Metric: `beam.atom.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.atom.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.atom_count` | UpDownCounter | `{atom}` | The number of atom currently existing at the local node. |
<!-- endsemconv -->

<!-- semconv metric.beam.atom.count(full) -->
<!-- endsemconv -->

### Metric: `beam.atom.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.atom.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.atom_limit` | UpDownCounter | `{atom}` | The maximum number of simultaneously existing atoms at the local node. |
<!-- endsemconv -->

<!-- semconv metric.beam.atom.limit(full) -->
<!-- endsemconv -->

## BEAM CPU

**Status**: [Experimental][DocumentStatus]

**Description:** BEAM metrics captured under the namespace `beam.cpu.*`

### Metric: `beam.cpu.async.time`

This metric is [Opt-In][MetricOptIn].

<!-- semconv metric.beam.cpu.async.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.async.time` | Counter | `s` | Async threads are used by various linked-in drivers (mainly the file drivers) do offload non-CPU intensive work. See erl +A for more details. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.async.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `beam.cpu.logical_number` | int | The logical thread number [0..n-1] | `1` | Recommended |
| `beam.cpu.work` | string | The work performed for this data point. | `gc` | Recommended |

`beam.cpu.work` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `aux` | Time spent handling auxiliary jobs. |
| `check_io` | Time spent checking for new I/O events. |
| `emulator` | Time spent executing Erlang processes. |
| `gc` | Time spent doing garbage collection. When extra states are enabled this is the time spent doing non-fullsweep garbage collections. |
| `other` | Time spent doing unaccounted things. |
| `port` | Time spent executing ports. |
| `sleep` | Time spent sleeping. |
| `alloc` | Time spent managing memory. Without extra states this time is spread out over all other states. |
| `bif` | Time spent in BIFs. Without extra states this time is part of the emulator state. |
| `busy_wait` | Time spent busy waiting. |
| `ets` | Time spent executing ETS BIFs. Without extra states this time is part of the emulator state. |
| `gc_full` | Time spent doing fullsweep garbage collection. Without extra states this time is part of the gc state. |
| `nif` | Time spent in NIFs. Without extra states this time is part of the emulator state. |
| `send` | Time spent sending messages (processes only). Without extra states this time is part of the emulator state. |
| `timers` | Time spent managing timers. Without extra states this time is part of the other state. |
<!-- endsemconv -->

### Metric: `beam.cpu.aux.time`

This metric is [Opt-In][MetricOptIn].

<!-- semconv metric.beam.cpu.aux.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.aux.time` | Counter | `s` | Takes care of any work that is not specifically assigned to a scheduler. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.aux.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `beam.cpu.logical_number` | int | The logical thread number [0..n-1] | `1` | Recommended |
| `beam.cpu.work` | string | The work performed for this data point. | `gc` | Recommended |

`beam.cpu.work` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `aux` | Time spent handling auxiliary jobs. |
| `check_io` | Time spent checking for new I/O events. |
| `emulator` | Time spent executing Erlang processes. |
| `gc` | Time spent doing garbage collection. When extra states are enabled this is the time spent doing non-fullsweep garbage collections. |
| `other` | Time spent doing unaccounted things. |
| `port` | Time spent executing ports. |
| `sleep` | Time spent sleeping. |
| `alloc` | Time spent managing memory. Without extra states this time is spread out over all other states. |
| `bif` | Time spent in BIFs. Without extra states this time is part of the emulator state. |
| `busy_wait` | Time spent busy waiting. |
| `ets` | Time spent executing ETS BIFs. Without extra states this time is part of the emulator state. |
| `gc_full` | Time spent doing fullsweep garbage collection. Without extra states this time is part of the gc state. |
| `nif` | Time spent in NIFs. Without extra states this time is part of the emulator state. |
| `send` | Time spent sending messages (processes only). Without extra states this time is part of the emulator state. |
| `timers` | Time spent managing timers. Without extra states this time is part of the other state. |
<!-- endsemconv -->

### Metric: `beam.cpu.dirty_cpu_scheduler.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.dirty_cpu_scheduler.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.dirty_cpu_scheduler.count` | UpDownCounter | `{scheduler}` | The number of scheduler dirty CPU scheduler threads used by the emulator. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.dirty_cpu_scheduler.count(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.dirty_cpu_scheduler.online`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.dirty_cpu_scheduler.online(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.dirty_cpu_scheduler.online` | UpDownCounter | `{scheduler}` | The number of dirty CPU scheduler threads online. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.dirty_cpu_scheduler.online(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.dirty_cpu_scheduler.run_queue_length`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.dirty_cpu_scheduler.run_queue_length(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.dirty_cpu_scheduler_run_queue_length` | UpDownCounter | `{process}` | Length of the dirty CPU run-queue. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.dirty_cpu_scheduler.run_queue_length(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.dirty_cpu_scheduler.time`

This metric is [Opt-In][MetricOptIn].

<!-- semconv metric.beam.cpu.dirty_cpu_scheduler.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.dirty_cpu_scheduler.time` | Counter | `s` | The threads for long running cpu intensive work. See erl +SDcpu for more details. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.dirty_cpu_scheduler.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `beam.cpu.logical_number` | int | The logical thread number [0..n-1] | `1` | Recommended |
| `beam.cpu.work` | string | The work performed for this data point. | `gc` | Recommended |

`beam.cpu.work` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `aux` | Time spent handling auxiliary jobs. |
| `check_io` | Time spent checking for new I/O events. |
| `emulator` | Time spent executing Erlang processes. |
| `gc` | Time spent doing garbage collection. When extra states are enabled this is the time spent doing non-fullsweep garbage collections. |
| `other` | Time spent doing unaccounted things. |
| `port` | Time spent executing ports. |
| `sleep` | Time spent sleeping. |
| `alloc` | Time spent managing memory. Without extra states this time is spread out over all other states. |
| `bif` | Time spent in BIFs. Without extra states this time is part of the emulator state. |
| `busy_wait` | Time spent busy waiting. |
| `ets` | Time spent executing ETS BIFs. Without extra states this time is part of the emulator state. |
| `gc_full` | Time spent doing fullsweep garbage collection. Without extra states this time is part of the gc state. |
| `nif` | Time spent in NIFs. Without extra states this time is part of the emulator state. |
| `send` | Time spent sending messages (processes only). Without extra states this time is part of the emulator state. |
| `timers` | Time spent managing timers. Without extra states this time is part of the other state. |
<!-- endsemconv -->

### Metric: `beam.cpu.dirty_io_scheduler.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.dirty_io_scheduler.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.dirty_io_scheduler.count` | UpDownCounter | `{scheduler}` | The number of scheduler dirty I/O scheduler threads used by the emulator. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.dirty_io_scheduler.count(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.dirty_io_scheduler.online`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.dirty_io_scheduler.online(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.dirty_io_scheduler.online` | UpDownCounter | `{scheduler}` | The number of scheduler dirty I/O scheduler threads online. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.dirty_io_scheduler.online(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.dirty_io_scheduler.run_queue_length`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.dirty_io_scheduler.run_queue_length(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.dirty_io_scheduler_run_queue_length` | UpDownCounter | `{process}` | Length of the dirty I/O run-queue. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.dirty_io_scheduler.run_queue_length(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.dirty_io_scheduler.time`

This metric is [Opt-In][MetricOptIn].

<!-- semconv metric.beam.cpu.dirty_io_scheduler.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.dirty_io_scheduler.time` | Counter | `s` | The threads for long running I/O work. See erl +SDio for more details. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.dirty_io_scheduler.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `beam.cpu.logical_number` | int | The logical thread number [0..n-1] | `1` | Recommended |
| `beam.cpu.work` | string | The work performed for this data point. | `gc` | Recommended |

`beam.cpu.work` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `aux` | Time spent handling auxiliary jobs. |
| `check_io` | Time spent checking for new I/O events. |
| `emulator` | Time spent executing Erlang processes. |
| `gc` | Time spent doing garbage collection. When extra states are enabled this is the time spent doing non-fullsweep garbage collections. |
| `other` | Time spent doing unaccounted things. |
| `port` | Time spent executing ports. |
| `sleep` | Time spent sleeping. |
| `alloc` | Time spent managing memory. Without extra states this time is spread out over all other states. |
| `bif` | Time spent in BIFs. Without extra states this time is part of the emulator state. |
| `busy_wait` | Time spent busy waiting. |
| `ets` | Time spent executing ETS BIFs. Without extra states this time is part of the emulator state. |
| `gc_full` | Time spent doing fullsweep garbage collection. Without extra states this time is part of the gc state. |
| `nif` | Time spent in NIFs. Without extra states this time is part of the emulator state. |
| `send` | Time spent sending messages (processes only). Without extra states this time is part of the emulator state. |
| `timers` | Time spent managing timers. Without extra states this time is part of the other state. |
<!-- endsemconv -->

### Metric: `beam.cpu.logical_processors`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.logical_processors(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.logical_processors` | UpDownCounter | `{cpu}` | The detected number of logical processors configured in the system. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.logical_processors(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.logical_processors_available`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.logical_processors_available(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.logical_processors_available` | UpDownCounter | `{cpu}` | The detected number of logical processors available to the Erlang runtime system. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.logical_processors_available(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.logical_processors_online`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.logical_processors_online(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.logical_processors_online` | UpDownCounter | `{cpu}` | The detected number of logical processors online on the system. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.logical_processors_online(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.poll.time`

This metric is [Opt-In][MetricOptIn].

<!-- semconv metric.beam.cpu.poll.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.poll.time` | Counter | `s` | Does the IO polling for the emulator. See erl +IOt for more details. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.poll.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `beam.cpu.logical_number` | int | The logical thread number [0..n-1] | `1` | Recommended |
| `beam.cpu.work` | string | The work performed for this data point. | `gc` | Recommended |

`beam.cpu.work` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `aux` | Time spent handling auxiliary jobs. |
| `check_io` | Time spent checking for new I/O events. |
| `emulator` | Time spent executing Erlang processes. |
| `gc` | Time spent doing garbage collection. When extra states are enabled this is the time spent doing non-fullsweep garbage collections. |
| `other` | Time spent doing unaccounted things. |
| `port` | Time spent executing ports. |
| `sleep` | Time spent sleeping. |
| `alloc` | Time spent managing memory. Without extra states this time is spread out over all other states. |
| `bif` | Time spent in BIFs. Without extra states this time is part of the emulator state. |
| `busy_wait` | Time spent busy waiting. |
| `ets` | Time spent executing ETS BIFs. Without extra states this time is part of the emulator state. |
| `gc_full` | Time spent doing fullsweep garbage collection. Without extra states this time is part of the gc state. |
| `nif` | Time spent in NIFs. Without extra states this time is part of the emulator state. |
| `send` | Time spent sending messages (processes only). Without extra states this time is part of the emulator state. |
| `timers` | Time spent managing timers. Without extra states this time is part of the other state. |
<!-- endsemconv -->

### Metric: `beam.cpu.scheduler.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.scheduler.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.scheduler.count` | UpDownCounter | `{scheduler}` | The number of scheduler threads used by the emulator. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.scheduler.count(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.scheduler.online`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.scheduler.online(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.scheduler.online` | UpDownCounter | `{scheduler}` | The number of schedulers online. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.scheduler.online(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.scheduler.run_queues_length`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.scheduler.run_queues_length(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.scheduler.run_queues_length` | UpDownCounter | `{process}` | Length of the normal run-queue. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.scheduler.run_queues_length(full) -->
<!-- endsemconv -->

### Metric: `beam.cpu.scheduler.time`

This metric is [Opt-In][MetricOptIn].

<!-- semconv metric.beam.cpu.scheduler.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.scheduler.time` | Counter | `s` | The main execution threads that do most of the work. See erl +S for more details. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.scheduler.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `beam.cpu.logical_number` | int | The logical thread number [0..n-1] | `1` | Recommended |
| `beam.cpu.work` | string | The work performed for this data point. | `gc` | Recommended |

`beam.cpu.work` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `aux` | Time spent handling auxiliary jobs. |
| `check_io` | Time spent checking for new I/O events. |
| `emulator` | Time spent executing Erlang processes. |
| `gc` | Time spent doing garbage collection. When extra states are enabled this is the time spent doing non-fullsweep garbage collections. |
| `other` | Time spent doing unaccounted things. |
| `port` | Time spent executing ports. |
| `sleep` | Time spent sleeping. |
| `alloc` | Time spent managing memory. Without extra states this time is spread out over all other states. |
| `bif` | Time spent in BIFs. Without extra states this time is part of the emulator state. |
| `busy_wait` | Time spent busy waiting. |
| `ets` | Time spent executing ETS BIFs. Without extra states this time is part of the emulator state. |
| `gc_full` | Time spent doing fullsweep garbage collection. Without extra states this time is part of the gc state. |
| `nif` | Time spent in NIFs. Without extra states this time is part of the emulator state. |
| `send` | Time spent sending messages (processes only). Without extra states this time is part of the emulator state. |
| `timers` | Time spent managing timers. Without extra states this time is part of the other state. |
<!-- endsemconv -->

### Metric: `beam.cpu.thread_pool_size`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.cpu.thread_pool_size(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.cpu.thread_pool_size` | UpDownCounter | `{thread}` | The number of async threads in the async thread pool used for asynchronous driver calls. |
<!-- endsemconv -->

<!-- semconv metric.beam.cpu.thread_pool_size(full) -->
<!-- endsemconv -->

## BEAM ETS

**Status**: [Experimental][DocumentStatus]

**Description:** BEAM metrics captured under the namespace `beam.ets.*`

### Metric: `beam.ets.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.ets.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.ets.limit` | UpDownCounter | `{table}` | The maximum number of ETS tables allowed. |
<!-- endsemconv -->

<!-- semconv metric.beam.ets.limit(full) -->
<!-- endsemconv -->

## BEAM Memory

**Status**: [Experimental][DocumentStatus]

**Description:** BEAM metrics captured under the namespace `beam.memory.*`

### Metric: `beam.memory.allocated`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.memory.allocated(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.memory.allocated` | UpDownCounter | `By` | The total amount of memory currently allocated. [1] |

**[1]:** This is the same as the sum of the memory size for processes and system.
<!-- endsemconv -->

<!-- semconv metric.beam.memory.allocated(full) -->
<!-- endsemconv -->

### Metric: `beam.memory.allocators`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.memory.allocators(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.memory.allocators` | UpDownCounter | `By` | Allocated (carriers_size) and used (blocks_size) memory for the different allocators in the VM. See erts_alloc(3). |
<!-- endsemconv -->

<!-- semconv metric.beam.memory.allocators(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `alloc` | string | The allocation type. | `sys_alloc` | Recommended |
| `instance_no` | int | The logical instance number [0..n] | `1` | Recommended |
| `kind` | string | The allocation kind. | `mbcs` | Recommended |
| `usage` | string | The usage type. | `blocks` | Recommended |

`alloc` MUST be one of the following:

| Value  | Description |
|---|---|
| `temp_alloc` | Allocator used for temporary allocations. |
| `eheap_alloc` | Allocator used for Erlang heap data, such as Erlang process heaps. |
| `binary_alloc` | Allocator used for Erlang binary data. |
| `ets_alloc` | Allocator used for ets data. |
| `driver_alloc` | Allocator used for driver data. |
| `literal_alloc` | Allocator used for constant terms in Erlang code. |
| `sl_alloc` | Allocator used for memory blocks that are expected to be short-lived. |
| `ll_alloc` | Allocator used for memory blocks that are expected to be long-lived, for example, Erlang code. |
| `fix_alloc` | A fast allocator used for some frequently used fixed size data types. |
| `std_alloc` | Allocator used for most memory blocks not allocated through any of the other allocators described above. |
| `sys_alloc` | This is normally the default malloc implementation used on the specific OS. |
| `mseg_alloc` | A memory segment allocator. |

`kind` MUST be one of the following:

| Value  | Description |
|---|---|
| `sbcs` | sbcs |
| `mbcs` | mbcs |
| `mbcs_pool` | mbcs_pool |

`usage` MUST be one of the following:

| Value  | Description |
|---|---|
| `carriers` | carriers |
| `carriers_size` | carriers_size |
| `blocks` | blocks |
| `blocks_size` | blocks_size |
<!-- endsemconv -->

### Metric: `beam.memory.atoms`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.memory.atoms(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.memory.atoms` | UpDownCounter | `By` | The total amount of memory currently allocated for atoms. [1] |

**[1]:** This memory is part of the memory presented as system memory.
<!-- endsemconv -->

<!-- semconv metric.beam.memory.atoms(full) -->
<!-- endsemconv -->

### Metric: `beam.memory.garbage_collection.bytes_reclaimed`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.memory.garbage_collection.bytes_reclaimed(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.memory.garbage_collection.bytes_reclaimed` | Counter | `By` | Garbage collection: bytes reclaimed. |
<!-- endsemconv -->

<!-- semconv metric.beam.memory.garbage_collection.bytes_reclaimed(full) -->
<!-- endsemconv -->

### Metric: `beam.memory.garbage_collection.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.memory.garbage_collection.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.memory.garbage_collection.count` | Counter | `{garbage_collection}` | Garbage collection: number of GCs. |
<!-- endsemconv -->

<!-- semconv metric.beam.memory.garbage_collection.count(full) -->
<!-- endsemconv -->

### Metric: `beam.memory.garbage_collection.words_reclaimed`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.memory.garbage_collection.words_reclaimed(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.memory.garbage_collection.words_reclaimed` | Counter | `{words}` | Garbage collection: words reclaimed. |
<!-- endsemconv -->

<!-- semconv metric.beam.memory.garbage_collection.words_reclaimed(full) -->
<!-- endsemconv -->

### Metric: `beam.memory.processes`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.memory.processes(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.memory.processes` | UpDownCounter | `By` | The total amount of memory currently allocated for the Erlang processes. |
<!-- endsemconv -->

<!-- semconv metric.beam.memory.processes(full) -->
<!-- endsemconv -->

### Metric: `beam.memory.system`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.memory.system(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.memory.system` | UpDownCounter | `By` | The total amount of memory currently allocated for the emulator that is not directly related to any Erlang process. [1] |

**[1]:** Memory presented as processes is not included in this memory.
<!-- endsemconv -->

<!-- semconv metric.beam.memory.system(full) -->
<!-- endsemconv -->

## BEAM Port

**Status**: [Experimental][DocumentStatus]

**Description:** BEAM metrics captured under the namespace `beam.port.*`

### Metric: `beam.port.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.port.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.port.count` | UpDownCounter | `{port}` | The number of ports currently existing at the local node. |
<!-- endsemconv -->

<!-- semconv metric.beam.port.count(full) -->
<!-- endsemconv -->

### Metric: `beam.port.io`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.port.io(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.port.io` | Counter | `By` | Total number of bytes read and written to/from ports. |
<!-- endsemconv -->

<!-- semconv metric.beam.port.io(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `port.io.direction` | string | The port I/O operation direction. | `read` | Recommended |

`port.io.direction` MUST be one of the following:

| Value  | Description |
|---|---|
| `read` | read |
| `write` | write |
<!-- endsemconv -->

### Metric: `beam.port.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.port.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.port.limit` | UpDownCounter | `{port}` | The maximum number of simultaneously existing ports at the local node. |
<!-- endsemconv -->

<!-- semconv metric.beam.port.limit(full) -->
<!-- endsemconv -->

## BEAM Process

**Status**: [Experimental][DocumentStatus]

**Description:** BEAM metrics captured under the namespace `beam.process.*`

### Metric: `beam.process.context_switches`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.process.context_switches(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.process.context_switches` | Counter | `{context_switch}` | Total number of context switches since the system started. |
<!-- endsemconv -->

<!-- semconv metric.beam.process.context_switches(full) -->
<!-- endsemconv -->

### Metric: `beam.process.count`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.process.count(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.process.count` | UpDownCounter | `{process}` | The number of processes currently existing at the local node. |
<!-- endsemconv -->

<!-- semconv metric.beam.process.count(full) -->
<!-- endsemconv -->

### Metric: `beam.process.cpu.time`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.process.cpu.time(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.process.cpu.time` | Counter | `s` | The sum of the runtime for all threads in the Erlang runtime system. |
<!-- endsemconv -->

<!-- semconv metric.beam.process.cpu.time(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `beam.process.cpu.state` | string | The CPU state for this data point. | `user` | Recommended |

`beam.process.cpu.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `user` | user |
| `wall` | wall |
<!-- endsemconv -->

### Metric: `beam.process.limit`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.process.limit(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.process.limit` | UpDownCounter | `{process}` | The maximum number of simultaneously existing processes at the local node. |
<!-- endsemconv -->

<!-- semconv metric.beam.process.limit(full) -->
<!-- endsemconv -->

### Metric: `beam.process.reductions`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.process.reductions(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.process.reductions` | Counter | `{reductions}` | Total reductions. |
<!-- endsemconv -->

<!-- semconv metric.beam.process.reductions(full) -->
<!-- endsemconv -->

## BEAM System

**Status**: [Experimental][DocumentStatus]

**Description:** BEAM metrics captured under the namespace `beam.system.*`

### Metric: `beam.system.wordsize`

This metric is [recommended][MetricRecommended].

<!-- semconv metric.beam.system.wordsize(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `beam.system.wordsize` | UpDownCounter | `By` | The size of Erlang term words in bytes. |
<!-- endsemconv -->

<!-- semconv metric.beam.system.wordsize(full) -->
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
[MetricOptIn]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/metric-requirement-level.md#opt-in
[MetricRecommended]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/metrics/metric-requirement-level.md#recommended
