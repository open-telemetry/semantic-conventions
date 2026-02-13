# Story Scenarios

Runnable story scenarios demonstrating GenAI Security Guardian semantic conventions.

> **See also**: [`../README.md`](../README.md) for full documentation, quickstart, and semantic convention coverage.

## Running Stories

```bash
cd prototype

# List available stories
python -m stories.story_runner --list

# Run all stories with console output
python -m stories.story_runner --all --exporters console

# Run specific stories
python -m stories.story_runner --story 4 5 7 --exporters console

# Run with App Insights export
python -m stories.story_runner --all --exporters appinsights

# Enable sensitive content capture (opt-in)
python -m stories.story_runner --all --exporters console --capture-content
```

## Story Summary

| ID | File | Scenario | Key Target Types |
|----|------|----------|------------------|
| 4 | `story_4_enterprise_rag_access_control.py` | Enterprise RAG | `knowledge_query`, `knowledge_result`, `memory_*` |
| 5 | `story_5_multi_tenant.py` | Multi-Tenant SaaS | `llm_input`, `llm_output` |
| 7 | `story_7_multi_agent.py` | Multi-Agent Swarm | `tool_definition`, `tool_call`, `message` |
| 10 | `story_10_progressive_jailbreak.py` | Jailbreak Detection | `llm_input` with `conversation.id` |
| 11 | `story_11_guardian_error_handling.py` | Error Handling | `llm_input` with `error.type` |

## Environment Variables

Copy `stories/.env.example` to `stories/.env.local` and configure:

### Required for Trace Export
- `APPLICATIONINSIGHTS_CONNECTION_STRING` - Azure App Insights

### Optional
- `OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT=true` - Enable sensitive content capture

## Files

| File | Purpose |
|------|---------|
| `story_runner.py` | CLI for running stories |
| `story_*.py` | Individual story implementations |
| `demo_llm.py` | Mock LLM for deterministic responses |
| `chat_span_utils.py` | Helpers for GenAI chat spans |

## Trace Coverage

See [`TRACE_COVERAGE.md`](TRACE_COVERAGE.md) for detailed mapping of stories to semantic convention attributes.
