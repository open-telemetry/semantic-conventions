# Observability for Non-Executed (Decision-Only) Operations

## Overview

In many real-world systems, requests or operations are evaluated but
intentionally **not executed**.

Common examples include policy denials, safety gates, compliance holds,
approval workflows, and quota enforcement. In these cases, the system
reaches a valid outcome without performing downstream work.

Today, such **decision-only outcomes** are often missing from traces or
represented inconsistently, despite being critical for auditability,
incident analysis, and explainability.

This document clarifies that non-executed operations are valid
observability targets and provides guidance on representing them using
existing OpenTelemetry concepts.

---

## Why This Matters

Non-executed outcomes are frequently more important than successful
execution paths:

- From an audit or compliance perspective, *why something did not run*
  is often the primary question.
- From an operational perspective, blocked or denied requests may
  indicate misconfiguration, policy drift, or emerging incidents.
- From an explainability perspective, silently dropped decisions reduce
  trust and make post-incident analysis difficult.

If these outcomes are not consistently observable, systems lose
important decision context even though a meaningful outcome occurred.

---

## Scope and Non-Goals

This guidance is intentionally minimal in scope.

**In scope:**
- Clarifying that decision-only outcomes are valid observability events
- Documenting common patterns using existing spans, events, and
  attributes

**Out of scope:**
- Introducing new signal types
- Mandating specific attribute names or schemas
- Defining domain-specific policy or security semantics
- Changing the OpenTelemetry data model

The goal is to document and normalize existing best practices, not to
prescribe a single implementation.

---

## Decision-Only Operations as Observability Targets

An operation does not need to perform downstream work to be observable.

If a system:
- evaluates a request,
- reaches a decision (e.g. allow, deny, hold),
- and produces a meaningful outcome,

then that decision point represents a valid unit of work for
observability purposes.

Whether represented as a span, an event, or metadata on an existing
span, the key requirement is that the decision outcome is **explicitly
recorded** and not lost due to non-execution.

---

## Relationship to Existing Concepts

Decision-only observability fits naturally within existing
OpenTelemetry concepts:

- **Spans** may represent evaluation or decision phases, even if no
  downstream execution occurs.
- **Events** may record blocked or denied outcomes on long-running or
  parent spans.
- **Attributes** may capture outcome, reason, or classification details
  without introducing new semantic domains.

This guidance does not require extending the OpenTelemetry specification;
it clarifies how current concepts can be applied consistently.

---

## Next Steps

This document establishes a shared understanding that non-executed
operations are first-class observability concerns.

Follow-up documentation may provide concrete examples illustrating
common representation patterns, while remaining implementation-neutral.

Community feedback is encouraged to ensure this guidance aligns with
existing usage and expectations.
