<!--- Hugo front matter used to generate the website version of this page:
linkTitle: InfluxDB
--->

# Semantic Conventions for InfluxDB

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [InfluxDB](https://www.influxdata.com/) extend and override
the [Database Semantic Conventions](database-spans.md)
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

`db.system` MUST be set to `"influxdb"`.

## Attributes

<!-- semconv db.influxdb(full,tag=tech-specific) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.namespace`](../attributes-registry/db.md) | string | The InfluxDB database name. [1] | `mydb` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`db.operation.name`](../attributes-registry/db.md) | string | The name of the command being executed. [2] | `CREATE DATABASE`; `DROP DATABASE`; `SELECT`; `write` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** For InfluxDB the `db.namespace` should be set to the InfluxDB database name.

**[2]:** See [InfluxDB database commands](https://docs.influxdata.com/influxdb/v1/query_language/).
<!-- endsemconv -->

## Example

| Key                 | Value                             |
|:--------------------|:----------------------------------|
| Span name           | `"SELECT mydb"`                   |
| `db.system`         | `"influxdb"`                      |
| `db.namespace`      | `"mydb"`                          |
| `server.address`    | `"localhost"`                     |
| `server.port`       | `"32771"`                         |
| `db.statement`      | `"SELECT * FROM mydb GROUP BY *"` |
| `db.operation.name` | `"SELECT"`                        |

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
