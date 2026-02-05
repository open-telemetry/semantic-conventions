<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Spans
--->

# Semantic Conventions for DHCP Spans

**Status**: [Development][DocumentStatus]

This document defines semantic conventions for DHCP spans, covering both
client and server instrumentation.

<!-- toc -->

- [Span Name](#span-name)
- [Span Kind](#span-kind)
- [Client Spans](#client-spans)
- [Server Spans](#server-spans)
- [Span Status](#span-status)
- [Span Events](#span-events)

<!-- tocstop -->

## Span Name

DHCP span names SHOULD follow the pattern: `DHCP {message_type}`

The `{message_type}` MUST be the value of `dhcp.message.type`.

**Examples:**

- `DHCP DISCOVER`
- `DHCP OFFER`
- `DHCP SOLICIT`
- `DHCP ADVERTISE`

## Span Kind

| Role                             | Span Kind  |
| -------------------------------- | ---------- |
| DHCP client sending request      | `CLIENT`   |
| DHCP server processing request   | `SERVER`   |
| DHCP relay agent forwarding      | `INTERNAL` |

## Client Spans

Client instrumentations SHOULD create a span for each DHCP message sent.

<!-- semconv dhcp.client -->
<!-- endsemconv -->

## Server Spans

Server instrumentations SHOULD create a span for each DHCP message processed.

<!-- semconv dhcp.server -->
<!-- endsemconv -->

## Span Status

Instrumentation SHOULD set span status as follows:

| Condition                                      | Span Status                    |
| ---------------------------------------------- | ------------------------------ |
| Successful response (ACK, REPLY with success)  | Leave unset (defaults to `OK`) |
| NAK received/sent                              | `ERROR`                        |
| Timeout waiting for response                   | `ERROR`                        |
| Address declined (in use)                      | `ERROR`                        |
| Processing error                               | `ERROR`                        |

When status is `ERROR`, the `error.type` attribute SHOULD be populated.

## Span Events

The following events MAY be recorded on DHCP spans:

| Event Name               | Description                 |
| ------------------------ | --------------------------- |
| `dhcp.message.sent`      | Message transmitted         |
| `dhcp.message.received`  | Message received            |
| `dhcp.address.allocated` | Address assigned to client  |
| `dhcp.address.released`  | Address released by client  |
| `dhcp.lease.expired`     | Lease expiration detected   |

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
