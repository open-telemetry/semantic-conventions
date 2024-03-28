<!--- Hugo front matter used to generate the website version of this page:
--->

# File

## File Attributes

<!-- semconv registry.file(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `file.directory` | string | Directory where the file is located. It should include the drive letter, when appropriate. | `/home/user`; `C:\Program Files\MyApp` |
| `file.extension` | string | File extension, excluding the leading dot. [1] | `png`; `gz` |
| `file.name` | string | Name of the file including the extension, without the directory. | `example.png` |
| `file.path` | string | Full path to the file, including the file name. It should include the drive letter, when appropriate. | `/home/alice/example.png`; `C:\Program Files\MyApp\myapp.exe` |
| `file.size` | int | File size in bytes. |  |

**[1]:** When the file name has multiple extensions (example.tar.gz), only the last one should be captured ("gz", not "tar.gz").
<!-- endsemconv -->
