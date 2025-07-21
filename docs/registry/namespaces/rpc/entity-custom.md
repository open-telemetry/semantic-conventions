# Service

**Summary:** Services are..

**Description:** A service is....

---------------------------------

## Entity: Service

**Status:** ![Stable](https://img.shields.io/badge/-stable-lightgreen)

**Summary:** A service instance.

**Signal Type:** Entity

**Entity Type:** `service`

**Description:** A service is

**Identifying Attributes:**

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`service.name`](attribute-custom.md) | string | Logical name of the service. | `shoppingcart` | `Required` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| [`service.instance.id`](attribute-custom.md) | string | The string ID of the service instance. | `627cc493-f310-47de-96bd-71410b7dec09` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |
| [`service.namespace`](attribute-custom.md) | string | A namespace for `service.name`. | `Shop` | `Recommended` | ![Development](https://img.shields.io/badge/-development-blue) |

**Descriptive Attributes:**

| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`service.version`](attribute-custom.md) | string | The version string of the service API or implementation. The format is not defined by these conventions. | `2.0.0`; `a01dbef8a` | `Recommended` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
