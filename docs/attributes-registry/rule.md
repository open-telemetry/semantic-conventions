<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Rule
--->

# Rule

## Rule Attributes

<!-- semconv registry.rule(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `rule.author` | string | Name, organization, or pseudonym of the author or authors who created the rule used to generate this event. | `username1` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.category` | string | A categorization value keyword used by the entity using the rule for detection of this event | `Attempted Information Leak` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.description` | string | The description of the rule generating the event. | `Block requests to public DNS over HTTPS / TLS protocols` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.id` | string | A rule ID that is unique within the scope of an agent, observer, or other entity using the rule for detection of this event. | `101` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.license` | string | Name of the license under which the rule used to generate this event is made available. | `Apache 2.0` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.name` | string | The name of the rule or signature generating the event. | `BLOCK_DNS_over_TLS` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.reference` | string | Reference URL to additional information about the rule used to generate this event. [1] | `https://en.wikipedia.org/wiki/DNS_over_TLS` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.ruleset` | string | Name of the ruleset, policy, group, or parent category in which the rule used to generate this event is a member. | `Standard_Protocol_Filters` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.uuid` | string | A rule ID that is unique within the scope of a set or group of agents, observers, or other entities using the rule for detection of this event. | `550e8400-e29b-41d4-a716-446655440000`; `1100110011` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `rule.version` | string | The version / revision of the rule being used for analysis. | `1.0.0` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The URL can point to the vendor’s documentation about the rule. If that’s not available, it can also be a link to a more general page describing this type of alert.
<!-- endsemconv -->
