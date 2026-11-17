<!--- Hugo front matter used to generate the website version of this page:
linkTitle: EKS
--->

# AWS EKS

**Status**: [Development][DocumentStatus]

An AWS Elastic Kubernetes Service (EKS) cluster is represented by the
[`k8s.cluster`](/docs/registry/entities/k8s.md#k8s-cluster) entity.

Its ARN MAY be reported using the
[`aws.eks.cluster.arn`](/docs/registry/attributes/aws.md#aws-eks-cluster-arn) resource attribute.

<!-- TODO: https://github.com/open-telemetry/semantic-conventions/issues/4303 - decide if aws.eks.cluster.arn is modeled as cloud.resource_id or needs an individual entity -->

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status/
