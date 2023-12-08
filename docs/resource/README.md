<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Resource
path_base_for_github_subdir:
  from: tmp/semconv/docs/resource/_index.md
  to: resource/README.md
--->

# Resource Semantic Conventions

**Status**: [Mixed][DocumentStatus]

This document defines standard attributes for resources. These attributes are typically used in the [Resource](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/resource/sdk.md) and are also recommended to be used anywhere else where there is a need to describe a resource in a consistent manner. The majority of these attributes are inherited from
[OpenCensus Resource standard](https://github.com/census-instrumentation/opencensus-specs/blob/master/resource/StandardResources.md).

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [TODOs](#todos)
- [Document Conventions](#document-conventions)
- [Attributes with Special Handling](#attributes-with-special-handling)
  * [Semantic Attributes with Dedicated Environment Variable](#semantic-attributes-with-dedicated-environment-variable)
  * [Semantic Attributes with SDK-provided Default Value](#semantic-attributes-with-sdk-provided-default-value)
- [Service](#service)
- [Service (Experimental)](#service-experimental)
- [Telemetry SDK](#telemetry-sdk)
- [Telemetry SDK (Experimental)](#telemetry-sdk-experimental)
- [Compute Unit](#compute-unit)
- [Compute Instance](#compute-instance)
- [Environment](#environment)
- [Version attributes](#version-attributes)
- [Cloud-Provider-Specific Attributes](#cloud-provider-specific-attributes)

<!-- tocstop -->

## TODOs

* Add more compute units: AppEngine unit, etc.
* Add Web Browser.
* Decide if lower case strings only.
* Consider to add optional/required for each attribute and combination of attributes
  (e.g when supplying a k8s resource all k8s may be required).

## Document Conventions

**Status**: [Stable][DocumentStatus]

Attributes are grouped logically by the type of the concept that they described. Attributes in the same group have a common prefix that ends with a dot. For example all attributes that describe Kubernetes properties start with "k8s."

See [Attribute Requirement Levels](../general/attribute-requirement-level.md) for details on when attributes
should be included.

## Attributes with Special Handling

**Status**: [Stable][DocumentStatus]

Given their significance some resource attributes are treated specifically as described below.

### Semantic Attributes with Dedicated Environment Variable

These are the attributes which MAY be configurable via a dedicated environment variable
as specified in [OpenTelemetry Environment Variable Specification](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/configuration/sdk-environment-variables.md):

- [`service.name`](#service)

### Semantic Attributes with SDK-provided Default Value

These are the attributes which MUST be provided by the SDK
as specified in the [Resource SDK specification](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/resource/sdk.md#sdk-provided-resource-attributes):

- [`service.name`](#service)
- [`telemetry.sdk` group](#telemetry-sdk)

## Service

**Status**: [Stable][DocumentStatus]

**type:** `service`

**Description:** A service instance.

<!-- semconv service -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `service.name` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Logical name of the service. [1] | `shoppingcart` | Required |
| `service.version` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The version string of the service API or implementation. The format is not defined by these conventions. | `2.0.0`; `a01dbef8a` | Recommended |

**[1]:** MUST be the same for all instances of horizontally scaled services. If the value was not specified, SDKs MUST fallback to `unknown_service:` concatenated with [`process.executable.name`](process.md#process), e.g. `unknown_service:bash`. If `process.executable.name` is not available, the value MUST be set to `unknown_service`.
<!-- endsemconv -->

## Service (Experimental)

**Status**: [Experimental][DocumentStatus]

**type:** `service`

**Description:** Additions to service instance.

<!-- semconv service_experimental -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `service.instance.id` | string | The string ID of the service instance. [1] | `my-k8s-pod-deployment-1`; `627cc493-f310-47de-96bd-71410b7dec09` | Recommended |
| `service.namespace` | string | A namespace for `service.name`. [2] | `Shop` | Recommended |

**[1]:** MUST be unique for each instance of the same `service.namespace,service.name` pair
(in other words `service.namespace,service.name,service.instance.id` triplet MUST be globally unique).
The ID helps to distinguish instances of the same service that exist at the same time
(e.g. instances of a horizontally scaled service). It is preferable for the ID to be persistent
and stay the same for the lifetime of the service instance, however it is acceptable that
the ID is ephemeral and changes during important lifetime events for the service
(e.g. service instance restarts).

If the instance has no inherent unique ID that can be used as the value of this attribute,
implementations MAY to generate a random Version 1 or Version 4
[RFC 4122](https://www.ietf.org/rfc/rfc4122.txt) UUID. When enough data is available,
implementations SHOULD use Version 5 and MUST use the following UUID as the namespace:
`4d63009a-8d0f-11ee-aad7-4c796ed8e320`.

UUIDs are typically recommended, as we only need an opaque yet reproducible value for
the purposes of identifying a service instance. Similar to what can be seen in the man page for the
[`/etc/machine-id`](https://www.freedesktop.org/software/systemd/man/machine-id.html) file,
the underlying data, such as pod name and namespace should be treated as
confidential by this algorithm, being the user's choice to expose it or not via another resource attribute.

When a UUID v5 is generated, the input MUST be prefixed with
`${telemetry.sdk.name}.${telemetry.sdk.language}.${service.namespace}.${service.name}`, followed by the
the workload identifier, which should tentatively stable. This means that the same service yields the
same UUID if the same identifier (`host.id`, `/etc/machine-id`, and so on) remains the same. It would still
yield different results for different services on the same host or namespace. When no namespaces or equivalent fields
are available, the prefix MUST then be `${telemetry.sdk.name}.${telemetry.sdk.language}.${service.name}`.

Users running their services on platforms such as Kubernetes are encouraged to explicitly set the
`service.instance.id` using their existing automation, or by setting a value that can be used for a
consistent value, such as `container.id`. Similarly, users of application servers such as `unicorn`
are encouraged to set the `service.instance.id` on a per-worker basis.

SDKs MUST use the following algorithm when generating `service.instance.id`:

- If the user has provided a `service.instance.id`, via environment
  variable, configuration or custom resource detection, this MUST take priority over generated IDs.
- When any of the below combinations of resource attribute are provided, they MUST be used as the input
  for generating a UUID v5 following the prefix mentioned above. The values within each combination MUST be separated with dots:
  * `container.id`, resulting in the input `${telemetry.sdk.name}.${telemetry.sdk.language}.${service.namespace}.${service.name}.${container.id}`, 
  possibly without the namespace.
  * `k8s.namespace.name`/`k8s.pod.name`/`k8s.container.name`, resulting in the input
  `${telemetry.sdk.name}.${telemetry.sdk.language}.${k8s.namespace.name}.${service.name}.${k8s.pod.name}.${k8s.container.name}`. In this case,
  the namespace MUST be used.
  * `host.id`, resulting in the input `${telemetry.sdk.name}.${telemetry.sdk.language}.${service.namespace}.${service.name}.${host.id}`,
  possibly without the namespace.
- When the SDK is running in an environment where a `/etc/machine-id`
  (see [MACHINE-ID(5)](https://www.freedesktop.org/software/systemd/man/machine-id.html))
  is available, the machine-id should be used in the input for generating a UUID v5 (possibly without the namespace):
  `${telemetry.sdk.name}.${telemetry.sdk.language}.${service.namespace}.${service.name}.${machine.id}`
- When the SDK is running on a Windows environment and there's a reasonable way to read
  registry keys for the SDK, the registry key
  `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography\MachineGuid` can be used in a
  similar way to Linux' machine-id above.
- When no other source is available the SDK MUST generate a value using UUID v1 or v4.
  This would also typically be the case for service instances running on Kubernetes,
  given that the pod's name and namespace are not unique enough to determine a service
  instance's identity and the container name cannot easily be inferred: on pods with
  multiple containers, the `service.instance.id` would yield the same results for all
  containers, which is not desirable. And given that the services are ephemeral on
  Kubernetes, the `service.instance.id` would change on each restart, being therefore
  no different than a completely new UUID per process.

Examples in Go, using the package "github.com/google/uuid" to generate the UUIDs:

```go
package main

import (
  "fmt"

  "github.com/google/uuid"
)

func main() {
  // fixed namespace for the purposes of this OTEP
  ns := uuid.MustParse("4d63009a-8d0f-11ee-aad7-4c796ed8e320")

  // prefix when no namespace is available
  prefix := "${telemetry.sdk.name}.${telemetry.sdk.language}.${service.name}"

  // prefix when a namespace is available
  prefix = "${telemetry.sdk.name}.${telemetry.sdk.language}.${service.namespace}.${service.name}"

  // actual prefix for the OTel Go SDK, for a service named "customers"
  prefix = "opentelemetry.go.customers"

  // the generated service.instance.id where a host.id is used
  host := "graviola"
  id := uuid.NewSHA1(ns, []byte(fmt.Sprintf("%s.%s", prefix, host))) // 17ffc8fd-6ed7-5069-a5fb-2fed78f5455f
  fmt.Printf("v5 host id: %v\n", id)

  // the generated service.instance.id where a typical kubernetes values are available
  namespace := "accounting"
  name := "vendors" // typically, the deployment name
  pod := "vendors-pqr-jh7d2"
  container := "some-sidecar"
  input := fmt.Sprintf("opentelemetry.go.%s.%s.%s.%s", namespace, name, pod, container)
  id = uuid.NewSHA1(ns, []byte(input)) // f3a5f61b-9fff-5707-8d41-d3a9d2423b7d
  fmt.Printf("v5 id: %v\n", id)
}
```

**[2]:** A string value having a meaning that helps to distinguish a group of services, for example the team name that owns a group of services. `service.name` is expected to be unique within the same namespace. If `service.namespace` is not specified in the Resource then `service.name` is expected to be unique for all services that have no explicit namespace defined (so the empty/unspecified namespace is simply one more valid namespace). Zero-length namespace string is assumed equal to unspecified namespace.
<!-- endsemconv -->

Note: `service.namespace` and `service.name` are not intended to be concatenated for the purpose of forming a single globally unique name for the service. For example the following 2 sets of attributes actually describe 2 different services (despite the fact that the concatenation would result in the same string):

```
# Resource attributes that describes a service.
namespace = Company.Shop
service.name = shoppingcart
```

```
# Another set of resource attributes that describe a different service.
namespace = Company
service.name = Shop.shoppingcart
```

## Telemetry SDK

**Status**: [Stable][DocumentStatus]

**type:** `telemetry.sdk`

**Description:** The telemetry SDK used to capture data recorded by the instrumentation libraries.

<!-- semconv telemetry -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `telemetry.sdk.language` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The language of the telemetry SDK. | `cpp` | Required |
| `telemetry.sdk.name` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The name of the telemetry SDK as defined above. [1] | `opentelemetry` | Required |
| `telemetry.sdk.version` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The version string of the telemetry SDK. | `1.2.3` | Required |

**[1]:** The OpenTelemetry SDK MUST set the `telemetry.sdk.name` attribute to `opentelemetry`.
If another SDK, like a fork or a vendor-provided implementation, is used, this SDK MUST set the
`telemetry.sdk.name` attribute to the fully-qualified class or module name of this SDK's main entry point
or another suitable identifier depending on the language.
The identifier `opentelemetry` is reserved and MUST NOT be used in this case.
All custom identifiers SHOULD be stable across different versions of an implementation.

`telemetry.sdk.language` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `cpp` | cpp |
| `dotnet` | dotnet |
| `erlang` | erlang |
| `go` | go |
| `java` | java |
| `nodejs` | nodejs |
| `php` | php |
| `python` | python |
| `ruby` | ruby |
| `rust` | rust |
| `swift` | swift |
| `webjs` | webjs |
<!-- endsemconv -->

## Telemetry SDK (Experimental)

**Status**: [Experimental][DocumentStatus]

**type:** `telemetry.sdk`

**Description:** Additions to the telemetry SDK.

<!-- semconv telemetry_experimental -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `telemetry.distro.name` | string | The name of the auto instrumentation agent or distribution, if used. [1] | `parts-unlimited-java` | Recommended |
| `telemetry.distro.version` | string | The version string of the auto instrumentation agent or distribution, if used. | `1.2.3` | Recommended |

**[1]:** Official auto instrumentation agents and distributions SHOULD set the `telemetry.distro.name` attribute to
a string starting with `opentelemetry-`, e.g. `opentelemetry-java-instrumentation`.
<!-- endsemconv -->

## Compute Unit

**Status**: [Experimental][DocumentStatus]

Attributes defining a compute unit (e.g. Container, Process, Function as a Service):

- [Container](./container.md)
- [Function as a Service](./faas.md)
- [Process](./process.md)
- [Web engine](./webengine.md)

## Compute Instance

**Status**: [Experimental][DocumentStatus]

Attributes defining a computing instance (e.g. host):

- [Host](./host.md)

## Environment

**Status**: [Experimental][DocumentStatus]

Attributes defining a running environment (e.g. Operating System, Cloud, Data Center, Deployment Service):

- [Operating System](./os.md)
- [Device](./device.md)
- [Cloud](./cloud.md)
- Deployment:
  - [Deployment Environment](./deployment-environment.md)
  - [Kubernetes](./k8s.md)
- [Browser](./browser.md)

## Version attributes

**Status**: [Stable][DocumentStatus]

Version attributes, such as `service.version`, are values of type `string`. They are
the exact version used to identify an artifact. This may be a semantic version, e.g., `1.2.3`, git hash, e.g.,
`8ae73a`, or an arbitrary version string, e.g., `0.1.2.20210101`, whatever was used when building the artifact.

## Cloud-Provider-Specific Attributes

**Status**: [Experimental][DocumentStatus]

Attributes that are only applicable to resources from a specific cloud provider. Currently, these
resources can only be defined for providers listed as a valid `cloud.provider` in
[Cloud](./cloud.md) and below. Provider-specific attributes all reside in the `cloud-provider` directory.
Valid cloud providers are:

- [Alibaba Cloud](https://www.alibabacloud.com/) (`alibaba_cloud`)
- [Amazon Web Services](https://aws.amazon.com/) ([`aws`](cloud-provider/aws/README.md))
- [Google Cloud Platform](https://cloud.google.com/) ([`gcp`](cloud-provider/gcp/README.md))
- [Microsoft Azure](https://azure.microsoft.com/) (`azure`)
- [Tencent Cloud](https://www.tencentcloud.com/) (`tencent_cloud`)
- [Heroku dyno](./cloud-provider/heroku.md)

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
