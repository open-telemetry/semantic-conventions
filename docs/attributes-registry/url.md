<!--- Hugo front matter used to generate the website version of this page:
linkTitle: URL
--->

# URL

## URL Attributes

<!-- semconv registry.url(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `url.domain` | string | Domain extracted from the `url.full`, such as "opentelemetry.io". [1] | `www.foo.bar`; `opentelemetry.io`; `3.12.167.2`; `[1080:0:0:0:8:800:200C:417A]` |
| `url.extension` | string | The file extension extracted from the `url.full`, excluding the leading dot. [2] | `png`; `gz` |
| `url.fragment` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The [URI fragment](https://www.rfc-editor.org/rfc/rfc3986#section-3.5) component | `SemConv` |
| `url.full` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [3] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `//localhost` |
| `url.original` | string | Unmodified original URL as seen in the event source. [4] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `search?q=OpenTelemetry` |
| `url.path` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component | `/search` |
| `url.port` | int | Port extracted from the `url.full` | `443` |
| `url.query` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [5] | `q=OpenTelemetry` |
| `url.registered_domain` | string | The highest registered url domain, stripped of the subdomain. [6] | `example.com`; `foo.co.uk` |
| `url.scheme` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `https`; `ftp`; `telnet` |
| `url.subdomain` | string | The subdomain portion of a fully qualified domain name includes all of the names except the host name under the registered_domain. In a partially qualified domain, or if the the qualification level of the full name cannot be determined, subdomain contains all of the names below the registered domain. [7] | `east`; `sub2.sub1` |
| `url.top_level_domain` | string | The effective top level domain (eTLD), also known as the domain suffix, is the last part of the domain name. For example, the top level domain for example.com is `com`. [8] | `com`; `co.uk` |

**[1]:** In some cases a URL may refer to an IP and/or port directly, without a domain name. In this case, the IP address would go to the domain field. If the URL contains a [literal IPv6 address](https://www.rfc-editor.org/rfc/rfc2732#section-2) enclosed by `[` and `]`, the `[` and `]` characters should also be captured in the domain field.

**[2]:** The file extension is only set if it exists, as not every url has a file extension. When the file name has multiple extensions `example.tar.gz`, only the last one should be captured `gz`, not `tar.gz`.

**[3]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it SHOULD be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password SHOULD be redacted and attribute's value SHOULD be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed) and SHOULD NOT be validated or modified except for sanitizing purposes.

**[4]:** In network monitoring, the observed URL may be a full URL, whereas in access logs, the URL is often just represented as a path. This field is meant to represent the URL as it was observed, complete or not.
`url.original` might contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case password and username SHOULD NOT be redacted and attribute's value SHOULD remain the same.

**[5]:** Sensitive content provided in query string SHOULD be scrubbed when instrumentations can identify it.

**[6]:** This value can be determined precisely with the [public suffix list](http://publicsuffix.org). For example, the registered domain for `foo.example.com` is `example.com`. Trying to approximate this by simply taking the last two labels will not work well for TLDs such as `co.uk`.

**[7]:** The subdomain portion of `www.east.mydomain.co.uk` is `east`. If the domain has multiple levels of subdomain, such as `sub2.sub1.example.com`, the subdomain field should contain `sub2.sub1`, with no trailing period.

**[8]:** This value can be determined precisely with the [public suffix list](http://publicsuffix.org).
<!-- endsemconv -->