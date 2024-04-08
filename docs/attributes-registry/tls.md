<!--- Hugo front matter used to generate the website version of this page:
--->

# TLS

## TLS Attributes

<!-- semconv registry.tls(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `tls.cipher` | string | String indicating the [cipher](https://datatracker.ietf.org/doc/html/rfc5246#appendix-A.5) used during the current connection. [1] | `TLS_RSA_WITH_3DES_EDE_CBC_SHA`; `TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.certificate` | string | PEM-encoded stand-alone certificate offered by the client. This is usually mutually-exclusive of `client.certificate_chain` since this value also exists in that list. | `MII...` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.certificate_chain` | string[] | Array of PEM-encoded certificates that make up the certificate chain offered by the client. This is usually mutually-exclusive of `client.certificate` since that value should be the first certificate in the chain. | `[MII..., MI...]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.hash.md5` | string | Certificate fingerprint using the MD5 digest of DER-encoded version of certificate offered by the client. For consistency with other hash values, this value should be formatted as an uppercase hash. | `0F76C7F2C55BFD7D8E8B8F4BFBF0C9EC` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.hash.sha1` | string | Certificate fingerprint using the SHA1 digest of DER-encoded version of certificate offered by the client. For consistency with other hash values, this value should be formatted as an uppercase hash. | `9E393D93138888D288266C2D915214D1D1CCEB2A` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.hash.sha256` | string | Certificate fingerprint using the SHA256 digest of DER-encoded version of certificate offered by the client. For consistency with other hash values, this value should be formatted as an uppercase hash. | `0687F666A054EF17A08E2F2162EAB4CBC0D265E1D7875BE74BF3C712CA92DAF0` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.issuer` | string | Distinguished name of [subject](https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.6) of the issuer of the x.509 certificate presented by the client. | `CN=Example Root CA, OU=Infrastructure Team, DC=example, DC=com` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.ja3` | string | A hash that identifies clients based on how they perform an SSL/TLS handshake. | `d4e5b18d6b55c71272893221c96ba240` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.not_after` | string | Date/Time indicating when client certificate is no longer considered valid. | `2021-01-01T00:00:00.000Z` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.not_before` | string | Date/Time indicating when client certificate is first considered valid. | `1970-01-01T00:00:00.000Z` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.server_name` | string | Also called an SNI, this tells the server which hostname to which the client is attempting to connect to. | `opentelemetry.io` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.subject` | string | Distinguished name of subject of the x.509 certificate presented by the client. | `CN=myclient, OU=Documentation Team, DC=example, DC=com` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.client.supported_ciphers` | string[] | Array of ciphers offered by the client during the client hello. | `["TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384", "..."]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.curve` | string | String indicating the curve used for the given cipher, when applicable | `secp256r1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.established` | boolean | Boolean flag indicating if the TLS negotiation was successful and transitioned to an encrypted tunnel. | `True` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.next_protocol` | string | String indicating the protocol being tunneled. Per the values in the [IANA registry](https://www.iana.org/assignments/tls-extensiontype-values/tls-extensiontype-values.xhtml#alpn-protocol-ids), this string should be lower case. | `http/1.1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.protocol.name` | string | Normalized lowercase protocol name parsed from original string of the negotiated [SSL/TLS protocol version](https://www.openssl.org/docs/man1.1.1/man3/SSL_get_version.html#RETURN-VALUES) | `ssl` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.protocol.version` | string | Numeric part of the version parsed from the original string of the negotiated [SSL/TLS protocol version](https://www.openssl.org/docs/man1.1.1/man3/SSL_get_version.html#RETURN-VALUES) | `1.2`; `3` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.resumed` | boolean | Boolean flag indicating if this TLS connection was resumed from an existing TLS negotiation. | `True` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.certificate` | string | PEM-encoded stand-alone certificate offered by the server. This is usually mutually-exclusive of `server.certificate_chain` since this value also exists in that list. | `MII...` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.certificate_chain` | string[] | Array of PEM-encoded certificates that make up the certificate chain offered by the server. This is usually mutually-exclusive of `server.certificate` since that value should be the first certificate in the chain. | `[MII..., MI...]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.hash.md5` | string | Certificate fingerprint using the MD5 digest of DER-encoded version of certificate offered by the server. For consistency with other hash values, this value should be formatted as an uppercase hash. | `0F76C7F2C55BFD7D8E8B8F4BFBF0C9EC` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.hash.sha1` | string | Certificate fingerprint using the SHA1 digest of DER-encoded version of certificate offered by the server. For consistency with other hash values, this value should be formatted as an uppercase hash. | `9E393D93138888D288266C2D915214D1D1CCEB2A` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.hash.sha256` | string | Certificate fingerprint using the SHA256 digest of DER-encoded version of certificate offered by the server. For consistency with other hash values, this value should be formatted as an uppercase hash. | `0687F666A054EF17A08E2F2162EAB4CBC0D265E1D7875BE74BF3C712CA92DAF0` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.issuer` | string | Distinguished name of [subject](https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.6) of the issuer of the x.509 certificate presented by the client. | `CN=Example Root CA, OU=Infrastructure Team, DC=example, DC=com` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.ja3s` | string | A hash that identifies servers based on how they perform an SSL/TLS handshake. | `d4e5b18d6b55c71272893221c96ba240` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.not_after` | string | Date/Time indicating when server certificate is no longer considered valid. | `2021-01-01T00:00:00.000Z` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.not_before` | string | Date/Time indicating when server certificate is first considered valid. | `1970-01-01T00:00:00.000Z` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls.server.subject` | string | Distinguished name of subject of the x.509 certificate presented by the server. | `CN=myserver, OU=Documentation Team, DC=example, DC=com` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The values allowed for `tls.cipher` MUST be one of the `Descriptions` of the [registered TLS Cipher Suits](https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#table-tls-parameters-4).

`tls.protocol.name` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `ssl` | ssl | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `tls` | tls | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->