<!--- Hugo front matter used to generate the website version of this page:
--->

# OpenTelemetry

## General Attributes

<!-- semconv registry.otel(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `otel.status_code` | string | Name of the code, either "OK" or "ERROR". MUST NOT be set if the status code is UNSET. | `OK` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `otel.status_description` | string | Description of the Status if it has a value, otherwise not set. | `resource not found` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`otel.status_code` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `OK` | The operation has been validated by an Application developer or Operator to have completed successfully. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `ERROR` | The operation contains an error. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

## Scope Attributes

<!-- semconv registry.otel.scope(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `otel.scope.name` | string | The name of the instrumentation scope - (`InstrumentationScope.Name` in OTLP). | `io.opentelemetry.contrib.mongodb` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `otel.scope.version` | string | The version of the instrumentation scope - (`InstrumentationScope.Version` in OTLP). | `1.0.0` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

## Deprecated OpenTelemetry Attributes

<!-- semconv registry.otel.library(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `otel.library.name` | string | None | `io.opentelemetry.contrib.mongodb` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>use the `otel.scope.name` attribute. |
| `otel.library.version` | string | None | `1.0.0` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>use the `otel.scope.version` attribute. |
<!-- endsemconv -->