<!--- Hugo front matter used to generate the website version of this page:
--->

# OpenTelemetry

<!-- toc -->

- [OpenTelemetry Attributes](#opentelemetry-attributes)
- [Deprecated OpenTelemetry Attributes](#deprecated-opentelemetry-attributes)

<!-- tocstop -->

## OpenTelemetry Attributes

<!-- semconv registry.otel.scope(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `otel.scope.name` | string | The name of the instrumentation scope - (`InstrumentationScope.Name` in OTLP). | `io.opentelemetry.contrib.mongodb` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `otel.scope.version` | string | The version of the instrumentation scope - (`InstrumentationScope.Version` in OTLP). | `1.0.0` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->

## Deprecated OpenTelemetry Attributes

<!-- semconv registry.otel.library.deprecated(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `otel.library.name` | string | None | `io.opentelemetry.contrib.mongodb` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>use the `otel.scope.name` attribute. |
| `otel.library.version` | string | None | `1.0.0` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>use the `otel.scope.version` attribute. |
<!-- endsemconv -->