<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Azure
--->

# Azure semantic conventions

**Status**: [Development][DocumentStatus]

This directory defines standards for resource attributes that only apply to
Azure resources. If an attribute could apply to resources from more than one
cloud provider (like account ID, operating system, etc), it belongs in the
parent `model` directory.

## Services

Attributes that relate to an individual Azure service:

- [Container Apps](./container-apps.md)

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
