# Trace Coverage (Stories → Traces)

This document maps the **runnable story suite** under `prototype/stories/` to the **trace variants** it emits for the GenAI Security Guardian proposal (the `apply_guardrail` span + `gen_ai.security.finding` events).

## How traces are identified

Each runnable scenario creates **one trace per root span** whose name starts with `story_<id>...`, for example:

- `story_5.acme_corp.pii_redaction_email_phone`
- `story_10.conv_jailbreak_001.invoke_agent Security Assistant`

Every trace root span includes:

- `story.id`
- `story.title`
- `scenario.name`

These fields are used by `prototype/stories/trace_viewer.py` to filter and display traces.

## Run

```bash
cd prototype
python stories/story_runner.py --list
python stories/story_runner.py --story 4 5 7 10 11 --exporters console
```

To run + view in the browser (App Insights):

```bash
cd prototype
python stories/run_and_view.py --story 4 5 7 10 11
```

To include opt-in content fields (SENSITIVE):

```bash
cd prototype
python stories/story_runner.py --all --exporters appinsights --capture-content
```

## Viewer walkthrough

In the local viewer (`prototype/stories/trace_viewer.py`):

1. Set time range to “Last 15 minutes” and click “Refresh”.
2. Use the “Story” filter (4/5/7/10/11) to focus the sidebar.
3. Click a trace (subtitle = root span name, e.g. `story_5.acme_corp.pii_redaction_email_phone`).
4. In the span tree:
   - Click a `chat …` or `invoke_agent …` span → open “Sensitive content (opt-in)” to see:
     - `gen_ai.system_instructions`
     - `gen_ai.input.messages` / `gen_ai.output.messages`
   - Click an `apply_guardrail …` span → open “Sensitive content (opt-in)” to see:
     - `gen_ai.security.content.input.value`
     - `gen_ai.security.content.output.value` (only on `modify`)

## Coverage summary

### `gen_ai.security.target.type` (suggested values)

| Target type | Covered by |
|---|---|
| `llm_input` | Story 5, Story 10, Story 11 |
| `llm_output` | Story 5 |
| `tool_call` | Story 7 |
| `tool_definition` | Story 7 |
| `message` | Story 7 |
| `knowledge_query` | Story 4 |
| `knowledge_result` | Story 4 |
| `memory_store` | Story 4 |
| `memory_retrieve` | Story 4 |

### `gen_ai.security.decision.type`

| Decision type | Covered by |
|---|---|
| `allow` | Stories 4, 5, 7, 10 |
| `warn` | Stories 5, 7, 10, 11 |
| `deny` | Stories 4, 5, 7, 10, 11 |
| `modify` | Stories 4, 5 |
| `audit` | Story 7 |

### Guardian errors (`error.type`)

| Pattern | Covered by |
|---|---|
| `error.type` set on `apply_guardrail` span (decision present) | Story 11 |

## Trace catalog

### Story 4 — Enterprise RAG Access Control (`prototype/stories/story_4_enterprise_rag_access_control.py`)

- `story_4.rag_query_allow_result_filter`
  - `apply_guardrail RAG Query Access Guard` → `target=knowledge_query`, `decision=allow`
  - `apply_guardrail RAG Result Filter` → `target=knowledge_result`, `decision=modify` (+ findings)
  - `apply_guardrail Memory Store Guard` → `target=memory_store`, `decision=allow`
  - `apply_guardrail Memory Retrieve Guard` → `target=memory_retrieve`, `decision=allow`
  - Viewer focus: click `apply_guardrail RAG Result Filter` → show `decision=modify`, finding event(s), and `gen_ai.security.content.*` (opt-in)
- `story_4.rag_query_blocked`
  - `apply_guardrail RAG Query Access Guard` → `target=knowledge_query`, `decision=deny` (+ findings)
  - Viewer focus: click `apply_guardrail RAG Query Access Guard` → show `decision=deny` + `decision.reason`
- `story_4.memory_store_secret_blocked`
  - `apply_guardrail Memory Store Guard` → `target=memory_store`, `decision=deny` (+ findings)
  - Viewer focus: click `apply_guardrail Memory Store Guard` → show `decision=deny` and why it was flagged as a secret

### Story 5 — Multi-Tenant SaaS (`prototype/stories/story_5_multi_tenant.py`)

- `story_5.acme_corp.normal_query`
  - Input guard: `target=llm_input`, `decision=allow`
  - Output guard: `target=llm_output`, `decision=allow`
  - Viewer focus: click the `chat …` span → show `tenant.id`, `gen_ai.*` request/response attributes
- `story_5.acme_corp.pii_redaction_email_phone`
  - Input guard: `target=llm_input`, `decision=allow`
  - Output guard: `target=llm_output`, `decision=modify` (+ findings, `gen_ai.security.content.redacted=true`)
  - Viewer focus: click the output guard span → show `content.input.value` (raw) vs `content.output.value` (redacted)
- `story_5.acme_corp.sensitive_topic_warn`
  - Input guard: `target=llm_input`, `decision=warn` (+ findings)
  - Output guard: `target=llm_output`, `decision=allow`
  - Viewer focus: click the input guard span → show `decision=warn` with the finding metadata
- `story_5.globalbank.pii_redaction_name_phone`
  - Output guard: `target=llm_output`, `decision=modify` (+ findings)
  - Viewer focus: click the output guard span → show redaction of both name + phone patterns
- `story_5.globalbank.sensitive_topic_deny`
  - Input guard: `target=llm_input`, `decision=deny` (+ findings)
  - Viewer focus: show that deny happens before any model output is produced (`gen_ai.response.finish_reasons=["content_filter"]`)
- `story_5.techstartup.sensitive_topic_allowed`
  - Input guard: `target=llm_input`, `decision=allow`
  - Viewer focus: compare `tenant.id=techstartup` vs strict tenants; show the same query is allowed here
- `story_5.techstartup.pii_redaction_email_phone`
  - Output guard: `target=llm_output`, `decision=modify` (+ findings)
  - Viewer focus: show different tenant policy IDs on spans/events even for the same risk category

### Story 7 — Multi-Agent Security Boundary (`prototype/stories/story_7_multi_agent.py`)

When `--capture-content` is enabled, `invoke_agent` and `create_agent` spans also include opt-in fields:
- `gen_ai.system_instructions`, `gen_ai.input.messages`, `gen_ai.output.messages`
- `gen_ai.tool.definitions` (tool schema)

- `story_7.create_agent.coordinator`
  - Tool validation: `target=tool_definition`, `decision=allow`
  - Viewer focus: show `gen_ai.agent.id` attribution + opt-in `content.input.value` containing the tool schema
- `story_7.create_agent.code_audited`
  - Tool validation: `target=tool_definition`, `decision=audit` (+ findings) for `execute_sandbox`
  - Viewer focus: show `decision=audit` as “log but allow” for risky tools
- `story_7.create_agent.communication`
  - Tool validation: `target=tool_definition`, `decision=allow`
- `story_7.create_agent.rogue_blocked`
  - Tool validation: `target=tool_definition`, `decision=deny` (+ findings) for `shell_exec`
  - Viewer focus: show hard deny on dangerous capability at agent startup
- `story_7.delegation.authorized_coordinator_to_communication`
  - Delegation guard: `target=tool_call`, `decision=warn` (+ findings)
  - Inter-agent message guard: `target=message`, `decision=allow`
  - Tool guard: `target=tool_call`, `decision=allow`
  - Viewer focus: show nested `invoke_agent` spans + how decisions differ by target type
- `story_7.delegation.unauthorized_research_to_communication`
  - Delegation guard: `target=tool_call`, `decision=deny` (+ findings)
  - Viewer focus: show deny on boundary crossing (source agent not allowed to delegate)
- `story_7.message.injection_attempt`
  - Delegation guard: `target=tool_call`, `decision=warn`
  - Inter-agent message guard: `target=message`, `decision=deny` (+ findings, `prompt_injection`)
  - Viewer focus: click the message guard span and show the `prompt_injection` finding
- `story_7.delegation.normal_chain_coordinator_to_research`
  - Delegation guard: `target=tool_call`, `decision=warn`
  - Inter-agent message guard: `target=message`, `decision=allow`
  - Tool guard: `target=tool_call`, `decision=allow`

### Story 10 — Progressive Jailbreak (`prototype/stories/story_10_progressive_jailbreak.py`)

Each **conversation** is a separate trace with an `invoke_agent` root span:

- `story_10.<conversation_id>.invoke_agent Security Assistant`

Within the trace, each turn is a child span named `turn_<n>` under the `invoke_agent` root.

Scenarios:

- `scenario.name=classic_progressive_jailbreak` (`conv_jailbreak_001`)
  - Turn 1: `decision=allow`
  - Turn 2: `decision=warn`
  - Turn 3: `decision=deny` (+ findings for `jailbreak` and `prompt_injection`)
  - Viewer focus: filter Story 10 → open the `invoke_agent` trace and expand `turn_1/2/3`
- `scenario.name=slow_burn_jailbreak` (`conv_slowburn_002`)
  - Escalates gradually; later turns may reach `warn`/`deny` depending on cumulative score
  - Viewer focus: show how findings include `cumulative_risk:*` in `gen_ai.security.risk.metadata`
- `scenario.name=benign_conversation` (`conv_benign_003`)
  - All turns: `decision=allow`
  - Viewer focus: show “normal chat” where guardian is present but non-blocking

### Story 11 — Guardian Error Handling (`prototype/stories/story_11_guardian_error_handling.py`)

- `story_11.fail_open`
  - `apply_guardrail External Guardian Service` → `error.type=GuardianTimeoutError`, `decision=warn` (+ findings, `custom:guardian_unavailable`)
  - Viewer focus: click the guardian span → show `error.type` + still having an explicit decision + finding
- `story_11.fail_closed`
  - `apply_guardrail External Guardian Service` → `error.type=GuardianTimeoutError`, `decision=deny` (+ findings)
  - Viewer focus: compare fail-open vs fail-closed (same error, different downstream enforcement)

---

## Framework Adapters

The `prototype/frameworks/` directory contains guardian adapters for popular agent frameworks. Each adapter maps framework-specific concepts to the GenAI Security semantic conventions.

### Adapter Coverage Matrix

| Framework | Location | Hook Points | Target Types Covered |
|-----------|----------|-------------|---------------------|
| **LangChain** | `frameworks/langchain/` | LLM callbacks, tool callbacks | `llm_input`, `llm_output`, `tool_call`, `tool_definition` |
| **LangGraph** | `frameworks/langgraph/` | Guard nodes, tool wrappers, memory nodes | `llm_input`, `llm_output`, `tool_call`, `memory_store`, `memory_retrieve` |
| **Agno** | `frameworks/agno/` | Pre/post model hooks, middleware | `llm_input`, `llm_output`, `tool_call`, `tool_definition`, `memory_store`, `memory_retrieve` |
| **Google ADK** | `frameworks/adk/` | Model middleware, tool executor | `llm_input`, `llm_output`, `tool_call`, `tool_definition`, `message` |
| **Semantic Kernel** | `frameworks/semantic_kernel/` | Function filters, plugin interception, memory connectors | `llm_input`, `llm_output`, `tool_call`, `tool_definition`, `memory_store`, `memory_retrieve` |
| **MCP** | `frameworks/mcp/` | Tool/resource/prompt interception, sampling | `llm_input`, `llm_output`, `tool_call`, `tool_definition`, `knowledge_query`, `knowledge_result` |

### Framework ID Mapping

Each adapter maps framework-specific identifiers to semantic convention attributes:

| Framework | Agent ID Source | Conversation ID Source |
|-----------|-----------------|------------------------|
| LangChain | `chain_id`, `agent_executor_id` | `run_id` |
| LangGraph | `graph_id.node_id` | `thread_id` |
| Agno | `agent_id` | `session_id`, `run_id` |
| Google ADK | `agent_id` | `session_id` |
| Semantic Kernel | `kernel_id` | `chat_id` |
| MCP | `server_name` | `session_id` |

### Using Framework Adapters

```python
# LangChain example
from frameworks.langchain import LangChainGuardianAdapter, LangChainContext

adapter = LangChainGuardianAdapter.create_default()
ctx = LangChainContext(run_id="run_123", chain_id="my_chain")
result = adapter.guard_llm_input("User message", ctx)

# LangGraph example
from frameworks.langgraph import LangGraphGuardianAdapter, LangGraphContext

adapter = LangGraphGuardianAdapter.create_default()
input_guard = adapter.create_input_guard_node(graph_id="my_graph")
output_guard = adapter.create_output_guard_node(graph_id="my_graph")

# MCP example
from frameworks.mcp import MCPGuardianAdapter, MCPContext

adapter = MCPGuardianAdapter.create_default(server_name="my-server")
ctx = MCPContext(server_name="my-server", session_id="sess_123")
result = adapter.guard_tool_call_mcp("calculator", {"expr": "2+2"}, ctx)
```

### Framework Adapter Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        BaseGuardianAdapter                          │
│  ─────────────────────────────────────────────────────────────────  │
│  - guard_llm_input()       - guard_memory_store()                   │
│  - guard_llm_output()      - guard_memory_retrieve()                │
│  - guard_tool_call()       - guard_knowledge_query()                │
│  - guard_tool_definition() - guard_knowledge_result()               │
│  - guard_message()                                                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │ extends
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  LangChain    │  │  LangGraph    │  │  Semantic     │
│  Adapter      │  │  Adapter      │  │  Kernel       │
├───────────────┤  ├───────────────┤  │  Adapter      │
│ - Callbacks   │  │ - Guard nodes │  ├───────────────┤
│ - Run IDs     │  │ - Thread IDs  │  │ - Filters     │
│ - Tool hooks  │  │ - Tool wrap   │  │ - Plugin IDs  │
└───────────────┘  └───────────────┘  └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │   otel_guardian_utils    │
              │  ──────────────────────  │
              │  - GuardianTracer        │
              │  - GuardianConfig        │
              │  - GuardianResult        │
              │  - SecurityFinding       │
              └──────────────────────────┘
```
