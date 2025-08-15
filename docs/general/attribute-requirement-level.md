# Attribute requirement levels

**Status**: [Stable][DocumentStatus]

<details>
<summary>Table of Contents</summary>

<!-- toc -->

- [Required](#required)
- [Conditionally Required](#conditionally-required)
- [Recommended](#recommended)
- [Opt-In](#opt-in)
- [Migrate](#migrate)
  - [Stable Instrumentation](#stable-instrumentation)
  - [Long-term Unstable Instrumentation](#long-term-unstable-instrumentation)
  - [Unstable Instrumentation](#unstable-instrumentation)
- [Remove](#remove)
  - [Stable Instrumentation](#stable-instrumentation-1)
  - [Long-term Unstable Instrumentation](#long-term-unstable-instrumentation-1)
  - [Unstable Instrumentation](#unstable-instrumentation-1)
- [Performance suggestions](#performance-suggestions)

<!-- tocstop -->

</details>

_This section applies to Log, Metric, Resource, and Span, and describes
requirement levels for attributes defined in semantic conventions._

Attribute requirement levels apply to the
[instrumentation library](https://opentelemetry.io/docs/concepts/glossary/#instrumentation-library).

The following attribute requirement levels are specified:

- [Required](#required)
- [Conditionally Required](#conditionally-required)
- [Recommended](#recommended)
- [Opt-In](#opt-in)

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

For example, [Database semantic convention](../database/README.md) references
`network.transport` attribute defined in [General attributes](./README.md) with
`Conditionally Required` level on it.

## Required

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

## Conditionally Required

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

For example, `server.address` is `Conditionally Required` by the
[Database convention](../database/README.md) when available. When
`network.peer.address` is available instead, instrumentation can do a DNS
lookup, cache and populate `server.address`, but only if the user explicitly
enables the instrumentation to do so, considering the performance issues that
DNS lookups introduce.

## Recommended

Instrumentations SHOULD add the attribute by default if it's readily available
and can be [efficiently populated](#performance-suggestions). Instrumentations
MAY offer a configuration option to disable Recommended attributes.

Instrumentations that decide not to populate `Recommended` attributes due to
[performance](#performance-suggestions), security, privacy, or other
consideration by default, SHOULD allow for users to opt-in to emit them as
defined for the `Opt-In` requirement level (if the attributes are logically
applicable).

## Opt-In

Instrumentations SHOULD populate the attribute if and only if the user
configures the instrumentation to do so. Instrumentation that doesn't support
configuration MUST NOT populate `Opt-In` attributes.

This attribute requirement level is recommended for attributes that are
particularly expensive to retrieve or might pose a security or privacy risk.
These should therefore only be enabled explicitly by a user making an informed
decision.

## Migrate

The migrate requirement level is reserved for deprecated attributes and is
designed to help support achieving a phased rollout of the stable semantic conventions.
Under no circumstances should this attribute be added to an existing instrumentation.

The type of instrumentation helps to determine how the attribute should be handled, see below.

### Stable Instrumentation

Should continue emitting the attribute unless:

* User has set the domain e.g. `database` via the `OTEL_SEMCONV_STABILITY_OPT_IN` environment variable.
* User has excluded the attribute via explicit configuration
* The instrumentation bumps its major version but will continue providing security patches for
the previous major version for at least 6 months.

Removal can occur when the major version is bumped provided previous major version will/has received 6 months of security patches from the time the replacement attribute is introduced.

### Long-term Unstable Instrumentation

> [!NOTE]
> Examples of long term unstable instrumentation, would be the OpenTelemetry Contrib packages as
> their stability is following that of the signal they are implementing.

Should stop emitting the attribute unless:

* User has set the domain e.g. `database/dup` via the `OTEL_SEMCONV_STABILITY_OPT_IN` environment variable.
* User has included the attribute via explicit configuration

Removal can occur when the deployment level of the package changes. For instance a beta package moves to release candidate.

### Unstable Instrumentation

Removal can occur once the new attribute is implemented,
provided that the instrumentation does not fall into any of the other categories.
Should that be the case the guidance for that category should be followed.

## Remove

The remove requirement level is reserved for deprecated attributes that are no longer relevant.
Under no circumstances should this attribute be added to an existing instrumentation.

The type of instrumentation helps to determine how the attribute should be handled, see below.

### Stable Instrumentation

Should continue emitting the attribute unless:

* User has excluded the attribute via explicit configuration
* The instrumentation bumps its major version but will continue providing security patches for
the previous major version for at least 6 months.

Removal can occur when the major version is bumped provided that previous major version will/has
received 6 months of security patches from the time that the default behaviour was changed to not emit.

### Long-term Unstable Instrumentation

Should stop emitting the attribute unless:

* User has included the attribute via explicit configuration

Removal can occur when the deployment level of the package changes. For instance a beta package moves to release candidate.

### Unstable Instrumentation

Can remove attribute at any time,
provided that the instrumentation does not fall into any of the other categories.
Should that be the case the guidance for that category should be followed.

## Performance suggestions

Here are several examples of expensive operations to be avoided by default:

- DNS lookups to populate `server.address` when only an IP address is available
  to the instrumentation. Caching lookup results does not solve the issue for
  all possible cases and should be avoided by default too.
- forcing an `http.route` calculation before the HTTP framework calculates it
- reading response stream to find `http.response.body.size` when
  `Content-Length` header is not available

[DocumentStatus]:
  https://opentelemetry.io/docs/specs/otel/document-status
