<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Database
path_base_for_github_subdir:
  from: tmp/semconv/docs/database/_index.md
  to: database/README.md
--->

# Semantic Conventions for Database Calls and Systems

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for database client spans as well as
database metrics and logs.

> **Warning**
> Existing database instrumentations that are using
> [v1.24.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.24.0/docs/database/README.md)
> (or prior) SHOULD NOT change the version of the database conventions that they emit
> until a transition plan to the (future) stable semantic conventions has been published.
> Conventions include, but are not limited to, attributes, metric and span names, and unit of measure.

Semantic conventions for database operations are defined for the following signals:

* [DB Spans](database-spans.md): Semantic Conventions for database client *spans*.
* [DB Metrics](database-metrics.md): Semantic Conventions for database operation *metrics*.

Technology specific semantic conventions are defined for the following databases:

* [AWS DynamoDB](dynamodb.md): Semantic Conventions for *AWS DynamoDB*.
* [Cassandra](cassandra.md): Semantic Conventions for *Cassandra*.
* [Cosmos DB](cosmosdb.md): Semantic Conventions for *Microsoft Cosmos DB*.
* [CouchDB](couchdb.md): Semantic Conventions for *CouchDB*.
* [Elasticsearch](elasticsearch.md): Semantic Conventions for *Elasticsearch*.
* [GraphQL](graphql.md): Semantic Conventions for *GraphQL Server*.
* [HBase](hbase.md): Semantic Conventions for *HBase*.
* [MongoDB](mongodb.md): Semantic Conventions for *MongoDB*.
* [MSSQL](mssql.md): Semantic Conventions for *MSSQL*.
* [Redis](redis.md): Semantic Conventions for *Redis*.
* [SQL](sql.md): Semantic Conventions for *SQL* databases.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
