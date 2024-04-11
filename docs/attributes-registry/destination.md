
<!--- Hugo front matter used to generate the website version of this page:
--->

# DESTINATION

- [destination](#destination)
- [Notes](#notes)

## destination Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `destination.address` | string | Destination address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] |`destination.example.com`; `10.1.2.80`; `/tmp/my.sock` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `destination.port` | int | Destination port number  |`3389`; `2888` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|

## Notes

[1]: When observed from the source side, and when communicating through an intermediary, `destination.address` SHOULD represent the destination address behind any intermediaries, for example proxies, if it's available.

