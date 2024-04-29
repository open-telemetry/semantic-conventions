<!--- Hugo front matter used to generate the website version of this page:
--->

# Process

## Process Attributes

<!-- semconv registry.process(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `process.command` | string | The command used to launch the process (i.e. the command name). On Linux based systems, can be set to the zeroth string in `proc/[pid]/cmdline`. On Windows, can be set to the first parameter extracted from `GetCommandLineW`. | `cmd/otelcol` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.command_args` | string[] | All the command arguments (including the command/executable itself) as received by the process. On Linux-based systems (and some other Unixoid systems supporting procfs), can be set according to the list of null-delimited strings extracted from `proc/[pid]/cmdline`. For libc-based executables, this would be the full argv vector passed to `main`. | `[cmd/otecol, --config=config.yaml]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.command_line` | string | The full command used to launch the process as a single string representing the full command. On Windows, can be set to the result of `GetCommandLineW`. Do not set this if you have to assemble it just for monitoring; use `process.command_args` instead. | `C:\cmd\otecol --config="my directory\config.yaml"` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.creation.time` | string | The date and time the process was created, in ISO 8601 format. | `2023-11-21T09:25:34.853Z` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.entity_id` | string | A unique identifier of the process. [1] | `9f26bf6c-2508-43e7-a048-ed1822d9ff52`; `903b0daafe95e8ed9c9c0c9070259c29` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.executable.name` | string | The name of the process executable. On Linux based systems, can be set to the `Name` in `proc/[pid]/status`. On Windows, can be set to the base name of `GetProcessImageFileNameW`. | `otelcol` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.executable.path` | string | The full path to the process executable. On Linux based systems, can be set to the target of `proc/[pid]/exe`. On Windows, can be set to the result of `GetProcessImageFileNameW`. | `/usr/bin/cmd/otelcol` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.exit.code` | int | The exit code of the process. | `127` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.exit.time` | string | The date and time the process exited, in ISO 8601 format. | `2023-11-21T09:26:12.315Z` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.group_leader.pid` | int | The PID of the process's group leader. This is also the process group ID (PGID) of the process. | `23` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.interactive` | boolean | Whether the process is connected to an interactive shell. |  | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.owner` | string | The username of the user that owns the process. | `root` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.parent_pid` | int | Parent Process identifier (PPID). | `111` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.pid` | int | Process identifier (PID). | `1234` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.real_user.id` | int | The real user ID (RUID) of the process. | `1000` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.real_user.name` | string | The username of the real user of the process. | `operator` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.runtime.description` | string | An additional description about the runtime of the process, for example a specific vendor customization of the runtime environment. | `Eclipse OpenJ9 Eclipse OpenJ9 VM openj9-0.21.0` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.runtime.name` | string | The name of the runtime of this process. For compiled native binaries, this SHOULD be the name of the compiler. | `OpenJDK Runtime Environment` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.runtime.version` | string | The version of the runtime of this process, as returned by the runtime without modification. | `14.0.2` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.saved_user.id` | int | The saved user ID (SUID) of the process. | `1002` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.saved_user.name` | string | The username of the saved user. | `operator` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.session_leader.pid` | int | The PID of the process's session leader. This is also the session ID (SID) of the process. | `14` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.user.id` | int | The effective user ID (EUID) of the process. | `1001` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.user.name` | string | The username of the effective user of the process. | `root` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `process.vpid` | int | Virtual process identifier. [2] | `12` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** A globally unique identifier of the process. This can be any format
of unique indentifier.

On Linux, where possible, it is RECOMMENDED that this is calculated
MD5 hash of the string `<pid>_<starttime>_<bootid>`.

e.g.

| Key | Description | Example Value |
| --- | --- | --- |
| `pid` | PID | "1201" |
| `starttime` | start time in seconds since boot | "3029" |
| `bootid` | boot ID, as read from `/proc/sys/kernel/random/boot_id` | "16b6f4a4-179e-4480-9561-0df471d8c6d4" |

md5("1201_3029_16b6f4a4-179e-4480-9561-0df471d8c6d4") -> "230d8ee6147ded8e31dcef082bdbc383"

By following this method, the same entity_id will be generated by all
observers of a given process.

**[2]:** The process ID within a PID namespace. This is not necessarily unique across all processes on the host but it is unique within the process namespace that the process exists within.
<!-- endsemconv -->
