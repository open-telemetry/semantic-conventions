# System semantic conventions: instrumentation design philosophy

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

## Two class design strategy

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

## Instrumentation design guide

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

For General Class, the value we can be prescriptive with the value of the
instrumentation. We want to ensure General Class instrumentation most closely
matches our vision for our general use cases, and we want to ensure that users
who are not specialists and just want the most important basic information can
acquire it as easily as possible using out-of-the-box semconv instrumentation.
This means we are more likely within General Class instrumentation to make
judgements about exactly what the value should be, and whether the value should
be reshaped by instrumentation in any case when pulling the values from sources
if it serves general purpose use cases.

For Specialist Class, we should strive not to be prescriptive and instead match
the concept being modeled as closely as possible. We expect specialist class
instrumentation to be enabled by the people who already understand it. In a
System Semconv context, these may be things a user previously gathered manually
or through existing OS tools that they want to model as OTLP.

### Case study: `process.cgroup`

Relevant discussions:
[\#1357](https://github.com/open-telemetry/semantic-conventions/issues/1357),
[\#1364 (particular thread)](https://github.com/open-telemetry/semantic-conventions/pull/1364#discussion_r1730743509)

In the `hostmetricsreceiver`, there is a Resource Attribute called
`process.cgroup`. How should this attribute be adopted in System Semantic
Conventions?

Based on our definitions, this attribute would fall under Specialist Class:

- `cgroups` are a Linux-specific feature
- It is not directly part of any of the default out-of-the-box usecases we want
  to cover

In this attribute's case, there are two important considerations when deciding
on the name:

- The attribute is specialist class
- It is Linux exclusive, and is unlikely to ever be introduced in other
  operating systems since the other major platforms have their own versions of
  it (Windows Job Objects, BSD Jails, etc)

This means we should pick a name that matches the verbiage used by specialists
in context when referring to this concept. The way you would refer to this would
be "a process's cgroup, collected from `/proc/<pid>/cgroup`". So we would start
with the name `process.cgroup`. We also determined that this attribute is
Linux-exclusive and are confident it will remain as such, so we land on the name
`process.linux.cgroup`.

Since this metric falls under Specialist Class, we don't want to be too
prescriptive about the value. A user who needs to know the `cgroup` of a process
likely already has a pretty good idea of how to interpret it and use it further,
and it would not be worth it for this Working Group to try and come up with
every possible edge case for how it might be used. It is much simpler for this
attribute, insofar as it falls under our purview, to simply reflect the value
from the OS, i.e. the direct value from `cat /proc/<pid>/cgroup`. With cgroups
in particular, there is high likelihood that more specialized semconv
instrumentation could be developed, particularly in support of more specialized
container runtime or systemd instrumentation. It's more useful for a working
group developing special instrumentation that leverages cgroups to be more
prescriptive about how the cgroup information should be interpreted and broken
down with more specificity.

## Operating System in names

Relevant discussions:
[\#1255](https://github.com/open-telemetry/semantic-conventions/issues/1255),
[\#1364](https://github.com/open-telemetry/semantic-conventions/pull/1364#discussion_r1852465994)

Monitoring operating systems is an old practice, and there are numerous heavily
differing approaches within different platforms. There are lots of metrics, even
considering common stats like memory usage, where there are platform-exclusive
pieces of information that are only valuable to those who specialize in that
platform.

Thus we have decided that any instrumentation that is:

1. Specific to a particular operating system
2. Not meant to be part of what we consider our most important general use cases

will have the Operating System name as part of the namespace.

For example, there may be `process.linux`, `process.windows`, or `process.posix`
names for metrics and attributes. We will not have root `linux.*`, `windows.*`,
or `posix.*` namespaces. This is because of the principle we’re trying to uphold
from the [Namespaces section](#namespaces); we still want the instrumentation
source to be represented by the root namespace of the attribute/metric. If we
had OS root namespaces, different sources like `system`, `process`, etc. could
get very tangled within each OS namespace, defeating the intended design
philosophy.

[use cases doc]: ./use-cases.md
