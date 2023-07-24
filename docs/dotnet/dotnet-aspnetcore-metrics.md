# Semantic Conventions for ASP.NET Core metrics

**Status**: [Experimental, Feature-freeze][DocumentStatus]

This document defines semantic conventions for ASP.NET Core metrics.

<!-- toc -->

- [Server](#server)
- [Routing](#routing)
  * [Metric: `aspnetcore.routing.match_attempts`](#metric-aspnetcoreroutingmatch_attempts)
- [Exception metrics](#exception-metrics)
  * [Metric: `aspnetcore.diagnostics.exceptions`](#metric-aspnetcorediagnosticsexceptions)
- [Rate-limiting](#rate-limiting)
  * [Metric: `aspnetcore.rate_limiting.active_request_leases`](#metric-aspnetcorerate_limitingactive_request_leases)
  * [Metric: `aspnetcore.rate_limiting.request_lease.duration`](#metric-aspnetcorerate_limitingrequest_leaseduration)
  * [Metric: `aspnetcore.rate_limiting.queued_requests`](#metric-aspnetcorerate_limitingqueued_requests)
  * [Metric: `aspnetcore.rate_limiting.request.time_in_queue`](#metric-aspnetcorerate_limitingrequesttime_in_queue)
  * [Metric: `aspnetcore.rate_limiting.requests`](#metric-aspnetcorerate_limitingrequests)

<!-- tocstop -->

## Server

## Routing

All routing metrics are reported by `Microsoft.AspNetCore.Routing` meter.

### Metric: `aspnetcore.routing.match_attempts`

<!-- semconv metric.aspnetcore.routing.match_attempts(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `aspnetcore.routing.match_attempts` | Counter | `{match_attempt}` | Number of requests that were attempted to be matched to an endpoint. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Routing`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.aspnetcore.routing.match_attempts(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aspnetcore.routing.match_status` | string | Match result - success or failure | `success`; `failure` | Required |
| `aspnetcore.routing.is_fallback_route` | boolean | A value that indicates whether the matched route is a fallback route. | `True` | Conditionally Required: if and only if a route was successfully matched. |
| `http.route` | string | The matched route (path template in the format used by the respective server framework). See note below [1] | `/users/:userID?`; `{controller}/{action}/{id?}` | Conditionally Required: if and only if a route was successfully matched. |

**[1]:** MUST NOT be populated when this is not supported by the HTTP server framework as the route attribute should have low-cardinality and the URI path can NOT substitute it.
SHOULD include the [application root](/docs/http/http-spans.md#http-server-definitions) if there is one.

`aspnetcore.routing.match_status` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `success` | Match succeeded |
| `failure` | Match failed |
<!-- endsemconv -->

## Exception metrics

Metrics reported by `Microsoft.AspNetCore.Diagnostics` meter.

### Metric: `aspnetcore.diagnostics.exceptions`

<!-- semconv metric.aspnetcore.diagnostics.exceptions(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `aspnetcore.diagnostics.exceptions` | Counter | `{exception}` | Number of exceptions caught by exception handling middleware. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.Diagnostics`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.aspnetcore.diagnostics.exceptions(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aspnetcore.diagnostics.exception.result` | string | ASP.NET Core exception middleware handling result | `handled`; `unhandled` | Required |
| `aspnetcore.diagnostics.handler.type` | string | Full type name of the [`IExceptionHandler`](https://learn.microsoft.com/dotnet/api/microsoft.aspnetcore.diagnostics.iexceptionhandler) implementation that handled the exception. | `Contoso.MyHandler` | Conditionally Required: [1] |
| `exception.type` | string | The full name of exception type. | `System.OperationCanceledException`; `Contoso.MyException` | Required |

**[1]:** if and only if the exception was handled by this handler.

`aspnetcore.diagnostics.exception.result` MUST be one of the following:

| Value  | Description |
|---|---|
| `handled` | Exception was handled by the exception handling middleware. |
| `unhandled` | Exception was not handled by the exception handling middleware. |
| `skipped` | Exception handling was skipped because the response had started. |
| `aborted` | Exception handling didn't run because the request was aborted. |
<!-- endsemconv -->

## Rate-limiting

All rate-limiting metrics are reported by `Microsoft.AspNetCore.RateLimiting` meter.

### Metric: `aspnetcore.rate_limiting.active_request_leases`

<!-- semconv metric.aspnetcore.rate_limiting.active_request_leases(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `aspnetcore.rate_limiting.active_request_leases` | UpDownCounter | `{request}` | Number of requests that are currently active on the server that hold a rate limiting lease. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.RateLimiting`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.aspnetcore.rate_limiting.active_request_leases(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aspnetcore.rate_limiting.policy` | string | Rate limiting policy name. | `fixed`; `sliding`; `token` | Conditionally Required: [1] |

**[1]:** if the matched endpoint for the request had a rate-limiting policy.
<!-- endsemconv -->

### Metric: `aspnetcore.rate_limiting.request_lease.duration`

<!-- semconv metric.aspnetcore.rate_limiting.request_lease.duration(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `aspnetcore.rate_limiting.request_lease.duration` | Histogram | `s` | The duration of rate limiting lease held by requests on the server. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.RateLimiting`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.aspnetcore.rate_limiting.request_lease.duration(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aspnetcore.rate_limiting.policy` | string | Rate limiting policy name. | `fixed`; `sliding`; `token` | Conditionally Required: [1] |

**[1]:** if the matched endpoint for the request had a rate-limiting policy.
<!-- endsemconv -->

### Metric: `aspnetcore.rate_limiting.queued_requests`

<!-- semconv metric.aspnetcore.rate_limiting.queued_requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `aspnetcore.rate_limiting.queued_requests` | UpDownCounter | `{request}` | Number of requests that are currently queued, waiting to acquire a rate limiting lease. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.RateLimiting`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.aspnetcore.rate_limiting.queued_requests(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aspnetcore.rate_limiting.policy` | string | Rate limiting policy name. | `fixed`; `sliding`; `token` | Conditionally Required: [1] |

**[1]:** if the matched endpoint for the request had a rate-limiting policy.
<!-- endsemconv -->

### Metric: `aspnetcore.rate_limiting.request.time_in_queue`

<!-- semconv metric.aspnetcore.rate_limiting.request.time_in_queue(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `aspnetcore.rate_limiting.request.time_in_queue` | Histogram | `s` | The time request spent in a queue, waiting to acquire a rate limiting lease. [1] |

**[1]:** Meter name: `Microsoft.AspNetCore.RateLimiting`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.aspnetcore.rate_limiting.request.time_in_queue(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aspnetcore.rate_limiting.policy` | string | Rate limiting policy name. | `fixed`; `sliding`; `token` | Conditionally Required: [1] |
| `aspnetcore.rate_limiting.result` | string | Rate-limiting result, shows whether lease was acquired or contains rejection reason | `acquired`; `request_canceled` | Required |

**[1]:** if the matched endpoint for the request had a rate-limiting policy.

`aspnetcore.rate_limiting.result` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `acquired` | Lease was acquired |
| `endpoint_limiter` | Lease request was rejected by the endpoint limiter |
| `global_limiter` | Lease request was rejected by the global limiter |
| `request_canceled` | Lease request was canceled |
<!-- endsemconv -->

### Metric: `aspnetcore.rate_limiting.requests`

<!-- semconv metric.aspnetcore.rate_limiting.requests(metric_table) -->
| Name     | Instrument Type | Unit (UCUM) | Description    |
| -------- | --------------- | ----------- | -------------- |
| `aspnetcore.rate_limiting.requests` | Counter | `{request}` | Number of requests that tried to acquire a rate limiting lease. [1] |

**[1]:** Requests could be rejected by global or endpoint rate limiting policies. Or the request could be cancelled while waiting for the lease.

Meter name: `Microsoft.AspNetCore.RateLimiting`; Added in: ASP.NET Core 8.0
<!-- endsemconv -->

<!-- semconv metric.aspnetcore.rate_limiting.requests(full) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aspnetcore.rate_limiting.policy` | string | Rate limiting policy name. | `fixed`; `sliding`; `token` | Conditionally Required: [1] |
| `aspnetcore.rate_limiting.result` | string | Rate-limiting result, shows whether lease was acquired or contains rejection reason | `acquired`; `request_canceled` | Required |

**[1]:** if the matched endpoint for the request had a rate-limiting policy.

`aspnetcore.rate_limiting.result` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `acquired` | Lease was acquired |
| `endpoint_limiter` | Lease request was rejected by the endpoint limiter |
| `global_limiter` | Lease request was rejected by the global limiter |
| `request_canceled` | Lease request was canceled |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
