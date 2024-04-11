
<!--- Hugo front matter used to generate the website version of this page:
--->

# GRAPHQL

- [graphql](#graphql)
- [Notes](#notes)

## graphql Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `graphql.operation.name` | string | The name of the operation being executed.  |
findBookById | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `graphql.operation.type` | string | The type of the operation being executed.  |`query`; `mutation`; `subscription` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `graphql.document` | string | The GraphQL document being executed. [1] |
query findBookById { bookById(id: ?) { name } } | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|

`graphql.operation.type` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `query` | GraphQL query |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `mutation` | GraphQL mutation |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `subscription` | GraphQL subscription |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |

## Notes

[1]: The value may be sanitized to exclude sensitive information.
