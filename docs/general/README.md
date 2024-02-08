<!--- Hugo front matter used to generate the website version of this page:
linkTitle: General
path_base_for_github_subdir:
  from: tmp/semconv/docs/general/_index.md
  to: general/README.md
weight: -1
--->

# General Semantic Conventions

This document defines general Semantic Conventions for spans, metrics, logs and events.

The following general Semantic Conventions are defined:

* **[General attributes](attributes.md): General semantic attributes**.
* [Events](events.md): General Semantic Conventions for events.
* [Logs](logs.md): General Semantic Conventions for logs.
* [Metrics](metrics.md): General Semantic Conventions for metrics.
* [Spans](trace.md): General Semantic Conventions for traces / spans.

## Event Name Reuse Prohibition

A new event MUST NOT be added with the same name as an event that existed in
the past but was renamed (with a corresponding schema file).

When introducing a new event name check all existing schema files to make sure
the name does not appear as a key of any "rename_events" section (keys denote
old event names in rename operations).
