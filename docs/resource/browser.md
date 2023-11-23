# Browser

**Status**: [Experimental][DocumentStatus]

**type:** `browser`

**Description**: The web browser in which the application represented by the resource is running. The `browser.*` attributes MUST be used only for resources that represent applications running in a web browser (regardless of whether running on a mobile or desktop device).

All of these attributes can be provided by the user agent itself in the form of an HTTP header (e.g. Sec-CH-UA, Sec-CH-Platform, User-Agent). However, the headers could be removed by proxy servers, and are tied to calls from individual clients. In order to support batching through services like the Collector and to prevent loss of data (e.g. due to proxy servers removing headers), these attributes should be used when possible.

<!-- semconv browser -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `browser.brands` | string[] | Array of brand name and version separated by a space [1] | `[ Not A;Brand 99, Chromium 99, Chrome 99]` | Recommended |
| `browser.instance.id` | string | Represents a browser instance, either a window or a tab | `ec34d777-1daf-416b-98b0-05beddfaa199` | Recommended |
| `browser.language` | string | Preferred language of the user using the browser [2] | `en`; `en-US`; `fr`; `fr-FR` | Recommended |
| `browser.mobile` | boolean | A boolean that is true if the browser is running on a mobile device [3] |  | Recommended |
| `browser.page.instance.id` | string | Represents an instance of a page in the browser [4] | `4e58989a-4e4d-4f62-bf4f-ac5cd49b4b9a` | Recommended |
| `browser.page.url` | string | Full URL of a page [5] | `https://www.netflix.com/Login` | Recommended |
| `browser.platform` | string | The platform on which the browser is running [6] | `Windows`; `macOS`; `Android` | Recommended |
| [`user_agent.original`](../attributes-registry/user-agent.md) | string | Full user-agent string provided by the browser [7] | `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36` | Recommended |

**[1]:** This value is intended to be taken from the [UA client hints API](https://wicg.github.io/ua-client-hints/#interface) (`navigator.userAgentData.brands`).

**[2]:** This value is intended to be taken from the Navigator API `navigator.language`.

**[3]:** This value is intended to be taken from the [UA client hints API](https://wicg.github.io/ua-client-hints/#interface) (`navigator.userAgentData.mobile`). If unavailable, this attribute SHOULD be left unset.

**[4]:** The same page when visited at a different time represents a new instance and should get a new id.

**[5]:** Represents the url of the current page in the browser.

**[6]:** This value is intended to be taken from the [UA client hints API](https://wicg.github.io/ua-client-hints/#interface) (`navigator.userAgentData.platform`). If unavailable, the legacy `navigator.platform` API SHOULD NOT be used instead and this attribute SHOULD be left unset in order for the values to be consistent.
The list of possible values is defined in the [W3C User-Agent Client Hints specification](https://wicg.github.io/ua-client-hints/#sec-ch-ua-platform). Note that some (but not all) of these values can overlap with values in the [`os.type` and `os.name` attributes](./os.md). However, for consistency, the values in the `browser.platform` attribute should capture the exact value that the user agent provides.

**[7]:** The user-agent value SHOULD be provided only from browsers that do not have a mechanism to retrieve brands and platform individually from the User-Agent Client Hints API. To retrieve the value, the legacy `navigator.userAgent` API can be used.
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
