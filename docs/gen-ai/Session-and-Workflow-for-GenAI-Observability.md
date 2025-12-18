# Proposal: Standardizing `session.id` and `workflow` Spans for GenAI Observability

## 1. Summary

This document proposes extending the GenAI semantic conventions to include two critical concepts for observing complex agentic systems:

1.  **`session.id` (Attribute):** A high-level **interaction scope** that ties together multiple traces, conversations, and workflows over time for a single user or job context.
2.  **`workflow` (Span):** A top-level **orchestration scope** representing a logical unit of work (e.g., a LangGraph run or CrewAI process) that coordinates one or more agents on a pre-defined logic path.

While OpenTelemetry already defines a generic `session.id`, this proposal normatively recommends its use on GenAI agent spans to solve correlation issues in multi-turn, multi-agent systems. Simultaneously, it introduces `workflow` spans to capture the lifecycle of the orchestration layer itself, distinct from the individual agents it manages.

---

## 2. Motivation

### 2.1 The Limitations of Current Semantics

Current GenAI semantic conventions focus heavily on `gen_ai.conversation.id` and individual agent spans. However, real-world agentic systems present challenges that these attributes alone cannot solve:

* **Multi-Conversation Contexts:** A single user "session" often involves parallel chats (e.g., a "Code Agent" thread and a "Test Agent" thread) sharing the same auth and workspace state. `conversation.id` isolates these, making it impossible to analyze the aggregate "visit" or session performance.
* **Long-Running & Resumable Workflows:** Autonomous agents may run for hours or days, spanning multiple traces and resuming across different time windows. A single `trace_id` is too fine-grained and fragmented to represent this entire job.
* **Orchestration Visibility:** Frameworks like LangGraph or CrewAI orchestrate complex patterns (loops, map-reduce). Without a dedicated `workflow` span, we see a "bag of agents" without understanding the parent process that coordinated them.

### 2.2 The Solution: `Session > Workflow > Agent`

We propose a clear hierarchy to address these gaps:

* **Session (`session.id`):** The **User/System Context**.
    * *Scope:* Cross-framework, Cross-time.
    * *Definition:* The bounded period of activity for a user or principal (e.g., "Monday's login" or "Job Run #55").
* **Workflow (`workflow` span):** The **Orchestration Unit**.
    * *Scope:* Framework-specific (Single trace or linked traces).
    * *Definition:* A specific execution of a pre-defined logic path (e.g., [Routing, Parallelization patterns](https://www.anthropic.com/engineering/building-effective-agents)).
* **Agent (`agent` span):** The **Worker Unit**.
    * *Definition:* An autonomous entity performing a specific task within the workflow.
* **Trace (`trace_id`):** The **Execution Mechanism**.
    * *Definition:* The standard distributed tracing boundary (HTTP request/RPC).

---

## 3. Attribute & Span Definitions

### 3.1 Recommended Attribute: `session.id`

We propose updating the **GenAI Agent and Orchestrator spans** specification to **strongly recommend** (SHOULD) the inclusion of `session.id`.

* **Name:** `session.id`
* **Type:** `string`
* **Cardinality:** 1 per span
* **Semantics:** An identifier for the logical session or job in which this agent span is executing. In a GenAI context, a session may span multiple conversations, traces, and service boundaries.

**Why `gen_ai.conversation.id` is not enough:**
`gen_ai.conversation.id` is excellent for analyzing a specific dialog thread. `session.id` is required to correlate multiple threads, background jobs, and tool usage that share a common security or user context but differ in conversation identity.

### 3.2 New Span Type: `workflow`

We propose adding a `workflow` span type to capture the top-level orchestration useful for multi-agent agentic systema with pre-defined logic path.
Unlike `session.id` (which is an attribute on spans), `workflow` is a distinct span kind that acts as the parent or root for agent operations.

**Span Name Format:**
* `workflow {gen_ai.workflow.name}`
* Example: `workflow multi_agent_rag`, `workflow fraud_detection_pipeline`.

**Required Attributes:**

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `gen_ai.workflow.name` | string | Name/identifier of the workflow (e.g., "customer_support_flow") |

**Optional Attributes:**

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `gen_ai.workflow.description` | string | Human-readable description of the workflow's purpose |
| `gen_ai.framework` | string | The framework implementing the workflow (e.g., "langgraph", "crewai") |
| `session.id` | string | **Recommended.** Links this specific workflow run to the broader user session |

**Event Attributes (Content Capture):**
To support debugging, workflow spans may optionally capture input/output via events:
* `gen_ai.input.messages`
* `gen_ai.output.messages`


**Examples of Workflows**
- Crew kick off in CrewAI
- Root chain in LangGraph
- OpenAI Agents higher level trace for multiple agents.[Higer level trace](https://openai.github.io/openai-agents-python/tracing/)
- ADK agents have workflow agents([multi-agent sequential, loop, parallel](https://google.github.io/adk-docs/agents/multi-agents/#workflow-agents-as-orchestrators))
---

## 4. Metrics and Attribution

To enable cost and performance analysis in multi-agent systems, we propose new metrics and the addition of agent context to existing LLM metrics.

### 4.1 Workflow Metrics

* **Metric:** `gen_ai.workflow.duration`
* **Type:** Histogram
* **Unit:** `s` (seconds)
* **Attributes:** `gen_ai.workflow.name`, `gen_ai.framework`.
* **Purpose:** Measures the total time of the orchestration, which may include user-in-the-loop latency or multi-agent coordination overhead.

* **Metric:** `gen_ai.agent.duration`
* **Type:** Histogram
* **Unit:** `s` (seconds)
* **Attributes:** `gen_ai.operation.name`, `gen_ai.agent.name`, `gen_ai.agent.id`, `gen_ai.framework`
* **Purpose:** Measures the duration of agent operations (extends existing agent spans with metrics).


### 4.2 Agent Attribution on LLM Metrics

We propose adding optional agent identification attributes to existing `gen_ai.client.*` metrics. This allows operators to break down token costs and latency by the *agent* that requested them, rather than just the model used.

**New Optional Attributes on `gen_ai.client.token.usage` and `gen_ai.client.operation.duration`:**

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `gen_ai.agent.name` | string | Human-readable name of the agent (e.g., "ResearchAgent") |
| `gen_ai.agent.id` | string | Unique identifier of the agent instance |

**Use Case:** Identifying which agent in a multi-agent "crew" is consuming the most tokens.

---

## 5. Concrete Example: Session containing a Workflow

This example demonstrates how a **Session** (User Visit) contains a **Workflow** (LangGraph execution), which orchestrates **Agents**.

**Scenario:**
A user logs in (Session `sess-001`) and triggers a "Research" workflow. The workflow coordinates a "Browser Agent" and a "Writer Agent".

**Hierarchy:**

```text
Span: workflow research_pipeline
    Attributes:
        session.id              = "sess-001"            <-- Links to User Session
        gen_ai.workflow.name    = "research_pipeline"
        gen_ai.framework        = "langgraph"
    |
    |-- Span: invoke_agent browser_agent
    |       Attributes:
    |           session.id            = "sess-001"
    |           gen_ai.agent.name     = "browser_agent"
    |       |
    |       |-- Span: gen_ai.client.chat (LLM Call)
    |               Attributes:
    |                   gen_ai.agent.name = "browser_agent"  <-- Cost Attribution
    |
    |-- Span: invoke_agent writer_agent
            Attributes:
                session.id            = "sess-001"
                gen_ai.agent.name     = "writer_agent"