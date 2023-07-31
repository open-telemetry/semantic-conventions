# OCI

**Status**: [Experimental][DocumentStatus]

**type:** `oci`

**Description:** An OCI instance.

<!-- semconv oci -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `oci.manifest.digest` | string | The digest of the OCI image manifest. Follows [OCI Image Manifest Specification](https://github.com/opencontainers/image-spec/blob/main/manifest.md), and specifically the [Digest property](https://github.com/opencontainers/image-spec/blob/main/descriptor.md#digests). An example can be found in [Example Image Manifest](https://docs.docker.com/registry/spec/manifest-v2-2/#example-image-manifest). | `sha256:e4ca62c0d62f3e886e684806dfe9d4e0cda60d54986898173c1083856cfda0f4`; `sha256:3c3a4604a545cdc127456d94e421cd355bca5b528f4a9c1905b15da2eb4a4c6b` | Recommended |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
