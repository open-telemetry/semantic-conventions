# OpenTelemetry Semantic Conventions

The Semantic Conventions define a common set of (semantic) attributes which provide meaning to data when collecting, producing and consuming it.
The Semantic Conventions specify among other things span names and kind, metric instruments and units as well as attribute names, types, meaning and valid values. For a detailed definition of the Semantic Conventions' scope see [Semantic Conventions Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability).
The benefit to using Semantic Conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms. This allows easier correlation and consumption of data.

Semantic Conventions are defined for the following areas:

* **[General](general/README.md): General Semantic Conventions**.
* [CloudEvents](cloudevents/README.md): Semantic Conventions for the CloudEvents specification.
* [Cloud Providers](cloud-providers/README.md): Semantic Conventions for cloud providers libraries.
* [Database](database/README.md): Semantic Conventions for database operations.
* [Exceptions](exceptions/README.md): Semantic Conventions for exceptions.
* [FaaS](faas/README.md): Semantic Conventions for Function as a Service (FaaS) operations.
* [Feature Flags](feature-flags/README.md): Semantic Conventions for feature flag evaluations.
* [HTTP](http/README.md): Semantic Conventions for HTTP client and server operations.
* [Messaging](messaging/README.md): Semantic Conventions for messaging operations and systems.
* [Object Stores](object-stores/README.md): Semantic Conventions for object stores operations.
* [RPC](rpc/README.md): Semantic Conventions for RPC client and server operations.
* [System](system/README.md): System Semantic Conventions.

Semantic Conventions by signals:

* [Events](general/events-general.md): Semantic Conventions for event data.
* [Logs](general/logs-general.md): Semantic Conventions for logs data.
* [Metrics](general/metrics-general.md): Semantic Conventions for metrics.
* [Resource](resource/README.md): Semantic Conventions for resources.
* [Trace](general/trace-general.md): Semantic Conventions for traces and spans.
