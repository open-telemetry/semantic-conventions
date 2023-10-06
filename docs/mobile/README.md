<!--- Hugo front matter used to generate the website version of this page:
linkTitle: mobile
path_base_for_github_subdir:
  from: content/en/docs/specs/semconv/mobile/_index.md
  to: mobile/README.md
--->

# Semantic Convention for Mobile Platform

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for mobile platform spans, metrics and logs.

Semantic conventions for the mobile platform are defined for the following signals:

* [Mobile Events](events.md) : Semantic Conventions for mobile events in *logs*.
  * All events MUST set `event.domain` as `device`

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
