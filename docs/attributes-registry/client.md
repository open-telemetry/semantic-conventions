<!--- Hugo front matter used to generate the website version of this page:
--->

# Client

- [Client](#client)

## Client Attributes

| Attribute        | Type   | Description                                                                                                                 | Examples                                          | Stability                                                  |
| ---------------- | ------ | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------- |
| `client.address` | string | Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `client.example.com`; `10.1.2.80`; `/tmp/my.sock` | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |
| `client.port`    | int    | Client port number. [2]                                                                                                     | `65123`                                           | ![Stable](https://img.shields.io/badge/-stable-lightgreen) |

**[1]:** When observed from the server side, and when communicating through an intermediary, `client.address` SHOULD represent the client address behind any intermediaries, for example proxies, if it's available.

**[2]:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries, for example proxies, if it's available.
