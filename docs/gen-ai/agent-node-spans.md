# Agent Node Spans (Draft)

| Attribute | Type | Description |
|-----------|------|-------------|
| `gen_ai.agent.node.type` | string | `"tool_call"`, `"decision"`, `"llm_call"`, etc. |
| `gen_ai.agent.node.id`   | string | Framework‑specific node ID |
| `gen_ai.agent.parent_id` | string | Upstream node ID (if any) |
