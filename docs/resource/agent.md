<!--- Hugo front matter used to generate the website version of this page:
--->

# Agent

## Agent Attributes

<!-- semconv agent(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`agent.type`](../attributes-registry/agent.md) | string | Agent type. [1] | `io.opentelemetry.collector`; `com.dynatrace.one_agent`; `com.newrelic.infra_agent` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`agent.distro`](../attributes-registry/agent.md) | string | Agent distribution. [2] | `github.com/signalfx/splunk-otel-collector`; `github.com/aws-observability/aws-otel-collector` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`agent.version`](../attributes-registry/agent.md) | string | The version string of the agent. The format is not defined by these conventions. | `2.0.0`; `a01dbef8a` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** A string that uniquely identifies the agent type. A recommended way to choose a value is to pick a reverse FQDN of a domain that is under the control of the agent's author. Must remain unchanged between different versions of the same agent type.

**[2]:** Identifies the distribution of the agent. A number of distributions can belong to the same `agent.type`. For example OpenTelemetry Collector has multiple known distributions, e.g. github.com/signalfx/splunk-otel-collector, github.com/aws-observability/aws-otel-collector, etc.  The value is typically a URL where the agent's source code is hosted  (without the preceding http/https scheme). However other approaches for choosing `agent.distro` values are also valid (e.g. reverse FQDN).
<!-- endsemconv -->
