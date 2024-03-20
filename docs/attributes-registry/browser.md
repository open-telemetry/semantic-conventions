<!--- Hugo front matter used to generate the website version of this page:
--->

# Browser

## Browser Attributes

<!-- semconv registry.browser(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `browser.brands` | string[] | Array of brand name and version separated by a space [1] | `[ Not A;Brand 99, Chromium 99, Chrome 99]` |
| `browser.language` | string | Preferred language of the user using the browser [2] | `en`; `en-US`; `fr`; `fr-FR` |
| `browser.mobile` | boolean | A boolean that is true if the browser is running on a mobile device [3] |  |
| `browser.platform` | string | The platform on which the browser is running [4] | `Windows`; `macOS`; `Android` |

**[1]:** This value is intended to be taken from the [UA client hints API](https://wicg.github.io/ua-client-hints/#interface) (`navigator.userAgentData.brands`).

**[2]:** This value is intended to be taken from the Navigator API `navigator.language`.

**[3]:** This value is intended to be taken from the [UA client hints API](https://wicg.github.io/ua-client-hints/#interface) (`navigator.userAgentData.mobile`). If unavailable, this attribute SHOULD be left unset.

**[4]:** This value is intended to be taken from the [UA client hints API](https://wicg.github.io/ua-client-hints/#interface) (`navigator.userAgentData.platform`). If unavailable, the legacy `navigator.platform` API SHOULD NOT be used instead and this attribute SHOULD be left unset in order for the values to be consistent.
The list of possible values is defined in the [W3C User-Agent Client Hints specification](https://wicg.github.io/ua-client-hints/#sec-ch-ua-platform). Note that some (but not all) of these values can overlap with values in the [`os.type` and `os.name` attributes](./os.md). However, for consistency, the values in the `browser.platform` attribute should capture the exact value that the user agent provides.
<!-- endsemconv -->
