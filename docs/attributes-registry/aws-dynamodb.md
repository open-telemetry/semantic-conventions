# AWS DynamoDB

## AWS DynamoDB Attributes
<!-- semconv registry.aws.dynamodb(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `aws.dynamodb.attribute_definitions` | string[] | The JSON-serialized value of each item in the `AttributeDefinitions` request field. | `[{ "AttributeName": "string", "AttributeType": "string" }]` |
| `aws.dynamodb.attributes_to_get` | string[] | The value of the `AttributesToGet` request parameter. | `[lives, id]` |
| `aws.dynamodb.consistent_read` | boolean | The value of the `ConsistentRead` request parameter. |  |
| `aws.dynamodb.consumed_capacity` | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` |
| `aws.dynamodb.count` | int | The value of the `Count` response parameter. | `10` |
| `aws.dynamodb.exclusive_start_table` | string | The value of the `ExclusiveStartTableName` request parameter. | `Users`; `CatsTable` |
| `aws.dynamodb.global_secondary_index_updates` | string[] | The JSON-serialized value of each item in the `GlobalSecondaryIndexUpdates` request field. | `[{ "Create": { "IndexName": "string", "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" }, "ProvisionedThroughput": { "ReadCapacityUnits": number, "WriteCapacityUnits": number } }]` |
| `aws.dynamodb.global_secondary_indexes` | string[] | The JSON-serialized value of each item of the `GlobalSecondaryIndexes` request field | `[{ "IndexName": "string", "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" }, "ProvisionedThroughput": { "ReadCapacityUnits": number, "WriteCapacityUnits": number } }]` |
| `aws.dynamodb.index_name` | string | The value of the `IndexName` request parameter. | `name_to_group` |
| `aws.dynamodb.item_collection_metrics` | string | The JSON-serialized value of the `ItemCollectionMetrics` response field. | `{ "string" : [ { "ItemCollectionKey": { "string" : { "B": blob, "BOOL": boolean, "BS": [ blob ], "L": [ "AttributeValue" ], "M": { "string" : "AttributeValue" }, "N": "string", "NS": [ "string" ], "NULL": boolean, "S": "string", "SS": [ "string" ] } }, "SizeEstimateRangeGB": [ number ] } ] }` |
| `aws.dynamodb.limit` | int | The value of the `Limit` request parameter. | `10` |
| `aws.dynamodb.local_secondary_indexes` | string[] | The JSON-serialized value of each item of the `LocalSecondaryIndexes` request field. | `[{ "IndexArn": "string", "IndexName": "string", "IndexSizeBytes": number, "ItemCount": number, "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" } }]` |
| `aws.dynamodb.projection` | string | The value of the `ProjectionExpression` request parameter. | `Title`; `Title, Price, Color`; `Title, Description, RelatedItems, ProductReviews` |
| `aws.dynamodb.provisioned_read_capacity` | double | The value of the `ProvisionedThroughput.ReadCapacityUnits` request parameter. | `1.0`; `2.0` |
| `aws.dynamodb.provisioned_write_capacity` | double | The value of the `ProvisionedThroughput.WriteCapacityUnits` request parameter. | `1.0`; `2.0` |
| `aws.dynamodb.scan_forward` | boolean | The value of the `ScanIndexForward` request parameter. |  |
| `aws.dynamodb.scanned_count` | int | The value of the `ScannedCount` response parameter. | `50` |
| `aws.dynamodb.segment` | int | The value of the `Segment` request parameter. | `10` |
| `aws.dynamodb.select` | string | The value of the `Select` request parameter. | `ALL_ATTRIBUTES`; `COUNT` |
| `aws.dynamodb.table_count` | int | The number of items in the `TableNames` response parameter. | `20` |
| `aws.dynamodb.table_names` | string[] | The keys in the `RequestItems` object field. | `[Users, Cats]` |
| `aws.dynamodb.total_segments` | int | The value of the `TotalSegments` request parameter. | `100` |
<!-- endsemconv -->
