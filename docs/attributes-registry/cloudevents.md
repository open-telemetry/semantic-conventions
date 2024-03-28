<!--- Hugo front matter used to generate the website version of this page:
--->

# CloudEvents

## CloudEvents Attributes

<!-- semconv registry.cloudevents(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `cloudevents.event_id` | string | The [event_id](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id) uniquely identifies the event. | `123e4567-e89b-12d3-a456-426614174000`; `0001` |
| `cloudevents.event_source` | string | The [source](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1) identifies the context in which an event happened. | `https://github.com/cloudevents`; `/cloudevents/spec/pull/123`; `my-service` |
| `cloudevents.event_spec_version` | string | The [version of the CloudEvents specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#specversion) which the event uses. | `1.0` |
| `cloudevents.event_subject` | string | The [subject](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#subject) of the event in the context of the event producer (identified by source). | `mynewfile.jpg` |
| `cloudevents.event_type` | string | The [event_type](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type) contains a value describing the type of event related to the originating occurrence. | `com.github.pull_request.opened`; `com.example.object.deleted.v2` |
<!-- endsemconv -->
