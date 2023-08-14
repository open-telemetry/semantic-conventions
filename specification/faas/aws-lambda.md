# Instrumenting AWS Lambda

**Status**: [Experimental][DocumentStatus]

This document defines how to apply semantic conventions when instrumenting an AWS Lambda request handler. AWS
Lambda largely follows the conventions for [FaaS][faas] while [HTTP](/specification/http/http-spans.md) conventions are also
applicable when handlers are for HTTP requests.

There are a variety of triggers for Lambda functions, and this document will grow over time to cover all the
use cases.

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i specification/faas/aws-lambda.md` -->

<!-- toc -->

- [All triggers](#all-triggers)
  * [Determining the remote parent span context](#determining-the-remote-parent-span-context)
    + [Composite EventToCarrier](#composite-eventtocarrier)
- [API Gateway](#api-gateway)
- [SQS](#sqs)
  * [SQS Event](#sqs-event)
  * [SQS Message](#sqs-message)
- [Examples](#examples)
  * [API Gateway Request Proxy (Lambda tracing passive)](#api-gateway-request-proxy-lambda-tracing-passive)
  * [API Gateway Request Proxy (Lambda tracing active)](#api-gateway-request-proxy-lambda-tracing-active)
  * [SQS (Lambda tracing passive)](#sqs-lambda-tracing-passive)
  * [SQS (Lambda tracing active)](#sqs-lambda-tracing-active)
- [Resource Detector](#resource-detector)

<!-- tocstop -->

## All triggers

For all events, a span with kind `SERVER` MUST be created corresponding to the function invocation unless stated
otherwise below. Unless stated otherwise below, the name of the span MUST be set to the function name from the
Lambda `Context`.

The following attributes SHOULD be set:

- [`faas.invocation_id`][faas] - The value of the AWS Request ID, which is always available through an accessor on the Lambda `Context`.
- [`cloud.account.id`][cloud] - In some languages, this is available as an accessor on the Lambda `Context`. Otherwise, it can be parsed from the ARN as the fifth item when splitting on `:`

Also consider setting other attributes of the [`faas` resource][faasres] and [trace][faas] conventions
and the [cloud resource conventions][cloud]. The following AWS Lambda-specific attribute MAY also be set:

<!-- semconv aws.lambda -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `aws.lambda.invoked_arn` | string | The full invoked ARN as provided on the `Context` passed to the function (`Lambda-Runtime-Invoked-Function-Arn` header on the `/runtime/invocation/next` applicable). [1] | `arn:aws:lambda:us-east-1:123456:function:myfunction:myalias` | Recommended |

**[1]:** This may be different from `cloud.resource_id` if an alias is involved.
<!-- endsemconv -->

[faas]: faas-spans.md (FaaS trace conventions)
[faasres]: /specification/resource/semantic_conventions/faas.md (FaaS resource conventions)
[cloud]: /specification/resource/semantic_conventions/cloud.md (Cloud resource conventions)

### Determining the remote parent span context

Lambda does not have HTTP headers to read from and instead stores the headers it was invoked with (including any propagated context, etc.) as part of the invocation event. If using AWS X-Ray tracing then the trace context is instead stored in the Lambda environment. It is also possible that both options are populated at the same time, with different values. Finally it is also possible to propagate tracing information in a SQS message using the system attribute of the message `AWSTraceHeader`. A single lambda function can be triggered from multiple sources, however spans can only have a single parent.

To determine the parent span context, the lambda instrumentation SHOULD use a `EventToCarrier`. `EventToCarrier` defines how the instrumentation should prepare a `Carrier` to be used by subsequent `TextMapPropagators`.

The `EventToCarrier` MUST implement the `Convert` operation to convert a lammbda `Event` into a `Carrier`.

The `Convert` operation MUST have the following parameters:
  `Carrier` - the carrier that will be populated from the `Event`
  `Event` - the lambda event.

#### Composite EventToCarrier

Implementations MUST provide a facility to group multiple `EventToCarrier`s. A composite `EventToCarrier` can be built from a list of `EventToCarrier`s. The resulting composite `EventToCarrier` will invoke the `Convert` operation of each individual `EventToCarrier` in the order they were specified, sequentially updating the carrier.

The list of `EventToCarrier`s passed to the composite `EventToCarrier` MUST be configured using the `OTEL_AWS_LAMBDA_EVENT_TO_CARRIERS`, as a comma separated list of values.

Valid values to configure the composite `EventToCarrier` are:

* `lambda_runtime` - populates the `Carrier` with a key `X-Amzn-Trace-Id` from the value of the `_X_AMZN_TRACE_ID` environment variable. (see note below)
* `http_headers` = populates the `Carrier` with the content of the http headers.
* `sqs` - populate the carrier with the content of the `AWSTraceHeader` system attribute of the message.

**NOTE**: When instrumenting a Java AWS Lambda, instrumentation SHOULD first try to parse the `X-Amzn-Trace-Id` out of the system property `com.amazonaws.xray.traceHeader` before checking and attempting to parse the environment variable `_X_AMZN_TRACE_ID`.

## API Gateway

API Gateway allows a user to trigger a Lambda function in response to HTTP requests. It can be configured to be
a pure proxy, where the information about the original HTTP request is passed to the Lambda function, or as a
configuration for a REST API, in which case only a deserialized body payload is available.  In the case the API
gateway is configured to proxy to the Lambda function, the instrumented request handler will have access to all
the information about the HTTP request in the form of an API Gateway Proxy Request Event.

The Lambda span name and the [`http.route` span attribute](/specification/http/http-spans.md#http-server-semantic-conventions) SHOULD
be set to the [resource property][] from the proxy request event, which corresponds to the user configured HTTP
route instead of the function name.

[`faas.trigger`][faas] MUST be set to `http`. [HTTP attributes](/specification/http/http-spans.md) SHOULD be set based on the
available information in the Lambda event initiated by the proxy request. `http.scheme` is available as the
`x-forwarded-proto` header in the Lambda event. Refer to the [input event format][] for more details.

[resource property]: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
[input event format]: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

## SQS

Amazon Simple Queue Service (SQS) is a message queue that triggers a Lambda function with a batch of messages.
So we consider processing both of a batch and of each individual message. The function invocation span MUST
correspond to the SQS event, which is the batch of messages. For each message, an additional span SHOULD be
created to correspond with the handling of the SQS message. Because handling of a message will be inside user
business logic, not the Lambda framework, automatic instrumentation mechanisms without code change will often
not be able to instrument the processing of the individual messages. Instrumentation SHOULD provide utilities
for creating message processing spans within user code.

The span kind for both types of SQS spans MUST be `CONSUMER`.

### SQS Event

For the SQS event span, if all the messages in the event have the same event source, the name of the span MUST
be `<event source> process`. If there are multiple sources in the batch, the name MUST be
`multiple_sources process`. The parent MUST be the `SERVER` span corresponding to the function invocation.

For every message in the event, the [message system attributes][] (not message attributes, which are provided by
the user) SHOULD be checked for the key `AWSTraceHeader`. If it is present, an OpenTelemetry `Context` SHOULD be
parsed from the value of the attribute using the [AWS X-Ray Propagator](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.21.0/specification/context/api-propagators.md) and
added as a link to the span. This means the span may have as many links as messages in the batch.
See [compatibility](../../supplementary-guidelines/compatibility/aws.md#context-propagation) for more info.

- [`faas.trigger`][faas] MUST be set to `pubsub`.
- [`messaging.operation`](/specification/messaging/messaging-spans.md) MUST be set to `process`.
- [`messaging.system`](/specification/messaging/messaging-spans.md) MUST be set to `AmazonSQS`.
- [`messaging.destination.kind` or `messaging.source.kind`](/specification/messaging/messaging-spans.md#messaging-attributes) MUST be set to `queue`.

### SQS Message

For the SQS message span, the name MUST be `<event source> process`.  The parent MUST be the `CONSUMER` span
corresponding to the SQS event. The [message system attributes][] (not message attributes, which are provided by
the user) SHOULD be checked for the key `AWSTraceHeader`. If it is present, an OpenTelemetry `Context` SHOULD be
parsed from the value of the attribute using the [AWS X-Ray Propagator](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.21.0/specification/context/api-propagators.md) and
added as a link to the span.
See [compatibility](../../supplementary-guidelines/compatibility/aws.md#context-propagation) for more info.

- [`faas.trigger`][faas] MUST be set to `pubsub`.
- [`messaging.operation`](/specification/messaging/messaging-spans.md#messaging-attributes) MUST be set to `process`.
- [`messaging.system`](/specification/messaging/messaging-spans.md#messaging-attributes) MUST be set to `AmazonSQS`.

Other [Messaging attributes](/specification/messaging/messaging-spans.md#messaging-attributes) SHOULD be set based on the available information in the SQS message
event.

Note that `AWSTraceHeader` is the only supported mechanism for propagating `Context` in instrumentation for SQS
to prevent conflicts with other sources. Notably, message attributes (user-provided, not system) are not supported -
the linked contexts are always expected to have been sent as HTTP headers of the `SQS.SendMessage` request that
the message originated from. This is a function of AWS SDK instrumentation, not Lambda instrumentation.

Using the `AWSTraceHeader` ensures that propagation will work across AWS services that may be integrated to
Lambda via SQS, for example a flow that goes through S3 -> SNS -> SQS -> Lambda. `AWSTraceHeader` is only a means
of propagating context and not tied to any particular observability backend. Notably, using it does not imply
using AWS X-Ray - any observability backend will fully function using this propagation mechanism.

[message system attributes]: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-message-metadata.html#sqs-message-system-attributes

## Examples

### API Gateway Request Proxy (Lambda tracing passive)

Given a process C that sends an HTTP request to an API Gateway endpoint with path `/pets/{petId}` configured for
a Lambda function F:

```
Process C: | Span Client        |
--
Function F:    | Span Function |
```

| Field or Attribute | `Span Client` | `Span Function` |
|-|-|-|
| Span name | `HTTP GET` | `/pets/{petId}` |
| Parent |  | Span Client |
| SpanKind | `CLIENT` | `SERVER` |
| Status | `Ok` | `Ok` |
| `faas.invocation_id` | | `79104EXAMPLEB723` |
| `faas.trigger` | | `http` |
| `cloud.account.id` | | `12345678912` |
| `server.address` | `foo.execute-api.us-east-1.amazonaws.com` |  |
| `server.port` | `413` |  |
| `http.request.method` | `GET` | `GET` |
| `user_agent.original` | `okhttp 3.0` | `okhttp 3.0` |
| `url.scheme` | | `https` |
| `url.path` | | `/pets/10` |
| `http.route` | | `/pets/{petId}` |
| `http.response.status_code` | `200` | `200` |

### API Gateway Request Proxy (Lambda tracing active)

Active tracing in Lambda means an API Gateway span `Span APIGW` and a Lambda runtime invocation span `Span Lambda`
will be exported to AWS X-Ray by the infrastructure (not instrumentation). All attributes above are the same
except that in this case, the parent of `APIGW` is `Span Client` and the parent of `Span Function` is
`Span Lambda`. This means the hierarchy looks like:

```
Span Client --> Span APIGW --> Span Lambda --> Span Function
```

### SQS (Lambda tracing passive)

Given a process P, that sends two messages to a queue Q on SQS, and a Lambda function F, which processes both of them in one batch (Span ProcBatch) and
generates a processing span for each message separately (Spans Proc1 and Proc2).

```
Process P: | Span Prod1 | Span Prod2 |
--
Function F:                      | Span ProcBatch |
                                        | Span Proc1 |
                                               | Span Proc2 |
```

| Field or Attribute | Span Prod1 | Span Prod2 | Span ProcBatch | Span Proc1 | Span Proc2 |
|-|-|-|-|-|-|
| Span name | `Q send` | `Q send` | `Q process` | `Q process` | `Q process` |
| Parent |  |  |  | Span ProcBatch | Span ProcBatch |
| Links |  |  |  | Span Prod1 | Span Prod2 |
| SpanKind | `PRODUCER` | `PRODUCER` | `CONSUMER` | `CONSUMER` | `CONSUMER` |
| Status | `Ok` | `Ok` | `Ok` | `Ok` | `Ok` |
| `messaging.system` | `AmazonSQS` | `AmazonSQS` | `AmazonSQS` | `AmazonSQS` | `AmazonSQS` |
| `messaging.destination.name` | `Q` | `Q` | | | |
| `messaging.source.name` | | | `Q` | `Q` | `Q` |
| `messaging.destination.kind` | `queue` | `queue` | | | |
| `messaging.source.kind` | | | `queue` | `queue` | `queue` |
| `messaging.operation` |  |  | `process` | `process` | `process` |
| `messaging.message.id` | | | | `"a1"` | `"a2"` |

Note that if Span Prod1 and Span Prod2 were sent to different queues, Span ProcBatch would not have
`messaging.source.name` set as it would correspond to multiple sources.

The above requires user code change to create `Span Proc1` and `Span Proc2`. In Java, the user would inherit from
[TracingSqsMessageHandler][] instead of Lambda's standard `RequestHandler` to enable them. Otherwise these two spans
would not exist.

[TracingSqsMessageHandler]: https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/v1.0.1/instrumentation/aws-lambda-1.0/library/src/main/java/io/opentelemetry/instrumentation/awslambda/v1_0/TracingSqsMessageHandler.java

### SQS (Lambda tracing active)

Active tracing in Lambda means a Lambda runtime invocation span `Span Lambda` will be exported to X-Ray by the
infrastructure (not instrumentation). In this case, all of the above is the same except `Span ProcBatch` will
have a parent of `Span Lambda`. This means the hierarchy looks like:

```
Span Lambda --> Span ProcBatch --> Span Proc1 (links to Span Prod1 and Span Prod2)
                               \-> Span Proc2 (links to Span Prod1 and Span Prod2)
```

## Resource Detector

AWS Lambda resource information is available as [environment variables][] provided by the runtime.

- [`cloud.provider`][cloud] MUST be set to `aws`
- [`cloud.region`][cloud] MUST be set to the value of the `AWS_REGION` environment variable
- [`faas.name`][faasres] MUST be set to the value of the `AWS_LAMBDA_FUNCTION_NAME` environment variable
- [`faas.version`][faasres] MUST be set to the value of the `AWS_LAMBDA_FUNCTION_VERSION` environment variable

Note that [`cloud.resource_id`][cloud] currently cannot be populated as a resource
because it is not available until function invocation.

[environment variables]: https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-runtime

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.21.0/specification/document-status.md
