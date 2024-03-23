# Semantic conventions for browser events

**Status**: [Experimental](../../../document-status.md)

<details>
<summary>Table of Contents</summary>
<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [Browser Events](#events)
  * [PageView](#pageview)
  * [PageNavigationTiming](#pagenavigationtiming)
  * [ResourceTiming](#resourcetiming)
  * [Exception](#exception)
  * [UserAction](#useraction)
  * [WebVital](#webvital)

<!-- tocstop -->

</details>

This document describes the semantic conventions for instrumentations that events on browser platform. All browser events MUST use a namespace of `browser` in the `event.name` property.

## Events

The events may be represented either as Span Events or Log Events.

All events have the following three high-level attributes. The event name is specified at the beginning of each section below. The payload of the event goes in an attribute called `event.data` of whose value is of type `map`. The contents of the `event.data` map for each event is listed in the sections below.

| Key  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `event.domain` | string | Fixed value: browser ||Required|
| `event.name` | string | Described in each section below||Required|
| `event.data` | map | A map of key/value pairs, with the keys for each event described in following sections||Recommended|

### PageView

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

**[1]:**  Alias for [`http.url`](../../../trace/semantic_conventions/http.md)
**[2]:** The URL fragment may be included for virtual pages

`type` MUST be one of the following:

| Value  | Description |
|---|---|
| `0` | physical_page - Initial page load within the browser and will generally also precede a PageNavigationTiming event.|
| `1` | virtual_page - This is for Single Page Applications (SPA) where the framework provides the ability to perform client side only page "navigation", the exact definition of what a virtual page change is determined by the SPA and the framework it is using.|

<details>
<summary>Sample PageView Event</summary>

```json
    "log_record": {
        "timeUnixNano":"1581452773000000789",
        "attributes": [
            {
                "key": "event.name",
                "value": {
                "stringValue": "browser.page_view"
                }
            }
        ]

        "body": {
                "kvlistValue": [
                    {
                        "key": "type",
                        "value": {
                        "intValue": "0"
                        }
                    },
                    {
                        "key": "url",
                        "value": {
                        "stringValue": "https://www.guidgenerator.com/online-guid-generator.aspx"
                        }
                    },
                    {
                        "key": "referrer",
                        "value": {
                        "stringValue": "https://wwww.google.com"
                        }
                    },
                    {
                        "key": "title",
                        "value": {
                        "stringValue": "Free Online GUID Generator"
                        }
                    },
                ]
        }
    }
```

</details>

### PageNavigationTiming

The event name MUST be`page_navigation_timing`.

This event describes the timing metrics of a page navigation as provided by
`PerformanceNavigationTiming` Performance API.

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

### ResourceTiming

The event name MUST be `resource_timing`.

This event describes the timing metrics as provided by `PerformanceResourceTiming`
Performance API.  These metrics are related to fetching a resource, such as
XMLHttpRequest, Fetch, sendBeacon APIs, SVG, image or script.

The following table describes the payload fields that MUST be used to describe the details of event.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
|name | string | URL of the requested resource || Recommended |
|fetchStart | long | || Recommended |
|domainLookupStart | long | || Recommended |
|domainLookupEnd | long | || Recommended |
|connectStart | long | || Recommended |
|secureConnectionStart | long | || Recommended |
|connectEnd | long | || Recommended |
|requestStart | long | || Recommended |
|responseStart | long | || Recommended |
|responseEnd | long | || Recommended |

### Exception

The event name MUST be `browser.exception`.

This event describes an error or exception that occurs in a browser application.

The following table describes the payload fields that MUST be used to describe the details of event.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `exception.file_name` | string | Name of the file that generated the error | `foo.js` | Recommended |
| `exception.line_number` | int | Line number where the error occurred |  | Recommended |
| `exception.column_number` | int | Column number where the error occurred |  | Recommended |
| `exception.message` | string | The exception message. | `Division by zero`; `Can't convert 'int' object to str implicitly` | Recommended |
| `exception.stacktrace` | string | A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG. | `Exception in thread "main" java.lang.RuntimeException: Test exception\n at com.example.GenerateTrace.methodB(GenerateTrace.java:13)\n at com.example.GenerateTrace.methodA(GenerateTrace.java:9)\n at com.example.GenerateTrace.main(GenerateTrace.java:5)` | Recommended |
| `exception.type` | string | The type of the exception (its fully-qualified class name, if applicable). The dynamic type of the exception should be preferred over the static type in languages that support it. | `java.net.ConnectException`; `OSError` | Recommended |

### UserAction

The event name MUST be`user_action`.

This event describes actions performed by the user such as click, scroll, zoom, resize, etc.

The following table describes the payload fields that MUST be used to describe the details of event.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `element` | string | Target element tag name (obtained via `event.target.tagName`) | `button` | Recommended |
| `element_xpath` | string | Target element xpath | `//*[@id="testBtn"]` | Recommended |
| `user_action_type` | string | Type of interaction. See enum [here](https://github.com/microsoft/ApplicationInsights-JS/blob/941ec2e4dbd017b8450f2b17c60088ead1e6c428/extensions/applicationinsights-clickanalytics-js/src/Enums.ts) for potential values we could add support for. | `click` | Required |
| `click_coordinates` | string | Click coordinates captured as a string in the format {x}X{y}.  Eg. 345X23 | `345X23` | Recommended |
| `tags` | string[] | Grab data from data-otel-* attributes in tree | `[data-otel-asd="value" -> asd attr w/ "value"]` | Recommended |

`user_action_type` MUST be one of the following:

| Value  | Description |
|---|---|
| `click` | click |

### WebVital

The event name MUST be `web_vital`.

This event describes the website performance metrics introduced by Google (See <https://web.dev/vitals/>).

The following table describes the payload fields that MUST be used to describe the details of event.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `name` | string | name of the web vital | `CLS` | Required |
| `value` | double | value of the web vital | `1.0`; `2.0` | Required |
| `delta` | double | The delta between the current value and the last-reported value | `0.2` | Required |
| `id` | string | A unique ID representing this particular metric instance | "v3-1677874579383-6381583661209" | Required |

`name` has the following list of well-known values. If one of them applies, then the respective value MUST be used, otherwise a custom value MAY be used.

| Value  | Description |
|---|---|
| `CLS` | Cumulative Layout Shift |
| `LCP` | Largest Contentful Paint |
| `FID` | First Input Delay |
| `INP` | Interation to Next Paint |
