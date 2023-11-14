<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Server
--->

# Server Attributes

These attributes may be used to describe the server in a connection-based network interaction
where there is one side that initiates the connection (the client is the side that initiates the connection).
This covers all TCP network interactions since TCP is connection-based and one side initiates the
connection (an exception is made for peer-to-peer communication over TCP where the "user-facing" surface of the
protocol / API does not expose a clear notion of client and server).
This also covers UDP network interactions where one side initiates the interaction, e.g. QUIC (HTTP/3) and DNS.

<!-- semconv server(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `server.address` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Server domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `example.com`; `10.1.2.80`; `/tmp/my.sock` |
| `server.geo.city_name` | string | City name. | `Montreal`; `Berlin` |
| `server.geo.continent_code` | string | Two-letter code representing continent’s name. | `AF` |
| `server.geo.continent_name` | string | Name of the continent. | `North America`; `Europe` |
| `server.geo.country_iso_code` | string | Two-letter ISO Country Code ([ISO 3166-1 alpha2](https://en.wikipedia.org/wiki/ISO_3166-1#Codes)). | `CA` |
| `server.geo.country_name` | string | Country name. | `Canada` |
| `server.geo.location.lat` | double | Latitude of the geo location in [WGS84](https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84). | `45.505918` |
| `server.geo.location.lon` | double | Longitude of the geo location in [WGS84](https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84). | `-73.61483` |
| `server.geo.name` | string | User-defined description of a location. [2] | `boston-dc` |
| `server.geo.postal_code` | string | Postal code associated with the location. Values appropriate for this field may also be known as a postcode or ZIP code and will vary widely from country to country. | `94040` |
| `server.geo.region_iso_code` | string | Region ISO code ([ISO 3166-2](https://en.wikipedia.org/wiki/ISO_3166-2)). | `CA-QC` |
| `server.geo.region_name` | string | Region name. | `Quebec` |
| `server.geo.timezone` | string | The time zone of the location, such as [IANA time zone name](https://nodatime.org/TimeZones). | `America/Argentina/Buenos_Aires` |
| `server.port` | int | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Server port number. [3] | `80`; `8080`; `443` |

**[1]:** When observed from the client side, and when communicating through an intermediary, `server.address` SHOULD represent the server address behind any intermediaries, for example proxies, if it's available.

**[2]:** User-defined description of a location, at the level of granularity they care about. Could be the name of their data centers, the floor number, if this describes a local physical entity, city names. Not typically used in automated geolocation.

**[3]:** When observed from the client side, and when communicating through an intermediary, `server.port` SHOULD represent the server port behind any intermediaries, for example proxies, if it's available.

`server.geo.continent_code` MUST be one of the following:

| Value  | Description |
|---|---|
| `AF` | Africa |
| `AN` | Antarctica |
| `AS` | Asia |
| `EU` | Europe |
| `NA` | North America |
| `OC` | Oceania |
| `SA` | South America |
<!-- endsemconv -->