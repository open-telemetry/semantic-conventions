# Copilot instructions for OpenTelemetry Semantic Conventions

## Overview
These instructions guide AI assistants in reviewing OpenTelemetry Semantic Conventions
pull requests to ensure consistency, quality, and adherence to established standards.

**CRITICAL REVIEW CRITERIA**: New areas require special scrutiny and must meet these requirements:

### Prerequisites for new areas
- **Domain Expertise**: Must have a group of people familiar with the domain
- **Active Involvement**: Contributors must be involved with instrumentation efforts in that area
- **Long-term Commitment**: Must have committed maintainers as points of contact for pull requests, issues, questions, and ongoing maintenance
1. **Project Management**: Follow [OpenTelemetry project management](https://github.com/open-telemetry/community/blob/main/project-management.md) guidelines
2. **Codeowners**: New areas MUST have assigned codeowners

## General review principles
- **YAML Models**: All attributes, metrics, and conventions are formally defined in YAML files under `model/` directory
  - Validate against [schema](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv.schema.json)
  - Verify clear `brief` and `note` sections with realistic examples
  - Confirm proper RFC 2119 keywords (MUST, SHOULD, MAY, etc.)

- **Scope**: ensure contributions belong here:
  - **SHOULD be included:**
    - Instrumentations hosted in OpenTelemetry
    - Common attributes and conventions used across multiple instrumentations
    - Conventions that benefit from centralized policy enforcement

  - **SHOULD NOT be included:**
    - Instrumentations following external schemas not fully compatible with OpenTelemetry
    - Domain-specific conventions better maintained in their own repositories

### Naming conventions
- Use lowercase with dot-separated namespaces (e.g., `service.name`)
- Multi-word components use snake_case (e.g., `http.response.status_code`)
- Only widely recognized abbreviations (HTTP, CPU, AWS, etc.)
- Proper namespace hierarchy

## Attribute review guidelines

### Requirements
- Clear benefit to end users with usage in spans, metrics, events, or entities
- Follow stability progression (development → stable)
- Reuse existing attributes when possible, check existing namespaces first
- Use appropriate type (string, int, double, boolean, array, enum)
- Define enums for closed sets, avoid unbounded values (>1KB strings, >1000 elements)
- Mark PII/sensitive data with warnings

### Types and usage
- **Timestamps**: ISO 8601 string format
- **Arrays**: Homogeneous; separate attributes for different concepts
- **Complex values**: Flatten when possible
- **Template attributes**: Dynamic names (last segment only)

## Event conventions
- MUST have unique, low-cardinality event name
- SHOULD have attributes for context, SHOULD NOT use body

## Error handling conventions
- **Spans**: Set status to Error, populate `error.type`, set description when helpful
- **Metrics**: Include `error.type` attribute for filtering and analysis
- **Consistency**: Same `error.type` across spans and metrics for same operation

## Common issues to flag

- Creating attributes without referencing them in spans, metrics, events, or entities
- Creating new attributes without clear use case or instrumentation that will use them
- Creating overly generic attributes without established standards
- Duplicating existing functionality
- Missing or inadequate documentation
- Inconsistent naming patterns
- Performance or security concerns not addressed

## Review response guidelines

### Constructive feedback

- Explain rationale behind suggestions
- Reference relevant documentation sections
- Provide specific examples of improvements
- Suggest alternatives when rejecting proposals

## Resources and references

- [Contributing to OpenTelemetry Semantic Conventions](../CONTRIBUTING.md)
- [How to define conventions](../docs/general/how-to-define-semantic-conventions.md)
- [YAML model documentation](../model/README.md)
- [Naming guidelines](../docs/general/naming.md)
- [Attribute requirement levels](../docs/general/attribute-requirement-level.md)
- [Error recording](../docs/general/recording-errors.md)
- [Event conventions](../docs/general/events.md)
