<!--- Hugo front matter used to generate the website version of this page:
linkTitle: HBase
--->

# Semantic Conventions for HBase

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [HBase](https://hbase.apache.org/) extend and override the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"hbase"`.

## Attributes

<!-- semconv db.hbase(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.name`](../attributes-registry/db.md) | string | The HBase namespace. [1] | `mynamespace` | `Conditionally Required` If applicable. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** For HBase the `db.name` should be set to the HBase namespace.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
