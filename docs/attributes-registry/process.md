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
| `process.end` | string | The date and time the process ended, in ISO 8601 format. | `2023-11-21T09:26:12.315Z` |
| `process.env_vars` | string[] | Array of environment variable bindings. [1] | `[PATH=/usr/local/bin;/usr/bin, USER=ubuntu]` |
| `process.executable.name` | string | The name of the process executable. On Linux based systems, can be set to the `Name` in `proc/[pid]/status`. On Windows, can be set to the base name of `GetProcessImageFileNameW`. | `otelcol` |
| `process.executable.path` | string | The full path to the process executable. On Linux based systems, can be set to the target of `proc/[pid]/exe`. On Windows, can be set to the result of `GetProcessImageFileNameW`. | `/usr/bin/cmd/otelcol` |
| `process.exit_code` | int | The exit code of the process. | `127` |
| `process.group_leader.pid` | int | The PID of the process's group leader. This is also the process group ID (PGID) of the process. | `23` |
| `process.interactive` | boolean | Whether the process is connected to an interactive shell. |  |
| `process.owner` | string | The username of the user that owns the process. [2] | `root` |
| `process.parent_pid` | int | Parent Process identifier (PPID). | `111` |
| `process.pid` | int | Process identifier (PID). | `1234` |
| `process.real_user.id` | int | The real user ID (RUID) of the process. | `1000` |
| `process.real_user.name` | string | The username of the real user of the process. | `operator` |
| `process.runtime.description` | string | An additional description about the runtime of the process, for example a specific vendor customization of the runtime environment. | `Eclipse OpenJ9 Eclipse OpenJ9 VM openj9-0.21.0` |
| `process.runtime.name` | string | The name of the runtime of this process. For compiled native binaries, this SHOULD be the name of the compiler. | `OpenJDK Runtime Environment` |
| `process.runtime.version` | string | The version of the runtime of this process, as returned by the runtime without modification. | `14.0.2` |
| `process.saved_user.id` | int | The saved user ID (SUID) of the process. | `1002` |
| `process.saved_user.name` | string | The username of the saved user. | `operator` |
| `process.session_leader.pid` | int | The PID of the process's session leader. This is also the session ID (SID) of the process. | `14` |
| `process.start` | string | The date and time the process started, in ISO 8601 format. | `2023-11-21T09:25:34.853Z` |
| `process.user.id` | int | The effective user ID (EUID) of the process. | `1001` |
| `process.user.name` | string | The username of the effective user of the process. | `root` |
| `process.vpid` | int | Virtual process identifier. [3] | `12` |

**[1]:** As environment variables may change during a process's lifespan, this should be captured as a snapshot when the event occurred.
May be filtered to protect sensitive information.

**[2]:** This is intended to be used with Windows only. On POSIX systems, processes can have multiple users (effective, real and saved). To avoid confusion about which user is being referenced, this field should not be used with POSIX systems.

**[3]:** The process ID within a PID namespace. This is not necessarily unique across all processes on the host but it is unique within the process namespace that the process exists within.
<!-- endsemconv -->
