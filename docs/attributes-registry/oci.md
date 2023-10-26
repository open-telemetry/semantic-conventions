## Open Container Initiative (OCI)

The [Open Container Initiative](https://opencontainers.org/) defines open industry standards around container formats and runtimes.

### OCI Image Manifest

<!-- semconv registry.oci.manifest(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `oci.manifest.digest` | string | The digest of the OCI image manifest. For container images specifically is the digest by which the container image is known. [1] | `sha256:e4ca62c0d62f3e886e684806dfe9d4e0cda60d54986898173c1083856cfda0f4` |

**[1]:** Follows [OCI Image Manifest Specification](https://github.com/opencontainers/image-spec/blob/main/manifest.md), and specifically the [Digest property](https://github.com/opencontainers/image-spec/blob/main/descriptor.md#digests).
An example can be found in [Example Image Manifest](https://docs.docker.com/registry/spec/manifest-v2-2/#example-image-manifest).
<!-- endsemconv -->