# ASP.NET Core

<!-- toc -->

- [ASP.NET Core Attributes](#aspnet-core-attributes

<!-- tocstop -->

## ASP.NET Core Attributes

<!-- semconv registry.aspnetcore(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `aspnetcore.rate_limiting.result` | string | Rate-limiting result, shows whether the lease was acquired or contains a rejection reason | `acquired`; `request_canceled` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `aspnetcore.diagnostics.handler.type` | string | Full type name of the [`IExceptionHandler`](https://learn.microsoft.com/dotnet/api/microsoft.aspnetcore.diagnostics.iexceptionhandler) implementation that handled the exception. | `Contoso.MyHandler` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `aspnetcore.diagnostics.exception.result` | string | ASP.NET Core exception middleware handling result | `handled`; `unhandled` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `aspnetcore.rate_limiting.policy` | string | Rate limiting policy name. | `fixed`; `sliding`; `token` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `aspnetcore.request.is_unhandled` | boolean | Flag indicating if request was handled by the application pipeline. | `True` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `aspnetcore.routing.is_fallback` | boolean | A value that indicates whether the matched route is a fallback route. | `True` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `aspnetcore.routing.match_status` | string | Match result - success or failure | `success`; `failure` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`aspnetcore.rate_limiting.result` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `acquired` | Lease was acquired | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `endpoint_limiter` | Lease request was rejected by the endpoint limiter | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `global_limiter` | Lease request was rejected by the global limiter | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `request_canceled` | Lease request was canceled | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`aspnetcore.diagnostics.exception.result` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `handled` | Exception was handled by the exception handling middleware. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `unhandled` | Exception was not handled by the exception handling middleware. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `skipped` | Exception handling was skipped because the response had started. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `aborted` | Exception handling didn't run because the request was aborted. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

`aspnetcore.routing.match_status` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `success` | Match succeeded | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `failure` | Match failed | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
<!-- endsemconv -->