# T-shaped Signals

Semantic Conventions approaches observability with a T-shaped mindset. This
splits signals into two types of a "T" shape:

```mermaid
block-beta
        columns 3
          Broad["Broadly Applicable Signals"]:3
        columns 3
          space:1
          Deep("Rich,\nDeep\nSignals")
          space:1
```

This matches an 80-20 rule, where 80% of users (or use-cases) can leverage the
broadly applicable signals and 20% of users (or use-cases) will dive deeply into
a problem with deep signals.

## Broadly Applicable Signals

These are conventions meant to provide a baseline observability experience
across a domain. An example includes HTTP semantic conventions that allow
general-purpose dashboarding, alerting, and diagnostics for HTTP
(micro-)services. These signals should provide "horizontal" coverage for
observability.

Examples include:

- Golden Signals / RED metrics (Saturation, Rate, Error, Duration)
- High Level Spans
- Error logs, Crash reports
- Request/Response logs

## Rich, Deep Signals

These are conventions meant to provide deep understanding of a specific
system, library, module, application or service. These are used to diagnose
issues specific to that system.

Examples include:

- Linux slab memory usage
- Specific database signals, e.g MySQL index usage
- Language-specific Garbage Collection metrics (JVM, Go, .NET, etc.)

## Recommendations

Defining semantic conventions is a balance between generating
broadly applicable signals and ensuring rich observability for a specific
technology. It is recommended to start with the *broad* use cases and signals
for a particular domain first. After providing a baseline set of signals for
that domain, then explore deeper integrations that may be vendor or
implementation specific.

For example, see [Database semantic conventions](/docs/db/README.md) where
there is general guidance for spans about communicating with a database, and
additionally there is database-specific guidance as an extension of the general.
