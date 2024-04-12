
<!--- Hugo front matter used to generate the website version of this page:
--->

# OTEL

- [otel](#otel)
- [otel library deprecated](#otel library deprecated)


## otel Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `otel.status_code` | string | Name of the code, either "OK" or "ERROR". MUST NOT be set if the status code is UNSET.  | `OK` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `otel.status_description` | string | Description of the Status if it has a value, otherwise not set.  | `resource not found` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
|---|---|---|---|---|


`otel.status_code` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `OK` | The operation has been validated by an Application developer or Operator to have completed successfully. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `ERROR` | The operation contains an error. | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |


## otel library deprecated Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `otel.library.name` | string |  [1] | `io.opentelemetry.contrib.mongodb` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
| `otel.library.version` | string |  [2] | `1.0.0` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
|---|---|---|---|---|

**[1]:** use the `otel.scope.name` attribute.
**[2]:** use the `otel.scope.version` attribute.

