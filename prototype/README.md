# GenAI Security Guardian Prototype

Runnable demonstrations of the proposed `apply_guardrail` span and `gen_ai.security.finding` event semantic conventions for GenAI security observability.

## Purpose

This prototype validates that the proposed semantic conventions can capture real-world GenAI security scenarios:

- **Input/output content filtering** - PII detection, toxicity filtering, sensitive topic blocking
- **Multi-tenant policy enforcement** - Per-tenant security configurations
- **Multi-agent delegation boundaries** - Tool validation, inter-agent message guards
- **Conversation-aware threat detection** - Progressive jailbreak detection across turns
- **Guardian service resilience** - Fail-open vs fail-closed fallback behavior

## Quickstart

```bash
cd prototype

# Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-appinsights.txt

# Configure credentials (copy template and edit)
cp stories/.env.example stories/.env.local
# Edit .env.local with your APPLICATIONINSIGHTS_CONNECTION_STRING

# Run all stories with console output
python -m stories.story_runner --all --exporters console

# Or run specific stories
python -m stories.story_runner --story 4 5 7 --exporters console
```

## Story Scenarios

| ID | Scenario | Key Conventions Demonstrated |
|----|----------|------------------------------|
| **4** | Enterprise RAG Access Control | `knowledge_query`, `knowledge_result`, `memory_store`, `memory_retrieve` target types |
| **5** | Multi-Tenant SaaS | `llm_input`, `llm_output` targets; `modify` decision; `tenant.id` attribute |
| **7** | Multi-Agent Orchestrator | `tool_definition`, `tool_call`, `message` targets; `gen_ai.agent.id` nesting |
| **10** | Progressive Jailbreak | `gen_ai.conversation.id` correlation; cumulative risk scoring across turns |
| **11** | Guardian Error Handling | `error.type` attribute; fail-open vs fail-closed fallback policies |

### Story 4: Enterprise RAG Access Control

An enterprise knowledge assistant that enforces access control at multiple stages - guards knowledge queries to block restricted searches based on user role, filters retrieved documents by permission level, and prevents sensitive data from being stored to memory.

### Story 5: Multi-Tenant AI Service

A shared AI assistant serving multiple tenants (Acme Corp, GlobalBank, TechStartup) with distinct security policies. Each tenant has different content filter levels and PII sensitivity settings.

### Story 7: Multi-Agent Swarm Orchestrator

A multi-agent system with security boundaries between specialized agents. Validates tool definitions at agent startup, enforces delegation policies, and guards inter-agent messages for prompt injection.

### Story 10: Conversation-Aware Security

Detects multi-turn jailbreak attacks by tracking cumulative risk across a conversation using `gen_ai.conversation.id`. Catches "slow-burn" attacks where individually innocent messages combine to exceed security thresholds.

### Story 11: Resilient Guardian Service

Demonstrates fallback behavior when the guardian service fails - fail-open mode logs a warning but allows requests, while fail-closed mode denies them entirely.

## Example Trace Structure

```
invoke_agent Coordinator (CLIENT span)
├── gen_ai.agent.id: agent_coordinator_v2
├── gen_ai.conversation.id: session_123
│
├── apply_guardrail Input Policy (INTERNAL span)
│   ├── gen_ai.operation.name: apply_guardrail
│   ├── gen_ai.security.target.type: llm_input
│   ├── gen_ai.security.decision.type: allow
│   ├── gen_ai.guardian.name: "Content Filter"
│   └── Events:
│       └── gen_ai.security.finding
│           ├── gen_ai.security.risk.category: prompt_injection
│           ├── gen_ai.security.risk.severity: low
│           └── gen_ai.security.risk.score: 0.15
│
└── apply_guardrail Output Policy (INTERNAL span)
    ├── gen_ai.security.target.type: llm_output
    ├── gen_ai.security.decision.type: modify
    ├── gen_ai.security.content.redacted: true
    └── Events:
        └── gen_ai.security.finding
            ├── gen_ai.security.risk.category: pii
            └── gen_ai.security.risk.severity: medium
```

## Key Files

| File | Purpose |
|------|---------|
| `otel_guardian_utils.py` | Core utilities for creating guardian spans and events |
| `otel_bootstrap.py` | OpenTelemetry exporter configuration |
| `stories/story_runner.py` | CLI for running story scenarios |
| `stories/story_*.py` | Individual story implementations |
| `frameworks/` | Framework adapter examples (LangChain, MCP) |

## Framework Adapters

The `frameworks/` directory contains integration patterns for popular agent frameworks:

- **LangChain** (`frameworks/langchain/`) - Callback-based integration
- **MCP** (`frameworks/mcp/`) - Model Context Protocol server integration

Each adapter demonstrates how to:
1. Create `apply_guardrail` spans as children of framework operations
2. Record `GuardianResult` and `SecurityFinding` attributes/events
3. Map framework-specific IDs to `gen_ai.agent.id` and `gen_ai.conversation.id`

## Content Capture (Opt-in)

Sensitive content is **never captured by default**. Enable explicitly via:

- CLI: `--capture-content`
- Environment: `OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT=true`

When enabled, demos may emit:
- `gen_ai.input.messages`, `gen_ai.output.messages`
- `gen_ai.security.content.input.value`, `gen_ai.security.content.output.value`

## Semantic Convention Coverage

This prototype demonstrates all proposed security attributes:

**Span Attributes (apply_guardrail)**:
- `gen_ai.operation.name` (required: `apply_guardrail`)
- `gen_ai.guardian.*` (id, name, version, provider.name)
- `gen_ai.security.decision.*` (type, reason, code)
- `gen_ai.security.target.*` (type, id)
- `gen_ai.security.policy.*` (id, name, version)
- `gen_ai.security.content.*` (redacted, input.hash, opt-in values)
- `gen_ai.agent.id`, `gen_ai.conversation.id`
- `error.type` (on guardian failures)

**Event Attributes (gen_ai.security.finding)**:
- `gen_ai.security.risk.*` (category, severity, score, metadata)
- `gen_ai.security.policy.*` (id, name, version)

**Decision Types**: `allow`, `deny`, `modify`, `warn`, `audit`

**Target Types**: `llm_input`, `llm_output`, `tool_call`, `tool_definition`, `message`, `memory_store`, `memory_retrieve`, `knowledge_query`, `knowledge_result`

## Related Specification

- **Spec document**: [`docs/gen-ai/gen-ai-security.md`](../docs/gen-ai/gen-ai-security.md)
- **Model definitions**: [`model/gen-ai/`](../model/gen-ai/)
- **Registry attributes**: [`model/gen-ai/registry.yaml`](../model/gen-ai/registry.yaml)
