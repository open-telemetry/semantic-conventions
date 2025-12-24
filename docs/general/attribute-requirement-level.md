# Attribute requirement levels

**Status**: [Stable][DocumentStatus]

<details>
<summary>Table of Contents</summary>

<!-- toc -->

- [Requirement Levels](#requirement-levels)
  - [Required](#required)
  - [Conditionally Required](#conditionally-required)
  - [Recommended](#recommended)
  - [Opt-In](#opt-in)
- [Performance suggestions](#performance-suggestions)

<!-- tocstop -->

</details>

_This section applies to Log, Metric, Resource, and Span, and describes
requirement levels for attributes defined in semantic conventions._

Attribute requirement levels apply to the
[instrumentation library](https://opentelemetry.io/docs/concepts/glossary/#instrumentation-library).

The requirement level for an attribute is specified by semantic conventions
depending on attribute availability across instrumented entities, performance,
security, and other factors. When specifying requirement levels, a semantic
convention MUST take into account signal-specific requirements.

For example, Metric attributes that may have high cardinality can only be
defined with `Opt-In` level.

A semantic convention that refers to an attribute from another semantic
convention MAY modify the requirement level within its own scope. Otherwise,
requirement level from the referred semantic convention applies.

<!-- TODO(jsuereth) - make examples not break on changes to semconv -->

For example, [Database semantic convention](/docs/db/README.md) references
`network.transport` attribute defined in [General attributes](./README.md) with
`Conditionally Required` level on it.

## Requirement Levels

The below table details the default inclusion behaviour of attributes on telemetry signals and
if it can be changed via configuration options.

| Level                                             | Included by default | Can be included via config | Can be excluded via Config |
| ------------------------------------------------- | ------------------- | -------------------------- | -------------------------- |
| [Required](#required)                             | Yes                 | n/a                        | No                         |
| [Conditionally Required](#conditionally-required) | Yes [1]             | No [1]                     | No [1]                     |
| [Recommended](#recommended)                       | Yes [2]             | No [2]                     | Yes                        |
| [Opt-In](#opt-in)                                 | No                  | Yes                        | Yes                        |

**[1]:** unless the attribute requirement conditions or instructions are not satisfied.

**[2]:** unless it was excluded for a reason outlined in [Recommended](#recommended) section.

### Required

All instrumentations MUST populate the attribute. A semantic convention defining
a Required attribute expects an absolute majority of instrumentation libraries
and applications are able to efficiently retrieve and populate it, and can
additionally meet requirements for cardinality, security, and any others
specific to the signal defined by the convention. `http.request.method` is an
example of a Required attribute.

_Note: Consumers of telemetry can detect if a telemetry item follows a specific
semantic convention by checking for the presence of a `Required` attribute
defined by such convention. For example, the presence of the `db.system.name`
attribute on a span can be used as an indication that the span follows database
semantics._

### Conditionally Required

All instrumentations MUST populate the attribute when the given condition is
satisfied. The semantic convention of a `Conditionally Required` attribute MUST
clarify the condition under which the attribute is to be populated.

`http.route` is an example of a conditionally required attribute that is
populated when the instrumented HTTP framework provides route information for
the instrumented request. Some low-level HTTP server implementations do not
support routing and corresponding instrumentations can't populate the attribute.

When a `Conditionally Required` attribute's condition is not satisfied, and
there is no requirement to populate the attribute, semantic conventions MAY
provide special instructions on how to handle it. If no instructions are given
and if instrumentation can populate the attribute, instrumentation SHOULD use
the `Opt-In` requirement level on the attribute.

<!-- TODO(jsuereth) - make examples not break on changes to semconv -->

For example, `server.address` is `Conditionally Required` by a convention. When
server IP address is available instead, instrumentation can do a DNS
lookup, cache and populate `server.address`, but only if the user explicitly
enables the instrumentation to do so, considering the performance issues that
DNS lookups introduce.

### Recommended

Instrumentations SHOULD add the attribute by default if it's readily available
and can be [efficiently populated](#performance-suggestions). Instrumentations
MAY offer a configuration option to disable Recommended attributes.

Instrumentations that decide not to populate `Recommended` attributes due to
[performance](#performance-suggestions), security, privacy, or other
consideration by default, SHOULD allow for users to opt-in to emit them as
defined for the `Opt-In` requirement level (if the attributes are logically
applicable).

### Opt-In

Instrumentations SHOULD populate the attribute if and only if the user
configures the instrumentation to do so. Instrumentation that doesn't support
configuration MUST NOT populate `Opt-In` attributes.

This attribute requirement level is recommended for attributes that are
particularly expensive to retrieve or might pose a security or privacy risk.
These should therefore only be enabled explicitly by a user making an informed
decision.

## Performance suggestions

Here are several examples of expensive operations to be avoided by default:

- DNS lookups to populate `server.address` when only an IP address is available
  to the instrumentation. Caching lookup results does not solve the issue for
  all possible cases and should be avoided by default too.
- forcing an `http.route` calculation before the HTTP framework calculates it
- reading response stream to find `http.response.body.size` when
  `Content-Length` header is not available

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
