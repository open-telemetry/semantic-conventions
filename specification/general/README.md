# General Semantic Conventions

This document defines general Semantic Conventions for spans, metrics, logs and events.

The following general Semantic Conventions are defined:

* [General attributes](general-attributes.md): General semantic attributes.
* [Spans](trace-general.md): General Semantic Conventions for traces / spans.
* [Metrics](metrics-general.md): General Semantic Conventions for metrics.
* [Logs](logs-general.md): General Semantic Conventions for logs.
* [Events](events-general.md): General Semantic Conventions for events.

## Event Name Reuse Prohibition

A new event MUST NOT be added with the same name as an event that existed in
the past but was renamed (with a corresponding schema file).

When introducing a new event name check all existing schema files to make sure
the name does not appear as a key of any "rename_events" section (keys denote
old event names in rename operations).
