# Resource and Entities

Table of Contents

- [Modelling Guide](#modelling-guide)
- FAQ
  - [When to define a new entity](#when-to-define-a-new-entity)
  - [When to define a new "is-a" relationship](#when-to-define-an-is-a-relationship-vs-extending-descriptive-attributes)
  - [How to define identifying attributes](#how-to-define-identifying-attributes)
  - [How to namespace entities](#how-to-namespace-entities)
- [Background](#background-resource-and-entities)

## Modelling Guide

To define an entity, create a new semantic convention model file, with a group type as `entity`, for example:

`model/{my_domain}/entities.yaml`:

```yaml
groups:
  - id: entity.my_entity
    type: entity
    stability: development
    name: my_entity
    brief: >
      A description of my_entity here.
    attributes:
      - ref: some.attribute
        role: identifying
      - ref: some.other_attribute
        role: descriptive
        ...
```

Here, the attributes field contains all attributes of the Entity.
The `role` of each attribute determines if it is identifying or
descriptive. See
[How to define identifying attributes?](#how-to-define-identifying-attributes)
for details on what these mean.

> Note: Declaring Entity relationships is not yet supported.

### Declaring associations between signals

You can declare which entities should be used with specific observability
signals.  For example, process metrics should be used with the process
entity, so that the metric is associated with a known process. To declare
this, use the `entity_associations` field on the signal and reference
another resource group *by name*.

`model/{my_domain}/metrics.yaml`:

```yaml
groups:
  - id: metric.some_metric
    type: metric
    ...
    entity_associations: 
      - my_entity
```

Notes:

- You cannot declare an association on an *unstable* resource from a
  *stable* signal.
- You can declare multiple associations. These form a "one or many" set,
  where one or many of the named entities may be associated with the
  metric. There is *no* requirement on disjointness due to how is-a
  relationships are modelled.

### Extending an entity

While not recommended for Semantic Conventions, you can define a new
"view" of an entity that includes additional descriptive attributes. To
do so, use the extends field on groups:

`model/{my_other_domain}/entities.yaml`:

```yaml
groups:
  - id: entity.my_entity_2
    type: entity
    extends: entity.my_entity
    attributes:
      - ref: new.attribute.name
        requirement_level: opt_in
        role: descriptive
```

Notes:

- You cannot change the `name` field of the new entity.
- You cannot change the set of identifying attributes.

## FAQ

### When to define a new entity?

There are two scenarios where entities should be defined:

- When you are generating a new signal (log, metric, span, etc.)
  and no existing entity makes sense as the "source".
- (future) When you need to describe an entity hierarchy from
  some system of record (e.g. resources in kubernetes, assets
  in a cloud).

For example, the Mainframe SIG in OpenTelemetry will need to outline a
set of entities and relationships to define observed telemetry. If a new
clustering solution (e.g. Hashicorp's Nomad) is defined, and existing
container-based entities are not enough, then new entities should be
defined.

### When to define an "is-a" relationship vs. extending descriptive attributes?

There are two key rules:

- Default to introducing separate entities with a clear "is a" (or similar) relationship
- Extend an entity with new descriptive attributes if and only if the following is true:
  - The extending entity cannot be associated with any telemetry by itself.
  - The extending entity doesn’t have any other entities that logically can only be associated with it.

This avoids the complexities of subtyping and ambiguous attribute usage.

### How to define identifying attributes?

The identifying attributes should be minimally sufficient to
identify an entity within the context of how that entity is
discovered. For example, when discovering kubernetes entities
like `k8s.pod`, `k8s.deployment`, the identifying attributes
should be sufficient to identify these entities within the
scope of a kubernetes cluster (or more specifically, the
kubernetes api server where the entities are discovered).

Commonly, a number of attributes of an entity are readily
available for the telemetry producer to compose an identity. Of
the available attributes the entity ID should include the
minimal set of attributes that is sufficient for uniquely identifying that entity. For example a process on a host can be
uniquely identified by (`process.pid`,`process.start_time`)
attributes. Adding for example `process.executable.name`
attribute to the identity is unnecessary and violates the
rule of having a [minimally sufficient ID](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.45.0/specification/entities/data-model.md#minimally-sufficient-identity).

#### Multi-Observer Guidance

When choosing Identifying attributes, care should be taken to ensure that
 multiple observers will find the same identifying attribute for the same
 entity. Generally, entities may be discovered both within OpenTelemetry
 SDKs and the Collector and should leverage identifying attributes that
 will be the same between these signal providers.

For example, service.instance.id can be problematic to detect from outside
an SDK and inside an SDK consistently. Generally, this can only be
achieved if some outside source injects a service.instance.id value into
the SDK that is externally visible.  An alternative is to have the SDK
provide a relationship between the service.instance.id and another entity
that is visible externally. Care should be taken when modelling Entities
to avoid this problem where possible.

### How to namespace entities?

Entities should be namespaced around the primary mechanism used to
identify the Entity. For Example, kubernetes entities use the `k8s`
namespace, and are primarily discovered using the kubernetes API or
working within kubernetes.

## Background: Resource and Entities

In OpenTelemetry, every signal is associated with a Resource.
According to the [Specification](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.45.0/specification/resource#overview)
this is:

> A Resource is a representation of the entity producing telemetry. Within
> OpenTelemetry, all signals are associated with a Resource, enabling contextual
> correlation of data from the same source. For example, if I see a high latency
> in a span I need to check the metrics for the same entity that produced that
> Span during the time when the latency was observed.
>
> Resource provides two important aspects for observability:
>
> * It MUST identify an entity that is producing telemetry.
> * It SHOULD allow users to determine where that entity resides within their
>   infrastructure.

All resources are composed of [Entities](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.45.0/specification/entities/README.md#overview).
An entity is specified as:

> Entity represents an object of interest associated with
> produced telemetry: traces, metrics, logs, profiles etc.

While there is overlap in the definition of Entity and Resource, there are
several key differences between the two:

- An Entity has a known "type", e.g. `service`, `k8s.pod`,
  `host`, etc.
- An Entity can distinguish *identifying* attributes from
  *descriptive* attributes.
  - Identifying attributes can be used to identify the entity
    within some system (See
    [minimally sufficient id](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.45.0/specification/entities/data-model.md#minimally-sufficient-identity)).
    For Example, the `k8s.pod.uid` would be considered an
    identifying attribute for a pod within kubernetes.
  - *Descriptive* attributes can be used to provide additional labels for
    entities, but do not uniquely identify that Entity.  
- A Resource is composed of *multiple* Entities.
  - Each of the entities within Resource is considered
    'contributing' to that telemetry.
  - For Example, today, most SDKs include the service entity,
    but also another entity, like `k8s.container`, `host`, etc.
- An Entity may be conceptually similar to another (which we
  call an "is-a" relationship).
  - For example, the `k8s.cluster` entity generically
    represents kubernetes clusters, while the `aws.eks.cluster`
    entity would represent the AWS specific concept of an
    Elastic Kubernetes cluster.
  - In this case, a Resource from EKS could contain both the
    `aws.eks.cluster` entity and the `k8s.cluster` entity.

There are two key principles that are important for Entities
and Resource in OpenTelemetry:

1. *Open expansion*: Allowing users outside of OpenTelemetry to provide
   Entity definitions and relationships within the system.
2. *Telescoping Identity*: Allowing flexible denormalization of
   observability data to optimise critical queries (e.g. alerts, dashboard,
   etc.)

### Open Expansion

OpenTelemetry is designed to be an open system. When it comes to defining
the core set of entities and relationships within systems, it needs to
remain open about what these entities and possible relationships are.  Any
system a user has should be able to model and participate with existing
OpenTelemetry semantic conventions.  This is done through two key aspects:

- Namespacing
- "Is-a" Relationships

When defining a new set of entities within OpenTelemetry Semantic
Conventions, they should be namespaced, as per the
[Semantic Convention naming policy](/docs/general/naming.md#general-naming-considerations).
This gives clear indication which concepts are clearly related with each
other.  For example, the k8s namespace would define kubernetes related
entities and their relationships. Users would know to create a new
namespace when modelling concepts on top of k8s.

Expansion to existing concepts is done through "is-a" relationships.
These are relationships where one entity is known to represent the same
concept as another entity, but in some new scoped context.  For example,
an `aws.eks.cluster` is a `k8s.cluster`, but not all `k8s.cluster`
entities are `aws.eks.cluster` entities.

### Telescoping Identity

Within OpenTelemetry, we want to give users the flexibility to decide
what information needs to be sent *with* observability signals and what
information can be later joined.  We call this "telescoping identity"
where users can decide how *small* or *large* the size of an OpenTelemetry
resource will be on the wire (and correspondingly, how large data points
may be when stored, depending on storage solution).

For example, in the extreme, OpenTelemery could synthesize a UUID for
every system which produces telemetry.  All identifying attributes for
Resource and Entity could be sent via a side channel with known
relationships to this UUID. While this would optimise the runtime
generation and sending of telemetry, it comes at the cost of downstream
storage systems needing to join data back together either at ingestion
time or query time. For high performance use cases, e.g. alerting, these
joins can be expensive.

In practice, users control Resource identity via the configuration of
Resource Detection within SDKs and the collector. Users wishing for
minimal identity may limit their resource detection just to a
`service.instance.id`. Some users highly customize resource detection with
many concepts being appended.

*OpenTelemetry should provide a good "out of the box" set of resource*
*detection that makes appropriate denormalization trade-offs for most*
*users, but allows users to fine-tune the system to their needs.*
