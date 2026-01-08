# System Semantic Conventions: Instrumentation Design Philosophy

The System Semantic Conventions are caught in a strange dichotomy that is unique
among other semconv groups. While we want to make sure we cover obvious generic
use cases, monitoring system health is a very old practice with lots of
different existing strategies. While we can cover the basic use cases in cross
platform ways, we want to make sure that users who specialize in certain
platforms aren't left in the lurch; if users aren't given recommendations for
particular types of data that isn't cross-platform and universal, they may come
up with their own disparate ideas for how that instrumentation should look,
leading to the kind of fracturing that the semantic conventions should be in
place to avoid.

The following sections address some of the most common instrumentation design
questions, and how we as a working group have opted to address them. In some
cases they are unique to the common semantic conventions guidance due to our
unique circumstance, and those cases will be called out specifically.

## Namespaces

Relevant discussions:
[\#1161](https://github.com/open-telemetry/semantic-conventions/issues/1161)

The System Semantic Conventions generally cover the following namespaces:

- `system`
- `process`
- `host`
- `memory`
- `network`
- `disk`
- `memory`
- `os`

Deciding on the namespace of a metric/attribute is generally informed by the
following belief:

**The namespace of a metric/attribute should logically map to the Operating
System concept being considered as the instrumentation source.**

The most obvious example of this is with language runtime metrics and `process`
namespace metrics. Many of these metrics are very similar; most language
runtimes provide some manner of `cpu.time`, `memory.usage` and similar metrics.
If we were considering de-duplication as the top value in our design, it would
follow that `process.cpu.time` and `process.memory.usage` should simply be
referenced by any language runtime that might produce those metrics. However, as
a working group we believe it is important that `process` namespace and runtime
namespace metrics remain separate, because `process` metrics are meant to
represent an **OS-level process as the instrumentation source**, whereas runtime
metrics represent **the language runtime as the instrumentation source**.

In some cases this is simply a matter of making the instrumentation's purpose as
clear as possible, but there are cases where attempts to share definitions
across distinct instrumentation sources poses the potential for a clash. The
concrete example of a time we accepted this consequence is with `cpu.mode`; the
decision was to
[unify all separate instances of `*.cpu.state` attributes into one shared `cpu.mode` attribute](https://github.com/open-telemetry/semantic-conventions/issues/1139).
The consequence of this is that `cpu.mode` needs to have a broad enum in its
root definition, with special exemptions in each different `ref` of `cpu.mode`,
since `cpu.mode` used in `process.cpu.time` vs `container.cpu.time` vs
`system.cpu.time` etc. has different subsets of the overall enum values. We
decided as a group to accept the consequence in this case, however it isn't
something we're keen on dealing with all over system semconv, as the
instrumentation ends up polluted with so many edge cases in each namespace that
it defeats the purpose of sharing the attribute in the first place.

## Two Class Design Strategy

Relevant discussions:
[\#1403 (particular comment)](https://github.com/open-telemetry/semantic-conventions/issues/1403#issuecomment-2368815634)

We are considering two personas for system semconv instrumentation. If we have a
piece of instrumentation, we decide which persona it is meant for and use that
to make the decision for how we should name/treat that piece of instrumentation.

### General class: A generalized cross-platform use case we want any user of instrumentation to be able to easily access

When instrumentation is meant for the General Class, we will strive to make the
names and examples as prescriptive as possible. This instrumentation is what
will drive the most important use cases we really want to cover with the system
semantic conventions. Things like dashboards, alerts, and broader o11y setup
tutorials will largely feature General Class instrumentation covering the [basic
use cases][use cases doc] we have laid out as a group. We want this
instrumentation to be very clear exactly how and when they should be used.
General Class instrumentation will be recommended as **on by default**.

### Specialist class: A more specific use case that specialists could enable to get more in-depth information that they already understand how to use

When instrumentation falls into the Specialist Class, we are assuming the target
audience is already familiar with the concept and knows exactly what they are
looking for and why. The goal for Specialist Class instrumentation is to ensure
that users who have very specific and detailed needs are still covered by our
semantic conventions so they don't need to go out of their way coming up with
their own, risking the same kind of disparate instrumentation problem that
semantic conventions are intended to solve. The main differences in how we
handle Speciialist Class instrumentation are:

1. The names and resulting values will map directly to what a user would expect
   hunting down the information themselves. We will rarely be prescriptive in
   how the information should be used or how it should be broken down. For
   example, a metric to represent a process's cgroup would have the resulting
   value match exactly to what the result would be if the user called
   `cat /proc/PID/cgroup`.
2. If a piece of instrumentation is specific to a particular operating system,
   the name of the operating system will be in the instrumentation name. See
   [Operating System in names](#operating-system-in-names) for more information.
   For example, a metric for a process's cgroup would be `process.linux.cgroup`,
   given that cgroups are a specific Linux kernel feature.

### Examples

Some General Class examples:

- Memory/CPU usage and utilization metrics
- General disk and network metrics
- Universal system/process information (names, identifiers, basic specs)

Some Specialist Class examples:

- Particular Linux features like special process/system information in procfs
  (see things like
  [/proc/meminfo](https://man7.org/linux/man-pages/man5/proc_meminfo.5.html) or
  [cgroups](https://man7.org/linux/man-pages/man7/cgroups.7.html))
- Particular Windows features like special process information (see things like
  [Windows Handles](https://learn.microsoft.com/windows/win32/sysinfo/about-handles-and-objects),
  [Process Working Set](https://learn.microsoft.com/windows/win32/procthread/process-working-set))
- Niche process information like open file descriptors, page faults, etc.

## Instrumentation Design Guide

When designing new instrumentation we will follow these steps as closely as
possible:

### Choosing instrumentation class

In System Semantic Conventions, the most important questions when deciding
whether a piece of instrumentation is General or Specialist would be:

- Is it cross-platform?
- Does it support our [most important use cases][use cases doc] then we will
  make it general class

The answer to both these questions will likely need to be "Yes" for the
instrumentation to be considered General Class. Since the General Class
instrumentation is what we expect the widest audience to use, we will need to
scrutinize it more closely to ensure all of it is as necessary and useful as
possible.

If the answer to either one of these is "No", then we will likely consider it
Specialist Class.

### Naming

For General Class, choose a name that most accurately descibes the general
concept without biasing to a platform. Lean towards simplicity where possible,
as this is the instrumentation that will be used by the widest audience; we want
it to be as clear to understand and ergonomic to use as possible.

For Specialist Class, choose a name that most directly matches the words
generally used to describe the concept in context. Since this instrumentation
will be optional, and likely sought out by the people who already know exactly
what they want out of it, we can prioritize matching the names as closely to
their definition as possible. For specialist class metrics that are platform
exclusive, we will include the OS in the namespace as a sub-namespace (not the
root namespace) if it is unlikely that the same metric name could ever be
applied in a cross-platform manner. See
[this section](#operating-system-in-names) for more details.

### Value

For General Class, we can be prescriptive with what the value of the
instrumentation should be. We want to ensure General Class instrumentation most
closely matches our vision for our general use cases, and we want to ensure that
users who are not specialists and just want the most important basic information
can acquire it as easily as possible using out-of-the-box semconv
instrumentation. This means we are more likely within General Class
instrumentation to make judgements about exactly what the value should be, and
whether the value should be reshaped by instrumentation in any case when pulling
the values from sources if it serves general purpose use cases.

For Specialist Class, we should strive not to be prescriptive and instead match
the concept being modeled as closely as possible. We expect specialist class
instrumentation to be enabled by the people who already understand it. In a
System Semconv context, these may be things a user previously gathered manually
or through existing OS tools that they want to model as OTLP.

### Descriptions

The concepts being modeled by System Semantic Conventions can be very complex,
sometimes requiring deeper knowledge of operating system and computing concepts
than most general practitioners would need. As a result, it is tempting to
provide detailed explanations of the concepts we are modelling. However, we feel
that the amount of explanation that would be required to teach these concepts to
a reader with no knowledge would require so much context and nuance that it
would clutter the resulting documentation and obscure the information we really
need to convey, which is not just what the instrumentation is but details about
how and why to instrument it certain ways.

This means that for System Semantic Conventions documentation, **we assume a
baseline level of knowledge of the concepts being instrumented**. The `brief`
and `note` fields of metrics and attributes should be used to convey information
that is crucial to understanding the instrumentation intention, i.e.:

- Differences in the same piece of data when it is instrumented on different
  platforms
- When we recommend calculations be done on particular data rather than
  surfacing direct values from existing tools
- When particular names or enum values were chosen when there are common
  alternate terms for the same concept

For root metrics and attributes, we will strive to always have a `brief` field.
The `brief` field should explain what the metric/attribute is, and if the
explanation of a value is simple (i.e. simply surfacing a value from a common
source like `procfs`) then the explanation of what the value should be can go in
the brief. If the value needs some calculation explanation and justification,
the information should be moved to the `note` field. For enum values, it is
often the case that the intention of these values is obvious given whatever
`brief` was provided for the attribute as a whole. A brief can be included in a
scenario where we have had to make some choice on the value that isn't
immediately obvious; the most common scenario is when some terminology differs
across platforms and we had to choose one term to represent all scenarios. In
this case, the `brief` can be used to clarify our intention.

In cases where information about a concept is required to describe our intention
for instrumentation, all information must come with citations to authoritative
documentation (i.e. Linux `man` pages, Win32 API docs, etc). We do not want to
invent any new explanations about existing concepts in our own words within our
convention documentation.

## Naming Platform-Exclusive Metrics

Relevant discussions:
[\#1255](https://github.com/open-telemetry/semantic-conventions/issues/1255),
[\#1364](https://github.com/open-telemetry/semantic-conventions/pull/1364#discussion_r1852465994)
[\#2984](https://github.com/open-telemetry/semantic-conventions/pull/2984#discussion_r2466369361)

Monitoring operating systems is a long-standing practice, and there are numerous
heavily differing approaches within different platforms. There are lots of
metrics, even considering common stats like patterns of memory usage, where
there are platform-exclusive pieces of information that are only valuable to
those who specialize in that platform.

With this in mind, we have made the following decision about the OS name in
OS-exclusive instrumentation:

### The OS name should be included in the metric in most cases

The primary reason for this is for discoverability and disambiguation. Sometimes
there are metrics that are non-obviously platform exclusive. A good example is
`process.handle.count`, since `handle` is common nomenclature for file
descriptors in Unix-likes but is in this case specifically referring to
[Windows system handles held by the process](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handles-and-objects)
and thus will not be enabled on any platform other than Windows. It helps to
disambiguate at a glance if the metric name has the platform inside of it.

The exception to this rule is if the name also contains the name of a subsystem
that is commonly understood to already belong to a particular platform. `cgroup`
for example is commonly known to be a Linux-exclusive subsystem, so including
`linux` in the name is redundant.

If a user is looking at Semantic Conventions directly within the Semantic
Conventions documentation, they can easily get all the nuanced information they
need. There are all kinds of varied cases where a user is not learning about
their instrumentation from our docs though, instead seeing it in their
observability backend UIs, Collector debug output, or auto-generated SDK code
etc. So this rule is intended to make our instrumentation simpler to understand
in a scenario where they need to be understood outside of our detailed
documentation.

### The OS name should not be the root namespace

This is for the sake of hierarchical organization of names. We consider the root
namespace of metrics to be crucial to the typical usage patterns we expect. A
user who wants to discover all of their `memory` metrics should only need to
search for `memory.*` to get all metrics related to `memory` in general. If the
OS was the root namespace, they would need to search for `linux.memory.*`,
`windows.memory.*`, etc. This is bad partially because of complicating queries,
but it would also require a user to go out of their way to gather all of the
platforms they need to search for just to get the whole picture on their
`memory` metrics.

### The OS name should be after the area of concern

Our expected usage pattern for these metrics is for a user to have some area of
concern within their system that they are monitoring (processes, memory,
filesystem, cpu, network, etc) and for a user with a specific concern to have a
clear way to discover the instrumentation supporting their area of concern.
Sometimes that area of concern is not just the absolute root of the namespace,
but also a number of sub-components in the root. The `system` namespace in
particular has many examples of this, `system.memory`, `system.network`, etc. If
we named the instrumentation as `system.linux.memory`, then just as in the
scenario above it becomes hard to discover all the available "system memory"
metrics. As a result, the OS name goes after the area of concern, i.e.
`system.memory.linux`.

[use cases doc]: ./use-cases.md
