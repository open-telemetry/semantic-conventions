Generated changelog updates for user:
## vTODO

### 🛑 Breaking changes 🛑

- `event`: Deprecate `event.name` attribute in favor of the top level event name property on the log record ([#1646](https://github.com/open-telemetry/semantic-conventions/issues/1646))
- `gen_ai`: Rename `gen_ai.openai.request.seed` to `gen_ai.request.seed` and use it on general GenAI conventions. ([#1715](https://github.com/open-telemetry/semantic-conventions/issues/1715))
- `code`: rename `code.function`, `code.lineno`, `code.column` and `code.filepath` ([#1377](https://github.com/open-telemetry/semantic-conventions/issues/1377), [#1599](https://github.com/open-telemetry/semantic-conventions/issues/1599))
  `code.function` renamed to `code.function.name`
  `code.lineno` renamed to `code.line.number`
  `code.column` renamed to `code.column.number`
  `code.filepath` renamed to `code.file.path`
  
- `system`: Replace `system.network.state` with `network.connection.state` ([#308](https://github.com/open-telemetry/semantic-conventions/issues/308))

### 🚀 New components 🚀

- `security-rule`: Introducing a new security rule namespace ([#903](https://github.com/open-telemetry/semantic-conventions/issues/903))

### 💡 Enhancements 💡

- `gen_ai`: Yamlify gen_ai events and clean up examples. ([#1469](https://github.com/open-telemetry/semantic-conventions/issues/1469))
- `genai`: Adds OpenAI API compatible `gen_ai.system` attribute values: `az.ai.openai`, `deepseek`, `gemini`, `groq`,
`perplexity` and `xai`. Elaborates that `openai` can be ambiguous due to API emulation.
 ([#1655](https://github.com/open-telemetry/semantic-conventions/issues/1655))
- `docs`: Update attribute, events, and metrics naming guidance to include new best practices. ([#1694](https://github.com/open-telemetry/semantic-conventions/issues/1694))
  - Use namespaces (with `.` delimiter) whenever possible.
  - Use precise, descriptive, unambiguous names that leave room for expansion.
  
- `k8s`: Add metrics for k8s deployment, replicaset, replication_controller, statefulset and hpa. ([#1636](https://github.com/open-telemetry/semantic-conventions/issues/1636), [#1637](https://github.com/open-telemetry/semantic-conventions/issues/1637), [#1644](https://github.com/open-telemetry/semantic-conventions/issues/1644))
  This addition focused on providing consistency between these metrics, while
  also ensuring alignment with recommendations from Kubernetes.
  More details in https://github.com/open-telemetry/semantic-conventions/issues/1637
  
- `k8s`: Add k8s deamonset related metrics ([#1649](https://github.com/open-telemetry/semantic-conventions/issues/1649))
- `aws`: Add extended request ID to general AWS attributes as `aws.extended_request_id` ([#1670](https://github.com/open-telemetry/semantic-conventions/issues/1670))
- `messaging`: Further clarify `{destination}` value on span names ([#1635](https://github.com/open-telemetry/semantic-conventions/issues/1635))
- `fake`: This is a fake changelog record to test CI. It also has a [non-existing link](https://dklfgjdflkgjlkdfgjkldjdflk.com) ([#1723](https://github.com/open-telemetry/semantic-conventions/issues/1723))
- `gen_ai`: Introduce gen_ai.request.seed and deprecated gen_ai.openai.request.seed ([#1710](https://github.com/open-telemetry/semantic-conventions/issues/1710))
- `k8s`: Add migration guide for K8s semantic conventions ([#1597](https://github.com/open-telemetry/semantic-conventions/issues/1597))
- `dotnet`: Mark .NET runtime metrics as stable ([#1602](https://github.com/open-telemetry/semantic-conventions/issues/1602))
- `vcs`: Adds `vcs.repository.name` attribute to registry and update
`vcs.repository.url.full` description for consistent representation. Updates
the VCS metrics to include `vcs.repository.name` as a recommended attribute.
 ([#1254](https://github.com/open-telemetry/semantic-conventions/issues/1254), [#1453](https://github.com/open-telemetry/semantic-conventions/issues/1453))

