<!--- Hugo front matter used to generate the website version of this page:
linkTitle: How to define new semantic conventions
--->

# How to define new semantic conventions

**Status**: [Development][DocumentStatus]

<!-- toc -->

- [Defining new conventions](#defining-new-conventions)
  - [Best practices](#best-practices)
    - [Defining attributes](#defining-attributes)
    - [Defining spans](#defining-spans)
    - [Defining metrics](#defining-metrics)
    - [Defining resources](#defining-resources)
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
      [set of standard attributes](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.44.0/specification/common/README.md#attribute))
      are supported on events and logs only. <!-- This may change, check out https://github.com/open-telemetry/opentelemetry-specification/pull/4485 to monitor the progress -->

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

#### Defining spans

TBD

#### Defining metrics

TBD

#### Defining resources

TBD

#### Defining events

TBD

## Stabilizing existing conventions

- All conventions MUST be defined in YAML before they can be declared stable
- Conventions that are not used by instrumentations MUST NOT be declared stable

TODO:

- prototyping/implementation requirements
- migration plan

### Migration plan

TODO

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
