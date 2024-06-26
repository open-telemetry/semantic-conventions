<!--- Hugo front matter used to generate the website version of this page:
--->

# Agent

## Agent Attributes

<!-- semconv registry.agent(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `agent.distro` | string | Agent distribution. [1] | `github.com/signalfx/splunk-otel-collector`; `github.com/aws-observability/aws-otel-collector` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `agent.id` | string | Unique identifier of agent instance. [2] | `627cc493-f310-47de-96bd-71410b7dec09` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `agent.type` | string | Agent type. [3] | `io.opentelemetry.collector`; `com.dynatrace.one_agent`; `com.newrelic.infra_agent` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `agent.version` | string | The version string of the agent. The format is not defined by these conventions. | `2.0.0`; `a01dbef8a` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Identifies the distribution of the agent. A number of distributions can belong to the same `agent.type`. For example OpenTelemetry Collector has multiple known distributions, e.g. github.com/signalfx/splunk-otel-collector, github.com/aws-observability/aws-otel-collector, etc.  The value is typically a URL where the agent's source code is hosted  (without the preceding http/https scheme). However other approaches for choosing `agent.distro` values are also valid (e.g. reverse FQDN).

**[2]:** If a deterministic source for an id is not available it is recommended to use a UUID v7 value.

**[3]:** A string that uniquely identifies the agent type. A recommended way to choose a value is to pick a reverse FQDN of a domain that is under the control of the agent's author. Must remain unchanged between different versions of the same agent type.
<!-- endsemconv -->
