<!--- Hugo front matter used to generate the website version of this page:
linkTitle: AWS DynamoDB
--->

# Semantic Conventions for AWS DynamoDB

**Status**: [Experimental][DocumentStatus]

The Semantic Conventions for [AWS DynamoDB](https://aws.amazon.com/dynamodb/) extend and override the general
[AWS SDK Semantic Conventions](/docs/cloud-providers/aws-sdk.md)
that describe common AWS SDK attributes and the [Database Semantic Conventions](database-spans.md).
that describe common database operations attributes in addition to the Semantic Conventions
described on this page.

## Common Attributes

These attributes are filled in for all DynamoDB request types.

<!-- semconv dynamodb.all -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`db.system`](../attributes-registry/db.md) | string | The value `dynamodb`. | `dynamodb` | `Required` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.BatchGetItem

<!-- semconv dynamodb.batchgetitem -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | The keys in the `RequestItems` object field. | `[Users, Cats]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.BatchWriteItem

<!-- semconv dynamodb.batchwriteitem -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.item_collection_metrics`](../attributes-registry/aws.md) | string | The JSON-serialized value of the `ItemCollectionMetrics` response field. | `{ "string" : [ { "ItemCollectionKey": { "string" : { "B": blob, "BOOL": boolean, "BS": [ blob ], "L": [ "AttributeValue" ], "M": { "string" : "AttributeValue" }, "N": "string", "NS": [ "string" ], "NULL": boolean, "S": "string", "SS": [ "string" ] } }, "SizeEstimateRangeGB": [ number ] } ] }` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | The keys in the `RequestItems` object field. | `[Users, Cats]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.CreateTable

<!-- semconv dynamodb.createtable -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.global_secondary_indexes`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item of the `GlobalSecondaryIndexes` request field | `[{ "IndexName": "string", "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" }, "ProvisionedThroughput": { "ReadCapacityUnits": number, "WriteCapacityUnits": number } }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.item_collection_metrics`](../attributes-registry/aws.md) | string | The JSON-serialized value of the `ItemCollectionMetrics` response field. | `{ "string" : [ { "ItemCollectionKey": { "string" : { "B": blob, "BOOL": boolean, "BS": [ blob ], "L": [ "AttributeValue" ], "M": { "string" : "AttributeValue" }, "N": "string", "NS": [ "string" ], "NULL": boolean, "S": "string", "SS": [ "string" ] } }, "SizeEstimateRangeGB": [ number ] } ] }` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.local_secondary_indexes`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item of the `LocalSecondaryIndexes` request field. | `[{ "IndexArn": "string", "IndexName": "string", "IndexSizeBytes": number, "ItemCount": number, "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" } }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.provisioned_read_capacity`](../attributes-registry/aws.md) | double | The value of the `ProvisionedThroughput.ReadCapacityUnits` request parameter. | `1.0`; `2.0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.provisioned_write_capacity`](../attributes-registry/aws.md) | double | The value of the `ProvisionedThroughput.WriteCapacityUnits` request parameter. | `1.0`; `2.0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.DeleteItem

<!-- semconv dynamodb.deleteitem -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.item_collection_metrics`](../attributes-registry/aws.md) | string | The JSON-serialized value of the `ItemCollectionMetrics` response field. | `{ "string" : [ { "ItemCollectionKey": { "string" : { "B": blob, "BOOL": boolean, "BS": [ blob ], "L": [ "AttributeValue" ], "M": { "string" : "AttributeValue" }, "N": "string", "NS": [ "string" ], "NULL": boolean, "S": "string", "SS": [ "string" ] } }, "SizeEstimateRangeGB": [ number ] } ] }` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.DeleteTable

<!-- semconv dynamodb.deletetable -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.DescribeTable

<!-- semconv dynamodb.describetable -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.GetItem

<!-- semconv dynamodb.getitem -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.consistent_read`](../attributes-registry/aws.md) | boolean | The value of the `ConsistentRead` request parameter. |  | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.projection`](../attributes-registry/aws.md) | string | The value of the `ProjectionExpression` request parameter. | `Title`; `Title, Price, Color`; `Title, Description, RelatedItems, ProductReviews` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.ListTables

<!-- semconv dynamodb.listtables -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.exclusive_start_table`](../attributes-registry/aws.md) | string | The value of the `ExclusiveStartTableName` request parameter. | `Users`; `CatsTable` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.limit`](../attributes-registry/aws.md) | int | The value of the `Limit` request parameter. | `10` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_count`](../attributes-registry/aws.md) | int | The number of items in the `TableNames` response parameter. | `20` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.PutItem

<!-- semconv dynamodb.putitem -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.item_collection_metrics`](../attributes-registry/aws.md) | string | The JSON-serialized value of the `ItemCollectionMetrics` response field. | `{ "string" : [ { "ItemCollectionKey": { "string" : { "B": blob, "BOOL": boolean, "BS": [ blob ], "L": [ "AttributeValue" ], "M": { "string" : "AttributeValue" }, "N": "string", "NS": [ "string" ], "NULL": boolean, "S": "string", "SS": [ "string" ] } }, "SizeEstimateRangeGB": [ number ] } ] }` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | The keys in the `RequestItems` object field. | `[Users, Cats]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.Query

<!-- semconv dynamodb.query -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.attributes_to_get`](../attributes-registry/aws.md) | string[] | The value of the `AttributesToGet` request parameter. | `[lives, id]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.consistent_read`](../attributes-registry/aws.md) | boolean | The value of the `ConsistentRead` request parameter. |  | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.index_name`](../attributes-registry/aws.md) | string | The value of the `IndexName` request parameter. | `name_to_group` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.limit`](../attributes-registry/aws.md) | int | The value of the `Limit` request parameter. | `10` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.projection`](../attributes-registry/aws.md) | string | The value of the `ProjectionExpression` request parameter. | `Title`; `Title, Price, Color`; `Title, Description, RelatedItems, ProductReviews` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.scan_forward`](../attributes-registry/aws.md) | boolean | The value of the `ScanIndexForward` request parameter. |  | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.select`](../attributes-registry/aws.md) | string | The value of the `Select` request parameter. | `ALL_ATTRIBUTES`; `COUNT` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.Scan

<!-- semconv dynamodb.scan -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.attributes_to_get`](../attributes-registry/aws.md) | string[] | The value of the `AttributesToGet` request parameter. | `[lives, id]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.consistent_read`](../attributes-registry/aws.md) | boolean | The value of the `ConsistentRead` request parameter. |  | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.count`](../attributes-registry/aws.md) | int | The value of the `Count` response parameter. | `10` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.index_name`](../attributes-registry/aws.md) | string | The value of the `IndexName` request parameter. | `name_to_group` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.limit`](../attributes-registry/aws.md) | int | The value of the `Limit` request parameter. | `10` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.projection`](../attributes-registry/aws.md) | string | The value of the `ProjectionExpression` request parameter. | `Title`; `Title, Price, Color`; `Title, Description, RelatedItems, ProductReviews` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.scanned_count`](../attributes-registry/aws.md) | int | The value of the `ScannedCount` response parameter. | `50` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.segment`](../attributes-registry/aws.md) | int | The value of the `Segment` request parameter. | `10` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.select`](../attributes-registry/aws.md) | string | The value of the `Select` request parameter. | `ALL_ATTRIBUTES`; `COUNT` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.total_segments`](../attributes-registry/aws.md) | int | The value of the `TotalSegments` request parameter. | `100` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.UpdateItem

<!-- semconv dynamodb.updateitem -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.item_collection_metrics`](../attributes-registry/aws.md) | string | The JSON-serialized value of the `ItemCollectionMetrics` response field. | `{ "string" : [ { "ItemCollectionKey": { "string" : { "B": blob, "BOOL": boolean, "BS": [ blob ], "L": [ "AttributeValue" ], "M": { "string" : "AttributeValue" }, "N": "string", "NS": [ "string" ], "NULL": boolean, "S": "string", "SS": [ "string" ] } }, "SizeEstimateRangeGB": [ number ] } ] }` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## DynamoDB.UpdateTable

<!-- semconv dynamodb.updatetable -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.dynamodb.attribute_definitions`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `AttributeDefinitions` request field. | `[{ "AttributeName": "string", "AttributeType": "string" }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.consumed_capacity`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.global_secondary_index_updates`](../attributes-registry/aws.md) | string[] | The JSON-serialized value of each item in the `GlobalSecondaryIndexUpdates` request field. | `[{ "Create": { "IndexName": "string", "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" }, "ProvisionedThroughput": { "ReadCapacityUnits": number, "WriteCapacityUnits": number } }]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.provisioned_read_capacity`](../attributes-registry/aws.md) | double | The value of the `ProvisionedThroughput.ReadCapacityUnits` request parameter. | `1.0`; `2.0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.provisioned_write_capacity`](../attributes-registry/aws.md) | double | The value of the `ProvisionedThroughput.WriteCapacityUnits` request parameter. | `1.0`; `2.0` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.dynamodb.table_names`](../attributes-registry/aws.md) | string[] | A single-element array with the value of the TableName request parameter. | `[Users]` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
