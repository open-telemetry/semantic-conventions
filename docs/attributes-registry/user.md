<!--- Hugo front matter used to generate the website version of this page:
--->

# User

## User Attributes

<!-- semconv registry.user(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `user.domain` | string | Name of the directory the user is a member of. For example, an LDAP or Active Directory domain name. | `internal.example.com` |
| `user.email` | string | User email address. | `a.einstein@example.com` |
| `user.full_name` | string | User's full name | `Albert Einstein` |
| `user.hash` | string | Unique user hash to correlate information for a user in anonymized form. [1] | `364fc68eaf4c8acec74a4e52d7d1feaa` |
| `user.id` | string | Unique identifier of the user. | `S-1-5-21-202424912787-2692429404-2351956786-1000` |
| `user.name` | string | Short name or login/username of the user. | `a.einstein` |
| `user.roles` | string[] | Array of user roles at the time of the event. | `[admin, reporting_user]` |

**[1]:** Useful if `user.id` or `user.name` contain confidential information and cannot be used.
<!-- endsemconv -->
