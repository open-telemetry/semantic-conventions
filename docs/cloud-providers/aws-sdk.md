<!--- Hugo front matter used to generate the website version of this page:
linkTitle: AWS SDK
--->

# Semantic Conventions for AWS SDK

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions to apply when instrumenting the AWS SDK. They map request or response
parameters in AWS SDK API calls to attributes on a Span. The conventions have been collected over time based
on feedback from AWS users of tracing and will continue to increase as new interesting conventions
are found.

Some descriptions are also provided for populating general OpenTelemetry semantic conventions based on these APIs.

## Context Propagation

See [compatibility](../../supplementary-guidelines/compatibility/aws.md#context-propagation).

## Common Attributes

The span name MUST be of the format `Service.Operation` as per the AWS HTTP API, e.g., `DynamoDB.GetItem`,
`S3.ListBuckets`. This is equivalent to concatenating `rpc.service` and `rpc.method` with `.` and consistent
with the naming guidelines for RPC client spans.

<!-- prettier-ignore-start -->
<!-- semconv aws -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aws.request_id` | string | The AWS request ID as returned in the response headers `x-amz-request-id` or `x-amz-requestid`. | `79b9da39-b7ae-508a-a6bc-864b2829c622`; `C9ER4AJX75574TDJ` | Recommended |
| [`rpc.method`](../rpc/rpc-spans.md) | string | The name of the operation corresponding to the request, as returned by the AWS SDK [1] | `GetItem`; `PutItem` | Recommended |
| [`rpc.service`](../rpc/rpc-spans.md) | string | The name of the service to which a request is made, as returned by the AWS SDK. [2] | `DynamoDB`; `S3` | Recommended |
| [`rpc.system`](../rpc/rpc-spans.md) | string | The value `aws-api`. | `aws-api` | Required |

**[1]:** This is the logical name of the method from the RPC interface perspective, which can be different from the name of any implementing method/function. The `code.function` attribute may be used to store the latter (e.g., method actually executing the call on the server side, RPC client stub method on the client side).

**[2]:** This is the logical name of the service from the RPC interface perspective, which can be different from the name of any implementing class. The `code.namespace` attribute may be used to store the latter (despite the attribute name, it may include a class name; e.g., class with method actually executing the call on the server side, RPC client stub class on the client side).
<!-- endsemconv -->
<!-- prettier-ignore-end -->

## AWS service specific attributes

The following Semantic Conventions extend the general AWS SDK attributes for specific AWS services:

- [AWS DynamoDB](/docs/database/dynamodb.md): Semantic Conventions for _AWS DynamoDB_.
- [AWS S3](/docs/object-stores/s3.md): Semantic Conventions for _AWS S3_.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
