# AWS

<!-- toc -->

- [AWS DynamoDB Attributes](#aws-dynamodb-attributes)
- [AWS ECS Attributes](#aws-ecs-attributes)
- [AWS EKS Attributes](#aws-eks-attributes)
- [AWS Logs Attributes](#aws-logs-attributes)

<!-- tocstop -->

## AWS DynamoDB Attributes
<!-- semconv registry.aws.dynamodb(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `aws.dynamodb.attribute_definitions` | string[] | The JSON-serialized value of each item in the `AttributeDefinitions` request field. | `[{ "AttributeName": "string", "AttributeType": "string" }]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.attributes_to_get` | string[] | The value of the `AttributesToGet` request parameter. | `[lives, id]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.consistent_read` | boolean | The value of the `ConsistentRead` request parameter. |  | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.consumed_capacity` | string[] | The JSON-serialized value of each item in the `ConsumedCapacity` response field. | `[{ "CapacityUnits": number, "GlobalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "LocalSecondaryIndexes": { "string" : { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number } }, "ReadCapacityUnits": number, "Table": { "CapacityUnits": number, "ReadCapacityUnits": number, "WriteCapacityUnits": number }, "TableName": "string", "WriteCapacityUnits": number }]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.count` | int | The value of the `Count` response parameter. | `10` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.exclusive_start_table` | string | The value of the `ExclusiveStartTableName` request parameter. | `Users`; `CatsTable` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.global_secondary_index_updates` | string[] | The JSON-serialized value of each item in the `GlobalSecondaryIndexUpdates` request field. | `[{ "Create": { "IndexName": "string", "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" }, "ProvisionedThroughput": { "ReadCapacityUnits": number, "WriteCapacityUnits": number } }]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.global_secondary_indexes` | string[] | The JSON-serialized value of each item of the `GlobalSecondaryIndexes` request field | `[{ "IndexName": "string", "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" }, "ProvisionedThroughput": { "ReadCapacityUnits": number, "WriteCapacityUnits": number } }]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.index_name` | string | The value of the `IndexName` request parameter. | `name_to_group` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.item_collection_metrics` | string | The JSON-serialized value of the `ItemCollectionMetrics` response field. | `{ "string" : [ { "ItemCollectionKey": { "string" : { "B": blob, "BOOL": boolean, "BS": [ blob ], "L": [ "AttributeValue" ], "M": { "string" : "AttributeValue" }, "N": "string", "NS": [ "string" ], "NULL": boolean, "S": "string", "SS": [ "string" ] } }, "SizeEstimateRangeGB": [ number ] } ] }` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.limit` | int | The value of the `Limit` request parameter. | `10` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.local_secondary_indexes` | string[] | The JSON-serialized value of each item of the `LocalSecondaryIndexes` request field. | `[{ "IndexArn": "string", "IndexName": "string", "IndexSizeBytes": number, "ItemCount": number, "KeySchema": [ { "AttributeName": "string", "KeyType": "string" } ], "Projection": { "NonKeyAttributes": [ "string" ], "ProjectionType": "string" } }]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.projection` | string | The value of the `ProjectionExpression` request parameter. | `Title`; `Title, Price, Color`; `Title, Description, RelatedItems, ProductReviews` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.provisioned_read_capacity` | double | The value of the `ProvisionedThroughput.ReadCapacityUnits` request parameter. | `1.0`; `2.0` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.provisioned_write_capacity` | double | The value of the `ProvisionedThroughput.WriteCapacityUnits` request parameter. | `1.0`; `2.0` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.scan_forward` | boolean | The value of the `ScanIndexForward` request parameter. |  | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.scanned_count` | int | The value of the `ScannedCount` response parameter. | `50` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.segment` | int | The value of the `Segment` request parameter. | `10` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.select` | string | The value of the `Select` request parameter. | `ALL_ATTRIBUTES`; `COUNT` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.table_count` | int | The number of items in the `TableNames` response parameter. | `20` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.table_names` | string[] | The keys in the `RequestItems` object field. | `[Users, Cats]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.dynamodb.total_segments` | int | The value of the `TotalSegments` request parameter. | `100` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## AWS ECS Attributes
<!-- semconv registry.aws.ecs(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `aws.ecs.task.id` | string | The ID of a running ECS task. The ID MUST be extracted from `task.arn`. | `10838bed-421f-43ef-870a-f43feacbbb5b`; `23ebb8ac-c18f-46c6-8bbe-d55d0e37cfbd` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.ecs.cluster.arn` | string | The ARN of an [ECS cluster](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/clusters.html). | `arn:aws:ecs:us-west-2:123456789123:cluster/my-cluster` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.ecs.container.arn` | string | The Amazon Resource Name (ARN) of an [ECS container instance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_instances.html). | `arn:aws:ecs:us-west-1:123456789123:container/32624152-9086-4f0e-acae-1a75b14fe4d9` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.ecs.launchtype` | string | The [launch type](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html) for an ECS task. | `ec2` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.ecs.task.arn` | string | The ARN of a running [ECS task](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-account-settings.html#ecs-resource-ids). | `arn:aws:ecs:us-west-1:123456789123:task/10838bed-421f-43ef-870a-f43feacbbb5b`; `arn:aws:ecs:us-west-1:123456789123:task/my-cluster/task-id/23ebb8ac-c18f-46c6-8bbe-d55d0e37cfbd` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.ecs.task.family` | string | The family name of the [ECS task definition](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html) used to create the ECS task. | `opentelemetry-family` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.ecs.task.revision` | string | The revision for the task definition used to create the ECS task. | `8`; `26` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`aws.ecs.launchtype` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `ec2` | ec2 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fargate` | fargate | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## AWS EKS Attributes
<!-- semconv registry.aws.eks(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `aws.eks.cluster.arn` | string | The ARN of an EKS cluster. | `arn:aws:ecs:us-west-2:123456789123:cluster/my-cluster` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## AWS Logs Attributes
<!-- semconv registry.aws.log(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `aws.log.group.arns` | string[] | The Amazon Resource Name(s) (ARN) of the AWS log group(s). [1] | `[arn:aws:logs:us-west-1:123456789012:log-group:/aws/my/group:*]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.log.group.names` | string[] | The name(s) of the AWS log group(s) an application is writing to. [2] | `[/aws/lambda/my-function, opentelemetry-service]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.log.stream.arns` | string[] | The ARN(s) of the AWS log stream(s). [3] | `[arn:aws:logs:us-west-1:123456789012:log-group:/aws/my/group:log-stream:logs/main/10838bed-421f-43ef-870a-f43feacbbb5b]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `aws.log.stream.names` | string[] | The name(s) of the AWS log stream(s) an application is writing to. | `[logs/main/10838bed-421f-43ef-870a-f43feacbbb5b]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** See the [log group ARN format documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/iam-access-control-overview-cwl.html#CWL_ARN_Format).

**[2]:** Multiple log groups must be supported for cases like multi-container applications, where a single application has sidecar containers, and each write to their own log group.

**[3]:** See the [log stream ARN format documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/iam-access-control-overview-cwl.html#CWL_ARN_Format). One log group can contain several log streams, so these ARNs necessarily identify both a log group and a log stream.
<!-- endsemconv -->