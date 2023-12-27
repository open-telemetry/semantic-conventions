# CloudFoundry

**Status**: [Experimental][DocumentStatus]

Useful resources to understand CloudFoundry metadata:

* <https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#VCAP-APPLICATION>
* <https://docs.cloudfoundry.org/devguide/deploy-apps/streaming-logs.html>
* <https://github.com/cloudfoundry/loggregator-api#v2-envelope>
* <https://bosh.io/docs/jobs/#properties-spec>

CloudFoundry organizes application deployments (apps) by spaces contained in
organizations (orgs). Names are unique only in their respective enclosing
entity. Ids are unique in the entire CloudFoundry installation. Different
instances of the same application are separated by an integer index. Apps can
consist of a main job and multiple tasks and side-cars, which can be
distinguished by different process attributes.

CloudFoundry can also emit signals from system components. They use a different
approach as applications, since they are not organized into orgs and spaces.
They align with the Bosh deployment tool of CloudFoundry.

## Organization

**type:** `cloudfoundry.org`

**Description:** A CloudFoundry Organization

<!-- semconv cloudfoundry.org -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`cloudfoundry.org.id`](../attributes-registry/cloudfoundry.md) | string | The guid of the CloudFoundry org the application is running in. [1] | `218fc5a9-a5f1-4b54-aa05-46717d0ab26d` | Recommended |
| [`cloudfoundry.org.name`](../attributes-registry/cloudfoundry.md) | string | The name of the CloudFoundry organization the app is running in. [2] | `my-org-name` | Recommended |

**[1]:** Application instrumentation should use the value from environment
variable `VCAP_APPLICATION.org_id`. This is the same value as
reported by `cf org <org-name> --guid`.

**[2]:** Application instrumentation should use the value from environment
variable `VCAP_APPLICATION.org_name`. This is the same value as
reported by `cf orgs`.
<!-- endsemconv -->

## Space

**type:** `cloudfoundry.space`

**Description:** A CloudFoundry Space

<!-- semconv cloudfoundry.space -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`cloudfoundry.space.id`](../attributes-registry/cloudfoundry.md) | string | The guid of the CloudFoundry space the application is running in. [1] | `218fc5a9-a5f1-4b54-aa05-46717d0ab26d` | Recommended |
| [`cloudfoundry.space.name`](../attributes-registry/cloudfoundry.md) | string | The name of the CloudFoundry space the application is running in. [2] | `my-space-name` | Recommended |

**[1]:** Application instrumentation should use the value from environment
variable `VCAP_APPLICATION.space_id`. This is the same value as
reported by `cf space <space-name> --guid`.

**[2]:** Application instrumentation should use the value from environment
variable `VCAP_APPLICATION.space_name`. This is the same value as
reported by `cf spaces`.
<!-- endsemconv -->

## Application

***type:** `cloudfoundry.app`

**Description:** A CloudFoundry Application

<!-- semconv cloudfoundry.app -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`cloudfoundry.app.id`](../attributes-registry/cloudfoundry.md) | string | The guid of the application. [1] | `218fc5a9-a5f1-4b54-aa05-46717d0ab26d` | Recommended |
| [`cloudfoundry.app.name`](../attributes-registry/cloudfoundry.md) | string | The name of the application. [2] | `my-app-name` | Recommended |

**[1]:** Application instrumentation should use the value from environment
variable `VCAP_APPLICATION.application_id`. This is the same value as
reported by `cf app <app-name> --guid`.

**[2]:** Application instrumentation should use the value from environment
variable `VCAP_APPLICATION.application_name`. This is the same value
as reported by `cf apps`.
<!-- endsemconv -->

## Process

**type:** `cloudfoundry.process`

**Description:** A CloudFoundry Application Process

<!-- semconv cloudfoundry.process -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`cloudfoundry.process.id`](../attributes-registry/cloudfoundry.md) | string | The UID identifying the process. [1] | `218fc5a9-a5f1-4b54-aa05-46717d0ab26d` | Recommended |
| [`cloudfoundry.process.type`](../attributes-registry/cloudfoundry.md) | string | The type of process. [2] | `web` | Recommended |

**[1]:** Application instrumentation should use the value from environment
variable `VCAP_APPLICATION.process_id`. It is supposed to be equal to
`VCAP_APPLICATION.app_id` for applications deployed to the runtime.
For system components, this could be the actual PID.

**[2]:** CloudFoundry applications can consist of multiple jobs. Usually the
main process will be of type `web`. There can be additional background
tasks or side-cars with different process types.
<!-- endsemconv -->

## Generic Source

**type:** `cloudfoundry`

**Description:** The generic source (app or system component)

<!-- semconv cloudfoundry(tag=generic) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`cloudfoundry.instance_id`](../attributes-registry/cloudfoundry.md) | string | An index or guid describing the concrete instance of the event source. [1] | `0`; `218fc5a9-a5f1-4b54-aa05-46717d0ab26d` | Required |
| [`cloudfoundry.source_id`](../attributes-registry/cloudfoundry.md) | string | A guid or another name describing the event source. [2] | `218fc5a9-a5f1-4b54-aa05-46717d0ab26d`; `cf/gorouter` | Required |

**[1]:** CloudFoundry defines the `instance_id` in the [Loggegator v2 envelope](https://github.com/cloudfoundry/loggregator-api#v2-envelope).
It is used for logs and metrics emitted by CloudFoundry. It is
supposed to contain the application instance index for applications
deployed on the runtime or the vm id for CloudFoundry components.

Application instrumentation should use the value from environment
variable `CF_INSTANCE_INDEX`.

When system components are instrumented, values from the [Bosh spec](https://bosh.io/docs/jobs/#properties-spec)
should be used. The `instance_id` should be set to `spec.id`.

**[2]:** CloudFoundry defines the `source_id` in the [Loggegator v2 envelope](https://github.com/cloudfoundry/loggregator-api#v2-envelope).
It is used for logs and metrics emitted by CloudFoundry. It is
supposed to contain the application id for applications deployed on
the runtime or the component name, e.g. "gorouter", for CloudFoundry
components.

Application instrumentation should use the value from environment
variable `VCAP_APPLICATION.application_id`. This is the same value as
reported by `cf app <app-name> --guid`.

When system components are instrumented, values from the [Bosh spec](https://bosh.io/docs/jobs/#properties-spec)
should be used. The `source_id` should be set to
`spec.deployment/spec.name`.
<!-- endsemconv -->

## Source Type

**type:**`cloudfoundry.source_type`

**Description:** The CloudFoundry source type.

<!-- semconv cloudfoundry(tag=source_type) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`cloudfoundry.source_type`](../attributes-registry/cloudfoundry.md) | string | The type of the event source. [1] | `APP/PROC/WEB/0`; `APP/TASK/jobscheduler-task-70013817-ab92-4f75-82d4-de8ae4dd64b4`; `RTR`; `STG` | Recommended |

**[1]:** CloudFoundry generates log messages with different source types for an
applications. This indicates, whether the log was created from the
actual application, a background task, the central load balancer, or
the CloudFoundry runtime, e.g. during a deployment.

The `source_type` is contained as a tag of the [Loggegator v2 envelope](https://github.com/cloudfoundry/loggregator-api#v2-envelope).
It is also available in the syslog drain structured data as documented
in the [CloudFoundry Dev Guide](https://docs.cloudfoundry.org/devguide/deploy-apps/streaming-logs.html).
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
