<!--- Hugo front matter used to generate the website version of this page:
aliases: [attribute-naming]
--->

# Naming

**Status**: [Stable][DocumentStatus], Unless otherwise specified.

<details>
<summary>Table of Contents</summary>

<!-- toc -->

- [General Naming Considerations](#general-naming-considerations)
- [Name Abbreviation Guidelines](#name-abbreviation-guidelines)
- [Name Reuse Prohibition](#name-reuse-prohibition)
- [Recommendations for OpenTelemetry Authors](#recommendations-for-opentelemetry-authors)
- [Recommendations for Application Developers](#recommendations-for-application-developers)
- [Attributes](#attributes)
  - [otel.\* Namespace](#otel-namespace)
  - [Attribute Name Pluralization Guidelines](#attribute-name-pluralization-guidelines)
  - [Signal-specific Attributes](#signal-specific-attributes)
- [Metrics](#metrics)
  - [Naming Rules for Counters and UpDownCounters](#naming-rules-for-counters-and-updowncounters)
    - [Pluralization](#pluralization)
    - [Use `count` Instead of Pluralization for UpDownCounters](#use-count-instead-of-pluralization-for-updowncounters)
    - [Do Not Use `total`](#do-not-use-total)
  - [Instrument Naming](#instrument-naming)

<!-- tocstop -->

</details>

## General Naming Considerations

_This section applies to attribute names (also
known as the "attribute keys"), as well as Metric and Event names. For brevity
within this section when we use the term "name" without an adjective it is
implied to mean all of these._

Every name MUST be a valid Unicode sequence.

_Note: we merely require that the names are represented as Unicode sequences.
This specification does not define how exactly the Unicode sequences are
encoded. The encoding can vary from one programming language to another and from
one wire format to another. Use the idiomatic way to represent Unicode in the
particular programming language or wire format._

Names SHOULD follow these rules:

- Names SHOULD be lowercase.

- Use namespacing. Delimit the namespaces using a dot character.
  For example `service.version` denotes the service version where
  `service` is the namespace and `version` is an attribute in that namespace.

- Namespaces can be nested. For example `telemetry.sdk` is a namespace inside
  top-level `telemetry` namespace and `telemetry.sdk.name` is an attribute
  inside `telemetry.sdk` namespace.

  Use namespaces (and dot separator) whenever it makes sense. For example
  when introducing an attribute representing a property of some object, follow
  `*{object}.{property}` pattern. Avoid using underscore (`*{object}_{property}`)
  if this object could have other properties.

- For each multi-word dot-delimited component of the name separate the
  words by underscores (i.e. use snake_case). For example
  `http.response.status_code` denotes the status code in the http namespace.

  Use underscore only when using dot (namespacing) does not make sense or changes
  the semantic meaning of the name. For example, use `rate_limiting`
  instead of `rate.limiting`.

- Be precise. Attribute, event, metric, and other names should be descriptive and
  unambiguous.
  - When introducing a name describing a certain property of the object,
    include the property name. For example, use `file.owner.name` instead of `file.owner`
    and `system.network.packet.dropped` instead of `system.network.dropped`
  - Avoid introducing names and namespaces that would mean different things when
    used by different conventions or instrumentations. For example, use `security_rule`
    instead of `rule`.

- Use shorter names when it does not compromise clarity. Drop namespace
  components or words in multi-word components when they are not necessary. For example,
  `vcs.change.id` describes pull request id as precisely as `vcs.repository.change.id` does.

## Name Abbreviation Guidelines

Abbreviations MAY be used when they are widely recognized and commonly used.

Examples include common technical abbreviations such as `IP`, `DB`, `CPU`,
`HTTP`, `URL`, or product names like `AWS`, `GCP`, `K8s`.

Abbreviations that are commonly recognized but only within a certain domain MAY
be used when qualified by the corresponding namespace.

For example, use `container.csi.*` instead of `container.container_storage_interface`
or `container.oci.*` instead of `container.open_container_initiative.*`

Abbreviations SHOULD be avoided if they are ambiguous, for example, when they apply
to multiple products or concepts.

## Name Reuse Prohibition

Two attributes, two metrics, or two events MUST NOT share the same name.
Different entities (attribute and metric, metric and event) MAY share the same name.

Attributes, metrics, and events SHOULD NOT be removed from semantic
conventions regardless of their maturity level. When the convention is renamed or
no longer recommended, it SHOULD be deprecated.

## Recommendations for OpenTelemetry Authors

- When coming up with a new semantic convention make sure to check existing
  namespaces ([Semantic Conventions](/docs/README.md)) to see if a similar namespace
  already exists.

- All names that are part of OpenTelemetry semantic conventions SHOULD be part
  of a namespace.

- When a new namespace is necessary consider whether it should be a top-level
  namespace (e.g. `service`) or a nested namespace (e.g. `service.instance`).

- Semantic conventions MUST limit names to printable Basic Latin characters
  (more precisely to
  [U+0021 .. U+007E](<https://wikipedia.org/wiki/Basic_Latin_(Unicode_block)#Table_of_characters>)
  subset of Unicode code points). It is recommended to further limit names to
  the following Unicode code points: Latin alphabet, Numeric, Underscore, Dot
  (as namespace delimiter).

> Note:
> Semantic Conventions tooling limits names to lowercase
> Latin alphabet, Numeric, Underscore, Dot (as namespace delimiter).
> Names must start with a letter, end with an alphanumeric character, and must not
> contain two or more consecutive delimiters (Underscore or Dot).

## Recommendations for Application Developers

As an application developer when you need to record an attribute, metric, event, or
other signal first consult existing [semantic conventions](./README.md).
If an appropriate name does not exists you will need to come up with a new name.
To do that consider a few options:

- The name is specific to your company and may be possibly used outside the
  company as well. To avoid clashes with names introduced by other companies (in
  a distributed system that uses applications from multiple vendors) it is
  recommended to prefix the new name by your company's reverse domain name, e.g.
  `com.acme.shopname`.

- The name is specific to your application that will be used internally only. If
  you already have an internal company process that helps you to ensure no name
  clashes happen then feel free to follow it. Otherwise it is recommended to
  prefix the attribute name by your application name, provided that the
  application name is reasonably unique within your organization (e.g.
  `myuniquemapapp.longitude` is likely fine). Make sure the application name
  does not clash with an existing semantic convention namespace.

- It is not recommended to use existing OpenTelemetry semantic convention
  namespace as a prefix for a new company- or application-specific attribute
  name. Doing so may result in a name clash in the future, if OpenTelemetry
  decides to use that same name for a different purpose or if some other third
  party instrumentation decides to use that exact same attribute name and you
  combine that instrumentation with your own.

- The name may be generally applicable to applications in the industry. In that
  case consider submitting a proposal to this specification to add a new name to
  the semantic conventions, and if necessary also to add a new namespace.

It is recommended to limit names to printable Basic Latin characters (more
precisely to
[U+0021 .. U+007E](<https://wikipedia.org/wiki/Basic_Latin_(Unicode_block)#Table_of_characters>)
subset of Unicode code points).

## Attributes

### otel.\* Namespace

Attribute names that start with `otel.` are reserved to be defined by
OpenTelemetry specification. These are typically used to express OpenTelemetry
concepts in formats that don't have a corresponding concept.

For example, the `otel.scope.name` attribute is used to record the
instrumentation scope name, which is an OpenTelemetry concept that is natively
represented in OTLP, but does not have an equivalent in other telemetry formats
and protocols.

Any additions to the `otel.*` namespace MUST be approved as part of
OpenTelemetry specification.

### Attribute Name Pluralization Guidelines

- When an attribute represents a single entity, the attribute name SHOULD be
  singular. Examples: `host.name`, `container.id`.

- When attribute can represent multiple entities, the attribute name SHOULD be
  pluralized and the value type SHOULD be an array. E.g. `process.command_args`
  might include multiple values: the executable name and command arguments.

- When an attribute represents a measurement,
  [Name Pluralization Guidelines](./naming.md#pluralization) SHOULD be
  followed for the attribute name.

### Signal-specific Attributes

**Status**: [Development][DocumentStatus]

Attributes are defined in semantic conventions in a signal-agnostic way. The same attribute
is expected to be used on multiple signals.

When an attribute is defined, it is not always clear if it will be applicable outside
of a certain metric, event, or other convention.

Attributes that are unlikely to have any usage beyond a specific convention,
SHOULD be added under that metric (event, etc) namespace.

Examples:

Attributes `mode` and `mountpoint` for metric `system.filesystem.usage`
should be namespaced as `system.filesystem.mode` and `system.filesystem.mountpoint`.

Metrics, events, resources, and other signals are expected and encouraged to use
applicable attributes from multiple namespaces.

Examples:

Metric `http.server.request.duration` uses attributes from the registry such as
`server.port`, `error.type`.

## Metrics

**Status**: [Development][DocumentStatus]

### Naming Rules for Counters and UpDownCounters

#### Pluralization

Metric namespaces SHOULD NOT be pluralized.

Metric names SHOULD NOT be pluralized, unless the value being recorded
represents discrete instances of a
[countable quantity](https://wikipedia.org/wiki/Count_noun).
Generally, the name SHOULD be pluralized only if the unit of the metric in
question is a non-unit (like `{fault}` or `{operation}`).

Examples:

* `system.filesystem.utilization`, `http.server.request.duration`, and `system.cpu.time`
should not be pluralized, even if many data points are recorded.
* `system.paging.faults`, `system.disk.operations`, and `system.network.packets`
should be pluralized, even if only a single data point is recorded.

#### Use `count` Instead of Pluralization for UpDownCounters

If the value being recorded represents the count of concepts signified
by the namespace then the metric should be named `count` (within its namespace).

For example if we have a namespace `system.process` which contains all metrics related
to the processes then to represent the count of the processes we can have a metric named
`system.process.count`.

#### Do Not Use `total`

UpDownCounters SHOULD NOT use `_total` because then they will look like
monotonic sums.

Counters SHOULD NOT append `_total` either because then their meaning will
be confusing in delta backends.

### Instrument Naming

**Status**: [Development][DocumentStatus]

- **limit** - an instrument that measures the constant, known total amount of
something should be called `entity.limit`. For example, `system.memory.limit`
for the total amount of memory on a system.

- **usage** - an instrument that measures an amount used out of a known total
(**limit**) amount should be called `entity.usage`. For example,
`system.memory.usage` with attribute `state = used | cached | free | ...` for the
amount of memory in a each state. Where appropriate, the sum of **usage**
over all attribute values SHOULD be equal to the **limit**.

  A measure of the amount consumed of an unlimited resource, or of a resource
  whose limit is unknowable, is differentiated from **usage**. For example, the
  maximum possible amount of virtual memory that a process may consume may
  fluctuate over time and is not typically known.

- **utilization** - an instrument that measures the _fraction_ of **usage**
out of its **limit** should be called `entity.utilization`. For example,
`system.memory.utilization` for the fraction of memory in use. Utilization can
be with respect to a fixed limit or a soft limit. Utilization values are
represented as a ratio and are typically in the range `[0, 1]`, but may go above 1
in case of exceeding a soft limit.

- **time** - an instrument that measures passage of time should be called
`entity.time`. For example, `system.cpu.time` with attribute `state = idle | user
| system | ...`. **time** measurements are not necessarily wall time and can
be less than or greater than the real wall time between measurements.

  **time** instruments are a special case of **usage** metrics, where the
  **limit** can usually be calculated as the sum of **time** over all attribute
  values. **utilization** for time instruments can be derived automatically
  using metric event timestamps. For example, `system.cpu.utilization` is
  defined as the difference in `system.cpu.time` measurements divided by the
  elapsed time and number of CPUs.

- **io** - an instrument that measures bidirectional data flow should be
called `entity.io` and have attributes for direction. For example,
`system.network.io`.

- Other instruments that do not fit the above descriptions may be named more
freely. For example, `system.paging.faults` and `system.network.packets`.
Units do not need to be specified in the names since they are included during
instrument creation, but can be added if there is ambiguity.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
