# General logs attributes

**Status**: [Experimental][DocumentStatus]

The attributes described in this section are rather generic.
They may be used in any Log Record they apply to.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [General log identification attributes](#general-log-identification-attributes)
- [Log Media](#log-media)
  * [Log File](#log-file)
  * [I/O Stream](#io-stream)

<!-- tocstop -->

The following semantic conventions for logs are defined:

* **[General](#general-log-identification-attributes): General semantic attributes that may be used in describing Log Records.**
* [Exceptions](/specification/exceptions/exceptions-logs.md): Semantic attributes that may be used in describing exceptions in logs.
* [Feature Flags](/specification/feature-flags/feature-flags-logs.md): Semantic attributes that may be used in describing feature flag evaluations in logs.

Apart from semantic conventions for logs, [events](events-general.md), [traces](trace-general.md), and [metrics](metrics-general.md),
OpenTelemetry also defines the concept of overarching [Resources](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.21.0/specification/resource/sdk.md) with their own
[Resource Semantic Conventions](/specification/resource/semantic_conventions/README.md).

## General log identification attributes

These attributes may be used for identifying a Log Record.

<!-- semconv log.record -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `log.record.uid` | string | A unique identifier for the Log Record. [1] | `01ARZ3NDEKTSV4RRFFQ69G5FAV` | Opt-In |

**[1]:** If an id is provided, other log records with the same id will be considered duplicates and can be removed safely. This means, that two distinguishable log records MUST have different values.
The id MAY be an [Universally Unique Lexicographically Sortable Identifier (ULID)](https://github.com/ulid/spec), but other identifiers (e.g. UUID) may be used as needed.
<!-- endsemconv -->

## Log Media

This section describes attributes for log media in OpenTelemetry. Log media are mechanisms by which logs are transmitted. Types of media include files, streams, network protocols, and os-specific logging services such as journald and Windows Event Log.

**Note:** The OpenTelemetry specification defines a [Resource](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.21.0/specification/resource/sdk.md#resource-sdk) as `an immutable representation of the entity producing telemetry`.
The following attributes do not describe entities that produce telemetry. Rather, they describe mechanisms of log transmission.
As such, these should be recorded as Log Record attributes when applicable. They should not be recorded as Resource attributes.

### Log File

**Description:** A file to which log was emitted.

<!-- semconv attributes.log.file -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `log.file.name` | string | The basename of the file. | `audit.log` | Recommended |
| `log.file.path` | string | The full path to the file. | `/var/log/mysql/audit.log` | Opt-In |
| `log.file.name_resolved` | string | The basename of the file, with symlinks resolved. | `uuid.log` | Opt-In |
| `log.file.path_resolved` | string | The full path to the file, with symlinks resolved. | `/var/lib/docker/uuid.log` | Opt-In |
<!-- endsemconv -->

### I/O Stream

**Description:** The I/O stream to which the log was emitted.

<!-- semconv attributes.log -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `log.iostream` | string | The stream associated with the log. See below for a list of well-known values. | `stdout` | Opt-In |

`log.iostream` MUST be one of the following:

| Value  | Description |
|---|---|
| `stdout` | Logs from stdout stream |
| `stderr` | Events from stderr stream |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
