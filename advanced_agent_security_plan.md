# Plan: Advanced Agent Patterns for GenAI Security (PR #3233)

## Objective
Validate the proposed GenAI security semantic conventions (the `apply_guardrail` span and
`gen_ai.security.finding` event) by implementing advanced agent patterns and runnable
prototypes across multiple agent frameworks. The output must be traceable, comparable
across frameworks, and aligned with the story runner and trace viewer in this repo.

## SemConv contract (PR #3233)
- Apply guardrail span:
  - Name: `apply_guardrail {gen_ai.guardian.name}` (fallback: `apply_guardrail {gen_ai.security.target.type}`)
  - Required attributes: `gen_ai.operation.name=apply_guardrail`, `gen_ai.security.target.type`,
    `gen_ai.security.decision.type`
  - Guardian identity: `gen_ai.guardian.id`, `gen_ai.guardian.name`, `gen_ai.guardian.version`,
    `gen_ai.guardian.provider.name`
  - Optional context: `gen_ai.agent.id`, `gen_ai.conversation.id`, `gen_ai.security.target.id`
  - Decision details: `gen_ai.security.decision.reason`, `gen_ai.security.decision.code`,
    `gen_ai.security.policy.*`, `gen_ai.security.content.redacted` (when modify)
  - Error reporting: `error.type` on guardian span when evaluation fails
  - Content capture: `gen_ai.security.content.input.value` / `output.value` opt-in only, prefer
    `gen_ai.security.content.input.hash` by default
- Finding event:
  - Name: `gen_ai.security.finding`
  - Required attributes: `gen_ai.security.risk.category`, `gen_ai.security.risk.severity`
  - Optional attributes: `gen_ai.security.risk.score`, `gen_ai.security.risk.metadata`,
    `gen_ai.security.policy.*`

## Strict semconv-only rules
- Emit only `gen_ai.*` attributes defined in `model/gen-ai/*.yaml`.
- Use only the predefined `gen_ai.security.target.type` values.
- Do not introduce custom target types, decision types, or non-spec metrics.
- Any additional grouping spans must not carry `gen_ai.*` attributes.

## Scenario grouping span (optional)
To group all operations for a single story scenario in one trace:
- Add a parent INTERNAL span named `scenario {story_id}.{scenario_name}`.
- Do not set `gen_ai.operation.name` or any `gen_ai.*` attributes on the grouping span.
- Keep `apply_guardrail` spans as children of the operation span they protect (for example,
  `chat`, `invoke_agent`, `execute_tool`).

## Story suite (advanced patterns)

| Story | File | Primary Focus |
|-------|------|---------------|
| 4 | `prototype/stories/story_4_enterprise_rag_access_control.py` | Knowledge and memory guardrails |
| 5 | `prototype/stories/story_5_multi_tenant.py` | Multi-tenant input/output safety |
| 7 | `prototype/stories/story_7_multi_agent.py` | Agent boundaries and tool governance |
| 10 | `prototype/stories/story_10_progressive_jailbreak.py` | Progressive jailbreak detection |
| 11 | `prototype/stories/story_11_guardian_error_handling.py` | Guardian failure and fallback |

### Story 4: Enterprise knowledge and memory guardrails
- Targets: `knowledge_query`, `knowledge_result`, `memory_store`, `memory_retrieve`
- Decisions: `allow`, `deny`, `modify`
- Findings: `sensitive_info_disclosure` with policy metadata
- Key attributes: `gen_ai.security.target.id`, `gen_ai.security.content.input.hash`,
  `gen_ai.security.content.output.value` (modify only)

### Story 5: Multi-tenant input/output safety
- Targets: `llm_input`, `llm_output`
- Decisions: `allow`, `warn`, `deny`, `modify`
- Findings: `sensitive_info_disclosure`, `pii`, `unbounded_consumption`
- Key attributes: `gen_ai.security.policy.*`, `gen_ai.security.decision.reason`,
  `gen_ai.security.content.redacted`

### Story 7: Multi-agent boundary and tool governance
- Targets: `tool_definition`, `tool_call`, `message`
- Decisions: `allow`, `audit`, `warn`, `deny`
- Findings: `excessive_agency`, `prompt_injection`
- Key attributes: `gen_ai.agent.id`, `gen_ai.security.target.id`, `gen_ai.security.decision.code`

### Story 10: Progressive jailbreak detection
- Targets: `llm_input`
- Decisions: `allow`, `warn`, `deny` across turns
- Findings: `jailbreak`, `prompt_injection`
- Key attributes: `gen_ai.conversation.id`, `gen_ai.security.risk.score`,
  `gen_ai.security.risk.metadata` (turn and cumulative risk)

### Story 11: Guardian failure with fallback enforcement
- Targets: `llm_input`
- Decisions: `warn`, `deny`
- Findings: `custom:guardian_unavailable`
- Key attributes: `error.type`, `gen_ai.security.decision.reason`, `gen_ai.security.policy.id`

## Framework prototypes (multi-framework instrumentation)
### Shared adapter
- Use `prototype/otel_guardian_utils.py` as the canonical helper and add a thin adapter per
  framework to:
  - Start `apply_guardrail` spans as children of the framework operation span
  - Record `GuardianResult` and `SecurityFinding` attributes/events
  - Honor opt-in content capture via `OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT`
  - Map framework-specific IDs to `gen_ai.agent.id` and `gen_ai.conversation.id`

### LangChain
- Hook points:
  - LLM callbacks for `llm_input` / `llm_output` guards
  - Tool execution callbacks for `tool_call` guards
  - Tool registration for `tool_definition` validation
- Emission details:
  - Wrap guard evaluation in `apply_guardrail` spans
  - Use run or session IDs for `gen_ai.conversation.id`
  - Use agent or executor identifiers for `gen_ai.agent.id`
  - Emit `gen_ai.security.finding` events per rule match
  - Set `gen_ai.security.content.redacted` and `content.output.value` on modify

### LangGraph
- Hook points:
  - Guard nodes before and after model nodes for `llm_input` / `llm_output`
  - Tool node wrapper for `tool_call`
  - Graph build step for `tool_definition` validation
  - Memory nodes for `memory_store` / `memory_retrieve`
- Emission details:
  - Each guard node emits an `apply_guardrail` span
  - Use thread or session IDs for `gen_ai.conversation.id`
  - Include `gen_ai.security.target.id` for tool calls and memory keys
  - Emit findings for blocked or modified decisions

### Agno
- Hook points:
  - Pre and post model hooks for `llm_input` / `llm_output`
  - Tool execution middleware for `tool_call`
  - Tool registry validation for `tool_definition`
  - Memory hooks for `memory_store` / `memory_retrieve`
- Emission details:
  - Apply guardrail spans under the agent run span
  - Map agent instance ID to `gen_ai.agent.id` and session ID to `gen_ai.conversation.id`
  - Emit `gen_ai.security.risk.metadata` for rule matches without raw content

### ADK (Agent Development Kit)
- Hook points:
  - Middleware around model invocation for `llm_input` / `llm_output`
  - Tool executor hooks for `tool_call` and `tool_definition`
  - Message pipeline hooks for inter-agent message guards
- Emission details:
  - Create `apply_guardrail` child spans per evaluation
  - Map agent and conversation IDs from the framework context
  - Record `error.type` and fallback decision when guardian service fails

### Semantic Kernel
- Hook points:
  - Function filters for `llm_input` / `llm_output`
  - Plugin invocation interception for `tool_call` and `tool_definition`
  - Memory connector hooks for `memory_store` / `memory_retrieve`
  - Prompt template rendering for pre-render content guards
- Emission details:
  - Create `apply_guardrail` spans within function execution context
  - Map execution context to `gen_ai.conversation.id`
  - Use plugin and function names for `gen_ai.security.target.id`
  - Emit findings via native span events

### MCP (Model Context Protocol)
- Hook points:
  - Tool call interception (`tools/call` requests) for `tool_call`
  - Tool registry discovery (`tools/list`) for `tool_definition`
  - Resource read request (`resources/read`) for `knowledge_query`
  - Resource read response for `knowledge_result`
  - Prompt retrieval (`prompts/get`) for `knowledge_query` / `knowledge_result`
  - Sampling requests for `llm_input` / `llm_output` (when MCP server proxies LLM)
- Emission details:
  - Use only standard `gen_ai.security.target.type` values
  - If the MCP server performs the guard evaluation, map its name to
    `gen_ai.guardian.name` and `gen_ai.guardian.provider.name`
  - Use MCP request ID for `gen_ai.security.target.id`
  - Record resource URI in `gen_ai.security.risk.metadata` for resource guards
  - Honor MCP transport context for distributed trace propagation

## Implementation roadmap
### Phase 1: Instrumentation adapters
1. Create `prototype/frameworks/<framework>/guardian_adapter.py` for LangChain, LangGraph, Agno,
   ADK, Semantic Kernel, and MCP.
2. Ensure adapters only emit semantic convention keys from `model/gen-ai/*.yaml`.
3. Add small smoke checks for required attributes (remove before shipping if needed).

### Phase 2: Story implementations per framework
4. Implement Story 4 and Story 5 first (input/output and knowledge/memory coverage).
5. Implement Story 7 for agent boundaries (tool_definition / tool_call / message).
6. Implement Story 10 for multi-turn risk scoring (conversation correlation).
7. Implement Story 11 for guardian error handling (`error.type` + fallback decision).

### Phase 3: Trace validation
8. Run stories via `prototype/stories/story_runner.py` and framework-specific runners.
9. Compare emitted attributes against `docs/gen-ai/gen-ai-security.md` and
   `prototype/stories/TRACE_COVERAGE.md`.
10. Extend `prototype/stories/TRACE_COVERAGE.md` with framework coverage notes.

### Phase 4: Documentation
11. Add README snippets for each framework showing span + event emission patterns.
12. Add trace viewer notes for interpreting guardrail spans and finding events.
