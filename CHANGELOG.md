# Changelog

Please update changelog as part of any significant pull request. Place short
description of your change into "Unreleased" section. As part of release process
content of "Unreleased" section content will generate release notes for the
release.

## Unreleased

### Breaking

### Features

### Fixes

## v1.23.0 (2023-11-03)

This release marks the first where the core of HTTP semantic conventions have
stabilized.

### Breaking

- BREAKING: Rename http.resend_count to http.request.resend_count.
  ([#374](https://github.com/open-telemetry/semantic-conventions/pull/374))
- BREAKING: Change `network.protocol.name` from recommended to opt-in in HTTP semconv.
  ([#398](https://github.com/open-telemetry/semantic-conventions/pull/398))
- BREAKING: Define url.scheme in terms of logical operation in HTTP server semconv.
  ([#376](https://github.com/open-telemetry/semantic-conventions/pull/376))
- BREAKING: Change `network.transport` from recommended to opt-in in HTTP semconv.
  ([#402](https://github.com/open-telemetry/semantic-conventions/pull/402))
- BREAKING: Change `network.type` from recommended to opt-in in HTTP semconv.
  ([#410](https://github.com/open-telemetry/semantic-conventions/pull/410))
- BREAKING: Factor in `X-Forwarded-Host` / `Forwarded` when capturing `server.address` and `server.port`.
  ([#411](https://github.com/open-telemetry/semantic-conventions/pull/411))
- Remove `thread.daemon`, and introduce `jvm.thread.daemon` instead.
  Introduce `jvm.thread.state` attribute and add it to `jvm.thread.count` metric.
  ([#297](https://github.com/open-telemetry/semantic-conventions/pull/297))
- Fix `server.port` to be not required when `server.address` is not set.
  ([#429](https://github.com/open-telemetry/semantic-conventions/pull/429))
- Use seconds as default duration for FaaS duration histograms
  ([#384](https://github.com/open-telemetry/semantic-conventions/pull/384))
- BREAKING: Remove `total` from list of well-known values of `system.memory.state` attribute.
  ([#409](https://github.com/open-telemetry/semantic-conventions/pull/409))
- Remove `url.path` default value.
  ([#462](https://github.com/open-telemetry/semantic-conventions/pull/462))
- Remove conditional requirement on `network.peer.address` and `network.peer.port`
  ([#449](https://github.com/open-telemetry/semantic-conventions/pull/449))
- Change `user_agent.original` from recommended to opt-in on HTTP client spans.
  ([#468](https://github.com/open-telemetry/semantic-conventions/pull/468))
- Change `http.request.body.size` and `http.response.body.size`
  from recommended to opt-in.
  ([#460](https://github.com/open-telemetry/semantic-conventions/pull/460))
- Clarify that `client.port` is the port of whichever client was captured in `client.address`.
  ([#471](https://github.com/open-telemetry/semantic-conventions/pull/471))
- Change `client.port` from recommended to opt-in on HTTP server spans
  ([#472](https://github.com/open-telemetry/semantic-conventions/pull/472))
- BREAKING: Make `url.scheme` opt_in for HTTP client and remove default value for
  `server.port` making it required on the client.
  ([#459](https://github.com/open-telemetry/semantic-conventions/pull/459))
- Make `client.address` sampling relevant on HTTP server spans.
  ([#469](https://github.com/open-telemetry/semantic-conventions/pull/469))
- Change `network.protocol.name` from opt-in to conditionally required.
  ([#478](https://github.com/open-telemetry/semantic-conventions/pull/478))
- Remove outdated `http.request.header.host` guidance
  ([#479](https://github.com/open-telemetry/semantic-conventions/pull/479))
- Change sampling relevant from `MUST` to `SHOULD`
  ([#486](https://github.com/open-telemetry/semantic-conventions/pull/486))
- Make `user_agent.original` and `http.request.header.*` sampling relevant
  on HTTP server spans.
  ([#467](https://github.com/open-telemetry/semantic-conventions/pull/467))
- BREAKING: Remove `event.domain` from log event attributes.
  ([#473](https://github.com/open-telemetry/semantic-conventions/pull/473))
- BREAKING: Change `event.name` definition to include `namespace`.
  ([#473](https://github.com/open-telemetry/semantic-conventions/pull/473))

### Features

- Adds `session.previous_id` to session.md
  ([#348](https://github.com/open-telemetry/semantic-conventions/pull/348))
- Metric namespaces SHOULD NOT be pluralized.
  ([#267](https://github.com/open-telemetry/opentelemetry-specification/pull/267))
- Add opt-in `system.memory.limit` metric.
  ([#409](https://github.com/open-telemetry/semantic-conventions/pull/409))
- Add `host.mac` resource attribute convention.
  ([#340](https://github.com/open-telemetry/semantic-conventions/pull/340))
- Mark HTTP semantic conventions as stable.
  ([#377](https://github.com/open-telemetry/semantic-conventions/pull/377))

### Fixes

- Clarify that `error.type` should be the fully-qualified exception class name
  when it represents an exception type.
  ([#387](https://github.com/open-telemetry/semantic-conventions/pull/387))
- Add cardinality warning about two opt-in HTTP metric attributes
  ([#401](https://github.com/open-telemetry/semantic-conventions/pull/401))
- Change `server.port` from recommended to conditionally required on HTTP server semconv.
  ([#399](https://github.com/open-telemetry/semantic-conventions/pull/399))
- Add cardinality warning about two opt-in HTTP metric attributes to all HTTP metrics.
  ([#412](https://github.com/open-telemetry/semantic-conventions/pull/412))
- Remove outdated note about not recording HTTP `server.address` when only IP address available.
  ([#413](https://github.com/open-telemetry/semantic-conventions/pull/413))
- Clarify HTTP server definitions and `server.address|port` notes.
  ([#423](https://github.com/open-telemetry/semantic-conventions/pull/423))
- Change the precedence between `:authority` and `Host` headers when populating
  `server.address` and `server.port` attributes.
  ([#455](https://github.com/open-telemetry/semantic-conventions/pull/455))
- Explain `deployment.environment` impact on service identity. ([#481](https://github.com/open-telemetry/semantic-conventions/pull/481))

## v1.22.0 (2023-10-12)

- Remove experimental Kafka metrics ([#338](https://github.com/open-telemetry/semantic-conventions/pull/338))
- Adds `session.id` and session.md to general docs and model
([#215](https://github.com/open-telemetry/semantic-conventions/pull/215))
- Add `container.labels.<key>` attributes.
  ([#125](https://github.com/open-telemetry/semantic-conventions/pull/125))
- Add `cluster.name` and `node.name` attributes to Elasticsearch semantic conventions.
  ([#285](https://github.com/open-telemetry/semantic-conventions/pull/285))
- Fix the unit of metric.process.runtime.jvm.system.cpu.load_1m to be {run_queue_item}
  ([#95](https://github.com/open-telemetry/semantic-conventions/pull/95))
- Update `.count` metric naming convention so that it only applies to UpDownCounters,
  and add that `.total` should not be used by either Counters or UpDownCounters
  ([#107](https://github.com/open-telemetry/semantic-conventions/pull/107))
- Add `oci.manifest.digest`, `container.image.repo_digests` attributes. Make `container.image.tag` array and in plural form.
  ([#159](https://github.com/open-telemetry/semantic-conventions/pull/159))
- BREAKING: Rename `http.client.duration` and `http.server.duration` metrics to
  `http.client.request.duration` and `http.server.request.duration` respectively.
  ([#224](https://github.com/open-telemetry/semantic-conventions/pull/224))
- Update HTTP `network.protocol.version` examples to match HTTP RFCs.
  ([#228](https://github.com/open-telemetry/semantic-conventions/pull/228))
- Re-introduce namespace and attributes to describe the original destination messages were
  published to (`messaging.destination_publish.*`).
  ([#156](https://github.com/open-telemetry/semantic-conventions/pull/156))
- Generate FaaS metric semantic conventions from YAML.
  ([#88](https://github.com/open-telemetry/semantic-conventions/pull/88))
  The conventions cover metrics that are recorded by the FaaS itself and not by
  clients invoking them.
- BREAKING: Rename all JVM metrics from `process.runtime.jvm.*` to `jvm.*`
  ([#241](https://github.com/open-telemetry/semantic-conventions/pull/241))
- BREAKING: Add namespaces to JVM metric attributes ([#20](https://github.com/open-telemetry/semantic-conventions/pull/20)).
  - Rename attributes `type` to `jvm.memory.type`, `pool` to `jvm.memory.pool.name`
  - Applies to metrics:
    - `jvm.memory.usage`
    - `jvm.memory.init`
    - `jvm.memory.committed`
    - `jvm.memory.limit`
    - `jvm.memory.usage_after_last_gc`
  - Rename attributes `gc` to `jvm.gc.name`, `action` to `jvm.gc.action`
  - Applies to metrics:
    - `jvm.gc.duration`
  - Rename attribute `daemon` to `thread.daemon`
  - Applies to metrics:
    - `jvm.threads.count`
  - Rename attribute `pool` to `jvm.buffer.pool.name`
  - Applies to metrics:
    - `jvm.buffer.usage`
    - `jvm.buffer.limit`
    - `jvm.buffer.count`
- Clarify that `http/dup` has higher precedence than `http` in case both values are present
  in `OTEL_SEMCONV_STABILITY_OPT_IN`
  ([#249](https://github.com/open-telemetry/semantic-conventions/pull/249))
- Add `jvm.cpu.count` metric.
  ([#52](https://github.com/open-telemetry/semantic-conventions/pull/52))
- BREAKING: Rename metrics `jvm.buffer.usage` to `jvm.buffer.memory.usage`
  and `jvm.buffer.limit` to `jvm.buffer.memory.limit`.
  ([#253](https://github.com/open-telemetry/semantic-conventions/pull/253))
- BREAKING: Rename `jvm.classes.current_loaded` metrics to `jvm.classes.count`
  ([#60](https://github.com/open-telemetry/semantic-conventions/pull/60))
- BREAKING: Remove pluralization from JVM metric namespaces.
  ([#252](https://github.com/open-telemetry/semantic-conventions/pull/252))
- Simplify HTTP metric briefs.
  ([#276](https://github.com/open-telemetry/semantic-conventions/pull/276))
- Add host cpu resource attributes.
  ([#209](https://github.com/open-telemetry/semantic-conventions/pull/209))
- Introduce `error.type` attribute and use it in HTTP conventions
  ([#205](https://github.com/open-telemetry/semantic-conventions/pull/205))
- BREAKING: Change HTTP span name when method is unknown (use `HTTP` instead of `_OTHER`)
  ([#270](https://github.com/open-telemetry/semantic-conventions/pull/270))
- Moved RPC streaming notes from metric brief section to notes section.
  ([#275](https://github.com/open-telemetry/semantic-conventions/pull/275))
- Updates `client.address` to allow domain names for consistency with `server.address`.
  ([#302](https://github.com/open-telemetry/semantic-conventions/pull/302))
- BREAKING: Generate System metrics semconv from YAML.
  ([#89](https://github.com/open-telemetry/semantic-conventions/pull/89))
  - Rename attributes for `system.cpu.*` metrics:
    - `state` to `system.cpu.state`
    - `cpu` to `system.cpu.logical_number`
  - Rename attributes for `system.memory.*` metrics:
    - `state` to `system.memory.state`
  - Rename attributes for `system.paging.*` metrics:
    - `state` to `system.paging.state`
    - `type` to `system.paging.type`
    - `direction` to `system.paging.direction`
  - Rename attributes for `system.disk.*` metrics:
    - `device` to `system.device`
    - `direction` to `system.disk.direction`
  - Rename attributes for `system.filesystem.*` metrics:
    - `device` to `system.device`
    - `state` to `system.filesystem.state`
    - `type` to `system.filesystem.type`
    - `mode` to `system.filesystem.mode`
    - `mountpoint` to `system.filesystem.mountpoint`
  - Rename attributes for `system.network.*` metrics:
    - `device` to `system.device`
    - `direction` to `system.network.direction`
    - `protocol` to `network.protocol`
    - `state` to `system.network.state`
  - Rename attributes for `system.processes.*` metrics:
    - `status` to `system.processes.status`
- BREAKING: Rename `messaging.message.payload_size_bytes` to `messaging.message.body.size`,
  remove `messaging.message.payload_compressed_size_bytes`.
  ([#229](https://github.com/open-telemetry/semantic-conventions/pull/229))
- Add `system.linux.memory.available` metric.
  ([#323](https://github.com/open-telemetry/semantic-conventions/pull/323))
- BREAKING: Rename `http.server.request.size` metric to `http.server.request.body.size`
  and `http.server.response.size` metric to `http.server.response.body.size`
  ([#247](https://github.com/open-telemetry/semantic-conventions/pull/247))
- Move non-`network.*` attributes out of network.yaml.
  ([#296](https://github.com/open-telemetry/semantic-conventions/pull/296))
- Introducing Android `android.os.api_level` resource attribute.
  ([#328](https://github.com/open-telemetry/semantic-conventions/pull/328))
- Added `os.build_id` resource attribute.
  ([#293](https://github.com/open-telemetry/semantic-conventions/pull/293))
- BREAKING: Remove the zero bucket boundary from `http.server.request.duration`
  and `http.client.request.duration`.
  ([#318](https://github.com/open-telemetry/semantic-conventions/pull/318))
- Encourage setting `network.transport` when reporting port numbers
  ([#289](https://github.com/open-telemetry/semantic-conventions/pull/289))
- BREAKING: Add `url.scheme` to `http.client.*` metrics
  ([#357](https://github.com/open-telemetry/semantic-conventions/pull/357))
- BREAKING: Remove `server.socket.address` from HTTP and RPC client metrics.
  ([#350](https://github.com/open-telemetry/semantic-conventions/pull/350))
- Improve network attribute briefs.
  ([#352](https://github.com/open-telemetry/semantic-conventions/pull/352))
- Document the difference between host and system metrics
  ([#324](https://github.com/open-telemetry/semantic-conventions/pull/324))
- BREAKING: Rename `telemetry.auto.version` resource attribute to `telemetry.distro.version`
  and add `telemetry.distro.name` resource attribute
  ([#178](https://github.com/open-telemetry/semantic-conventions/pull/178))
- Add `system.cpu.frequency` metric.
  ([#337](https://github.com/open-telemetry/semantic-conventions/pull/337))
- Improve HTTP metric briefs.
  ([#366](https://github.com/open-telemetry/semantic-conventions/pull/366))
- Add `host.ip` resource attribute convention.
  ([#203](https://github.com/open-telemetry/semantic-conventions/pull/203))
- BREAKING: remove `-` to `_` normalization from http header and rpc metadata
  attribute keys.
  ([#369](https://github.com/open-telemetry/semantic-conventions/pull/369))
- BREAKING: Rename/replace `(client|server).socket.(address|port)` attributes
  with `network.(peer|local).(address|port)`.
  ([#342](https://github.com/open-telemetry/semantic-conventions/pull/342))
- Make `network.protocol.name|version` description consistent between HTTP
  spans and metrics.
  ([#367](https://github.com/open-telemetry/semantic-conventions/pull/367))

## v1.21.0 (2023-07-13)

Note: This is the first release of Semantic Conventions separate from the Specification.

- Add GCP Bare Metal Solution as a cloud platform
  ([#64](https://github.com/open-telemetry/semantic-conventions/pull/64))
- Clarify the scope of the HTTP client span.
  ([#3290](https://github.com/open-telemetry/opentelemetry-specification/pull/3290))
- Add moratorium on relying on schema transformations for telemetry stability
  ([#3380](https://github.com/open-telemetry/opentelemetry-specification/pull/3380))
- Mark "Instrumentation Units" and "Instrumentation Types" sections of the general
  metric semantic conventions as stable
  ([#3294](https://github.com/open-telemetry/opentelemetry-specification/pull/3294))
- Add clarification that UCUM c/s variant applies to all units other than `1` and
  those using [annotations](https://ucum.org/ucum.html#para-curly).
  ([#3393](https://github.com/open-telemetry/opentelemetry-specification/pull/3393))
- Specify that seconds should be used for measuring durations.
  ([#3388](https://github.com/open-telemetry/opentelemetry-specification/pull/3388))
- Change http.server.duration and http.client.duration units to seconds
  ([#3390](https://github.com/open-telemetry/opentelemetry-specification/pull/3390))
- BREAKING: Remove `messaging.consumer.id`, make `messaging.client_id` generic
  ([#3336](https://github.com/open-telemetry/opentelemetry-specification/pull/3336))
- Add transition plan for upcoming breaking changes to the unstable HTTP semantic
  conventions.
  ([#3443](https://github.com/open-telemetry/opentelemetry-specification/pull/3443))
- Rename `net.peer.*`, `net.host.*`, and `net.sock.*` attributes to align with ECS
  ([#3402](https://github.com/open-telemetry/opentelemetry-specification/pull/3402))
  BREAKING: rename `net.peer.name` to `server.address` on client side and to `client.address` on server side,
  `net.peer.port` to `server.port` on client side and to `client.port` on server side,
  `net.host.name` and `net.host.port` to `server.address` and `server.port` (since `net.host.*` attributes only applied to server instrumentation),
  `net.sock.peer.addr` to `server.socket.address` on client side and to `client.socket.address` on server side,
  `net.sock.peer.port` to `server.socket.port` on client side and to `client.socket.port` on server side,
  `net.sock.peer.name` to `server.socket.domain` (since `net.sock.peer.name` only applied to client instrumentation),
  `net.sock.host.addr` to `server.socket.address` (since `net.sock.host.*` only applied to server instrumentation),
  `net.sock.host.port` to `server.socket.port` (similarly since `net.sock.host.*` only applied to server instrumentation),
  `http.client_ip` to `client.address`
- BREAKING: Introduce `network.transport` defined as
  [OSI Transport Layer](https://osi-model.com/transport-layer/) or
  [Inter-process Communication method](https://en.wikipedia.org/wiki/Inter-process_communication).
  Introduce `network.type` defined as [OSI Network Layer](https://osi-model.com/network-layer/)
  or non-OSI equivalent. Remove `net.transport` and `net.sock.family`.
  Rename `net.protocol.*` to `network.protocol.*`,
  `net.host.connection.*` to `network.connection.*`, and
  `net.host.carrier.*` to `network.carrier.*`.
  ([#3426](https://github.com/open-telemetry/opentelemetry-specification/pull/3426))
- BREAKING: Adopt ECS attributes in HTTP semantic conventions.
  Renames: `http.method` to `http.request.method`,
  `http.status_code` to `http.response.status_code`,
  `http.request_content_length` to `http.request.body.size`,
  `http.response_content_length` to `http.response.body.size`,
  `http.url` to `url.full`,
  `http.scheme` to `url.scheme`,
  and removes `http.target` breaking it down to `http.target` to `url.path`, `url.query`, and `url.fragment`.
  ([#3355](https://github.com/open-telemetry/opentelemetry-specification/pull/3355))
- Add `gcp.cloud_run.job.execution` and `gcp.cloud_run.job.task_id` resource
  attributes for GCP Cloud Run Jobs ([#3378](https://github.com/open-telemetry/opentelemetry-specification/pull/3378))
- Specify second unit (`s`) and advice bucket boundaries of `[]`
  for `process.runtime.jvm.gc.duration`.
  ([#3458](https://github.com/open-telemetry/opentelemetry-specification/pull/3458))
- Specify the value range for JVM CPU metrics.
  ([#13](https://github.com/open-telemetry/semantic-conventions/pull/13))
- Rename `process.runtime.jvm.cpu.utilization` to `process.runtime.jvm.cpu.recent_utilization`.
  ([#53](https://github.com/open-telemetry/semantic-conventions/pull/53))
- Clarify `process.runtime.jvm.threads.count` refers to platform threads.
  ([#54](https://github.com/open-telemetry/semantic-conventions/pull/54))
- Add `gcp.gce.instance.name` and `gcp.gce.instance.hostname` resource
  attributes for GCP Compute Engine VMs. ([#15](https://github.com/open-telemetry/semantic-conventions/pull/15))
- Add note that HTTP duration metrics should match HTTP span duration.
  ([#69](https://github.com/open-telemetry/semantic-conventions/pull/69))
- Clarify when HTTP client spans should end.
  ([#70](https://github.com/open-telemetry/semantic-conventions/pull/70))
- Clarify that OTEL_SEMCONV_STABILITY_OPT_IN is a comma-separated list of values
  ([#104](https://github.com/open-telemetry/semantic-conventions/pull/104))
- Add `process.runtime.jvm.cpu.time` metric.
  ([#55](https://github.com/open-telemetry/semantic-conventions/pull/55))
- Split out sections for proposed stable JVM metrics and experimental JVM metrics.
  ([#56](https://github.com/open-telemetry/semantic-conventions/pull/56))
- Make `url.query` conditionally required for HTTP spans.
  ([#118](https://github.com/open-telemetry/semantic-conventions/pull/118))
- Change `server.address` and `server.port` requirement levels on HTTP server metrics
  from `required` to `opt_in`.
  ([#109](https://github.com/open-telemetry/semantic-conventions/pull/109))
- Updated AWS Java Lambda guidance - using system properties.
  ([#27](https://github.com/open-telemetry/semantic-conventions/pull/27))
- Limit `http.request.method` values to a closed set of known values,
  introduce `http.request.method_original` for the original value.
  ([#17](https://github.com/open-telemetry/semantic-conventions/pull/17))
- Mark service.version as stable.
  ([#106](https://github.com/open-telemetry/semantic-conventions/pull/106))
- Mark initial set of HTTP semantic conventions as frozen
  ([#105](https://github.com/open-telemetry/semantic-conventions/pull/105))
- BREAKING: Remove `messaging.source.*` attributes and use `messaging.destination.*`
  attributes on producer and consumer to describe messaging queue or topic.
  ([#100](https://github.com/open-telemetry/semantic-conventions/pull/100))
- Mark `process.runtime.jvm.system.cpu.load_1m` and `process.runtime.jvm.system.cpu.utilization` metrics as opt-in.
  ([#57](https://github.com/open-telemetry/semantic-conventions/pull/57))
- Add container `image.id`, `command`, `command_line` and `command_args` resource attributes.
  ([#39](https://github.com/open-telemetry/semantic-conventions/pull/39))
- Add Elasticsearch client semantic conventions.
  ([#23](https://github.com/open-telemetry/semantic-conventions/pull/23))
- Add YAML definitions for log semantic conventions and define requirement levels
  ([#133](https://github.com/open-telemetry/semantic-conventions/pull/133))
- Add markdown file for url semantic conventions
  ([#174](https://github.com/open-telemetry/semantic-conventions/pull/174))
- Add `system.cpu.physical.count` and `system.cpu.logical.count` metrics.
  ([#99](https://github.com/open-telemetry/opentelemetry-specification/pull/99))

## v1.20.0 (2023-04-07)

This and earlier versions were released as part of [the Specification](https://github.com/open-telemetry/opentelemetry-specification/). See [the specification changelog](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.20.0/CHANGELOG.md) if you'd like to `git blame` a changelog entry.

- Clarify that attribute requirement levels apply to the instrumentation library
  ([#3289](https://github.com/open-telemetry/opentelemetry-specification/pull/3289))
- Fix grammatical number of metric units.
  ([#3298](https://github.com/open-telemetry/opentelemetry-specification/pull/3298))
- Rename `net.app.protocol.(name|version)` to `net.protocol.(name|version)`
  ([#3272](https://github.com/open-telemetry/opentelemetry-specification/pull/3272))
- Replace `http.flavor` with `net.protocol.(name|version)`
  ([#3272](https://github.com/open-telemetry/opentelemetry-specification/pull/3272))
- Metric requirement levels are now stable
  ([#3271](https://github.com/open-telemetry/opentelemetry-specification/pull/3271))
- BREAKING: remove `messaging.destination.kind` and `messaging.source.kind`.
  ([#3214](https://github.com/open-telemetry/opentelemetry-specification/pull/3214),
  [#3348](https://github.com/open-telemetry/opentelemetry-specification/pull/3348))
- Define attributes collected for `cosmosdb` by Cosmos DB SDK
  ([#3097](https://github.com/open-telemetry/opentelemetry-specification/pull/3097))
- Clarify stability requirements of semantic conventions
  ([#3225](https://github.com/open-telemetry/opentelemetry-specification/pull/3225))
- BREAKING: Change span statuses for gRPC server spans.
  ([#3333](https://github.com/open-telemetry/opentelemetry-specification/pull/3333))
- Stabilize key components of `service.*` and `telemetry.sdk.*` resource
  semantic conventions.
  ([#3202](https://github.com/open-telemetry/opentelemetry-specification/pull/3202))
- Fixed attributes requirement level in semantic conventions for hardware metrics
  ([#3258](https://github.com/open-telemetry/opentelemetry-specification/pull/3258))
- Added AWS S3 semantic conventions.
  ([#3251](https://github.com/open-telemetry/opentelemetry-specification/pull/3251))
- Fix units in the Kafka metric semantic conventions.
  ([#3300](https://github.com/open-telemetry/opentelemetry-specification/pull/3300))
- Add Trino to Database specific conventions
  ([#3347](https://github.com/open-telemetry/opentelemetry-specification/pull/3347))
- Change `db.statement` to only be collected if there is sanitization.
  ([#3127](https://github.com/open-telemetry/opentelemetry-specification/pull/3127))
- BREAKING: Remove `http.status_code` attribute from the
  `http.server.active_requests` metric.
  ([#3366](https://github.com/open-telemetry/opentelemetry-specification/pull/3366))
- Mark attribute requirement levels as stable
  ([#3368](https://github.com/open-telemetry/opentelemetry-specification/pull/3368))

## v1.19.0 (2023-03-06)

- Move X-Ray Env Variable propagation to span link instead of parent for AWS Lambda.
  ([#3166](https://github.com/open-telemetry/opentelemetry-specification/pull/3166))
- Add heroku resource semantic conventions.
  [#3075](https://github.com/open-telemetry/opentelemetry-specification/pull/3075)
- BREAKING: Rename faas.execution to faas.invocation_id
  ([#3209](https://github.com/open-telemetry/opentelemetry-specification/pull/3209))
- BREAKING: Change faas.max_memory units to Bytes instead of MB
  ([#3209](https://github.com/open-telemetry/opentelemetry-specification/pull/3209))
- BREAKING: Expand scope of faas.id to cloud.resource_id
  ([#3188](https://github.com/open-telemetry/opentelemetry-specification/pull/3188))
- Add Connect RPC specific conventions
  ([#3116](https://github.com/open-telemetry/opentelemetry-specification/pull/3116))
- Rename JVM metric attribute value from `nonheap` to `non_heap`
  ([#3250](https://github.com/open-telemetry/opentelemetry-specification/pull/3250))
- Mark the attribute naming guidelines in the specification as stable.
  ([#3220](https://github.com/open-telemetry/opentelemetry-specification/pull/3220))
- Mark telemetry schema readme stable.
  ([#3221](https://github.com/open-telemetry/opentelemetry-specification/pull/3221))
- Remove mention of `net.transport` from HTTP semantic conventions
  ([#3244](https://github.com/open-telemetry/opentelemetry-specification/pull/3244))
- Clarifies that if an HTTP client request is explicitly made to an IP address,
  e.g. `http://x.x.x.x:8080`, then `net.peer.name` SHOULD be the IP address `x.x.x.x`
  ([#3276](https://github.com/open-telemetry/opentelemetry-specification/pull/3276))
- Mark `net.sock.host.port` as conditionally required.
  ([#3246](https://github.com/open-telemetry/opentelemetry-specification/pull/3246))
- Rename Optional attribute requirement level to Opt-In.
  ([#3228](https://github.com/open-telemetry/opentelemetry-specification/pull/3228))
- Rename `http.user_agent` to `user_agent.original`.
  ([#3190](https://github.com/open-telemetry/opentelemetry-specification/pull/3190))
- Expand the declaration of `pool.name`.
  ([#3050](https://github.com/open-telemetry/opentelemetry-specification/pull/3050))

## v1.18.0 (2023-02-09)

- Add Cloud Spanner and Microsoft SQL Server Compact to db.system semantic conventions
  ([#3105](https://github.com/open-telemetry/opentelemetry-specification/pull/3105)).
- Enable semantic convention tooling for metrics in spec
  ([#3119](https://github.com/open-telemetry/opentelemetry-specification/pull/3119))
- Rename google openshift platform attribute from `google_cloud_openshift` to `gcp_openshift`
  to match the existing `cloud.provider` prefix.
  ([#3095](https://github.com/open-telemetry/opentelemetry-specification/pull/3095))
- Changes http server span names from `{http.route}` to `{http.method} {http.route}`
  (when route is available), and from `HTTP {http.method}` to `{http.method}` (when
  route is not available).
  Changes http client span names from `HTTP {http.method}` to `{http.method}`.
  ([#3165](https://github.com/open-telemetry/opentelemetry-specification/pull/3165))
- Mark `http.server.duration` and `http.client.duration` metrics as required, and mark
  all other HTTP metrics as optional.
  [#3158](https://github.com/open-telemetry/opentelemetry-specification/pull/3158)
- Add `net.host.port` to `http.server.active_requests` metrics attributes.
  [#3158](https://github.com/open-telemetry/opentelemetry-specification/pull/3158)
- `http.route` SHOULD contain the "application root" if there is one.
  ([#3164](https://github.com/open-telemetry/opentelemetry-specification/pull/3164))

## v1.17.0 (2023-01-17)

- Clarify common HTTP attributes apply to both clients and servers
  ([#3044](https://github.com/open-telemetry/opentelemetry-specification/pull/3044))
- Add `code.lineno` source code attribute
  ([#3029](https://github.com/open-telemetry/opentelemetry-specification/pull/3029))
- Add ClickHouse to db.system semantic conventions
  ([#3011](https://github.com/open-telemetry/opentelemetry-specification/pull/3011))
- Refactor messaging attributes and per-message attributes in batching scenarios.
  ([#2957](https://github.com/open-telemetry/opentelemetry-specification/pull/2957)).
  BREAKING: rename `messaging.consumer_id` to `messaging.consumer.id`,
  `messaging.destination` to `messaging.destination.name`,
  `messaging.temp_destination` to `messaging.destination.temporary`,
  `messaging.destination_kind` to `messaging.destination.kind`,
  `messaging.message_id` to `messaging.message.id`,
  `messaging.protocol` to `net.app.protocol.name`,
  `messaging.protocol_version`, `net.app.protocol.version`,
  `messaging.conversation_id` to `messaging.message.conversation_id`,
  `messaging.message_payload_size_bytes` to `messaging.message.payload_size_bytes`,
  `messaging.message_payload_compressed_size_bytes` to `messaging.message.payload_compressed_size_bytes`,
  `messaging.rabbitmq.routing_key`: `messaging.rabbitmq.destination.routing_key`,
  `messaging.kafka.message_key` to `messaging.kafka.message.key`,
  `messaging.kafka.consumer_group` to `messaging.kafka.consumer.group`,
  `messaging.kafka.partition` to `messaging.kafka.destination.partition`,
  `messaging.kafka.tombstone` to `messaging.kafka.message.tombstone`,
  `messaging.rocketmq.message_type` to `messaging.rocketmq.message.type`,
  `messaging.rocketmq.message_tag` to `messaging.rocketmq.message.tag`,
  `messaging.rocketmq.message_keys` to `messaging.rocketmq.message.keys`;
  Removed `messaging.url`;
  Renamed `send` operation to `publish`;
  Split `destination` and `source` namespaces and clarify per-message attributes in batching scenarios.

## v1.16.0 (2022-12-08)

- Add `process.runtime.jvm.gc.duration` metric to semantic conventions.
  ([#2903](https://github.com/open-telemetry/opentelemetry-specification/pull/2903))
- Make http.status_code metric attribute an int.
  ([#2943](https://github.com/open-telemetry/opentelemetry-specification/pull/2943))
- Add IBM Cloud as a cloud provider.
  ([#2965](https://github.com/open-telemetry/opentelemetry-specification/pull/2965))
- Add semantic conventions for Feature Flags
  ([#2529](https://github.com/open-telemetry/opentelemetry-specification/pull/2529))
- Rename `rpc.request.metadata.<key>` and `rpc.response.metadata.<key>` to
  `rpc.grpc.request.metadata.<key>` and `rpc.grpc.response.metadata.<key>`
  ([#2981](https://github.com/open-telemetry/opentelemetry-specification/pull/2981))
- List the machine-id as potential source for a unique host.id
  ([#2978](https://github.com/open-telemetry/opentelemetry-specification/pull/2978))
- Add `messaging.kafka.message.offset` attribute.
  ([#2982](https://github.com/open-telemetry/opentelemetry-specification/pull/2982))
- Update hardware metrics to use `direction` as per general semantic conventions
  ([#2942](https://github.com/open-telemetry/opentelemetry-specification/pull/2942))

## v1.15.0 (2022-11-09)

- Change to messaging.kafka.max.lag from UpDownCounter to Gauge (and rename it)
  ([#2837](https://github.com/open-telemetry/opentelemetry-specification/pull/2837))
- Add daemon attribute to jvm threads metric
  ([#2828](https://github.com/open-telemetry/opentelemetry-specification/pull/2828))
- Add gRPC request and response metadata semantic conventions
  ([#2874](https://github.com/open-telemetry/opentelemetry-specification/pull/2874))
- Add `process.paging.faults` metric to semantic conventions
  ([#2827](https://github.com/open-telemetry/opentelemetry-specification/pull/2827))
- Define semantic conventions yaml for non-otlp conventions
  ([#2850](https://github.com/open-telemetry/opentelemetry-specification/pull/2850))
- Add more semantic convetion attributes of Apache RocketMQ
  ([#2881](https://github.com/open-telemetry/opentelemetry-specification/pull/2881))
- Add `process.runtime.jvm.memory.usage_after_last_gc` metric to semantic conventions.
  ([#2901](https://github.com/open-telemetry/opentelemetry-specification/pull/2901))

## v1.14.0 (2022-10-04)

- Add `process.context_switches`, and `process.open_file_descriptors`, to the
  metrics semantic conventions
  ([#2706](https://github.com/open-telemetry/opentelemetry-specification/pull/2706))
- Add exceptions to the logs semantic conventions
  ([#2819](https://github.com/open-telemetry/opentelemetry-specification/pull/2819))
- Make context propagation requirements explicit for messaging semantic conventions
  ([#2750](https://github.com/open-telemetry/opentelemetry-specification/pull/2750)).
- Update http metrics to use `http.route` instead of `http.target` for servers,
  drop `http.url` for clients
  ([#2818](https://github.com/open-telemetry/opentelemetry-specification/pull/2818)).

## v1.13.0 (2022-09-19)

- Add `net.app.protocol.*` attributes
  ([#2602](https://github.com/open-telemetry/opentelemetry-specification/pull/2602))
- Add network metrics to process semantic conventions
  ([#2556](https://github.com/open-telemetry/opentelemetry-specification/pull/2556))
- Adopt attribute requirement levels in semantic conventions
  ([#2594](https://github.com/open-telemetry/opentelemetry-specification/pull/2594))
- Add semantic conventions for GraphQL
  ([#2456](https://github.com/open-telemetry/opentelemetry-specification/pull/2456))
- Change `cloudevents.event_spec_version` and `cloudevents.event_type` level from `required` to `recommended`
  ([#2618](https://github.com/open-telemetry/opentelemetry-specification/pull/2618))
- Change `faas.document.time` and `faas.time` level from `required` to `recommended`
  ([#2627](https://github.com/open-telemetry/opentelemetry-specification/pull/2627))
- Add `rpc.grpc.status_code` to RPC metric semantic conventions
  ([#2604](https://github.com/open-telemetry/opentelemetry-specification/pull/2604))
- Add `http.*.*.size` metric semantic conventions for tracking size of requests
  / responses for http servers / clients
  ([#2588](https://github.com/open-telemetry/opentelemetry-specification/pull/2588))
- BREAKING: rename `net.peer.ip` to `net.sock.peer.addr`, `net.host.ip` to `net.sock.host.addr`,
  `net.peer.name` to `net.sock.peer.name` for socket-level instrumentation.
  Define socket-level attributes and clarify logical peer and host attributes meaning
  ([#2594](https://github.com/open-telemetry/opentelemetry-specification/pull/2594))
- Add semantic conventions for JVM buffer pool usage
  ([#2650](https://github.com/open-telemetry/opentelemetry-specification/pull/2650))
- Improve the definition of `state` attribute for metric `system.network.connections`
  ([#2663](https://github.com/open-telemetry/opentelemetry-specification/pull/2663))
- Add `process.parent_pid` attribute for use in reporting parent process id (PID)
  ([#2691](https://github.com/open-telemetry/opentelemetry-specification/pull/2691))
- Add OpenSearch to db.system semantic conventions
  ([#2718](https://github.com/open-telemetry/opentelemetry-specification/pull/2718))
- Clarify when "count" is used instead of pluralization
  ([#2613](https://github.com/open-telemetry/opentelemetry-specification/pull/2613))
- Add the convention 'type' to the YAML definitions for all existing semantic conventions
  ([#2693](https://github.com/open-telemetry/opentelemetry-specification/pull/2693))
- Remove alternative attribute sets from HTTP semantic conventions
  ([#2469](https://github.com/open-telemetry/opentelemetry-specification/pull/2469))

## v1.12.0 (2022-06-10)

- Add semantic conventions for JVM CPU metrics
  ([#2292](https://github.com/open-telemetry/opentelemetry-specification/pull/2292))
- Add details for FaaS conventions for Azure Functions and allow FaaS/Cloud
  resources as span attributes on incoming FaaS spans
  ([#2502](https://github.com/open-telemetry/opentelemetry-specification/pull/2502))
- Define attribute requirement levels
  ([#2522](https://github.com/open-telemetry/opentelemetry-specification/pull/2522))
- Initial addition of Kafka metrics
  ([#2485](https://github.com/open-telemetry/opentelemetry-specification/pull/2485)).
- Add semantic conventions for Kafka consumer metrics
  ([#2536](https://github.com/open-telemetry/opentelemetry-specification/pull/2536))
- Add database connection pool metrics semantic conventions
  ([#2273](https://github.com/open-telemetry/opentelemetry-specification/pull/2273)).
- Specify how to obtain a Ruby thread's id
  ([#2508](https://github.com/open-telemetry/opentelemetry-specification/pull/2508)).
- Refactor jvm classes semantic conventions
  ([#2550](https://github.com/open-telemetry/opentelemetry-specification/pull/2550)).
- Add browser.\* attributes
  ([#2353](https://github.com/open-telemetry/opentelemetry-specification/pull/2353)).
- Change JVM runtime metric `process.runtime.jvm.memory.max`
  to `process.runtime.jvm.memory.limit`
  ([#2605](https://github.com/open-telemetry/opentelemetry-specification/pull/2605)).
- Add semantic conventions for hardware metrics
  ([#2518](https://github.com/open-telemetry/opentelemetry-specification/pull/2518)).

## v1.11.0 (2022-05-04)

- Note added that `net.peer.name` SHOULD NOT be set if capturing it would require an
  extra reverse DNS lookup. And moved `net.peer.name` from common http attributes to
  just client http attributes.
  ([#2446](https://github.com/open-telemetry/opentelemetry-specification/pull/2446))
- Add `net.host.name` and `net.host.ip` conventions for rpc server spans.
  ([#2447](https://github.com/open-telemetry/opentelemetry-specification/pull/2447))
- Allow all metric conventions to be either synchronous or asynchronous.
  ([#2458](https://github.com/open-telemetry/opentelemetry-specification/pull/2458)
- Update JVM metrics with JMX Gatherer values
  ([#2478](https://github.com/open-telemetry/opentelemetry-specification/pull/2478))
- Add HTTP/3
  ([#2507](https://github.com/open-telemetry/opentelemetry-specification/pull/2507))
- Map SunOS to solaris for os.type resource attribute
  ([#2509](https://github.com/open-telemetry/opentelemetry-specification/pull/2509))

## v1.10.0 (2022-04-01)

- Define span structure for HTTP retries and redirects.
  ([#2078](https://github.com/open-telemetry/opentelemetry-specification/pull/2078))
- Changed `rpc.system` to an enum (allowing custom values), and changed the
  `rpc.system` value for .NET WCF from `wcf` to `dotnet_wcf`.
  ([#2377](https://github.com/open-telemetry/opentelemetry-specification/pull/2377))
- Define JavaScript runtime semantic conventions.
  ([#2290](https://github.com/open-telemetry/opentelemetry-specification/pull/2290))
- Add semantic conventions for [CloudEvents](https://cloudevents.io).
  ([#1978](https://github.com/open-telemetry/opentelemetry-specification/pull/1978))
- Add `process.cpu.utilization` metric.
  ([#2436](https://github.com/open-telemetry/opentelemetry-specification/pull/2436))
- Add `rpc.system` value for Apache Dubbo.
  ([#2453](https://github.com/open-telemetry/opentelemetry-specification/pull/2453))

## v1.9.0 (2022-02-10)

- Align runtime metric and resource namespaces
  ([#2112](https://github.com/open-telemetry/opentelemetry-specification/pull/2112))
- Prohibit usage of retired names in semantic conventions.
  ([#2191](https://github.com/open-telemetry/opentelemetry-specification/pull/2191))
- Add `device.manufacturer` to describe mobile device manufacturers.
  ([2100](https://github.com/open-telemetry/opentelemetry-specification/pull/2100))
- Change golang namespace to 'go', rather than 'gc'
  ([#2262](https://github.com/open-telemetry/opentelemetry-specification/pull/2262))
- Add JVM memory runtime semantic
  conventions. ([#2272](https://github.com/open-telemetry/opentelemetry-specification/pull/2272))
- Add opentracing.ref_type semantic convention.
  ([#2297](https://github.com/open-telemetry/opentelemetry-specification/pull/2297))

## v1.8.0 (2021-11-12)

- Add `k8s.container.restart_count` Resource attribute.
  ([#1945](https://github.com/open-telemetry/opentelemetry-specification/pull/1945))
- Add "IBM z/Architecture" (`s390x`) to `host.arch`
  ([#2055](https://github.com/open-telemetry/opentelemetry-specification/pull/2055))
- BREAKING: Remove db.cassandra.keyspace and db.hbase.namespace, and clarify db.name
  ([#1973](https://github.com/open-telemetry/opentelemetry-specification/pull/1973))
- Add AWS App Runner as a cloud platform
  ([#2004](https://github.com/open-telemetry/opentelemetry-specification/pull/2004))
- Add Tencent Cloud as a cloud provider.
  ([#2006](https://github.com/open-telemetry/opentelemetry-specification/pull/2006))
- Don't set Span.Status for 4xx http status codes for SERVER spans.
  ([#1998](https://github.com/open-telemetry/opentelemetry-specification/pull/1998))
- Add attributes for Apache RocketMQ.
  ([#1904](https://github.com/open-telemetry/opentelemetry-specification/pull/1904))
- Define http tracing attributes provided at span creation time
  ([#1916](https://github.com/open-telemetry/opentelemetry-specification/pull/1916))
- Change meaning and discourage use of `faas.trigger` for FaaS clients (outgoing).
  ([#1921](https://github.com/open-telemetry/opentelemetry-specification/pull/1921))
- Clarify difference between container.name and k8s.container.name
  ([#1980](https://github.com/open-telemetry/opentelemetry-specification/pull/1980))

## v1.7.0 (2021-09-30)

- BREAKING: Change enum member IDs to lowercase without spaces, not starting with numbers.
  Change values of `net.host.connection.subtype` to match.
  ([#1863](https://github.com/open-telemetry/opentelemetry-specification/pull/1863))
- Lambda instrumentations should check if X-Ray parent context is valid
  ([#1867](https://github.com/open-telemetry/opentelemetry-specification/pull/1867))
- Update YAML definitions for events
  ([#1843](https://github.com/open-telemetry/opentelemetry-specification/pull/1843)):
  - Mark exception as semconv type "event".
  - Add YAML definitions for grpc events.
- Add `messaging.consumer_id` to differentiate between message consumers.
  ([#1810](https://github.com/open-telemetry/opentelemetry-specification/pull/1810))
- Clarifications for `http.client_ip` and `http.host`.
  ([#1890](https://github.com/open-telemetry/opentelemetry-specification/pull/1890))
- Add HTTP request and response headers semantic conventions.
  ([#1898](https://github.com/open-telemetry/opentelemetry-specification/pull/1898))

## v1.6.0 (2021-08-06)

- Add mobile-related network state: `net.host.connection.type`, `net.host.connection.subtype` & `net.host.carrier.*` [#1647](https://github.com/open-telemetry/opentelemetry-specification/issues/1647)
- Adding alibaba cloud as a cloud provider.
  ([#1831](https://github.com/open-telemetry/opentelemetry-specification/pull/1831))

## v1.5.0 (2021-07-08)

- Clean up FaaS semantic conventions, add `aws.lambda.invoked_arn`.
  ([#1781](https://github.com/open-telemetry/opentelemetry-specification/pull/1781))
- Remove `rpc.jsonrpc.method`, clarify that `rpc.method` should be used instead.
  ([#1748](https://github.com/open-telemetry/opentelemetry-specification/pull/1748))

## v1.4.0 (2021-06-07)

- Add JSON RPC specific conventions ([#1643](https://github.com/open-telemetry/opentelemetry-specification/pull/1643)).
- Add Memcached to Database specific conventions ([#1689](https://github.com/open-telemetry/opentelemetry-specification/pull/1689)).
- Add semantic convention attributes for the host device and added OS name and version ([#1596](https://github.com/open-telemetry/opentelemetry-specification/pull/1596)).
- Add CockroachDB to Database specific conventions ([#1725](https://github.com/open-telemetry/opentelemetry-specification/pull/1725)).

## v1.3.0 (2021-05-05)

- Fix the inconsistent formatting of semantic convention enums. ([#1598](https://github.com/open-telemetry/opentelemetry-specification/pull/1598/))
- Add details for filling resource for AWS Lambda. ([#1610](https://github.com/open-telemetry/opentelemetry-specification/pull/1610))
- Add already specified `messaging.rabbitmq.routing_key` span attribute key to the respective YAML file. ([#1651](https://github.com/open-telemetry/opentelemetry-specification/pull/1651))
- Clarify usage of "otel." attribute namespace. ([#1640](https://github.com/open-telemetry/opentelemetry-specification/pull/1640))
- Add possibility to disable `db.statement` via instrumentation configuration. ([#1659](https://github.com/open-telemetry/opentelemetry-specification/pull/1659))

## v1.2.0 (2021-04-14)

- Add semantic conventions for AWS SDK operations and DynamoDB ([#1422](https://github.com/open-telemetry/opentelemetry-specification/pull/1422))
- Add details for filling semantic conventions for AWS Lambda ([#1442](https://github.com/open-telemetry/opentelemetry-specification/pull/1442))
- Update semantic conventions to distinguish between int and double ([#1550](https://github.com/open-telemetry/opentelemetry-specification/pull/1550))
- Add semantic convention for AWS ECS task revision ([#1581](https://github.com/open-telemetry/opentelemetry-specification/pull/1581))

## v1.1.0 (2021-03-11)

- Add `elasticsearch` to `db.system` semantic conventions ([#1463](https://github.com/open-telemetry/opentelemetry-specification/pull/1463))
- Add `arch` to `host` semantic conventions ([#1483](https://github.com/open-telemetry/opentelemetry-specification/pull/1483))
- Add `runtime` to `container` semantic conventions ([#1482](https://github.com/open-telemetry/opentelemetry-specification/pull/1482))
- Rename `gcp_gke` to `gcp_kubernetes_engine` to have consistency with other
  Google products under `cloud.infrastructure_service` ([#1496](https://github.com/open-telemetry/opentelemetry-specification/pull/1496))
- `http.url` MUST NOT contain credentials ([#1502](https://github.com/open-telemetry/opentelemetry-specification/pull/1502))
- Add `aws.eks.cluster.arn` to EKS specific semantic conventions ([#1484](https://github.com/open-telemetry/opentelemetry-specification/pull/1484))
- Rename `zone` to `availability_zone` in `cloud` semantic conventions ([#1495](https://github.com/open-telemetry/opentelemetry-specification/pull/1495))
- Rename `cloud.infrastructure_service` to `cloud.platform` ([#1530](https://github.com/open-telemetry/opentelemetry-specification/pull/1530))
- Add section describing that libraries and the collector should autogenerate
  the semantic convention keys. ([#1515](https://github.com/open-telemetry/opentelemetry-specification/pull/1515))

## v1.0.1 (2021-02-11)

N/A

## v1.0.0 (2021-02-10)

First release of OpenTelemetry Specification. Semantic conventions were not explicitly tracked in changelog up to this point.
