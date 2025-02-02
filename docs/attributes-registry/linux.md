<!-- NOTE: THIS FILE IS AUTOGENERATED. DO NOT EDIT BY HAND. -->
<!-- see templates/registry/markdown/attribute_namespace.md.j2 -->

# Linux

## Linux Memory Attributes

Describes Linux Memory attributes

| Attribute | Type | Description | Examples | Stability |
|---|---|---|---|---|
| <a id="linux-memory-slab-state" href="#linux-memory-slab-state">`linux.memory.slab.state`</a> | string | The Linux Slab memory state | `reclaimable`; `unreclaimable` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

---

`linux.memory.slab.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `reclaimable` | reclaimable | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `unreclaimable` | unreclaimable | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
