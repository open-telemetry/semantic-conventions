Semantic conventions for Nginx Ingress Controller events

**Status**: [Experimental](../../../document-status.md)

<details>
<summary>Table of Contents</summary>
<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Access](#access)
- [Error](#error)

<!-- tocstop -->

</details>

This document describes the semantic conventions for events in Nginx Ingress Controller. All Nginx Ingress Controller events MUST use a namespace of `nginx_ingress_controller` in the `event.name` property.

## Access

The event name MUST be `nginx_ingress_controller.access`.

This event describes the details of an the Nginx access.

| Body Field | Type | Description | Examples | Requirement Level |
|---|---|---|---|---|
| `http.request.id` | string | The randomly generated ID of the request | `529a007902362a5f51385a5fa7049884` | Required |
| `http.request.length` | int | The request length (including request line, header, and request body) | `89` | Recommended |
| `http.request.time` | double | Time elapsed since the first bytes were read from the client | `0.001`| Recommended |
| `remote_ip_list` | array | An array of remote IP addresses. It is a list because it is common to include, besides the client IP address, IP addresses from headers like X-Forwarded-For. Real source IP is restored to source.ip. | `["192.168.64.1"]` | Recommended |
| `upstream.alternative_name` | string | The name of the alternative upstream. |  | Recommended |
| `upstream.ip` | string | The IP address of the upstream server. If several servers were contacted during request processing, their addresses are separated by commas. | `172.17.0.5` |Recommended |
| `upstream.name` | string | The name of the upstream. | `default-web-8080` | Recommended |
| `upstream.port` | string | The port of the upstream server. | `8080` | Recommended |
| `upstream.response.length` | int | The length of the response obtained from the upstream server | `59` | Recommended |
| `response.length_list` | array | An array of upstream response lengths. It is a list because it is common that several upstream servers were contacted during request processing. |  | Recommended |
| `response.status_code` | int | The status code of the response obtained from the upstream server | `200` | Recommended |
| `status_code_list` |  array | An array of upstream response status codes. It is a list because it is common that several upstream servers were contacted during request processing. | | Recommended |
| `response.time` | int | The time spent on receiving the response from the upstream server as seconds with millisecond resolution | `0` | Recommended |
| `response.time_list` | array | An array of upstream response durations. It is a list because it is common that several upstream servers were contacted during request processing. | | Recommended |
| `upstream_address_list` |  array | An array of the upstream addresses. It is a list because it is common that several upstream servers were contacted during request processing. |  | Recommended |

# Error

The event name MUST be `nginx_ingress_controller.error`.

This event describes the details of an the error in Nginx Ingress Controller.

| Body Field | Type | Description | Examples | Requirement Level |
|---|---|---|---|---|
| `source.file` | string | Source file | `client_config.go` | Recommended |
| `source.line_number` | int | Source line number | 608 | Recommended |
| `thread_id` | int | Thread ID | 8 | Recommended |
