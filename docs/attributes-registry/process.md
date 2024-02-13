<!--- Hugo front matter used to generate the website version of this page:
--->

# Process

## Process Attributes

<!-- semconv registry.process(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `process.command` | string | The command used to launch the process (i.e. the command name). On Linux based systems, can be set to the zeroth string in `proc/[pid]/cmdline`. On Windows, can be set to the first parameter extracted from `GetCommandLineW`. | `cmd/otelcol` |
| `process.command_args` | string[] | All the command arguments (including the command/executable itself) as received by the process. On Linux-based systems (and some other Unixoid systems supporting procfs), can be set according to the list of null-delimited strings extracted from `proc/[pid]/cmdline`. For libc-based executables, this would be the full argv vector passed to `main`. | `[cmd/otecol, --config=config.yaml]` |
| `process.command_line` | string | The full command used to launch the process as a single string representing the full command. On Windows, can be set to the result of `GetCommandLineW`. Do not set this if you have to assemble it just for monitoring; use `process.command_args` instead. | `C:\cmd\otecol --config="my directory\config.yaml"` |
| `process.executable.name` | string | The name of the process executable. On Linux based systems, can be set to the `Name` in `proc/[pid]/status`. On Windows, can be set to the base name of `GetProcessImageFileNameW`. | `otelcol` |
| `process.executable.path` | string | The full path to the process executable. On Linux based systems, can be set to the target of `proc/[pid]/exe`. On Windows, can be set to the result of `GetProcessImageFileNameW`. | `/usr/bin/cmd/otelcol` |
| `process.owner` | string | The username of the user that owns the process. | `root` |
| `process.parent_pid` | int | Parent Process identifier (PPID). | `111` |
| `process.pid` | int | Process identifier (PID). | `1234` |
| `process.runtime.description` | string | An additional description about the runtime of the process, for example a specific vendor customization of the runtime environment. | `Eclipse OpenJ9 Eclipse OpenJ9 VM openj9-0.21.0` |
| `process.runtime.name` | string | The name of the runtime of this process. For compiled native binaries, this SHOULD be the name of the compiler. | `OpenJDK Runtime Environment` |
| `process.runtime.version` | string | The version of the runtime of this process, as returned by the runtime without modification. | `14.0.2` |
<!-- endsemconv -->
