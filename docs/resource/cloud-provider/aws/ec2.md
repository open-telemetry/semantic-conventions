# AWS EC2

**Status**: [Experimental][DocumentStatus]

**type:** `aws.ec2`

**Description:** Resources used by Amazon Elastic Compute Cloud (Amazon EC2).

<!-- semconv aws.ec2 -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aws.ec2.instance.id` | string | The instance id of an AWS EC2 instance. This is the value provided by the [EC2 Metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-categories.html) endpoint under `instance-id`. [1] | `i-1234567890abcdef0` | Recommended |

**[1]:** When both `host.id` and `aws.ec2.instance.id` are present, they SHOULD be equal.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
