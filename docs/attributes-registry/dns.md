<!--- Hugo front matter used to generate the website version of this page:
--->

# DNS

## DNS Attributes

<!-- semconv registry.dns(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `dns.question.name` | string | The name being queried. [1] | `www.example.com`; `opentelemetry.io` |

**[1]:** If the name field contains non-printable characters (below 32 or above 126), those characters should be represented as escaped base 10 integers (\DDD). Back slashes and quotes should be escaped. Tabs, carriage returns, and line feeds should be converted to \t, \r, and \n respectively.
<!-- endsemconv -->