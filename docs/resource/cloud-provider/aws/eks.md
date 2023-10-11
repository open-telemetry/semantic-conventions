# AWS EKS

**Status**: [Experimental][DocumentStatus]

**type:** `aws.eks`

**Description:** Resources used by AWS Elastic Kubernetes Service (EKS).

<!-- semconv aws.eks -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aws.eks.cluster.arn` | string | The ARN of an EKS cluster. | `arn:aws:ecs:us-west-2:123456789123:cluster/my-cluster` | Recommended |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
