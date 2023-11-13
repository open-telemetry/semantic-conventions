<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Client
--->

# Client Attributes

These attributes may be used to describe the client in a connection-based network interaction
where there is one side that initiates the connection (the client is the side that initiates the connection).
This covers all TCP network interactions since TCP is connection-based and one side initiates the
connection (an exception is made for peer-to-peer communication over TCP where the "user-facing" surface of the
protocol / API does not expose a clear notion of client and server).
This also covers UDP network interactions where one side initiates the interaction, e.g. QUIC (HTTP/3) and DNS.

<!-- semconv client(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `client.address` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Client address - domain name if available without reverse DNS lookup; otherwise, IP address or Unix domain socket name. [1] | `client.example.com`; `10.1.2.80`; `/tmp/my.sock` |
| `client.geo.city_name` | string | City name. | `Montreal`; `Berlin` |
| `client.geo.continent_code` | string | Two-letter code representing continent’s name. | `AF` |
| `client.geo.continent_name` | string | Name of the continent. | `North America`; `Europe` |
| `client.geo.country_iso_code` | string | Two-letter ISO Country Code (ISO 3166-1 alpha2). | `CA` |
| `client.geo.country_name` | string | Country name. | `Canada` |
| `client.geo.location.lat` | double | Latitude of the geo location in WGS84. | `45.505918` |
| `client.geo.location.lon` | double | Longitude of the geo location in WGS84. | `-73.61483` |
| `client.geo.name` | string | User-defined description of a location. [2] | `boston-dc` |
| `client.geo.postal_code` | string | Postal code associated with the location. Values appropriate for this field may also be known as a postcode or ZIP code and will vary widely from country to country. | `94040` |
| `client.geo.region_iso_code` | string | Region ISO code (ISO 3166-2). | `CA-QC` |
| `client.geo.region_name` | string | Region name. | `Quebec` |
| `client.geo.timezone` | string | The time zone of the location, such as IANA time zone name. | `America/Argentina/Buenos_Aires` |
| `client.port` | int | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Client port number. [3] | `65123` |

**[1]:** When observed from the server side, and when communicating through an intermediary, `client.address` SHOULD represent the client address behind any intermediaries,  for example proxies, if it's available.

**[2]:** User-defined description of a location, at the level of granularity they care about. Could be the name of their data centers, the floor number, if this describes a local physical entity, city names. Not typically used in automated geolocation.

**[3]:** When observed from the server side, and when communicating through an intermediary, `client.port` SHOULD represent the client port behind any intermediaries,  for example proxies, if it's available.

`client.geo.continent_code` MUST be one of the following:

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
