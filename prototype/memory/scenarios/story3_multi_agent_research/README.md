# Story 3: Multi-Agent Research Crew

A team of specialized AI agents collaborating on market research, demonstrating team-scoped and agent-scoped memory sharing patterns.

## Narrative

**Context**: ResearchCo uses a team of specialized AI agents to conduct market research. The team includes a Researcher (gathers data), an Analyst (interprets data), and a Writer (produces reports). They need both shared team knowledge and agent-specific procedural knowledge.

**User Journey**: ResearchCo receives a request to analyze the electric vehicle market:

1. **Team Setup**: A shared team knowledge base is created for this project
2. **Researcher Works**: Gathers market data and stores findings in team knowledge
3. **Analyst Learns**: Develops analysis methodology, stores in agent-specific memory
4. **Knowledge Sharing**: Analyst appends analysis results to team knowledge
5. **Collaboration**: Writer searches team knowledge to access all findings

## Why Memory Observability Matters

- **Collaboration Debugging**: Trace knowledge flow between agents
- **Attribution**: Identify which agent contributed what knowledge via `gen_ai.agent.id`
- **Optimization**: Monitor team knowledge base growth and search efficiency

## Architecture

### Memory Scope Architecture

```mermaid
flowchart TB
    subgraph "Agent-Scoped Memory"
        R[Researcher Agent] --> RM[(Researcher's<br/>Memory Store)]
        A[Analyst Agent] --> AM[(Analyst's<br/>Memory Store)]
        W[Writer Agent] --> WM[(Writer's<br/>Memory Store)]
    end

    subgraph "Team-Scoped Memory"
        TK[(Team Knowledge Base<br/>ev-research-team)]
    end

    R -->|share finding| TK
    A -->|append analysis| TK
    W -->|search for report| TK

    style TK fill:#e1f5fe
```

### Agent Collaboration Sequence

```mermaid
sequenceDiagram
    participant Crew as Research Crew
    participant R as Researcher
    participant A as Analyst
    participant W as Writer
    participant Team as Team Store<br/>(team scope)
    participant Agent as Agent Store<br/>(agent scope)

    Note over Crew: Project Kickoff

    rect rgb(240, 248, 255)
        Crew->>Team: create_memory_store<br/>scope: team
    end

    Note over R: Research Phase

    rect rgb(240, 255, 240)
        R->>R: Gather market data
        R->>Team: update_memory<br/>agent_id: researcher
        Note right of Team: Finding: Market size $500B
    end

    Note over A: Analysis Phase

    rect rgb(255, 250, 240)
        A->>Agent: create_memory_store<br/>scope: agent
        A->>Agent: update_memory<br/>procedure: trend_analysis_v2
    end

    rect rgb(255, 250, 240)
        A->>A: Run analysis
        A->>Team: update_memory<br/>strategy: append<br/>agent_id: analyst
        Note right of Team: Analysis: 25% CAGR
    end

    Note over W: Report Phase

    rect rgb(248, 240, 255)
        W->>Team: search_memory<br/>agent_id: writer
        Team-->>W: 8 findings from all agents
        W->>W: Generate report
    end
```

### Knowledge Flow State Diagram

```mermaid
stateDiagram-v2
    [*] --> ProjectStart

    ProjectStart --> TeamStoreCreated: create_memory_store<br/>scope: team

    TeamStoreCreated --> ResearchPhase

    state ResearchPhase {
        [*] --> GatheringData
        GatheringData --> StoreFinding: update_memory<br/>agent_id: researcher
        StoreFinding --> GatheringData
        StoreFinding --> [*]
    }

    ResearchPhase --> AnalysisPhase

    state AnalysisPhase {
        [*] --> CreateAgentStore: create_memory_store<br/>scope: agent
        CreateAgentStore --> StoreProcedure: update_memory<br/>(agent-scoped)
        StoreProcedure --> RunAnalysis
        RunAnalysis --> ShareAnalysis: update_memory<br/>strategy: append
        ShareAnalysis --> [*]
    }

    AnalysisPhase --> ReportPhase

    state ReportPhase {
        [*] --> SearchKnowledge: search_memory<br/>agent_id: writer
        SearchKnowledge --> GenerateReport
        GenerateReport --> [*]
    }

    ReportPhase --> ProjectComplete
    ProjectComplete --> [*]
```

## Technical Breakdown

### Spans Generated

| Step | Agent | Operation | Key Attributes |
|------|-------|-----------|----------------|
| 1 | Crew | `create_memory_store` | scope=team, namespace=project_id |
| 2 | Researcher | `update_memory` | agent_id=researcher |
| 3 | Researcher | `update_memory` | agent_id=researcher |
| 4 | Analyst | `create_memory_store` | scope=agent |
| 5 | Analyst | `update_memory` | type=long_term, agent_id=analyst |
| 6 | Analyst | `update_memory` | strategy=append, agent_id=analyst |
| 7 | Writer | `search_memory` | result_count=8, agent_id=writer |

### Attribute Coverage

| Attribute | Value | Purpose |
|-----------|-------|---------|
| `gen_ai.memory.scope` | `team` | Shared knowledge base |
| `gen_ai.memory.scope` | `agent` | Private procedural memory |
| `gen_ai.memory.type` | `long_term` | Persistent knowledge |
| `gen_ai.memory.update.strategy` | `append` | Add without overwriting |
| `gen_ai.memory.namespace` | `ev_research_2025` | Project isolation |
| `gen_ai.agent.id` | `researcher_agent`, etc. | Attribution |

### Sample Trace Output

```json
{
  "name": "update_memory ev-research-team",
  "kind": "SpanKind.CLIENT",
  "parent_id": "invoke_agent analyst_agent",
  "attributes": {
    "gen_ai.operation.name": "update_memory",
    "gen_ai.provider.name": "milvus",
    "gen_ai.memory.store.id": "store_team_ev_research_2025",
    "gen_ai.memory.store.name": "ev-research-team",
    "gen_ai.memory.id": "analysis_abc123def456",
    "gen_ai.memory.type": "long_term",
    "gen_ai.memory.update.strategy": "append",
    "gen_ai.memory.namespace": "ev_research_2025",
    "gen_ai.agent.id": "analyst_agent"
  }
}
```

## Running the Scenario

```bash
# Activate virtual environment
source ../../../.venv/bin/activate

# Run the scenario
python python/main.py

# With OTLP export
GENAI_MEMORY_USE_OTLP=true python python/main.py

# With query/content capture
GENAI_MEMORY_CAPTURE_CONTENT=true python python/main.py
```

## Expected Output

```
======================================================================
  Story 3: Multi-Agent Research Crew
======================================================================

Scenario: ResearchCo receives a request to analyze the EV market...

======================================================================
  Step 1: Create Team Knowledge Base
======================================================================

  [create_memory_store (team)]
    gen_ai.memory.scope: team
    gen_ai.memory.namespace: ev_research_2025
    ...

======================================================================
  Step 2: Researcher Gathers Data
======================================================================

  [update_memory (researcher finding)]
    gen_ai.agent.id: researcher_agent
    ...

  Researcher stored: 'EV market size reached $500B in 2024'
```

## Multi-Agent Patterns

### Team vs Agent Scope

| Scope | Use Case | Example |
|-------|----------|---------|
| `team` | Shared findings, collaboration | Market research findings |
| `agent` | Private procedures, learned methods | Analysis methodology |

### Update Strategies

| Strategy | Use Case |
|----------|----------|
| `append` | Add new findings to team knowledge |
| `merge` | Combine analysis with existing data |
| `overwrite` | Replace outdated information |

### Attribution Tracking

The `gen_ai.agent.id` attribute enables:
- **Knowledge Attribution**: Who contributed what
- **Debugging**: Which agent's contribution caused issues
- **Analytics**: Agent contribution metrics

## Related Stories

- [Story 4: Multi-Tenant SaaS](../story4_multi_tenant_saas/) - Namespace isolation
- [Story 5: Compliance Audit](../story5_compliance_audit/) - Tracing agent operations
