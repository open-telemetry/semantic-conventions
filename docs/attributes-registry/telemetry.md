<!--- Hugo front matter used to generate the website version of this page:
--->

# Telemetry SDK

## Telemetry SDK Attributes

<!-- semconv registry.telemetry(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `telemetry.sdk.language` | string | The language of the telemetry SDK. | `cpp` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `telemetry.sdk.name` | string | The name of the telemetry SDK as defined above. [1] | `opentelemetry` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `telemetry.sdk.version` | string | The version string of the telemetry SDK. | `1.2.3` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `telemetry.distro.name` | string | The name of the auto instrumentation agent or distribution, if used. [2] | `parts-unlimited-java` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `telemetry.distro.version` | string | The version string of the auto instrumentation agent or distribution, if used. | `1.2.3` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The OpenTelemetry SDK MUST set the `telemetry.sdk.name` attribute to `opentelemetry`.
If another SDK, like a fork or a vendor-provided implementation, is used, this SDK MUST set the
`telemetry.sdk.name` attribute to the fully-qualified class or module name of this SDK's main entry point
or another suitable identifier depending on the language.
The identifier `opentelemetry` is reserved and MUST NOT be used in this case.
All custom identifiers SHOULD be stable across different versions of an implementation.

**[2]:** Official auto instrumentation agents and distributions SHOULD set the `telemetry.distro.name` attribute to
a string starting with `opentelemetry-`, e.g. `opentelemetry-java-instrumentation`.

`telemetry.sdk.language` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `cpp` | cpp | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `dotnet` | dotnet | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `erlang` | erlang | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `go` | go | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `java` | java | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `nodejs` | nodejs | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `php` | php | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `python` | python | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `ruby` | ruby | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `rust` | rust | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `swift` | swift | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `webjs` | webjs | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->
