<!--- Hugo front matter used to generate the website version of this page:
linkTitle: System use cases
--->

# System semantic conventions: general use cases

This document is a collection of the use cases that we want to cover with the
System Semantic Conventions. The use cases outlined here inform the working
group’s decisions around what instrumentation is considered **required**. Use
cases in this document will be stated in a generic way that does not refer to
any potentially existing instrumentation in semconv as of writing, such that
when we do dig into specific instrumentation, we understand their importance
based on our holistic view of expected use cases.

## _Legend_

`General Information` \= The information that should be discoverable either
through the entity, metrics, or metric attributes.

`Dashboard` \= The information that should be attainable through metrics to
create a comprehensive dashboard.

`Alerts` \= Some examples of common alerts that should be creatable with the
available information.

## **Host**

A user should be able to monitor the health of a host, including monitoring
resource consumption, unexpected errors due to resource exhaustion or
malfunction of core components of a host or fleet of hosts (network stack,
memory, CPU, etc.).

### General information

- Machine name
- ID (relevant to its context, could be a cloud provider ID or just base machine
  ID)
- OS information (platform, version, architecture, etc)
- CPU Information
- Memory Capacity

### Dashboard

- Memory utilization
- CPU utilization
- Disk utilization
- Disk throughput
- Network traffic

### Alerts

- VM is down unexpectedly
- Network activity spikes unexpectedly
- Memory/CPU/Disk utilization goes above a % threshold

## Notes

The alerts in particular should be capable of being uniformly applied to a
heterogenous fleet of hosts. We will value the nature of cross-platform
instrumentation to allow for effective alerting across a fleet regardless of the
potential mixture of operating system platforms within it.

The term `host` can mean different things in other contexts:

- The term `host` in a network context, a central machine that many others are
  networked to, or the term `host` in a virtualization context
- The term `host` in a virtualization context, something that is hosting virtual
  guests such as VMs or containers

In this context, a host is generally considered to be some individual machine,
physical or virtual. This can be extra confusing, because a unique machine
`host` can also be a network `host` or virtualization `host` at the same time.
This is a complexity we will have to accept due to the fact that the `host`
namespace is deeply embedded in existing OpenTelemetry instrumentation and
general verbiage. To the best of our ability, network and virtualization `host`
instrumentation will be kept distinct by being within other namespaces that
clearly denote which version of the term `host` is being referred to, while the
root `host` namespace will refer to an individual machine.

## **Process**

A user should be able to monitor the health of an arbitrary process using data
provided by the OS. Reasons a user may want this:

1. The process they want to monitor doesn't have in-process runtime-specific
   instrumentation enabled or is not instrumentable at all, such as an antivirus
   or another background process.
2. They are monitoring lots of processes and want to have a set of uniform
   instrumentation for all of them.
3. Personal preference/legacy reasons; they might already be using OS signals to
   monitor stuff and it's an easier lift for them to move to basic process
   instrumentation, then move to other specific semconv over time.

### General information

- Process name
- Pid
- User/owner

### Dashboard

- Physical Memory usage and/or utilization
- Virtual Memory usage
- CPU usage and/or utilization
- Disk throughput
- Network throughput

### Alert

- Process stops unexpectedly
- Memory/CPU usage/utilization goes above a threshold
- Memory exclusively rises over a period of time (memory leak detection)

### Notes

On top of alerts and dashboards, we will also consider the basic benchmarking of
a process to be a general usecase. The basic cross platform stats that can be
provided in a cross-platform manner can also be effectively used for this, and
we will consider that when making decisions about process instrumentation.
