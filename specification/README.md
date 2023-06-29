# OpenTelemetry Semantic Conventions

The Semantic Conventions define a common set of (semantic) attributes which provide meaning to data when collecting, producing and consuming it.
The Semantic Conventions specify among other things span names and kind, metric instruments and units as well as attribute names, types, meaning and valid values. For a detailed definition of the Semantic Conventions' scope see [Semantic Conventions Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability).
The benefit to using Semantic Conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms. This allows easier correlation and consumption of data.

Semantic Conventions are defined for the following areas:

* [HTTP](http/README.md): Semantic Conventions for HTTP client and server operations.
* *Other areas can be found in the signal specific Semantic Conventions below*

Semantic Conventions by signals:

* [Resource](resource/semantic_conventions/README.md): Semantic Conventions for resources.
* [Trace](trace/semantic_conventions/README.md): Semantic Conventions for traces and spans.
* [Metrics](metrics/semantic_conventions/README.md): Semantic Conventions for metrics.
* [Logs](logs/semantic_conventions/README.md): Semantic Conventions for logs and event data.
