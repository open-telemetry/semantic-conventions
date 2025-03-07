<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Database
--->

# Semantic conventions for database calls and systems

**Status**: [Mixed][DocumentStatus]

This document defines semantic conventions for database client spans as well as
database metrics and logs.

> **Warning**
>
> Existing database instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/database-spans.md)
> (or prior):
>
> * SHOULD NOT change the version of the database conventions that they emit by default
>   until the database semantic conventions are marked stable.
>   Conventions include, but are not limited to, attributes,
>   metric and span names, and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   in the existing major version which is a comma-separated list of values.
>   The list of values includes:
>   * `database` - emit the new, stable database conventions,
>     and stop emitting the old experimental database conventions
>     that the instrumentation emitted previously.
>   * `database/dup` - emit both the old and the stable database conventions,
>     allowing for a seamless transition.
>   * The default behavior (in the absence of one of these values) is to continue
>     emitting whatever version of the old experimental database conventions
>     the instrumentation was emitting previously.
>   * Note: `database/dup` has higher precedence than `database` in case both values are present
> * SHOULD maintain (security patching at a minimum) the existing major version
>   for at least six months after it starts emitting both sets of conventions.
> * SHOULD drop the environment variable in the next major version.

Semantic conventions for database operations are defined for the following signals:

* [DB Spans](database-spans.md): Semantic Conventions for database client *spans*.
* [DB Metrics](database-metrics.md): Semantic Conventions for database operation *metrics*.

Technology specific semantic conventions are defined for the following databases:

* [AWS DynamoDB](dynamodb.md): Semantic Conventions for *AWS DynamoDB*.
* [Cassandra](cassandra.md): Semantic Conventions for *Cassandra*.
* [Azure Cosmos DB](cosmosdb.md): Semantic Conventions for *Azure Cosmos DB*.
* [CouchDB](couchdb.md): Semantic Conventions for *CouchDB*.
* [Elasticsearch](elasticsearch.md): Semantic Conventions for *Elasticsearch*.
* [HBase](hbase.md): Semantic Conventions for *HBase*.
* [MongoDB](mongodb.md): Semantic Conventions for *MongoDB*.
* [Microsoft SQL Server](mssql.md): Semantic Conventions for *Microsoft SQL Server*.
* [Oracle Database](oracledb.md): Semantic Conventions for *Oracle Database*.
* [Redis](redis.md): Semantic Conventions for *Redis*.
* [SQL](sql.md): Semantic Conventions for *SQL* databases.

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
