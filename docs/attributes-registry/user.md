<!--- Hugo front matter used to generate the website version of this page:
--->

# User

## User Attributes

<!-- semconv registry.user(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `user.domain` | string | Name of the directory the user is a member of. For example, an LDAP or Active Directory domain name. | `internal.example.com` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `user.email` | string | User email address. | `a.einstein@example.com` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `user.full_name` | string | User's full name | `Albert Einstein` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `user.hash` | string | Unique user hash to correlate information for a user in anonymized form. [1] | `364fc68eaf4c8acec74a4e52d7d1feaa` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `user.id` | string | Unique identifier of the user. | `S-1-5-21-202424912787-2692429404-2351956786-1000` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `user.name` | string | Short name or login/username of the user. | `a.einstein` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `user.roles` | string[] | Array of user roles at the time of the event. | `[admin, reporting_user]` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** Useful if `user.id` or `user.name` contain confidential information and cannot be used.
<!-- endsemconv -->
