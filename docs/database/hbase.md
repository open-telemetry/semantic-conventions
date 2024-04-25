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
| [`db.collection.name`](../attributes-registry/db.md) | string | The HBase table name. [1] | `mytable`; `ns:table` | `Conditionally Required` If applicable. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.namespace`](../attributes-registry/db.md) | string | The HBase namespace. [2] | `mynamespace` | `Conditionally Required` If applicable. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If table name includes the namespace, the `db.collection.name` SHOULD be set to the full table name.

**[2]:** When performing table-related operations, the instrumentations SHOULD extract the namespace from the table name according to the [HBase table naming conventions](https://hbase.apache.org/book.html#namespace_creation). If namespace is not provided, instrumentation SHOULD set `db.namespace` value to `default`.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
