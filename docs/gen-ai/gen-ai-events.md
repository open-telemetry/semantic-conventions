<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Events
--->

# Semantic conventions for generative AI events

**Status**: [Development][DocumentStatus]

<!-- toc -->

- [Events](#events)
- [Custom events](#custom-events)
- [Examples](#examples)
  - [Chat completion](#chat-completion)
  - [Tools](#tools)
  - [Chat completion with multiple choices](#chat-completion-with-multiple-choices)

<!-- tocstop -->

> [!Warning]
>
> Existing GenAI instrumentations that are using
> [v1.36.0 of this document](https://github.com/open-telemetry/semantic-conventions/blob/v1.36.0/docs/gen-ai/README.md)
> (or prior):
>
> * SHOULD NOT change the version of the GenAI conventions that they emit by default.
>   Conventions include, but are not limited to, attributes, metric, span and event names,
>   span kind and unit of measure.
> * SHOULD introduce an environment variable `OTEL_SEMCONV_STABILITY_OPT_IN`
>   as a comma-separated list of category-specific values. The list of values
>   includes:
>   * `gen_ai_latest_experimental` - emit the latest experimental version of
>     GenAI conventions (supported by the instrumentation) and do not emit the
>     old one (v1.36.0 or prior).
>   * The default behavior is to continue emitting whatever version of the GenAI
>     conventions the instrumentation was emitting (1.36.0 or prior).
>
> This transition plan will be updated to include stable version before the
> GenAI conventions are marked as stable.

GenAI instrumentations MAY capture user inputs sent to the model and responses received from it as [events](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/specification/logs/data-model.md#events).

> Note:
> Events are in-development and not yet available in some languages. Check [spec-compliance matrix](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.46.0/spec-compliance-matrix.md#logs) to see the implementation status in corresponding language.

Instrumentations MAY capture inputs and outputs if and only if application has enabled the collection of this data.
This is for three primary reasons:

1. Data privacy concerns. End users of GenAI applications may input sensitive information or personally identifiable information (PII) that they do not wish to be sent to a telemetry backend.
2. Data size concerns. Although there is no specified limit to sizes, there are practical limitations in programming languages and telemetry systems. Some GenAI systems allow for extremely large context windows that end users may take full advantage of.
3. Performance concerns. Sending large amounts of data to a telemetry backend may cause performance issues for the application.

Body fields that contain user input, model output, or other potentially sensitive and verbose data
SHOULD NOT be captured by default.

Semantic conventions for individual systems which extend content events SHOULD document all additional body fields and specify whether they
should be captured by default or need application to opt into capturing them.

Telemetry consumers SHOULD expect to receive unknown body fields.

Instrumentations SHOULD NOT capture undocumented body fields and MUST follow the documented defaults for known fields.
Instrumentations MAY offer configuration options allowing to disable events or allowing to capture all fields.

## Events

Is now described in the namespace registry.

## Custom events

System-specific events that are not covered in this document SHOULD be documented in corresponding Semantic Conventions extensions and
SHOULD follow `{gen_ai.provider.name}.*` naming pattern.

## Examples

### Chat completion

This is an example of telemetry generated for a chat completion call with system and user messages.

```mermaid
%%{init:
{
  "sequence": { "messageAlign": "left", "htmlLabels":true },
  "themeVariables": { "noteBkgColor" : "green", "noteTextColor": "black", "activationBkgColor": "green", "htmlLabels":true }
}
}%%
sequenceDiagram
    participant A as Application
    participant I as Instrumented Client
    participant M as Model
    A->>+I: #U+200D
    I->>M: gen_ai.system.message: You are a helpful bot<br/>gen_ai.user.message: Tell me a joke about OpenTelemetry
    Note left of I: GenAI Client span
    I-->M: gen_ai.choice: Why did the developer bring OpenTelemetry to the party? Because it always knows how to trace the fun!
    I-->>-A: #U+200D
```

**GenAI Client span:**

|   Attribute name                |                     Value                  |
|---------------------------------|--------------------------------------------|
| Span name                       | `"chat gpt-4"`                             |
| `gen_ai.provider.name`            | `"openai"`                                 |
| `gen_ai.request.model`          | `"gpt-4"`                                  |
| `gen_ai.request.max_tokens`     | `200`                                      |
| `gen_ai.request.top_p`          | `1.0`                                      |
| `gen_ai.response.id`            | `"chatcmpl-9J3uIL87gldCFtiIbyaOvTeYBRA3l"` |
| `gen_ai.response.model`         | `"gpt-4-0613"`                             |
| `gen_ai.usage.output_tokens`    | `47`                                       |
| `gen_ai.usage.input_tokens`     | `52`                                       |
| `gen_ai.response.finish_reasons`| `["stop"]`                                 |

**Events:**

1. `gen_ai.system.message`

   |   Property          |                     Value                             |
   |---------------------|-------------------------------------------------------|
   | `gen_ai.provider.name`| `"openai"`                                            |
   | Event body (with content enabled) | `{"content": "You're a helpful bot"}` |

2. `gen_ai.user.message`

   |   Property          |                     Value                             |
   |---------------------|-------------------------------------------------------|
   | `gen_ai.provider.name`| `"openai"`                                            |
   | Event body (with content enabled) | `{"content":"Tell me a joke about OpenTelemetry"}` |

3. `gen_ai.choice`

   |   Property          |                     Value                             |
   |---------------------|-------------------------------------------------------|
   | `gen_ai.provider.name`| `"openai"`                                            |
   | Event body (with content enabled) | `{"index":0,"finish_reason":"stop","message":{"content":"Why did the developer bring OpenTelemetry to the party? Because it always knows how to trace the fun!"}}` |
   | Event body (without content) | `{"index":0,"finish_reason":"stop","message":{}}` |

### Tools

This is an example of telemetry generated for a chat completion call with user message and function definition
that results in a model requesting application to call provided function. Application executes a function and
requests another completion now with the tool response.

```mermaid
%%{init:
{
  "sequence": { "messageAlign": "left", "htmlLabels":true },
  "themeVariables": { "noteBkgColor" : "green", "noteTextColor": "black", "activationBkgColor": "green", "htmlLabels":true }
}
}%%
sequenceDiagram
    participant A as Application
    participant I as Instrumented Client
    participant M as Model
    A->>+I: #U+200D
    I->>M: gen_ai.user.message: What's the weather in Paris?
    Note left of I: GenAI Client span 1
    I-->M: gen_ai.choice: Call to the get_weather tool with Paris as the location argument.
    I-->>-A: #U+200D
    A -->> A: parse tool parameters<br/>execute tool<br/>update chat history
    A->>+I: #U+200D
    I->>M: gen_ai.user.message: What's the weather in Paris?<br/>gen_ai.assistant.message: get_weather tool call<br/>gen_ai.tool.message: rainy, 57°F
    Note left of I: GenAI Client span 2
    I-->M: gen_ai.choice: The weather in Paris is rainy and overcast, with temperatures around 57°F
    I-->>-A: #U+200D
```

Here's the telemetry generated for each step in this scenario:

**GenAI Client span 1:**

|   Attribute name    |                     Value                             |
|---------------------|-------------------------------------------------------|
| Span name           | `"chat gpt-4"`                             |
| `gen_ai.provider.name`| `"openai"`                                            |
| `gen_ai.request.model`| `"gpt-4"`                                           |
| `gen_ai.request.max_tokens`| `200`                                          |
| `gen_ai.request.top_p`| `1.0`                                               |
| `gen_ai.response.id`| `"chatcmpl-9J3uIL87gldCFtiIbyaOvTeYBRA3l"`            |
| `gen_ai.response.model`| `"gpt-4-0613"`                                     |
| `gen_ai.usage.output_tokens`| `17`                                          |
| `gen_ai.usage.input_tokens`| `47`                                           |
| `gen_ai.response.finish_reasons`| `["tool_calls"]`                          |

  **Events**:

  All the following events are parented to the **GenAI chat span 1**.

  1. `gen_ai.user.message` (not reported when capturing content is disabled)

     |   Property          |                     Value                             |
     |---------------------|-------------------------------------------------------|
     | `gen_ai.provider.name`| `"openai"`                                            |
     | Event body          | `{"content":"What's the weather in Paris?"}` |

  2. `gen_ai.choice`

     |   Property          |                     Value                             |
     |---------------------|-------------------------------------------------------|
     | `gen_ai.provider.name`| `"openai"`                                            |
     | Event body (with content)    | `{"index":0,"finish_reason":"tool_calls","message":{"tool_calls":[{"id":"call_VSPygqKTWdrhaFErNvMV18Yl","function":{"name":"get_weather","arguments":"{\"location\":\"Paris\"}"},"type":"function"}]}` |
     | Event body (without content) | `{"index":0,"finish_reason":"tool_calls","message":{"tool_calls":[{"id":"call_VSPygqKTWdrhaFErNvMV18Yl","function":{"name":"get_weather"},"type":"function"}]}` |

**GenAI Client span 2:**

   |   Attribute name                |                     Value                             |
   |---------------------------------|-------------------------------------------------------|
   | Span name                       | `"chat gpt-4"`                                        |
   | `gen_ai.provider.name`            | `"openai"`                                            |
   | `gen_ai.request.model`          | `"gpt-4"`                                             |
   | `gen_ai.request.max_tokens`     | `200`                                                 |
   | `gen_ai.request.top_p`          | `1.0`                                                 |
   | `gen_ai.response.id`            | `"chatcmpl-call_VSPygqKTWdrhaFErNvMV18Yl"`            |
   | `gen_ai.response.model`         | `"gpt-4-0613"`                                        |
   | `gen_ai.usage.output_tokens`    | `52`                                                  |
   | `gen_ai.usage.input_tokens`     | `47`                                                  |
   | `gen_ai.response.finish_reasons`| `["stop"]`                                            |

  **Events**:

  All the following events are parented to the **GenAI chat span 2**.

  In this example, the event content matches the original messages, but applications may also drop messages or change their content.

  1. `gen_ai.user.message`

     |   Property                       |                     Value                                  |
     |----------------------------------|------------------------------------------------------------|
     | `gen_ai.provider.name`             | `"openai"`                                                 |
     | Event body                       | `{"content":"What's the weather in Paris?"}` |

  2. `gen_ai.assistant.message`

     |   Property                       |                     Value                                                                                                                  |
     |----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
     | `gen_ai.provider.name`             | `"openai"`                                                                                                                                 |
     | Event body (content enabled)     | `{"tool_calls":[{"id":"call_VSPygqKTWdrhaFErNvMV18Yl","function":{"name":"get_weather","arguments":"{\"location\":\"Paris\"}"},"type":"function"}]}` |
     | Event body (content not enabled) | `{"tool_calls":[{"id":"call_VSPygqKTWdrhaFErNvMV18Yl","function":{"name":"get_weather"},"type":"function"}]}`                 |

  3. `gen_ai.tool.message`

     |   Property                       |                     Value                                                                      |
     |----------------------------------|------------------------------------------------------------------------------------------------|
     | `gen_ai.provider.name`             | `"openai"`                                                                                     |
     | Event body (content enabled)     | `{"content":"rainy, 57°F","id":"call_VSPygqKTWdrhaFErNvMV18Yl"}` |
     | Event body (content not enabled) | `{"id":"call_VSPygqKTWdrhaFErNvMV18Yl"}`                                             |

  4. `gen_ai.choice`

     |   Property                       |                     Value                                                                                                     |
     |----------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
     | `gen_ai.provider.name`             | `"openai"`                                                                                                                    |
     | Event body (content enabled)     | `{"index":0,"finish_reason":"stop","message":{"content":"The weather in Paris is rainy and overcast, with temperatures around 57°F"}}` |
     | Event body (content not enabled) | `{"index":0,"finish_reason":"stop","message":{}}` |

### Chat completion with multiple choices

This example covers the scenario when user requests model to generate two completions for the same prompt :

```mermaid
%%{init:
{
  "sequence": { "messageAlign": "left", "htmlLabels":true },
  "themeVariables": { "noteBkgColor" : "green", "noteTextColor": "black", "activationBkgColor": "green", "htmlLabels":true }
}
}%%
sequenceDiagram
    participant A as Application
    participant I as Instrumented Client
    participant M as Model
    A->>+I: #U+200D
    I->>M: gen_ai.system.message - "You are a helpful bot"<br/>gen_ai.user.message - "Tell me a joke about OpenTelemetry"
    Note left of I: GenAI Client span
    I-->M: gen_ai.choice - Why did the developer bring OpenTelemetry to the party? Because it always knows how to trace the fun!<br/>gen_ai.choice - Why did OpenTelemetry get promoted? It had great span of control!
    I-->>-A: #U+200D
```

**GenAI Client Span**:

|   Attribute name    |                     Value                  |
|---------------------|--------------------------------------------|
| Span name           | `"chat gpt-4"`                             |
| `gen_ai.provider.name`| `"openai"`                                 |
| `gen_ai.request.model`| `"gpt-4"`                                |
| `gen_ai.request.max_tokens`| `200`                               |
| `gen_ai.request.top_p`| `1.0`                                    |
| `gen_ai.response.id`| `"chatcmpl-9J3uIL87gldCFtiIbyaOvTeYBRA3l"` |
| `gen_ai.response.model`| `"gpt-4-0613"`                          |
| `gen_ai.usage.output_tokens`| `77`                               |
| `gen_ai.usage.input_tokens`| `52`                                |
| `gen_ai.response.finish_reasons`| `["stop", "stop"]`             |

**Events**:

All events are parented to the GenAI chat span above.

1. `gen_ai.system.message`: the same as in the [Chat Completion](#chat-completion) example
2. `gen_ai.user.message`: the same as in the [Chat Completion](#chat-completion) example
3. `gen_ai.choice`

   |   Property                   |                     Value                             |
   |------------------------------|-------------------------------------------------------|
   | `gen_ai.provider.name`         | `"openai"`                                            |
   | Event body (content enabled) | `{"index":0,"finish_reason":"stop","message":{"content":"Why did the developer bring OpenTelemetry to the party? Because it always knows how to trace the fun!"}}` |

4. `gen_ai.choice`

   |   Property                   |                     Value                             |
   |------------------------------|-------------------------------------------------------|
   | `gen_ai.provider.name`         | `"openai"`                                            |
   | Event body (content enabled) | `{"index":1,"finish_reason":"stop","message":{"content":"Why did OpenTelemetry get promoted? It had great span of control!"}}` |

[DocumentStatus]: https://opentelemetry.io/docs/specs/otel/document-status
