# Blah

- BREAKING: Generate process metrics from YAML
  ([#330](https://github.com/open-telemetry/semantic-conventions/pull/330))
  - Rename attributes for `process.cpu.*`
    - `state` to `process.cpu.state`
  - Change attributes for `process.disk.io`
    - Instead of `direction` use `disk.io.direction` from global registry
  - Change attributes for `process.network.io`
    - Instead of `direction` use `network.io.direction` from global registry
  - Rename `process.threads` to `process.thread.count`
  - Rename `process.open_file_descriptors` to `process.open_file_descriptor.count`
  - Rename attributes for `process.context_switches`
    - `type` to `process.context_switch_type`
  - Rename attributes for `process.paging.faults`
    - `type` to `process.paging.fault_type`
