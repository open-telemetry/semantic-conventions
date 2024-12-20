<!--- Hugo front matter used to generate the website version of this page:
linkTitle: How To Define New Semantic Conventions
aliases: [how-to-define-new-semantic-conventions]
--->

# How to define new semantic conventions

**Status**: [Development][DocumentStatus]

<!-- toc -->

<!-- tocstop -->

This document describes requirements, recommendations, and best practices on how to define conventions
for the new areas or make substantial changes to the existing ones.

## Defining new conventions

- New conventions MUST have a group of codeowners. See [project management](https://github.com/open-telemetry/community/blob/main/project-management.md) for more details.
  <!-- TODO: add CI check for CODEOWNERS file (when a new area is added) -->
- New conventions SHOULD be defined in YAML files. See [YAML Model for Semantic Conventions](/model/README.md) for the details.
- New conventions SHOULD be defined with `development` stability level.
- New conventions SHOULD include attributes and telemetry signal definitions (spans, metrics, events, resources, profiles).

### Best practices

#### Defining attributes

Reuse existing attributes when possible. Look through [existing conventions](/docs/attributes-registry/) for similar areas,
check out [common attributes](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/attributes.md).
Semantic conventions are encouraged to use attributes from different namespaces.

Introduce new attributes when there is a clear use-case for them. Check if the most of the following applies:

- you see a clear benefit for the end users to have it on their telemetry
- you're going to use this attribute on any spans, metrics, events, resources, or other telemetry signals
- you're going to use this attribute in instrumentations

Postpone adding new attributes if it's not yet clear how beneficial having it on the telemetry is.

When defining a new attribute

- follow the [naming guidance](/docs/general/naming.md)
- make sure to provide descriptive `brief` and `note` - it should be clear what this attribute represents.
  - If it represents some common concept documented externally, make sure to provide links. For example,
    always provide links to attributes describing notions defined in RFCs or other standards.
  - If attribute value is likely to contain PII or other sensitive information, make sure to capture it in the `note`.

    Include the following warning <!-- TODO: update existing semconv -->
    ```yaml
      - id: user.full_name
        ...
        note: |
          ...

          > [!WARNING]
          >
          > This field contains sensitive (PII) information.
    ```
- use appropriate [attribute type](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md#type)
  - If value has a reasonably short (open or closed) set of possible values, it should be an enum.
  - If value is a timestamp, it should be recorded as a string in ISO 8601 format.
  - If value is an array of primitives, use array type. Avoid recording arrays as a string
  - Use template type to define attributes with variable name (only the last segment of the name is dynamic). It's
    useful to record user-defined set of key=value pairs such as HTTP headers.
  - Capture complex values as a set of flat attributes. <!-- This may change, check out https://github.com/open-telemetry/semantic-conventions/issues/1669 to monitor the progress -->
- new attributes should always be defined with `development` stability
- provide realistic examples
- Avoid defining attributes with potentially unbound values. For example, strings that are longer than 1KB
  or arrays with more than a thousand elements. Such value should be recoded in log/event body instead.

Consider the scope attribute should be applicable in and how it may evolve in the future

- when defining an attribute for a narrow use-case, consider other possible use-cases.
  For example, when defining system-specific attribute, check if other systems in this domain would need
  a similar attribute in the future.
  Or, when defining a boolean flag such as `foo.is_error`, consider if you can represent it, along with
  additional details, in a more extensible way, for example, with `foo.status_code` attribute.

- when defining a very broad attribute applicable to multiple domains or systems, check if there are
  standards or common best practices in the industry to rely on.
  Avoid defining generic attributes that are not grounded by some existing standard.

> [!NOTE]
>
> When defining conventions for an area with multiple implementations or systems such as databases, identity providers,
> or cloud providers it takes some time to find the right balance between being overly generic vs not generic enough.
>
> It's essential to start with experimental conventions, document how these conventions apply to a diverse set
> of provides/systems/libraries, and prototype instrumentations.
>
> The end-user experience should be used as the main guiding principle:
>
> - if the attribute is expected to be used on general-purpose metrics for this area,
>   consider introducing common attribute.
>
>   For example, almost every messaging system has a notion of queue or topic. The
>   queue or topic name is essential on latency or throughput metrics and equally
>   important on spans to debug and visualize message flow. This is a good sign
>   that we need a generic attribute that represents any type of messaging destination.
>
> - if the attribute represents something that would be useful in a narrow set of scenarios
>   or only on a system-specific metrics/spans/events, it's usually a sign that this
>   attribute does not need to be generic.

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






