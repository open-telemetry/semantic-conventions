
<!--- Hugo front matter used to generate the website version of this page:
--->

# SOURCE

- [source](#source)


## source Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `source.address` | string | Source address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] |`source.example.com`; `10.1.2.80`; `/tmp/my.sock` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `source.port` | int | Source port number  |`3389`; `2888` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|

**[1]:** When observed from the destination side, and when communicating through an intermediary, `source.address` SHOULD represent the source address behind any intermediaries, for example proxies, if it's available.


