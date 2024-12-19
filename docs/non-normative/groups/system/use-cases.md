# **System Semantic Conventions: General Use Cases**

This document is a collection of the use cases that we want to cover with the System Semantic Conventions. The use cases outlined here inform the working group’s decisions around what instrumentation is considered **required**.  
Use cases in this document will be stated in a generic way that does not refer to any potentially existing instrumentation in semconv as of writing, such that when we do dig into specific instrumentation, we understand their importance based on our holistic view of expected use cases.

## *Legend*

`General Information` \= The information that should be discoverable either through the entity, metrics, or metric attributes.

`Dashboard` \= The information that should be attainable through metrics to create a comprehensive dashboard.

`Alerts` \= Some examples of common alerts that should be creatable with the available information.

## **Host**

A user should be able to monitor the health of a host, including monitoring resource consumption, unexpected errors due to resource exhaustion or malfunction of core components of a host or fleet of hosts (network stack, memory, CPU…).

### General Information

* Machine name  
* ID (relevant to its context, could be a cloud provider ID or just base machine ID)  
* OS information (platform, version, architecture, etc)  
* Number of CPU cores  
* Memory Capacity

### Dashboard

* Memory utilization  
* CPU utilization  
* Disk utilization  
* Disk throughput  
* Network traffic

### Alerts

* VM is up  
* Memory/CPU/Disk utilization goes above a % threshold  
* Network activity spikes unexpectedly

## Notes

* The alerts in particular should be capable of being uniformly applied to an entire fleet of hosts  
* The user may be monitoring a virtualization host i.e. VMWare or Proxmox, and the instrumentation to monitor the health of the root host and the virtual machines it's spawned can be largely the same

## **Process**

A user should be able to monitor the health of an arbitrary process using data provided by the OS.  
Reasons a user may want this:

1. The process they want to monitor isn't covered by more specific semconv instrumentation such as language runtime metrics, db, http, etc.  
2. They are monitoring lots of processes and want to have a set of uniform instrumentation for all of them.  
3. Personal preference/legacy reasons; they might already be using OS signals to monitor stuff and it's an easier lift for them to move to basic process instrumentation, then move to other specific semconv over time.

### General Information

* Process name  
* Pid  
* User/owner

### Dashboard

* Physical Memory usage and/or utilization  
* Virtual Memory usage  
* CPU usage and/or utilization  
* Disk throughput  
* Network throughput

### Alert

* Process stops  
* Memory/CPU usage/utilization goes above a threshold  
* Memory exclusively rises over a period of time (memory leak detection)

### Notes

* Unless the OS provides the utilization data directly, the utilization requires calculation. Process instrumentation would need to be associated with a host entity that contains data about its memory capacity for utilization metrics to be calculated.  
* Process instrumentation can also be used as data for benchmark evaluations, collecting the data for a period of time and evaluating the timeseries to get benchmarking/overhead insights about the process
