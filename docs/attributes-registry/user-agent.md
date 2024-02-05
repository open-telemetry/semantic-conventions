<!--- Hugo front matter used to generate the website version of this page:
--->

# User agent

## User agent Attributes

<!-- semconv registry.user_agent(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `user_agent.name` | string | Name of the user-agent extracted from original. Usually refers to the browser's name. [1] | `Safari`; `YourApp` |
| `user_agent.original` | string | ![Stable](https://img.shields.io/badge/-stable-lightgreen)<br>Value of the [HTTP User-Agent](https://www.rfc-editor.org/rfc/rfc9110.html#field.user-agent) header sent by the client. | `CERN-LineMode/2.15 libwww/2.17b3`; `Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1`; `YourApp/1.0.0 grpc-java-okhttp/1.27.2` |
| `user_agent.version` | string | Version of the user-agent extracted from original. Usually refers to the browser's version [2] | `14.1.2`; `1.0.0` |

**[1]:** [Example](https://www.whatsmyua.info) of extracting browser's name from original string. In the case of using a user-agent for non-browser products, such as microservices with multiple names/versions inside the `user_agent.original`, the most significant name SHOULD be selected. In such a scenario it should align with  `user_agent.version`

**[2]:** [Example](https://www.whatsmyua.info) of extracting browser's version from original string. In the case of using a user-agent for non-browser products, such as microservices with multiple names/versions inside the `user_agent.original`, the most significant version SHOULD be selected. In such a scenario it should align with `user_agent.name`
<!-- endsemconv -->
