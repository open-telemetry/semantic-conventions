<!--- Hugo front matter used to generate the website version of this page:
--->

# URL

These attributes may be used for any url related operation.

## URL Attributes

<!-- semconv registry.url(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `url.fragment` | string | The [URI fragment](https://www.rfc-editor.org/rfc/rfc3986#section-3.5) component | `SemConv` |
| `url.full` | string | Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [1] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `//localhost` |
| `url.path` | string | The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component [2] | `/search` |
| `url.query` | string | The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [3] | `q=OpenTelemetry` |
| `url.scheme` | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `https`; `ftp`; `telnet` |

**[1]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password should be redacted and attribute's value should be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed) and SHOULD NOT be validated or modified except for sanitizing purposes.

**[2]:** When missing, the value is assumed to be `/`

**[3]:** Sensitive content provided in query string SHOULD be scrubbed when instrumentations can identify it.
<!-- endsemconv -->