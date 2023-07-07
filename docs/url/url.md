<!--- Hugo front matter used to generate the website version of this page:
linkTitle: URL
--->

# Semantic Conventions for URL

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions that describe URL and its components.

<details>
<summary>Table of Contents</summary>

<!-- toc -->

- [Attributes](#attributes)
- [Sensitive information](#sensitive-information)

<!-- tocstop -->

</details>

## Attributes

<!-- semconv url -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `url.scheme` | string | The [URI scheme](https://www.rfc-editor.org/rfc/rfc3986#section-3.1) component identifying the used protocol. | `https`; `ftp`; `telnet` | Recommended |
| `url.full` | string | Absolute URL describing a network resource according to [RFC3986](https://www.rfc-editor.org/rfc/rfc3986) [1] | `https://www.foo.bar/search?q=OpenTelemetry#SemConv`; `//localhost` | Recommended |
| `url.path` | string | The [URI path](https://www.rfc-editor.org/rfc/rfc3986#section-3.3) component [2] | `/search` | Recommended |
| `url.query` | string | The [URI query](https://www.rfc-editor.org/rfc/rfc3986#section-3.4) component [3] | `q=OpenTelemetry` | Recommended |
| `url.fragment` | string | The [URI fragment](https://www.rfc-editor.org/rfc/rfc3986#section-3.5) component | `SemConv` | Recommended |
| `url.registered_domain` | string | The highest registered url domain, stripped of the subdomain.
For example, the registered domain for "foo.example.com" is "example.com".
This value can be determined precisely with a list like the public suffix list (`http://publicsuffix.org`). Trying to approximate this by simply taking the last two labels will not work well for TLDs such as "co.uk". | `example.com` | Opt-In |
| `url.subdomain` | string | The subdomain portion of a fully qualified domain name includes all of the names except the host name under the registered_domain. In a partially qualified domain, or if the the qualification level of the full name cannot be determined, subdomain contains all of the names below the registered domain.
For example the subdomain portion of `www.east.mydomain.co.uk` is "east". If the domain has multiple levels of subdomain, such as `sub2.sub1.example.com`, the subdomain field should contain "sub2.sub1", with no trailing period. | `east` | Opt-In |
| `url.top_level_domain` | string | The effective top level domain (eTLD), also known as the domain suffix, is the last part of the domain name. For example, the top level domain for example.com is "com".
This value can be determined precisely with a list like the public suffix list (`http://publicsuffix.org`). Trying to approximate this by simply taking the last label will not work well for effective TLDs such as `co.uk`. | `co.uk` | Opt-In |
| `url.username` | string | Username of the request. | `user42` | Opt-In |
| `url.password` | string | Password of the request. | `changeme` | Opt-In |
| `url.extension` | string | The field contains the file extension from the original request url, excluding the leading dot.
The file extension is only set if it exists, as not every url has a file extension.
The leading period must not be included. For example, the value must be "png", not ".png".
Note that when the file name has multiple extensions (example.tar.gz), only the last one should be captured ("gz", not "tar.gz"). | `png` | Opt-In |
| `url.domain` | string | Domain of the url, such as `www.opentelemetry.io`.
In some cases a URL may refer to an IP and/or port directly, without a domain name. In this case, the IP address would go to the domain field.
If the URL contains a literal IPv6 address enclosed by [ and ] (IETF RFC 2732), the [ and ] characters should also be captured in the domain field. | `www.opentelemetry.io` | Opt-In |
| `url.port` | int | Port of the request | `9090` | Opt-In |
| `url.original` | string | Unmodified original URL as seen in the event source.
Note that in network monitoring, the observed URL may be a full URL, whereas in access logs, the URL is often just represented as a path.
This field is meant to represent the URL as it was observed, complete or not. | `https://www.opentelemetry.io/search/?q=container` | Opt-In |

**[1]:** For network calls, URL usually has `scheme://host[:port][path][?query][#fragment]` format, where the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless.
`url.full` MUST NOT contain credentials passed via URL in form of `https://username:password@www.example.com/`. In such case username and password should be redacted and attribute's value should be `https://REDACTED:REDACTED@www.example.com/`.
`url.full` SHOULD capture the absolute URL when it is available (or can be reconstructed) and SHOULD NOT be validated or modified except for sanitizing purposes.

**[2]:** When missing, the value is assumed to be `/`

**[3]:** Sensitive content provided in query string SHOULD be scrubbed when instrumentations can identify it.
<!-- endsemconv -->

## Sensitive information

Capturing URL and its components MAY impose security risk. User and password information, when they are provided in [User Information](https://datatracker.ietf.org/doc/html/rfc3986#section-3.2.1) subcomponent, MUST NOT be recorded.

Instrumentations that are aware of specific sensitive query string parameters MUST scrub their values before capturing `url.query` attribute. For example, native instrumentation of a client library that passes credentials or user location in URL, must scrub corresponding properties.

_Note: Applications and telemetry consumers should scrub sensitive information from URL attributes on collected telemetry. In systems unable to identify sensitive information, certain attribute values may be redacted entirely._

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
