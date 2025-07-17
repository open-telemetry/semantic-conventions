# {{vendor.name}}

**Summary:** {{vendor.brief}}

{{vendor.header}}

**Description:** {{vendor.note}}


## {{implementation.name}}

**Summary:** {{implementation.brief}}

**Package:** {{implementation.package}}

**Description:** {{implementation.note}}

**Configuration:**

|Setting|Type|Summary|Default|
|---|---|---|---|
|*.{{Namespace}}. Include{{Property}}|boolean||false|
|*.Host.IncludeIP|boolean||false|
|*.{{Namespace}}.{{Property}}|string||false|
|*.Host.Name|string||false|

---------------------------------

### Events:

{{block of events}}

#### {{event.name}}:

**Summary:** {{event.brief}}

**Description:** {{event.note}}

**Attributes:**

{{table of attributes which has been implemented}}

|Key|Type|Summary|Value|
|---|---|---|---|
|[CustomAttribute](attribute-custom.md)|[CustomType](type-custom.md)|This is an attribute| RabbitMQ|

**Body:**

{{table of body properties which has been implemented}}

|Body Field|Type|Summary|Value|
|---|---|---|---|
name|[CustomType](type-custom.md)|This is an attribute| |

### Metrics:

{{block of metrics}}

#### {{metric.name}}

**Summary:** {{metric.brief}}

..... {{spot for signal specific properties}}

**Description:** {{metric.note}}

**Attributes:**

{{table of attributes which has been implemented}}

|Key|Type|Summary|Value|
|---|---|---|---|
|[CustomAttribute](attribute-custom.md)|[CustomType](type-custom.md)|This is an attribute| RabbitMQ|

### Spans:

{{block of spans}}

#### {{span.name}}

**Summary:** {{metric.brief}}

..... {{spot for signal specific properties}}

**Description:** {{metric.note}}

**Attributes:**

{{table of attributes which has been implemented}}

|Key|Type|Summary|Value|
|---|---|---|---|
|[CustomAttribute](attribute-custom.md)|[CustomType](type-custom.md)|This is an attribute| RabbitMQ||

---------------------------------

{{namespace.footer}}