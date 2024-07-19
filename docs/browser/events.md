# Semantic conventions for browser events

**Status**: [Experimental](../../../document-status.md)

<details>
<summary>Table of Contents</summary>
<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [PageView](#pageview)
- [PageNavigationTiming](#pagenavigationtiming)
- [ResourceTiming](#resourcetiming)
- [UserAction](#useraction)
- [WebVital](#webvital)

<!-- tocstop -->

</details>

This document describes the semantic conventions for events on browser platform. All browser events MUST use a namespace of `browser` in the `event.name` property.

## PageView

The event name MUST be `browser.page_view`.

This event describes the details of the web page visited.

The following table describes the payload fields that MUST be used to describe the details of event.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `referrer` | string | Referring Page URI (`document.referrer`) whenever available. | `https://en.wikipedia.org/wiki/Main_Page` | Recommended |
| `type` | int | Browser page type | `0` | Required |
| `title` | string | Page title DOM property | `Shopping cart page` | Recommended |
| `url` [1] | string | Full HTTP request URL in the form `scheme://host[:port]/path?query[#fragment]`. Usually the fragment is not transmitted over HTTP, but if it is known, it should be included nevertheless. [2] | `https://en.wikipedia.org/wiki/Main_Page`; `https://en.wikipedia.org/wiki/Main_Page#foo` | Required |
| `changeState` | string | Type of state change used for the virtual page navigation | `pushState`, `replaceState` | Recommended |

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`session.id`](../attributes-registry/session.md) | string | A unique id to identify a session. | `00112233-4455-6677-8899-aabbccddeeff` | `Opt-In` |
| `browser.page.instance_id` | string | A unique id that identifies the instance of the page where the event is emitted. | `e611e02f-c9d2-47b3-a678-df1465e0f401` | `Opt-In` |

**[1]:** Alias for [`http.url`](../../../trace/semantic_conventions/http.md)
**[2]:** The URL fragment may be included for virtual pages

`type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.:

| Value  | Description |
|---|---|
| `0` | physical_page - Initial page load within the browser and will generally also precede a PageNavigationTiming event.|
| `1` | virtual_page - This is for Single Page Applications (SPA) where the framework provides the ability to perform client side only page "navigation", the exact definition of what a virtual page change is determined by the SPA and the framework it is using.|

## PageNavigationTiming

The event name MUST be `browser.page_navigation_timing`.

This event describes the timing metrics of a page navigation as provided by
[PerformanceNavigationTiming](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceNavigationTiming) Performance API.

The following table describes the payload fields that MUST be used to describe the details of event.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| name | string | URL of the page || Recommended |
| fetchStart | long | || Recommended |
| unloadEventStart | long | || Recommended |
| unloadEventEnd | long | || Recommended |
| domInteractive | long | || Recommended |
| domContentLoadedEventStart | long | || Recommended |
| domContentLoadedEventEnd | long | || Recommended |
| domComplete | long | || Recommended |
| loadEventStart | long | || Recommended |
| loadEventEnd | long | || Recommended |
| firstPaint | long | || Recommended |
| firstContentfulPaint | long | || Recommended |

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`session.id`](../attributes-registry/session.md) | string | A unique id to identify a session. | `00112233-4455-6677-8899-aabbccddeeff` | `Opt-In` |
| `browser.page.instance_id` | string | A unique id that identifies the instance of the page where the event is emitted. | `e611e02f-c9d2-47b3-a678-df1465e0f401` | `Opt-In` |

## ResourceTiming

The event name MUST be `browser.resource_timing`.

This event describes the timing metrics as provided by [PerformanceResourceTiming](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceResourceTiming)
Performance API.  These metrics are related to fetching a resource, such as
XMLHttpRequest, Fetch, sendBeacon APIs, SVG, image or script.

The following table describes the payload fields that MUST be used to describe the details of event.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `connectEnd` | long | Time when the browser finishes establishing the connection to the server. | | Recommended |
| `connectStart` | long | Time when the browser starts establishing the connection to the server. | | Recommended |
| `decodedBodySize` | long | Size of the response body after it has been decoded. | | Recommended |
| `deliveryType` | string | Type of delivery for the resource, for eg., 'cache'. | | Recommended |
| `domainLookupEnd` | long | Time when the domain name lookup is finished. | | Recommended |
| `domainLookupStart` | long | Time when the domain name lookup starts. | | Recommended |
| `encodedBodySize` | long | Size of the response body as it is received from the server. | | Recommended |
| `fetchStart` | long | Time when the browser starts fetching the resource. | | Recommended |
| `initiatorType` | string | Type of resource that initiated the request. | | Recommended |
| `name` | string | URL of the resource. | | Recommended |
| `redirectEnd` | long | Time when the last redirect is completed. | | Recommended |
| `redirectStart` | long | Time when the first redirect starts. | | Recommended |
| `requestStart` | long | Time when the browser starts requesting the resource. | | Recommended |
| `responseEnd` | long | Time when the browser finishes receiving the response. | | Recommended |
| `responseStart` | long | Time when the browser starts receiving the response. | | Recommended |
| `responseStatus` | string | HTTP response status code. | | Recommended |
| `secureConnectionStart` | long | Time when the secure connection starts. | | Recommended |
| `transferSize` | string | Size of the resource transferred over the network. | | Recommended |

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`session.id`](../attributes-registry/session.md) | string | A unique id to identify a session. | `00112233-4455-6677-8899-aabbccddeeff` | `Opt-In` |
| `browser.page.instance_id` | string | A unique id that identifies the instance of the page where the event is emitted. | `e611e02f-c9d2-47b3-a678-df1465e0f401` | `Opt-In` |

## UserAction

The event name MUST be `browser.user_action`.

This event describes actions performed by the user such as click, scroll, zoom, resize, etc.

The following table describes the payload fields that MUST be used to describe the details of event.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `element` | string | Target element tag name (obtained via `event.target.tagName`) | `button` | Recommended |
| `element_xpath` | string | Target element xpath | `//*[@id="testBtn"]` | Recommended |
| `user_action_type` | string | Type of interaction. See enum [here](https://github.com/microsoft/ApplicationInsights-JS/blob/941ec2e4dbd017b8450f2b17c60088ead1e6c428/extensions/applicationinsights-clickanalytics-js/src/Enums.ts) for potential values we could add support for. | `click` | Required |
| `click_coordinates` | string | Click coordinates captured as a string in the format {x}X{y}.  Eg. 345X23 | `345X23` | Recommended |
| `tag.<key>` | string[] | Grab data from data-otel-* attributes in tree | `[data-otel-xyz="value" -> tag.xyz=["value"]` | Recommended |

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`session.id`](../attributes-registry/session.md) | string | A unique id to identify a session. | `00112233-4455-6677-8899-aabbccddeeff` | `Opt-In` |
| `browser.page.instance_id` | string | A unique id that identifies the instance of the page where the event is emitted. | `e611e02f-c9d2-47b3-a678-df1465e0f401` | `Opt-In` |

`user_action_type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.:

| Value  | Description |
|---|---|
| `click` | click |

## WebVital

The event name MUST be `browser.web_vital`.

This event describes the website performance metrics introduced by Google (See <https://web.dev/vitals/>).

The following table describes the payload fields that MUST be used to describe the details of event. Please refer to web-vitals library [documentation](https://github.com/GoogleChrome/web-vitals?tab=readme-ov-file#metric) for more detailed description of these fields.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `name` | string | name of the web vital metric | `CLS`, `FCP` | Required |
| `value` | double | value of the web vital | `1.0`; `2.0` | Required |
| `delta` | double | The delta between the current value and the last-reported value | `0.2` | Required |
| `id` | string | A unique ID representing this particular metric instance | "v3-1677874579383-6381583661209" | Required |
| `rating` | string | The rating of the metric | `good`, `needs-improvement`, `poor` | Recommended |
| `navigationType` | string | The type of navigation | | Recommended |
| `debug_taget` | string | The debug target when [sending attribution data](https://github.com/GoogleChrome/web-vitals?tab=readme-ov-file#send-attribution-data). | | 'Opt-In' |


| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| [`session.id`](../attributes-registry/session.md) | string | A unique id to identify a session. | `00112233-4455-6677-8899-aabbccddeeff` | `Opt-In` |
| `browser.page.instance_id` | string | A unique id that identifies the instance of the page where the event is emitted. | `e611e02f-c9d2-47b3-a678-df1465e0f401` | `Opt-In` |

`name` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `CLS` | Cumulative Layout Shift |
| `LCP` | Largest Contentful Paint |
| `FID` | First Input Delay |
| `INP` | Interation to Next Paint |
