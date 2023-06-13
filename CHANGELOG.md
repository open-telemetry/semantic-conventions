# Changelog

Please update changelog as part of any significant pull request. Place short
description of your change into "Unreleased" section. As part of release process
content of "Unreleased" section content will generate release notes for the
release.

## Unreleased

- Updated AWS Java Lambda guidance - using system properties.

### Semantic Conventions

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
     `net.host.name` and `net.host.port` to `server.name` and `server.port` (since `net.host.*` attributes only applied to server instrumentation)
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
- Mark initial set of HTTP semantic conventions as frozen
  ([#105](https://github.com/open-telemetry/semantic-conventions/pull/105))
