<!--- Hugo front matter used to generate the website version of this page:
linkTitle: GCP
path_base_for_github_subdir:
  from: content/en/docs/specs/semconv/resource/cloud_provider/gcp/_index.md
  to: resource/cloud_provider/gcp/README.md
--->

# GCP Semantic Conventions

**Status**: [Experimental][DocumentStatus]

This directory defines standards for resource attributes that only apply to
Google Cloud Platform (GCP). If an attribute could apply to resources from more than one cloud
provider (like account ID, operating system, etc), it belongs in the parent
`semantic_conventions` directory.

## Services

- [Cloud Run](./cloud-run.md)
- [Compute Engine](./gce.md)

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
