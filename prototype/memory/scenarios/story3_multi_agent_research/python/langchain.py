#!/usr/bin/env python3
"""
Story 3: Multi-Agent Research Crew (LangChain Implementation)

This shows how multi-agent scenarios with shared memory map to LangChain patterns.

Key Patterns Demonstrated:
- Shared memory across agents (team scope) using a common VectorStore
- Agent-specific memory (agent scope)
- Append strategy for accumulating findings

LangChain Multi-Agent Patterns:
- CrewAI/AutoGen style: Agents share a common memory backend
- LangGraph: State passed between nodes can be instrumented as memory
- Agent Tools: Memory search as a tool available to agents

Key Mappings:
| Pattern                        | gen_ai.operation.name | gen_ai.memory.scope |
|--------------------------------|----------------------|---------------------|
| Shared VectorStore             | search_memory        | team                |
| Agent stores finding           | update_memory        | team + agent.id     |
| Agent-specific memory          | update_memory        | agent               |
| Append to existing findings    | update_memory        | strategy: append    |

Run with:
    pip install langchain langchain-openai opentelemetry-api
    python langchain.py
"""

import os
import sys
import uuid
from typing import Dict, Any, List

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core', 'python'))

from opentelemetry import trace
from opentelemetry.trace import SpanKind

from genai_memory_otel import (
    setup_tracing,
    MemoryType,
    MemoryScope,
    MemoryUpdateStrategy,
    MemoryAttributes,
    GenAIAttributes,
)


class InstrumentedSharedMemory:
    """
    Simulates a shared memory store accessible by multiple agents.

    In LangChain/CrewAI patterns, this could be:
    - A shared VectorStore instance passed to all agents
    - A Redis/Postgres backend that multiple agents connect to
    - LangGraph state that flows between agent nodes

    Maps to team-scoped memory with agent attribution.
    """

    def __init__(
        self,
        tracer: trace.Tracer,
        *,
        store_name: str,
        namespace: str,
        capture_content: bool = False,
    ):
        self.tracer = tracer
        self.store_name = store_name
        self.store_id = f"store_{namespace}_team"
        self.namespace = namespace
        self.capture_content = capture_content
        self._findings: List[Dict[str, Any]] = []

    def add_finding(
        self,
        agent_id: str,
        content: str,
        *,
        strategy: str = MemoryUpdateStrategy.APPEND,
    ) -> None:
        """
        Agent adds a finding to shared team memory.

        In CrewAI: agent.memory.add(finding)
        In LangGraph: state["findings"].append(finding)

        OTel Span: update_memory with team scope and agent attribution
        """
        memory_id = f"finding_{len(self._findings):03d}"

        with self.tracer.start_as_current_span(
            f"update_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "update_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.MEMORY_ID: memory_id,
                MemoryAttributes.SCOPE: MemoryScope.TEAM,
                MemoryAttributes.TYPE: MemoryType.LONG_TERM,
                MemoryAttributes.NAMESPACE: self.namespace,
                MemoryAttributes.UPDATE_STRATEGY: strategy,
                GenAIAttributes.AGENT_ID: agent_id,  # Attribution
            },
        ) as span:
            self._findings.append({
                "id": memory_id,
                "agent_id": agent_id,
                "content": content,
            })

            if self.capture_content:
                span.set_attribute(MemoryAttributes.CONTENT, content[:500])

    def search(
        self,
        query: str,
        agent_id: str,
        *,
        similarity_threshold: float = 0.7,
    ) -> List[Dict[str, Any]]:
        """
        Agent searches shared team memory.

        In CrewAI: agent.memory.search(query)
        In LangGraph: Access state["findings"]

        OTel Span: search_memory with team scope
        """
        with self.tracer.start_as_current_span(
            f"search_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "search_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.SCOPE: MemoryScope.TEAM,
                MemoryAttributes.TYPE: MemoryType.LONG_TERM,
                MemoryAttributes.NAMESPACE: self.namespace,
                MemoryAttributes.SEARCH_SIMILARITY_THRESHOLD: similarity_threshold,
                GenAIAttributes.AGENT_ID: agent_id,
            },
        ) as span:
            if self.capture_content and query:
                span.set_attribute(MemoryAttributes.QUERY, query)

            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, len(self._findings))
            return self._findings.copy()


class InstrumentedAgentMemory:
    """
    Agent-specific memory that is not shared with other agents.

    This represents an agent's private working memory or procedural memory.

    Maps to agent-scoped memory.
    """

    def __init__(
        self,
        tracer: trace.Tracer,
        *,
        agent_id: str,
        agent_name: str,
        capture_content: bool = False,
    ):
        self.tracer = tracer
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.store_name = f"{agent_name}-memory"
        self.store_id = f"store_{agent_id}"
        self.capture_content = capture_content
        self._procedures: List[str] = []

    def store_procedure(self, procedure: str) -> None:
        """
        Agent stores a learned procedure in its private memory.

        OTel Span: update_memory with agent scope
        """
        memory_id = f"proc_{self.agent_id}_{len(self._procedures):03d}"

        with self.tracer.start_as_current_span(
            f"update_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "update_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.MEMORY_ID: memory_id,
                MemoryAttributes.SCOPE: MemoryScope.AGENT,
                MemoryAttributes.TYPE: MemoryType.LONG_TERM,
                GenAIAttributes.AGENT_ID: self.agent_id,
            },
        ) as span:
            self._procedures.append(procedure)

            if self.capture_content:
                span.set_attribute(MemoryAttributes.CONTENT, procedure[:500])

    def recall_procedures(self) -> List[str]:
        """
        Agent recalls its learned procedures.

        OTel Span: search_memory with agent scope
        """
        with self.tracer.start_as_current_span(
            f"search_memory {self.store_name}",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "search_memory",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                MemoryAttributes.STORE_ID: self.store_id,
                MemoryAttributes.STORE_NAME: self.store_name,
                MemoryAttributes.SCOPE: MemoryScope.AGENT,
                MemoryAttributes.TYPE: MemoryType.LONG_TERM,
                GenAIAttributes.AGENT_ID: self.agent_id,
            },
        ) as span:
            span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, len(self._procedures))
            return self._procedures.copy()


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def run_multi_agent_scenario():
    """
    Run the multi-agent research scenario using LangChain-style patterns.
    """
    print_section("Story 3: Multi-Agent Research Crew (LangChain Style)")
    print("""
This example shows how multi-agent memory patterns map to our semantic conventions:

- Team-scoped shared memory for findings all agents can access
- Agent-scoped private memory for individual procedures
- Agent attribution (gen_ai.agent.id) for tracking who stored what
- Append strategy for accumulating research findings

In CrewAI/AutoGen/LangGraph, agents often share a common memory backend.
Our conventions capture this with:
- gen_ai.memory.scope: team
- gen_ai.agent.id: which agent performed the operation
""")

    # Setup tracing
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="research-crew-langchain",
        use_console=use_console,
        capture_content=capture_content,
    )

    # Research project parameters
    project_id = f"project_{uuid.uuid4().hex[:8]}"

    # Define agents
    researcher_id = "agent_researcher_001"
    analyst_id = "agent_analyst_002"
    writer_id = "agent_writer_003"

    print(f"\nProject Info:")
    print(f"  Project ID: {project_id}")
    print(f"  Agents: Researcher, Analyst, Writer")

    # Initialize shared team memory
    team_memory = InstrumentedSharedMemory(
        tracer,
        store_name="team-knowledge",
        namespace=project_id,
        capture_content=capture_content,
    )

    # Initialize agent-specific memories
    researcher_memory = InstrumentedAgentMemory(
        tracer,
        agent_id=researcher_id,
        agent_name="researcher",
        capture_content=capture_content,
    )

    analyst_memory = InstrumentedAgentMemory(
        tracer,
        agent_id=analyst_id,
        agent_name="analyst",
        capture_content=capture_content,
    )

    # Start crew orchestration
    with tracer.start_as_current_span(
        "invoke_agent ResearchCrew",
        kind=SpanKind.CLIENT,
        attributes={
            GenAIAttributes.OPERATION_NAME: "invoke_agent",
            GenAIAttributes.PROVIDER_NAME: "langchain",
            GenAIAttributes.AGENT_NAME: "ResearchCrew",
        },
    ):
        # Step 1: Researcher finds data
        print_section("Step 1: Researcher Agent Stores Finding")
        with tracer.start_as_current_span(
            f"invoke_agent Researcher",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "invoke_agent",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                GenAIAttributes.AGENT_ID: researcher_id,
                GenAIAttributes.AGENT_NAME: "Researcher",
            },
        ):
            # Store finding in team memory (with agent attribution)
            team_memory.add_finding(
                researcher_id,
                "Found 3 key papers on transformer architectures",
                strategy=MemoryUpdateStrategy.APPEND,
            )
            print("  Researcher stored finding in team memory")
            print(f"    gen_ai.agent.id: {researcher_id}")
            print("    gen_ai.memory.scope: team")
            print("    gen_ai.memory.update.strategy: append")

            # Store procedure in agent's private memory
            researcher_memory.store_procedure("Use arXiv API for paper search")
            print("  Researcher stored procedure in private memory")

        # Step 2: Analyst reads and adds analysis
        print_section("Step 2: Analyst Agent Adds Analysis")
        with tracer.start_as_current_span(
            f"invoke_agent Analyst",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "invoke_agent",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                GenAIAttributes.AGENT_ID: analyst_id,
                GenAIAttributes.AGENT_NAME: "Analyst",
            },
        ):
            # Search team memory
            findings = team_memory.search(
                "transformer papers",
                analyst_id,
                similarity_threshold=0.7,
            )
            print(f"  Analyst searched team memory, found {len(findings)} items")

            # Append analysis
            team_memory.add_finding(
                analyst_id,
                "Analysis: Papers show attention mechanism improvements of 15%",
                strategy=MemoryUpdateStrategy.APPEND,
            )
            print("  Analyst appended analysis to team memory")
            print(f"    gen_ai.agent.id: {analyst_id}")

            # Store procedure
            analyst_memory.store_procedure("Compare metrics across papers")

        # Step 3: Writer compiles report
        print_section("Step 3: Writer Agent Compiles Report")
        with tracer.start_as_current_span(
            f"invoke_agent Writer",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "invoke_agent",
                GenAIAttributes.PROVIDER_NAME: "langchain",
                GenAIAttributes.AGENT_ID: writer_id,
                GenAIAttributes.AGENT_NAME: "Writer",
            },
        ):
            # Search all team findings
            all_findings = team_memory.search(
                "all research and analysis",
                writer_id,
            )
            print(f"  Writer searched team memory, found {len(all_findings)} items:")
            for finding in all_findings:
                print(f"    - From {finding['agent_id']}: {finding['content'][:50]}...")

    # Summary
    print_section("Multi-Agent Memory Mapping Summary")
    print("""
| Multi-Agent Pattern              | OTel Mapping                                     |
|----------------------------------|--------------------------------------------------|
| Shared team VectorStore          | scope: team, namespace: project_id               |
| Agent stores finding             | update_memory + gen_ai.agent.id attribution      |
| Agent reads shared memory        | search_memory + gen_ai.agent.id (who searched)   |
| Append findings (not replace)    | update_memory + strategy: append                 |
| Agent-specific memory            | scope: agent                                     |

Key Insight: In multi-agent systems, gen_ai.agent.id is critical for debugging:
- "Which agent stored incorrect information?"
- "Why did the writer miss the analyst's findings?"
- "How long did each agent spend on memory operations?"

The team scope + agent attribution pattern is unique to AI memory - traditional
databases don't track this semantic relationship between multiple autonomous actors.
""")


if __name__ == "__main__":
    run_multi_agent_scenario()
