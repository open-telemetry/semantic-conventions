<!--- Hugo front matter used to generate the website version of this page:
linkTitle: How to write conventions
aliases: [/docs/specs/semconv/general/how-to-define-semantic-conventions]
--->

# How to write semantic conventions

**Status**: [Development][DocumentStatus]

<!-- toc -->

- [Defining new conventions](#defining-new-conventions)
  - [Best practices](#best-practices)
    - [Prototyping](#prototyping)
    - [Defining attributes](#defining-attributes)
    - [Defining enum attribute members](#defining-enum-attribute-members)
    - [Defining spans](#defining-spans)
    - [Defining metrics](#defining-metrics)
    - [Defining entities](#defining-entities)
    - [Defining events](#defining-events)
- [Stabilizing existing conventions](#stabilizing-existing-conventions)
  - [Migration plan](#migration-plan)

<!-- tocstop -->

This document describes requirements, recommendations, and best practices on how to define conventions
for new areas or make substantial changes to the existing ones.

## Defining new conventions

- New conventions MUST have a group of codeowners. See [project management](https://github.com/open-telemetry/community/blob/main/project-management.md) for more details.
  <!-- TODO: add CI check for CODEOWNERS file (when a new area is added) -->
- New conventions SHOULD be defined in YAML files. See [YAML Model for Semantic Conventions](/model/README.md) for the details.
- New conventions SHOULD be defined with `development` stability level.
- New conventions SHOULD include telemetry signal definitions (spans, metrics, events, resources, profiles) and MAY include new attribute definitions.

### Best practices

> [!NOTE]
>
> This section contains non-normative guidance.

Please read [T-Shaped Signals](t-shaped-signals.md)
for guidance on how to approach creating Semantic Conventions through defining
key use cases for conventions.

#### Prototyping

It is strongly recommended to prototype proposed conventions in one or more instrumentations and:

- validate the feasibility of collecting the proposed telemetry and attributes, ensuring the information is available and can be gathered with reasonable overhead,

- confirm that the proposed terminology applies across the diverse libraries and technologies covered by the conventions,

- provide actionable guidance to instrumentation authors on when and how to collect attributes and record telemetry,

- evaluate how the new or updated telemetry integrates with other instrumentation layers, identifying gaps, duplication, or opportunities to improve the end-user experience.

#### Defining attributes

Reuse existing attributes when possible. Look through [existing conventions](/docs/registry/attributes/) for similar areas,
check out [common attributes](/docs/general/attributes.md).
Semantic conventions authors are encouraged to use attributes from different namespaces.

Consider adding a new attribute if all of the following apply:

- It provides a clear benefit to end users by enhancing telemetry.
- There is a clear plan to use the attributes when defining spans, metrics, events, resources, or other telemetry signals in semantic conventions.
- There is a clear plan on how these attributes will be used by instrumentations

Semantic convention maintainers may reject the addition of a new attribute if its benefits
and use-cases are not yet clear.

When defining a new attribute:

- Follow the [naming guidance](/docs/general/naming.md)
- Provide descriptive `brief` and `note` sections to clearly explain what the attribute represents.
  - If the attribute represents a common concept documented externally, include relevant links.
    For example, always link to concepts defined in RFCs or other standards.
  - If the attribute's value might contain PII or other sensitive information, explicitly call this out in
    the `note`.

    Include a warning similar to the following: <!-- TODO: update existing semconv -->

    ```yaml
      - id: user.full_name
        ...
        note: |
          ...

          > [!WARNING]
          >
          > This attribute contains sensitive (PII) information.
    ```

- Use the appropriate [attribute type](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md#type)
  - If the value has a reasonably short (open or closed) set of possible values, define it as an enum.
  - If the value is a timestamp, record it as a string in ISO 8601 format.
  - For arrays of primitives, use the array type. Avoid recording arrays as a single string.
  - Arrays should be homogeneous, meaning all elements share the same type and represent the same concept.
    For example:
    - Latitude and longitude should be defined as separate attributes (`geo.lat` and `geo.lon`)
      rather than combining them into a single array, as they represent distinct concepts.
  - Use the template type to define attributes with dynamic names (only the last segment of the name should be dynamic).
    This is useful for capturing user-defined key-value pairs, such as HTTP headers.
  - Represent complex values as a set of flat attributes whenever possible.
    - Complex or structured attributes (not listed in the
      [set of standard attributes](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.53.0/specification/common/README.md#attribute))
      could be referenced on events and spans (![Development](https://img.shields.io/badge/-development-blue)) only.

      Semantic convention authors should assume that backends do not index individual properties of complex attributes,
      that querying or aggregating on such properties is inefficient and complicated,
      and that reporting complex attributes carries higher performance overhead.

- Define new attributes with `development` stability.
- Provide realistic examples
- Avoid defining attributes with potentially unbounded values, such as strings longer than
  1 KB or arrays with more than 1,000 elements. Such values should be recorded in the log or event body instead. <!-- This may change, check out https://github.com/open-telemetry/semantic-conventions/issues/1651 to monitor the progress -->

Consider the scope of the attribute and how it may evolve in the future:

- When defining an attribute for a narrow use case, think about potential broader use cases.
  For example, if creating a system-specific attribute, evaluate whether other systems
  in the same domain might need a similar attribute in the future.

  Similarly, instead of defining a simple boolean flag indicating a success or failure, consider a
  more extensible approach, such as using a `foo.status_code` attribute to include additional details.

- When defining a broad attribute applicable across multiple domains or systems,
  check for existing standards or widely accepted best practices in the industry.
  Avoid creating generic attributes that are not based on established standards.

> [!NOTE]
>
> When defining conventions for areas with multiple implementations or systems — such as databases,
> or cloud providers — it can take time to strike the right balance between being
> overly generic and not generic enough.
>
> Start with experimental conventions, document how they apply to a diverse range
> of providers, systems, or libraries, and prototype instrumentations.
>
> The end-user experience should serve as the primary guiding principle:
>
> - If the attribute is expected to be used in general-purpose metrics for the area,
>   consider introducing a common attribute.
>
>   For example, most messaging systems have a concept like a queue or topic.
>   Queue or topic names are critical for latency and throughput metrics and
>   equally important for spans to debug and visualize message flow.
>   This indicates the need for a generic attribute representing any type of messaging destination.
>
> - If the attribute represents something useful in a narrow set of scenarios or
>   is specific to certain system metrics, spans, or events, it likely does not need to be generic.

#### Defining enum attribute members

Enum attributes generally fall into three main categories:

**Complete enums** document all possible values. For example, `cpu.mode` covers
all known CPU modes. Metrics like `system.cpu.time` depend on having all modes
defined. Authors should document all known values upfront, though new values
may be added later to support new operating systems or CPU architectures.

**Open enums** like `error.type` allow conventions and instrumentations to define
their own applicable values.

**System identifier enums** specify a system, project, provider, product, or protocol.
For example, `db.system.name` contains database names like `mongodb` or `mysql`.

System identifier enums help differentiate telemetry signals. MongoDB and MySQL
both follow general database conventions, but populate attributes like `db.collection.name` differently and have system-specific attributes. Each system has its own span
definitions and documentation.
See [MongoDB](/docs/db/mongodb.md) and [MySQL](/docs/db/mysql.md) as examples
and check out [system-specific naming](../general/naming.md#system-specific-attributes)
for naming guidance.

> [!IMPORTANT]
> System identifier enums don't need to list every possible system, component, or technology.
>
> OpenTelemetry instrumentations that use enum attributes SHOULD document their values before releasing **stable** artifacts and MAY support undocumented values in unstable artifacts or behind a feature flag.

Only define new system identifiers when you also document how conventions apply
to that system. For example, when adding a new `db.system.name` value, create
documentation and span definitions that show how generic attributes work for that
database.

#### Defining spans

TBD

#### Defining metrics

TBD

#### Defining entities

Follow the [Entity Modeling Guide](resource-and-entities.md).

#### Defining events

TBD

## Stabilizing existing conventions

- All conventions MUST be defined in YAML before they can be declared stable
- Conventions that are not used by instrumentations MUST NOT be declared stable

TODO:

- migration plan

### Migration plan

TODO

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
