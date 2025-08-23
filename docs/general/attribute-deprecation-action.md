# Attribute deprecation actions

**Status**: [Stable][DocumentStatus]

<details>
<summary>Table of Contents</summary>

<!-- toc -->

- [Migrate](#migrate)
  - [Stable Instrumentation](#stable-instrumentation)
  - [Long-term Unstable Instrumentation](#long-term-unstable-instrumentation)
  - [Unstable Instrumentation](#unstable-instrumentation)
- [Rename](#rename)
- [Remove](#remove)
  - [Stable Instrumentation](#stable-instrumentation-1)
  - [Long-term Unstable Instrumentation](#long-term-unstable-instrumentation-1)
  - [Unstable Instrumentation](#unstable-instrumentation-1)
- [Update](#update)
- [Drop](#drop)

<!-- tocstop -->

</details>

## Migrate

The migrate action helps to facilitate a tranisition
from a deprecated attribute to the replacement attribute.
Under no circumstances should this attribute be added to an existing instrumentation.

The type of instrumentation helps to determine how the attribute should be handled, see below.

### Stable Instrumentation

Should continue emitting the attribute unless:

* User has set the domain e.g. `database` via the `OTEL_SEMCONV_STABILITY_OPT_IN` environment variable.
* User has excluded the attribute via explicit configuration
* The instrumentation bumps its major version but will continue providing security patches for
the previous major version for at least 6 months.

The [Drop Action](#drop) can occur when the major version is bumped provided that the previous major version will/has received 6 months of security patches from the time the replacement attribute is introduced.

### Long-term Unstable Instrumentation

> [!NOTE]
> Examples of long term unstable instrumentation, would be the OpenTelemetry Contrib packages as
> their stability is following that of the signal they are implementing.

Should stop emitting the attribute unless:

* User has set the domain e.g. `database/dup` via the `OTEL_SEMCONV_STABILITY_OPT_IN` environment variable.
* User has included the attribute via explicit configuration

The [Drop Action](#drop) can occur when the deployment level of the package changes.
For instance a beta package moves to release candidate.

### Unstable Instrumentation

Should follow the definition of the [Drop Action](#drop) for how to proceed.

## Rename

The implementation is able to rename the attribute currently being emitted without needing to support the existing attribute anymore. 

This equivilant to adding a new attribute and performing the [Drop Action](#drop) on the old attribute.

## Remove

The remove action helps to facilitate the removal of a deprecated attribute.
Under no circumstances should this attribute be added to an existing instrumentation.

The type of instrumentation helps to determine how the attribute should be handled, see below.

### Stable Instrumentation

Should continue emitting the attribute unless:

* User has excluded the attribute via explicit configuration
* The instrumentation bumps its major version but will continue providing security patches for
the previous major version for at least 6 months.

The [Drop Action](#drop) can occur when the major version is bumped provided that previous major version will/has
received 6 months of security patches from the time that the default behaviour was changed to not emit.

### Long-term Unstable Instrumentation

Should stop emitting the attribute unless:

* User has included the attribute via explicit configuration

The [Drop Action](#drop) can occur when the deployment level of the package changes. For instance a beta package moves to release candidate.

### Unstable Instrumentation

Should follow the definition of the [Drop Action](#drop) for how to proceed.

## Update

The update action indicates that the replacement attribute is not just a rename of the existing attribute but something more.
This could be a split of the value into multiple attributes, change in units/type of the value or something else.
The deprecation note should provide more details of the change required and it is assumed that this action behaves just like the [Migrate action](#migrate) unless stated otherwise.

## Drop

The drop action is where an attribute can be removed from the implementation so that the signal will not natively emit that attribute again.
There is no ability for a user to configure that attribute to be emitted.

Under no circumstances should this attribute be added to an existing instrumentation.


[DocumentStatus]:
  https://opentelemetry.io/docs/specs/otel/document-status
