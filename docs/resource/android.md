# Android

**Status**: [Experimental][DocumentStatus]

**type:** `android`

**Description**: The Android platform on which the Android application is running.

<!-- semconv android -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `android.os.api_level` | string | Uniquely identifies the framework API revision offered by a version (`os.version`) of the android operating system. More information can be found [here](https://developer.android.com/guide/topics/manifest/uses-sdk-element#ApiLevels). | `33`; `32` | Recommended |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
