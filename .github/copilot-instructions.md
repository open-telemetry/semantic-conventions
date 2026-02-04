# Copilot Instructions for OpenTelemetry Semantic Conventions

## Overview

These instructions guide AI assistants in reviewing pull requests for the
OpenTelemetry Semantic Conventions repository. Follow these guidelines to
ensure consistency, quality, and adherence to established standards.

This repository contains semantic conventions supported by the OpenTelemetry ecosystem.

**CRITICAL REVIEW CRITERIA**: New areas require special scrutiny and must meet
these requirements:

### Prerequisites for New Convention Areas

- **Domain Expertise**: Must have a group of people familiar with the domain
- **Active Involvement**: Contributors must be involved with instrumentation
  efforts in that area
- **Long-term Commitment**: Must have committed maintainers to be point of contact for:
  pull requests, issues, question, ongoing maintenance

### Process for New Areas

1. **Project Management**: Follow [OpenTelemetry project management](https://github.com/open-telemetry/community/blob/main/project-management.md) guidelines
2. **Codeowners**: New areas MUST have assigned codeowners

## General Review Principles

- **YAML Models**: All attributes, metrics, and conventions are formally defined
  in YAML files under `model/` directory
  - Validate against [schema](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv.schema.json)
  - Verify all new conventions are documented with clear `brief` and `note` sections
  - Validate that examples are realistic and helpful
  - Confirm proper use of RFC 2119 keywords (MUST, SHOULD, MAY, etc.)
- **Scope**: ensure contributions belong here:
  - **SHOULD be included:**
    - Instrumentations hosted in OpenTelemetry
    - Common attributes and conventions used across multiple instrumentations
    - Conventions that benefit from centralized policy enforcement
  - **SHOULD NOT be included:**
    - Instrumentations following external schemas not fully compatible with OpenTelemetry
    - Domain-specific conventions better maintained in their own repositories

### Naming Conventions

- **Attributes/Metrics/Events**: Use lowercase with dot-separated namespaces
  (e.g., `service.name`)
- **Multi-word components**: Use snake_case (e.g., `http.response.status_code`)
- **Abbreviations**: Only use widely recognized abbreviations (HTTP, CPU, AWS, etc.)
- **Namespacing**: Ensure proper namespace hierarchy and avoid name collisions
- **No reuse**: Different entities cannot share the same name within their category

## Attribute Guidelines

### New Attribute Requirements

- Must have clear benefit to end users
- Should be used by spans/metrics/events/entities
- Must follow stability progression (development → stable)
- Should reuse existing attributes when possible
- Check against existing namespaces before creating new ones

### Attribute Definition Standards

- Use appropriate type (string, int, double, boolean, array, enum)
- Define enums for short, closed sets of values
- Use template type only for dynamic names (last segment only)
- Avoid unbounded values (>1KB strings, >1000 element arrays)
- Avoid high-cardinality attributes in metrics
- Mark PII/sensitive data with warnings

### Attribute Types and Usage

- **Timestamps**: Use string in ISO 8601 format
- **Arrays**: Must be homogeneous; use separate attributes for different concepts
- **Complex values**: Flatten into multiple attributes when possible
- **Template attributes**: For user-defined key-value pairs (e.g., HTTP headers)

## Event Guidelines

- SHOULD have attributes for additional context
- SHOULD NOT use body

## Entity Requirements

- Use `type: entity` with proper `name` field for entity groups
- Distinguish between `identifying` and `descriptive` attribute roles
- Identifying attributes must be minimally sufficient for unique identification and
  must not change during entity lifespan
- Use proper namespacing based on discovery mechanism (e.g., `k8s.*` for Kubernetes)
- Use `entity_associations` field to link signals with appropriate entities

## Error Handling Conventions

### Error Recording Standards

- **Spans**: Set status to Error, populate `error.type`, set description when helpful
- **Metrics**: Include `error.type` attribute for filtering and analysis
- **Exceptions**: Record as span events or log records using SDK APIs
- **Consistency**: Same `error.type` across spans and metrics for same operation

## Common Issues to Flag

- Creating attributes without referenicng them in spans/metrics/events/entities
- Creating new attributes without clear use case or instrumentation that will use them
- Creating overly generic attributes without established standards
- Duplicating existing functionality
- Missing or inadequate documentation
- Missing, incorrect YAML syntax or schema violations
- Inconsistent naming patterns
- Missing required fields or metadata
- Performance or security concerns not addressed

## Review Response Guidelines

- Explain rationale behind suggestions
- Reference relevant documentation sections
- Provide specific examples of improvements
- Suggest alternatives when rejecting proposals

## Resources and References

- [How to Define Conventions](../docs/how-to-write-conventions/README.md)
- [YAML Model Documentation](../model/README.md)
- [Naming Guidelines](../docs/general/naming.md)
- [Attribute Requirement Levels](../docs/general/attribute-requirement-level.md)
- [Error Recording](../docs/general/recording-errors.md)
- [Event Conventions](../docs/general/events.md)
