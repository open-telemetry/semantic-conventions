
<!--- Hugo front matter used to generate the website version of this page:
--->

# SYSTEM

- [system deprecated](#system deprecated)


## system deprecated Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `system.processes.status` | string | Deprecated, use `system.process.status` instead. [1] | `running` | ![Deprecated](https://img.shields.io/badge/-deprecated-red) |
|---|---|---|---|---|

**[1]:** Replaced by `system.process.status`.

`system.processes.status` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `running` | none | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `sleeping` | none | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `stopped` | none | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `defunct` | none | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

