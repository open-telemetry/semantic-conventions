
<!--- Hugo front matter used to generate the website version of this page:
--->

# SERVER

- [server](#server)


## server Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `server.address` | string | Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `server.port` | int | Server port number. [2] | `80`; `8080`; `443` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
|---|---|---|---|---|

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[2]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.


