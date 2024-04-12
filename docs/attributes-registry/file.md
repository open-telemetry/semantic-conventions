
<!--- Hugo front matter used to generate the website version of this page:
--->

# FILE

- [file](#file)


## file Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `file.directory` | string | Directory where the file is located. It should include the drive letter, when appropriate. | `/home/user`; `C:\Program Files\MyApp` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `file.extension` | string | File extension, excluding the leading dot. [1] | `png`; `gz` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `file.name` | string | Name of the file including the extension, without the directory. | `example.png` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `file.path` | string | Full path to the file, including the file name. It should include the drive letter, when appropriate. | `/home/alice/example.png`; `C:\Program Files\MyApp\myapp.exe` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `file.size` | int | File size in bytes. |  | ![Experimental](https://img.shields.io/badge/-experimental-blue) |


**[1]:** When the file name has multiple extensions (example.tar.gz), only the last one should be captured ("gz", not "tar.gz").


