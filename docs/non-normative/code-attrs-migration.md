<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Code attributes migration
--->

# Code attributes semantic convention stability migration guide

The experimental `code.*` semantic conventions were promoted to stable in
[v1.33.0](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.33.0).
This guide outlines the breaking changes and offers migration guidance for
instrumentations and telemetry backends adopting the stable attributes.

Instrumentation authors MAY use the standard `OTEL_SEMCONV_STABILITY_OPT_IN`
migration approach. When used, it should support the `code` and `code/dup`
values.

## Summary of changes

This section summarizes the changes made to the code attribute semantic
conventions from
[v1.29.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.29.0/docs/attributes-registry/code.md)
to
[v1.33.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.33.0/docs/attributes-registry/code.md).

<!-- prettier-ignore-start -->
| Change                                    | Comments                                      |
| ----------------------------------------- | --------------------------------------------- |
| `code.lineno` &rarr; `code.line.number`   |                                               |
| `code.column` &rarr; `code.column.number` |                                               |
| `code.filepath` &rarr; `code.file.path`   |                                               |
| `code.namespace`                          | Removed, integrated into `code.function.name` |
| `code.function`                           | Removed, integrated into `code.function.name` |
| New: `code.function.name`                 | See definition and examples below             |
<!-- prettier-ignore-end -->

`code.function.name` is defined as follows:

> The method or function fully-qualified name without arguments.
> The value should fit the natural representation of the language runtime,
> which is also likely the same used within `code.stacktrace` attribute value.
>
> Examples:
>
> * Java method: `com.example.MyHttpService.serveRequest`
> * Java anonymous class method: `com.mycompany.Main$1.myMethod`
> * Java lambda method: `com.mycompany.Main$$Lambda/0x0000748ae4149c00.myMethod`
> * PHP function: `GuzzleHttp\Client::transfer`
> * Go function: `github.com/my/repo/pkg.foo.func5`
> * Elixir: `OpenTelemetry.Ctx.new`
> * Erlang: `opentelemetry_ctx:new`
> * Rust: `playground::my_module::my_cool_func`
> * C function: `fopen`
