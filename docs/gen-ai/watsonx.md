<!--- Hugo front matter used to generate the website version of this page:
linkTitle: IBM WatsonX AI
--->

# IBM WatsonX AI

**Status**: [Experimental](../document-status.md)

This document defines semantic conventions for IBM WatsonX AI.

## Attributes

The following attributes are specific to IBM WatsonX AI:

| Attribute | Type | Description | Examples | Requirement Level |
| --- | --- | --- | --- | --- |
| `gen_ai.watsonx.request.project_id` | string | The project ID in IBM WatsonX AI | `12345678-abcd-1234-efgh-1234567890ab` | Conditionally Required [1] |
| `gen_ai.watsonx.request.space_id` | string | The space ID in IBM WatsonX AI | `abcdef12-3456-7890-abcd-ef1234567890` | Conditionally Required [1] |
| `gen_ai.watsonx.request.version` | string | The version of the model being used | `1.0`, `2.3.1` | Recommended |
| `gen_ai.watsonx.response.trace_id` | string | The trace ID returned by IBM WatsonX AI | `wxt-12345678-abcd-1234-efgh-1234567890ab` | Conditionally Required [2] |

**[1]**: If the request includes this information.

**[2]**: If the response was received and includes a trace ID.

## Spans

### IBM WatsonX AI Client

**Span kind**: [Client](../../specification/trace/api.md#spankind)

| Attribute | Type | Description | Examples | Requirement Level |
| --- | --- | --- | --- | --- |
| `gen_ai.system` | string | The GenAI system identifier | `ibm.watsonx.ai` | Required |
| `gen_ai.request.model` | string | The name of the GenAI model a request is being made to | `ibm/granite-13b-chat-v2` | Required |
| `gen_ai.operation.name` | string | The name of the operation being performed | `chat`, `embeddings` | Required |
| `gen_ai.watsonx.request.project_id` | string | The project ID in IBM WatsonX AI | `12345678-abcd-1234-efgh-1234567890ab` | Conditionally Required [1] |
| `gen_ai.watsonx.request.space_id` | string | The space ID in IBM WatsonX AI | `abcdef12-3456-7890-abcd-ef1234567890` | Conditionally Required [1] |
| `gen_ai.watsonx.request.version` | string | The version of the model being used | `1.0`, `2.3.1` | Recommended |
| `gen_ai.watsonx.response.trace_id` | string | The trace ID returned by IBM WatsonX AI | `wxt-12345678-abcd-1234-efgh-1234567890ab` | Conditionally Required [2] |
| `llm.watsonx.decoding_method` | string | The decoding method used by WatsonX for generating responses | `greedy`, `sample` | Recommended |
| `llm.watsonx.random_seed` | int | The random seed used by WatsonX for deterministic generation | `42` | Recommended |
| `llm.watsonx.max_new_tokens` | int | The maximum number of new tokens to generate in the response | `100` | Recommended |
| `llm.watsonx.min_new_tokens` | int | The minimum number of new tokens to generate in the response | `10` | Recommended |
| `llm.watsonx.repetition_penalty` | double | The penalty applied to repeated tokens in the generated response | `1.2` | Recommended |
| `gen_ai.usage.input_tokens` | int | The number of tokens used in the prompt sent to IBM WatsonX AI | `100` | Recommended |
| `gen_ai.usage.output_tokens` | int | The number of tokens used in the completions from IBM WatsonX AI | `180` | Recommended |

**[1]**: If the request includes this information.

**[2]**: If the response was received and includes a trace ID.

## Metrics

The following metrics are specific to IBM WatsonX AI:

| Metric Name | Description | Unit | Instrument | Attribute Key | Attribute Values | Requirement Level |
| --- | --- | --- | --- | --- | --- | --- |
| `llm.watsonx.completions.duration` | Measures the duration of WatsonX completions operations | s | Histogram | | | Recommended |
| `llm.watsonx.completions.exceptions` | Counts the number of exceptions that occurred during WatsonX completions operations | {exception} | Counter | | | Recommended |
| `llm.watsonx.completions.responses` | Counts the number of responses received from WatsonX completions operations | {response} | Counter | | | Recommended |
| `llm.watsonx.completions.tokens` | Counts the number of tokens processed in WatsonX completions operations | {token} | Counter | `gen_ai.token.type` | `input`, `output` | Required |

## Common Models

IBM WatsonX AI provides several foundation models. Here are some common models:

| Model Name | Description |
| --- | --- |
| `ibm/granite-13b-chat-v2` | IBM's Granite 13B chat model |
| `ibm/granite-13b-instruct-v2` | IBM's Granite 13B instruct model |
| `ibm/mpt-7b-instruct` | MPT 7B instruct model |
| `ibm/flan-ul2` | Flan UL2 model |
| `meta-llama/llama-2-70b-chat` | Meta's Llama 2 70B chat model |
| `bigcode/starcoder` | StarCoder model for code generation |

## Examples

### Tracing a chat completion request to IBM WatsonX AI

```python
# Example using hypothetical OpenTelemetry instrumentation for WatsonX
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
import watsonx

tracer = trace.get_tracer("example-watsonx-client")

with tracer.start_as_current_span(
    "watsonx.chat",
    kind=trace.SpanKind.CLIENT,
    attributes={
        "gen_ai.system": "ibm.watsonx.ai",
        "gen_ai.operation.name": "chat",
        "gen_ai.request.model": "ibm/granite-13b-chat-v2",
        "gen_ai.watsonx.request.project_id": "12345678-abcd-1234-efgh-1234567890ab",
        "gen_ai.watsonx.request.space_id": "abcdef12-3456-7890-abcd-ef1234567890",
        "gen_ai.request.temperature": 0.7,
        "llm.watsonx.decoding_method": "greedy",
        "llm.watsonx.max_new_tokens": 100,
        "llm.watsonx.min_new_tokens": 10,
        "llm.watsonx.repetition_penalty": 1.2,
        "llm.watsonx.random_seed": 42,
    }
) as span:
    try:
        response = watsonx.chat.completions.create(
            model="ibm/granite-13b-chat-v2",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"}
            ],
            temperature=0.7,
            project_id="12345678-abcd-1234-efgh-1234567890ab",
            space_id="abcdef12-3456-7890-abcd-ef1234567890",
            decoding_method="greedy",
            max_new_tokens=100,
            min_new_tokens=10,
            repetition_penalty=1.2,
            random_seed=42
        )
        
        # Add response attributes
        span.set_attribute("gen_ai.response.id", response.id)
        span.set_attribute("gen_ai.response.model", response.model)
        span.set_attribute("gen_ai.response.finish_reasons", response.choices[0].finish_reason)
        span.set_attribute("gen_ai.usage.input_tokens", response.usage.prompt_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", response.usage.completion_tokens)
        
        if hasattr(response, "trace_id"):
            span.set_attribute("gen_ai.watsonx.response.trace_id", response.trace_id)
            
        span.set_status(Status(StatusCode.OK))
    except Exception as e:
        span.set_status(Status(StatusCode.ERROR, str(e)))
        span.record_exception(e)
        raise
