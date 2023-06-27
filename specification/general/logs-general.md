# General logs attributes

**Status**: [Experimental][DocumentStatus]

The attributes described in this section are rather generic.
They may be used in any Log Record they apply to.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [General log identification attributes](#general-log-identification-attributes)

<!-- tocstop -->

The following semantic conventions for logs are defined:

* [General](#general-log-identification-attributes): General semantic attributes that may be used in describing Log Records.
* [Log Media](/specification/logs/semantic_conventions/media.md): Semantic attributes that may be used in describing the source of a log.
* [Exceptions](/specification/logs/semantic_conventions/exceptions.md): Semantic attributes that may be used in describing exceptions in logs.
* [Feature Flags](/specification/logs/semantic_conventions/feature-flags.md): Semantic attributes that may be used in describing feature flag evaluations in logs.

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

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
