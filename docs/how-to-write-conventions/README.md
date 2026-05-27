<!--- Hugo front matter used to generate the website version of this page:
linkTitle: How to write conventions
aliases: [/docs/specs/semconv/general/how-to-define-semantic-conventions]
--->

# How to write semantic conventions

**Status**: [Development][DocumentStatus]

<!-- START doctoc -->

- [Defining new conventions](#defining-new-conventions)
  - [Best practices](#best-practices)
    - [Prototyping](#prototyping)
    - [Defining attributes](#defining-attributes)
    - [Defining enum attribute members](#defining-enum-attribute-members)
    - [Defining spans](#defining-spans)
      - [What operation does this span represent](#what-operation-does-this-span-represent)
      - [Naming pattern](#naming-pattern)
      - [Status](#status)
      - [Kind](#kind)
      - [Attributes](#attributes)
    - [Defining metrics](#defining-metrics)
    - [Defining entities](#defining-entities)
    - [Defining events](#defining-events)
      - [What occurrence does this event represent](#what-occurrence-does-this-event-represent)
      - [Event naming pattern](#event-naming-pattern)
      - [Timestamps](#timestamps)
      - [Severity](#severity)
      - [Event attributes and body](#event-attributes-and-body)
- [Stabilizing existing conventions](#stabilizing-existing-conventions)
  - [Migration plan](#migration-plan)

<!-- END doctoc -->

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
      [set of standard attributes](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.57.0/specification/common/README.md#attribute))
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

Spans describe individual executions of specific operations within a trace.

When to define spans:

- The corresponding operation is significant for your observability needs.
- The operation has duration.

For example, define spans for operations that involve one or more network calls.

> [!NOTE]
>
> Known exception: [messaging `create`](/docs/messaging/messaging-spans.md#operation-types) span
> is defined for a local call. This is necessary when publishing batches of
> messages to ensure each message has a unique context and can be traced
> individually end-to-end.

When not to define spans:

- For point-in-time occurrences - use events instead.
- For short operations that don't involve out-of-process calls, such as serialization
  or deserialization.
- If there is an existing span definition that captures a very similar operation.
  For example, a DB client span represents DB query execution from ORM or DB
  driver perspectives. Both layers could be instrumented, but inner layers may be
  suppressed to reduce duplication.

> [!IMPORTANT]
>
> It's a common practice to accompany a span definition with:
>
> - A metric that measures the duration of the same operation.
> - An event that records exceptions that prevent this operation from completing
>   successfully.
>
> For example, the `http.client.request.duration` metric and
> `http.client.request.exception` event are recorded alongside the corresponding
> HTTP client span.

A span definition should describe the [operation it represents](#what-operation-does-this-span-represent),
the [naming pattern](#naming-pattern), considerations for setting span [status](#status),
the [span kind](#kind), and the list of applicable [attributes](#attributes).

##### What operation does this span represent

Define the scope and boundaries of the operation:

- When the span starts and ends.
- If this span represents a client call, specify whether it captures the logical call
  (as observed by the API caller) or the physical call (per-attempt).
- Define a different span for different operations - e.g., when spans have different
  kinds or a significantly different set of attributes.
  For example, HTTP client and server spans are two independent definitions.
  Messaging publishing and receiving are also different span types.

##### Naming pattern

- Span names must have low cardinality and should provide a reasonable grouping
  for that operation. See [Span name guidelines](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.57.0/specification/trace/api.md#span)
  for details.

- Span names usually follow the `{action} {target}` pattern. For example, `send orders_queue`.

- Span names should only include information that's available as span attributes.
  That is, `{action}` and `{target}` are usually also available as attributes and
  are used on metrics describing that operation.

- Static text should not be included in span names but can be used as a fallback.
  For example, we use `GET /orders/{id}` instead of `HTTP GET /orders/{id}` for HTTP
  server span names.

- Provide fallback values in case some of the attributes used in the span name are not
  available or could be problematic in edge cases (e.g., have high cardinality).

- If a span name can become too long, define limits and truncation strategies
  (e.g., DB conventions define a 255-character limit).

##### Status

Define what constitutes an error for that operation.

If there are no special considerations, reference the [Recording errors](/docs/general/recording-errors.md)
document.

Certain conditions can't be clearly classified as errors or non-errors (such as cancellations,
HTTP 404, and others). Avoid using strict requirements — allow instrumentations
to leverage additional context to provide a more accurate status.

##### Kind

All span definitions MUST include a specific [span kind](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.57.0/specification/trace/api.md#spankind). One span definition can
only mention one span kind.

##### Attributes

Capture only the important details of the specific operation. Parent operations or sub-operations
will have their own spans.

For example, when recording a call to upload a file to an object store,
include the endpoint, operation name (such as upload file), collection, and object
identifier. Don't include details of the underlying HTTP/gRPC requests unless
there is a strong reason to do so.

Only include attributes that bring clear value — this keeps telemetry
volume and performance overhead low. Don't try to capture all available details.
When in doubt, don't reference additional attributes - they can be added incrementally
based on feedback.

Define which additional properties this span needs to be useful:

- Include the `error.type` attribute. If the operation you're describing typically has a
  domain-specific error code, include that as a separate attribute as well.
  Document which error codes constitute an error.

- Include `server.address` and `server.port` on client spans.

- Include applicable `network.*` attributes on spans that describe network calls.

- Include some form of operation name to describe the action being performed.

  For example, in the case of HTTP, it's `http.request.method`; in the case of RPC,
  it's `rpc.method`; for messaging, `messaging.operation.name`; and for GenAI, `gen_ai.operation.name`.
  This attribute typically serves as the `{action}` in the span name and may be used
  across multiple span definitions within the same domain.

- Identify other important characteristics such as the operation target (DB collection,
  messaging queue, GenAI model, object store collection), input parameters, and
  result properties that should be recorded on the span.

- When referencing an attribute:
  - Specify if an attribute is relevant for head-sampling. Such attributes should be
    provided at start time so that they will be passed to the sampler. Usually, these are
    attributes that have low cardinality and are easy to obtain.
  - Specify [requirement level](/docs/general/attribute-requirement-level.md).
    Only absolutely essential (and always available) attributes can be `required`.
    Attributes that may include sensitive information, are expensive to obtain,
    or are verbose, should be `opt-in`.
  - Update the brief and note to tailor the attribute definition to that operation.

#### Defining metrics

TBD

#### Defining entities

Follow the [Entity Modeling Guide](resource-and-entities.md).

#### Defining events

Events describe named occurrences at a meaningful point in time.

This section covers standalone events represented by `LogRecord`s. See
[Semantic conventions for events](/docs/general/events.md) for general event
semantics.

When to define events:

- The occurrence is significant for your observability needs.
- The occurrence does not require a new trace context or child operations.
- The occurrence represents a checkpoint, state change, or outcome in a longer
  operation or asynchronous flow.

For example, define events for application interactions, state transitions,
feature flag evaluations, and exceptions that occur while an operation is being
executed.

When not to define events:

- For operations with a duration and meaningful operation boundary - use spans
  instead.
- For properties that describe a whole span and do not need their own timestamp -
  use span attributes instead.
- For details that are already captured by an existing event definition with the
  same meaning and structure - reuse or extend the existing event definition
  instead.
- For unstructured diagnostic messages that are not intended to be queried as
  named events - use logs instead.

Events often complement span definitions. If an event is emitted while a related
span is active, instrumentations should associate the event with the corresponding
span context. Events do not create trace context and do not have child spans.

Use an event instead of a span attribute when the data describes a distinct
occurrence within the operation, can happen zero or more times for the same span,
or needs its own timestamp, severity, or occurrence-specific attributes.
Use a span attribute when the data describes the operation as a whole, especially
when it is useful for sampling or is known when the span starts.

An event definition should describe the
[occurrence it represents](#what-occurrence-does-this-event-represent), the
[event name](#event-naming-pattern), when instrumentations should record it,
which [timestamp](#timestamps) to use, the default [severity](#severity), whether
the event is expected to be recorded with a parent span context, and the
applicable [attributes and body](#event-attributes-and-body).

##### What occurrence does this event represent

Define the scope and meaning of the occurrence:

- When the event is recorded, including the timestamp it represents.
- Whether the event is recorded once, can be recorded multiple times, or is
  recorded for both start and end checkpoints.
- Whether the event is meaningful only when associated with a parent span, or
  whether it can also be emitted independently.
- Conditions under which instrumentation SHOULD or SHOULD NOT record the event.

If the event can be emitted independently of a span, define enough attributes to
make the event useful without relying on span attributes.

Define separate events for occurrences that have different meanings, different
severity, or a significantly different set of attributes. Reuse the same event
definition across multiple operations when it represents the same occurrence and
has the same event name, severity guidance, and attribute structure.

##### Event naming pattern

Event names uniquely identify an event structure. When users query for a specific
event name, they should get events that comply with the corresponding semantic
convention.

- Event names MUST be low-cardinality.
- Event names SHOULD follow the [Naming guidelines](/docs/general/naming.md).
- Event names SHOULD NOT include runtime values. Use attributes for identifiers,
  names, or other values that vary per occurrence.
- Use a domain-specific name when the event is tied to a specific operation or
  system. For example, `http.client.request.exception` represents exceptions
  during HTTP client requests.
- Use a shared name only when the same definition applies to all occurrences
  recorded with that name.

When many related event definitions need a common grouping, such as audit or
security relevance, prefer defining or reusing a low-cardinality classification
attribute instead of using a broad event name with different meanings and
attribute sets.

When recording events from an existing system that does not have a single event
name, follow [External event compatibility](/docs/general/events.md#external-event-compatibility).

##### Timestamps

Events MUST set
[Timestamp](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.57.0/specification/logs/data-model.md#field-timestamp)
to the time when the event occurred.

Events MUST NOT set
[ObservedTimestamp](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.57.0/specification/logs/data-model.md#field-observedtimestamp).

When defining an event, document which occurrence time should be used as the
event timestamp when it is not obvious, especially for events received from
external systems.

##### Severity

Events SHOULD specify a default
[severity number](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.57.0/specification/logs/data-model.md#field-severitynumber).

Define the severity number based on the expected impact of the occurrence.
If the same event can have different severity depending on context, document the
conditions for setting each severity.

For exception events, follow the severity guidance in
[Semantic conventions for exceptions in logs](/docs/exceptions/exceptions-logs.md#severity).

Semantic conventions SHOULD NOT define a
[severity text](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.57.0/specification/logs/data-model.md#field-severitytext)
value only to mirror the severity number short name. If instrumentation receives
a meaningful severity string from an external system, document how that string
is mapped to severity number and whether it is preserved as severity text.

##### Event attributes and body

Semantic conventions that define events MUST document the event name and
attributes. See [General event semantics](/docs/general/events.md#general-event-semantics).

Use attributes to represent structured event details and context:

- Reuse existing attributes when possible, especially attributes that are used on
  related spans, metrics, resources, or other events.
- Include attributes that users are likely to filter, group, aggregate, or
  correlate on.
- When the event is normally associated with a span, avoid copying every span
  attribute by default. Reference span-level attributes on the event only when
  they are needed to understand, route, or retain the event without the span.
- Prefer flat attributes when the value can be represented clearly without
  structure. Use complex attributes only when the structure is part of the
  event semantics and a flat representation would be awkward or lossy.
- Include `error.type` when the event represents a failure that users need to
  classify.
- Specify [requirement level](/docs/general/attribute-requirement-level.md) and
  tailor the brief and note to the event.
- Document attributes that may contain sensitive information, be expensive to
  collect, have high cardinality, or be especially large.

Events SHOULD NOT use
[body](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.57.0/specification/logs/data-model.md#field-body)
except to represent a string display message of the event. Do not put structured
event fields in the body when they can be defined as event attributes.

## Stabilizing existing conventions

- All conventions MUST be defined in YAML before they can be declared stable
- Conventions that are not used by instrumentations MUST NOT be declared stable

TODO:

- migration plan

### Migration plan

TODO

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
