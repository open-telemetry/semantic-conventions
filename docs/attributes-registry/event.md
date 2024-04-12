
<!--- Hugo front matter used to generate the website version of this page:
--->

# EVENT

- [event](#event)


## event Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `event.name` | string | Identifies the class / type of event. [1] |`browser.mouse.click`; `device.app.lifecycle` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|

**[1]:** Event names are subject to the same rules as [attribute names](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/common/attribute-naming.md). Notably, event names are namespaced to avoid collisions and provide a clean separation of semantics for events in separate domains like browser, mobile, and kubernetes.


