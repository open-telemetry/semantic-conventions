<!--- Hugo front matter used to generate the website version of this page:
--->

# Thread

These attributes may be used for any operation to store information about a thread.

## Thread Attributes

<!-- semconv registry.thread(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `thread.id` | int | Current "managed" thread ID (as opposed to OS thread ID). | `42` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `thread.name` | string | Current thread name. | `main` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->