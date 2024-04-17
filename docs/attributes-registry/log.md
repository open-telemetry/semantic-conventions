<!--- Hugo front matter used to generate the website version of this page:
--->

# Log

<!-- toc -->

- [Log Attributes](#log-attributes)
  - [Generic log attributes](#generic-log-attributes)
  - [File log attributes](#file-log-attributes)
  - [Record log attributes](#record-log-attributes)

<!-- tocstop -->

## Log Attributes

### Generic log attributes

<!-- semconv registry.log(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `log.iostream` | string | The stream associated with the log. See below for a list of well-known values. | `stdout` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`log.iostream` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `stdout` | Logs from stdout stream | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `stderr` | Events from stderr stream | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### File log attributes

<!-- semconv registry.log.file(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `log.file.name` | string | The basename of the file. | `audit.log` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `log.file.name_resolved` | string | The basename of the file, with symlinks resolved. | `uuid.log` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `log.file.path` | string | The full path to the file. | `/var/log/mysql/audit.log` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `log.file.path_resolved` | string | The full path to the file, with symlinks resolved. | `/var/lib/docker/uuid.log` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

### Record log attributes

<!-- semconv registry.log.record(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `log.record.uid` | string | A unique identifier for the Log Record. [1] | `01ARZ3NDEKTSV4RRFFQ69G5FAV` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** If an id is provided, other log records with the same id will be considered duplicates and can be removed safely. This means, that two distinguishable log records MUST have different values.
The id MAY be an [Universally Unique Lexicographically Sortable Identifier (ULID)](https://github.com/ulid/spec), but other identifiers (e.g. UUID) may be used as needed.
<!-- endsemconv -->