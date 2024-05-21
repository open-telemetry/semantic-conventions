<!--- Hugo front matter used to generate the website version of this page:
linkTitle: AWS
path_base_for_github_subdir:
  from: tmp/semconv/docs/resource/cloud-provider/aws/_index.md
  to: resource/cloud-provider/aws/README.md
--->

# AWS Semantic Conventions

**Status**: [Experimental][DocumentStatus]

This directory defines standards for resource attributes that only apply to Amazon
Web Services (AWS) resources. If an attribute could apply to resources from more than one cloud
provider (like account ID, operating system, etc), it belongs in the parent
`model` directory.

## Generic AWS Attributes

Attributes that relate to AWS or use AWS-specific terminology, but are used by several
services within AWS or are abstracted away from any particular service:

- [AWS Logs](./logs.md)

## Services

Attributes that relate to an individual AWS service:

- [Elastic Container Service (ECS)](./ecs.md)
- [Elastic Kubernetes Service (EKS)](./eks.md)

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.33.0/specification/document-status.md
