<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Client
--->

# Connection

These attributes may be used to describe the socket connection.

<!-- semconv connection(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `connection.state` | string | State of the connection in the connection pool. | `active` |

`connection.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `active` | Connection is being used. |
| `idle` | Connection idle |
<!-- endsemconv -->