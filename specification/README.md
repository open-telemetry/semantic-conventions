# OpenTelemetry Semantic Conventions

The Semantic Conventions define a common set of (semantic) attributes which provide meaning to data when collecting, producing and consuming it.
The Semantic Conventions specify among other things span names and kind, metric instruments and units as well as attribute names, types, meaning and valid values. For a detailed definition of the Semantic Conventions' scope see [Semantic Conventions Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability).
The benefit to using Semantic Conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms. This allows easier correlation and consumption of data.

Semantic Conventions are defined for the following areas:

* [General](general/README.md): General Semantic Conventions.
* [Exceptions](exceptions/README.md): Semantic Conventions for Exceptions.
* [FaaS](faas/README.md): Semantic Conventions for Function as a Service (FaaS) operations.
* [CloudEvents](cloudevents/README.md): Semantic Conventions for the CloudEvents specification.
* [Feature Flags](http/README.md): Semantic Conventions for feature flag evaluations.
* [HTTP](http/README.md): Semantic Conventions for HTTP client and server operations.
* [Database](database/README.md): Semantic Conventions for database operations.
* [System](system/README.md): System Semantic Conventions.
* *Other areas can be found in the signal specific Semantic Conventions below*

Semantic Conventions by signals:

* [Resource](resource/semantic_conventions/README.md): Semantic Conventions for resources.
* [Trace](general/trace-general.md): Semantic Conventions for traces and spans.
* [Metrics](general/metrics-general.md): Semantic Conventions for metrics.
* [Logs](general/logs-general.md): Semantic Conventions for logs data.
* [Events](general/events-general.md): Semantic Conventions for event data.
