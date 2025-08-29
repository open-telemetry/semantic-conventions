# Attribute Capture Scope

## Any

This attribute can be captured in any of the possible scopes listed below however it is suggested to capture the attribute at the earliest stage possible.
By capturing the attribute at the earliest stage it is possible to reduce data storage and in some cases facilitate additional use cases.

This is the default scope of all attributes.

## Span Creation

This attribute can be important for making sampling decisions and SHOULD be provided at span creation time (if provided at all).

By capturing it it at span creation this attribute can be utilised in head sampling as well as tail sampling.

## Instrumentation

This scope is for scenarios where an attribute should be remaining constant through the life-cycle of the instrumentation generating the telemetry.

Example of this would be the `messaging.system.name` being interacted with when instrumentation only interacts with 1 messaging system.

## Resource

This scope is for scenarios where an attribute should be remaining constant through the life-cycle of the service generating the telemetry.

Example of this would be the `host.name` as a service can only be running on one host at a time.
