# AWS EKS

**Status**: [Experimental][DocumentStatus]

**type:** `aws.eks`

**Description:** Resources used by AWS Elastic Kubernetes Service (EKS).

<!-- semconv aws.eks -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.eks.cluster.arn`](../../../attributes-registry/aws.md) | string | The ARN of an EKS cluster. | `arn:aws:ecs:us-west-2:123456789123:cluster/my-cluster` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
