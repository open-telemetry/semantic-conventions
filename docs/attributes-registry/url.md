<!--- Hugo front matter used to generate the website version of this page:
linkTitle: URL
--->
# URL

## URL Attributes

<!-- semconv registry.url(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `url.fragment` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The [URI fragment](https://www.rfc-editor.org/rfc/rfc3986#section-3.5) component | `SemConv` |
| `url.full` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [1] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `//localhost` |
| `url.path` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component | `/search` |
| `url.query` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [2] | `q=OpenTelemetry` |
| `url.scheme` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `https`; `ftp`; `telnet` |

**[1]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it SHOULD be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password SHOULD be redacted and attribute's value SHOULD be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed) and SHOULD NOT be validated or modified except for sanitizing purposes.

**[2]:** Sensitive content provided in query string SHOULD be scrubbed when instrumentations can identify it.
<!-- endsemconv -->