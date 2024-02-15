# Semantic Conventions for Android Activity creation Spans

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for Android Spans related to the creation of an [Activity](https://developer.android.com/reference/android/app/Activity).

Ensuring that an Activity subclass takes a reasonable amount of time to get started, hence displaying a screen initial content as fast as possible, is important to provide a good user experience. The spans
mentioned in this document are meant to cover all Activity-creation related methods in order to provide a screen's overall screen rendering time.

There are 3 methods that are relevant to measure the time it takes for an Activity to get created, those are: `onCreate`, `onStart`, and `onResume`. Each of
those will be called sequentially in that order, therefore, to cover an Activity creation, a span MUST be created for each
of the those 3 methods per Activity.

## Name

For each of the 3 spans, their names MUST start with the method name, followed by the screen name if available:

```
<method name> [<screen name whenever available>]
```

For example, for the creation of an Activity with screen name "Home", the 3 span names would look like the following: `onCreate Home`, `onStart Home`, and `onResume Home`.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
