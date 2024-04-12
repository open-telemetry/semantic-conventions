
<!--- Hugo front matter used to generate the website version of this page:
--->

# CODE

- [code](#code)


## code Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `code.column` | int | The column number in `code.filepath` best representing the operation. It SHOULD point within the code unit named in `code.function`.  |
16 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code.filepath` | string | The source code file name that identifies the code unit as uniquely as possible (preferably an absolute file path).  |
/usr/local/MyApplication/content_root/app/index.php | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code.function` | string | The method or function name, or equivalent (usually rightmost part of the code unit's name).  |
serveRequest | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code.lineno` | int | The line number in `code.filepath` best representing the operation. It SHOULD point within the code unit named in `code.function`.  |
42 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code.namespace` | string | The "namespace" within which `code.function` is defined. Usually the qualified class or module name, such that `code.namespace` + some separator + `code.function` form a unique identifier for the code unit.  |
com.example.MyHttpService | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `code.stacktrace` | string | A stacktrace as a string in the natural representation for the language runtime. The representation is to be determined and documented by each language SIG.  |
at com.example.GenerateTrace.methodB(GenerateTrace.java:13)\n at com.example.GenerateTrace.methodA(GenerateTrace.java:9)\n at com.example.GenerateTrace.main(GenerateTrace.java:5) | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|


