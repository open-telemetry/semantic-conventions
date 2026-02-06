#!/usr/bin/env python3
"""
Story 3: Multi-Agent Research Crew

This scenario demonstrates a team of specialized AI agents collaborating:
1. Team knowledge base (team scope) for shared findings
2. Agent-specific procedural stores (agent scope)
3. Researcher stores findings with agent attribution
4. Analyst appends analysis using update.strategy="append"
5. Writer searches team knowledge for report generation

Key Attributes Demonstrated:
- gen_ai.memory.scope: agent, team (on create_memory_store)
- gen_ai.memory.type: long_term
- gen_ai.memory.update.strategy: append
- gen_ai.agent.id: attribution for each agent

Memory Spans Used:
- create_memory_store: Team and agent stores
- update_memory: Store findings with append strategy
- search_memory: Retrieve team knowledge

Run with:
    python main.py

To export to OTLP:
    GENAI_MEMORY_USE_OTLP=true python main.py
"""

import os
import json
import sys
import uuid

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "core", "python"))

from opentelemetry.trace import SpanKind

from genai_memory_otel import (
    GenAIAttributes,
    LLMClient,
    MemoryAttributes,
    MemoryScope,
    MemorySpanBuilder,
    MemoryType,
    MemoryUpdateStrategy,
    execute_tool_span,
    setup_tracing,
)


def print_section(title: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print("=" * 70)


def print_span_info(operation: str, attributes: dict) -> None:
    print(f"\n  [{operation}]")
    for key, value in attributes.items():
        print(f"    {key}: {value}")


def run_agent_llm_step(
    tracer,
    *,
    llm: LLMClient,
    agent_name: str,
    task: str,
    conversation_id: str,
    context: str = "",
    max_tokens: int = 300,
) -> str:
    full_task = f"Task: {task}"
    if context:
        full_task = f"{context}\n\nTask: {task}"

    result = llm.chat(
        tracer,
        messages=[{"role": "user", "content": full_task}],
        system_prompt=f"You are {agent_name}, part of a multi-agent research crew analyzing the EV market. Provide detailed, data-driven insights.",
        conversation_id=conversation_id,
        max_tokens=max_tokens,
        temperature=0.3,
        emit_events=True,
    )
    return result.content


# Real EV market data for enriched context
EV_MARKET_DATA = {
    "market_size": {
        "2023": "$500 billion",
        "2024": "$623 billion",
        "2025_projected": "$780 billion",
        "2030_projected": "$1.9 trillion",
    },
    "market_share": {
        "Tesla": "19.5%",
        "BYD": "17.8%",
        "Volkswagen Group": "8.2%",
        "SAIC Motor": "6.1%",
        "Hyundai-Kia": "5.8%",
        "GM": "4.9%",
        "BMW Group": "4.2%",
        "Mercedes-Benz": "3.8%",
        "Stellantis": "3.5%",
        "Others": "26.2%",
    },
    "regional_growth": {
        "China": {"share": "59%", "growth": "+22% YoY", "units_2024": "10.1M"},
        "Europe": {"share": "21%", "growth": "+18% YoY", "units_2024": "3.6M"},
        "North America": {"share": "12%", "growth": "+25% YoY", "units_2024": "2.0M"},
        "Rest of World": {"share": "8%", "growth": "+35% YoY", "units_2024": "1.4M"},
    },
    "key_trends": [
        "Battery costs declined 14% in 2024 to $115/kWh average",
        "Solid-state batteries expected commercial 2027-2028",
        "Average EV range increased to 320 miles (up from 280 in 2023)",
        "Charging infrastructure grew 45% globally in 2024",
        "EV-to-grid (V2G) adoption accelerating in Europe and California",
    ],
    "challenges": [
        "Raw material supply constraints (lithium, cobalt, nickel)",
        "Charging infrastructure gaps in rural areas",
        "Grid capacity concerns in high-adoption regions",
        "Used EV market uncertainty affecting resale values",
    ],
    "policy_drivers": [
        "EU: 2035 ICE ban confirmed",
        "US: $7,500 tax credit with domestic content requirements",
        "China: NEV mandate requiring 38% of sales by 2025",
        "California: 100% ZEV sales by 2035",
    ],
}


def run_multi_agent_research_scenario() -> None:
    print_section("Story 3: Multi-Agent Research Crew")
    print(
        """
Scenario: ResearchCo receives a request to analyze the EV market.
The team includes:
  - Researcher Agent: Gathers market data
  - Analyst Agent: Interprets data and identifies trends
  - Writer Agent: Produces the final report

Memory Architecture:
  - Team Knowledge Base: Shared findings (team scope)
  - Agent Procedural Stores: Agent-specific methods (agent scope)
"""
    )

    # Setup tracing
    use_otlp = os.getenv("GENAI_MEMORY_USE_OTLP", "false").lower() == "true"
    use_console = os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true"
    capture_content = os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"

    tracer = setup_tracing(
        service_name="genai-memory-stories",
        use_console=use_console,
        use_otlp=use_otlp,
        capture_content=capture_content,
    )
    span_builder = MemorySpanBuilder(tracer, capture_content=capture_content)

    # Team and agent identifiers
    project_id = "ev_research_2025"
    team_store_id = f"store_team_{project_id}"
    researcher_id = "researcher_agent"
    analyst_id = "analyst_agent"
    writer_id = "writer_agent"
    conversation_id = f"conv_research_{uuid.uuid4().hex[:8]}"

    print(f"\nProject: {project_id}")
    print(f"Team Store: {team_store_id}")
    print(f"Agents: {researcher_id}, {analyst_id}, {writer_id}")
    print(f"Conversation ID: {conversation_id}")

    llm = LLMClient()
    agent_provider = llm.provider_name()

    with tracer.start_as_current_span(
        f"story_3.multi_agent_research.{conversation_id}",
        kind=SpanKind.INTERNAL,
        attributes={
            "story.id": 3,
            "story.title": "Multi-Agent Research Crew",
            "scenario.name": "ev_market_research",
            GenAIAttributes.CONVERSATION_ID: conversation_id,
        },
    ):
        # Optional: demonstrate create_agent spans (remote agent service semantics)
        for agent_name, agent_id in [
            ("ResearchCrew", "crew_001"),
            ("Researcher", researcher_id),
            ("Analyst", analyst_id),
            ("Writer", writer_id),
        ]:
            with tracer.start_as_current_span(
                f"create_agent {agent_name}",
                kind=SpanKind.CLIENT,
                attributes={
                    GenAIAttributes.OPERATION_NAME: "create_agent",
                    GenAIAttributes.PROVIDER_NAME: agent_provider,
                    GenAIAttributes.REQUEST_MODEL: llm.model,
                    "server.address": "api.openai.com",
                    GenAIAttributes.AGENT_NAME: agent_name,
                    GenAIAttributes.AGENT_ID: agent_id,
                    GenAIAttributes.CONVERSATION_ID: conversation_id,
                },
            ):
                pass

        with tracer.start_as_current_span(
            "invoke_agent ResearchCrew",
            kind=SpanKind.CLIENT,
            attributes={
                GenAIAttributes.OPERATION_NAME: "invoke_agent",
                GenAIAttributes.PROVIDER_NAME: agent_provider,
                GenAIAttributes.REQUEST_MODEL: llm.model,
                "server.address": "api.openai.com",
                GenAIAttributes.AGENT_NAME: "ResearchCrew",
                GenAIAttributes.AGENT_ID: "crew_001",
                GenAIAttributes.CONVERSATION_ID: conversation_id,
            },
        ) as crew_span:
            crew_request = "Analyze the EV market for 2025 and produce a concise report."
            if capture_content:
                crew_span.set_attribute(
                    "gen_ai.input.messages",
                    json.dumps(
                        [{"role": "user", "parts": [{"type": "text", "content": crew_request}]}],
                        ensure_ascii=False,
                    ),
                )

            # 1. Create team knowledge base
            print_section("Step 1: Create Team Knowledge Base")

            with span_builder.create_memory_store_span(
                provider_name="milvus",
                store_name="ev-research-team",
                scope=MemoryScope.TEAM,
                memory_type=MemoryType.LONG_TERM,
                namespace=project_id,
            ) as span:
                span.set_attribute(MemoryAttributes.STORE_ID, team_store_id)
                print_span_info(
                    "create_memory_store (team)",
                    {
                        "gen_ai.operation.name": "create_memory_store",
                        "gen_ai.provider.name": "milvus",
                        "gen_ai.memory.store.name": "ev-research-team",
                        "gen_ai.memory.store.id": team_store_id,
                        "gen_ai.memory.scope": MemoryScope.TEAM,
                        "gen_ai.memory.type": MemoryType.LONG_TERM,
                        "gen_ai.memory.namespace": project_id,
                    },
                )

            # 2. Researcher gathers data and stores findings
            print_section("Step 2: Researcher Gathers Data")

            with tracer.start_as_current_span(
                "invoke_agent Researcher",
                kind=SpanKind.CLIENT,
                attributes={
                    GenAIAttributes.OPERATION_NAME: "invoke_agent",
                    GenAIAttributes.PROVIDER_NAME: agent_provider,
                    GenAIAttributes.REQUEST_MODEL: llm.model,
                    "server.address": "api.openai.com",
                    GenAIAttributes.AGENT_NAME: "Researcher",
                    GenAIAttributes.AGENT_ID: researcher_id,
                    GenAIAttributes.CONVERSATION_ID: conversation_id,
                },
            ) as researcher_span:
                with execute_tool_span(
                    tracer,
                    tool_name="fetch_market_data",
                    tool_type="function",
                    tool_description="Fetch EV market data from an external API",
                    tool_call_id=f"call_{uuid.uuid4().hex[:10]}",
                    arguments={"topic": "EV market", "region": "global", "year": 2025},
                    result={"status": "ok", "items": 3},
                    capture_content=capture_content,
                ):
                    pass

                researcher_context = f"""
You have gathered the following EV market data from reliable sources:

MARKET SIZE:
{json.dumps(EV_MARKET_DATA['market_size'], indent=2)}

MARKET SHARE BY MANUFACTURER:
{json.dumps(EV_MARKET_DATA['market_share'], indent=2)}

REGIONAL GROWTH:
{json.dumps(EV_MARKET_DATA['regional_growth'], indent=2)}
"""
                researcher_output = run_agent_llm_step(
                    tracer,
                    llm=llm,
                    agent_name="Researcher",
                    task="Summarize the key findings from this EV market data. Focus on market size trajectory, leading manufacturers, and regional dynamics.",
                    conversation_id=conversation_id,
                    context=researcher_context,
                    max_tokens=400,
                )
                print(f"\n  Researcher: {researcher_output}")

                if capture_content:
                    researcher_span.set_attribute(
                        "gen_ai.input.messages",
                        json.dumps(
                            [{"role": "user", "parts": [{"type": "text", "content": "Task: gather EV market data"}]}],
                            ensure_ascii=False,
                        ),
                    )
                    researcher_span.set_attribute(
                        "gen_ai.output.messages",
                        json.dumps(
                            [{"role": "assistant", "parts": [{"type": "text", "content": researcher_output}]}],
                            ensure_ascii=False,
                        ),
                    )

                finding_id_1 = f"finding_{uuid.uuid4().hex[:12]}"
                with span_builder.update_memory_span(
                    provider_name="milvus",
                    store_id=team_store_id,
                    store_name="ev-research-team",
                    memory_id=finding_id_1,
                    memory_type=MemoryType.LONG_TERM,
                    agent_id=researcher_id,
                    namespace=project_id,
                    conversation_id=conversation_id,
                ) as span:
                    print_span_info(
                        "update_memory (researcher finding)",
                        {
                            "gen_ai.operation.name": "update_memory",
                            "gen_ai.provider.name": "milvus",
                            "gen_ai.memory.store.id": team_store_id,
                            "gen_ai.memory.id": finding_id_1,
                            "gen_ai.memory.type": MemoryType.LONG_TERM,
                            "gen_ai.agent.id": researcher_id,
                        },
                    )

                print("\n  Researcher stored: 'EV market size reached $500B in 2024'")

                finding_id_2 = f"finding_{uuid.uuid4().hex[:12]}"
                with span_builder.update_memory_span(
                    provider_name="milvus",
                    store_id=team_store_id,
                    store_name="ev-research-team",
                    memory_id=finding_id_2,
                    memory_type=MemoryType.LONG_TERM,
                    agent_id=researcher_id,
                    namespace=project_id,
                    conversation_id=conversation_id,
                ):
                    pass

                print("  Researcher stored: 'Tesla maintains 20% market share'")

                researcher_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 450)
                researcher_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 350)

            # 3. Analyst creates agent-specific procedural store
            print_section("Step 3: Analyst Creates Procedural Memory")

            analyst_store_id = f"store_{analyst_id}_procedures"
            with span_builder.create_memory_store_span(
                provider_name="chroma",
                store_name="analyst-procedures",
                scope=MemoryScope.AGENT,
                memory_type=MemoryType.LONG_TERM,
            ) as span:
                span.set_attribute(MemoryAttributes.STORE_ID, analyst_store_id)
                print_span_info(
                    "create_memory_store (agent)",
                    {
                        "gen_ai.operation.name": "create_memory_store",
                        "gen_ai.provider.name": "chroma",
                        "gen_ai.memory.store.name": "analyst-procedures",
                        "gen_ai.memory.store.id": analyst_store_id,
                        "gen_ai.memory.scope": MemoryScope.AGENT,
                        "gen_ai.memory.type": MemoryType.LONG_TERM,
                    },
                )

            proc_id = f"proc_{uuid.uuid4().hex[:12]}"
            with span_builder.update_memory_span(
                provider_name="chroma",
                store_id=analyst_store_id,
                store_name="analyst-procedures",
                memory_id=proc_id,
                memory_type=MemoryType.LONG_TERM,
                agent_id=analyst_id,
            ) as span:
                print_span_info(
                    "update_memory (analyst procedure)",
                    {
                        "gen_ai.operation.name": "update_memory",
                        "gen_ai.provider.name": "chroma",
                        "gen_ai.memory.store.id": analyst_store_id,
                        "gen_ai.memory.id": proc_id,
                        "gen_ai.memory.type": MemoryType.LONG_TERM,
                        "gen_ai.agent.id": analyst_id,
                    },
                )

            print("\n  Analyst stored procedure: 'trend_analysis_v2'")

            # 4. Analyst shares analysis with team (append strategy)
            print_section("Step 4: Analyst Shares Analysis (Append)")

            with tracer.start_as_current_span(
                "invoke_agent Analyst",
                kind=SpanKind.CLIENT,
                attributes={
                    GenAIAttributes.OPERATION_NAME: "invoke_agent",
                    GenAIAttributes.PROVIDER_NAME: agent_provider,
                    GenAIAttributes.REQUEST_MODEL: llm.model,
                    "server.address": "api.openai.com",
                    GenAIAttributes.AGENT_NAME: "Analyst",
                    GenAIAttributes.AGENT_ID: analyst_id,
                    GenAIAttributes.CONVERSATION_ID: conversation_id,
                },
            ) as analyst_span:
                analyst_context = f"""
Building on the researcher's findings, analyze these trends and factors:

KEY INDUSTRY TRENDS:
{json.dumps(EV_MARKET_DATA['key_trends'], indent=2)}

MARKET CHALLENGES:
{json.dumps(EV_MARKET_DATA['challenges'], indent=2)}

POLICY DRIVERS:
{json.dumps(EV_MARKET_DATA['policy_drivers'], indent=2)}

GROWTH DATA:
- Market grew from $500B (2023) to $623B (2024) = 24.6% growth
- Projected to reach $1.9T by 2030 (CAGR ~20%)
- Global EV sales: 17.1M units in 2024 (up from 14.2M in 2023)
"""
                analyst_output = run_agent_llm_step(
                    tracer,
                    llm=llm,
                    agent_name="Analyst",
                    task="Analyze the growth trajectory and identify the 3-4 most critical factors that will determine EV market success through 2030. Include specific projections.",
                    conversation_id=conversation_id,
                    context=analyst_context,
                    max_tokens=500,
                )
                print(f"\n  Analyst: {analyst_output}")

                if capture_content:
                    analyst_span.set_attribute(
                        "gen_ai.input.messages",
                        json.dumps(
                            [{"role": "user", "parts": [{"type": "text", "content": "Task: analyze growth trends"}]}],
                            ensure_ascii=False,
                        ),
                    )
                    analyst_span.set_attribute(
                        "gen_ai.output.messages",
                        json.dumps(
                            [{"role": "assistant", "parts": [{"type": "text", "content": analyst_output}]}],
                            ensure_ascii=False,
                        ),
                    )

                analysis_id = f"analysis_{uuid.uuid4().hex[:12]}"
                with span_builder.update_memory_span(
                    provider_name="milvus",
                    store_id=team_store_id,
                    store_name="ev-research-team",
                    memory_id=analysis_id,
                    memory_type=MemoryType.LONG_TERM,
                    update_strategy=MemoryUpdateStrategy.APPEND,
                    agent_id=analyst_id,
                    namespace=project_id,
                    conversation_id=conversation_id,
                ) as span:
                    print_span_info(
                        "update_memory (append analysis)",
                        {
                            "gen_ai.operation.name": "update_memory",
                            "gen_ai.provider.name": "milvus",
                            "gen_ai.memory.store.id": team_store_id,
                            "gen_ai.memory.id": analysis_id,
                            "gen_ai.memory.type": MemoryType.LONG_TERM,
                            "gen_ai.memory.update.strategy": MemoryUpdateStrategy.APPEND,
                            "gen_ai.agent.id": analyst_id,
                        },
                    )

                print("\n  Analyst appended: 'Growth projection: 25% CAGR through 2030'")

                analyst_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 520)
                analyst_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 450)

            # 5. Writer searches team knowledge for report
            print_section("Step 5: Writer Searches Team Knowledge")

            with tracer.start_as_current_span(
                "invoke_agent Writer",
                kind=SpanKind.CLIENT,
                attributes={
                    GenAIAttributes.OPERATION_NAME: "invoke_agent",
                    GenAIAttributes.PROVIDER_NAME: agent_provider,
                    GenAIAttributes.REQUEST_MODEL: llm.model,
                    "server.address": "api.openai.com",
                    GenAIAttributes.AGENT_NAME: "Writer",
                    GenAIAttributes.AGENT_ID: writer_id,
                    GenAIAttributes.CONVERSATION_ID: conversation_id,
                },
            ) as writer_span:
                with span_builder.search_memory_span(
                    provider_name="milvus",
                    store_id=team_store_id,
                    store_name="ev-research-team",
                    query="EV market size growth projections",
                    memory_type=MemoryType.LONG_TERM,
                    namespace=project_id,
                    agent_id=writer_id,
                    conversation_id=conversation_id,
                ) as span:
                    span.set_attribute(MemoryAttributes.SEARCH_RESULT_COUNT, 8)
                    print_span_info(
                        "search_memory (writer)",
                        {
                            "gen_ai.operation.name": "search_memory",
                            "gen_ai.provider.name": "milvus",
                            "gen_ai.memory.store.id": team_store_id,
                            "gen_ai.memory.query": (
                                "EV market size growth projections" if capture_content else "(opt-in disabled)"
                            ),
                            "gen_ai.memory.type": MemoryType.LONG_TERM,
                            "gen_ai.memory.search.result.count": 8,
                            "gen_ai.agent.id": writer_id,
                        },
                    )

                print("\n  Writer retrieved 8 findings from team knowledge:")
                print("    - 2 findings from Researcher (market data)")
                print("    - 1 analysis from Analyst (growth projections)")
                print("    - 5 additional context items")

                writer_context = f"""
You are compiling the final EV Market Research Report for 2025. Based on the team's findings:

RESEARCHER'S KEY FINDINGS:
{researcher_output}

ANALYST'S STRATEGIC ANALYSIS:
{analyst_output}

COMPREHENSIVE DATA AVAILABLE:
- Market Size: $623B (2024) → $780B (2025 projected) → $1.9T (2030 projected)
- Total 2024 Sales: 17.1 million units globally
- Leading Players: Tesla (19.5%), BYD (17.8%), VW Group (8.2%)
- Fastest Growing Region: Rest of World (+35% YoY)
- Largest Market: China (59% share, 10.1M units)
- Key Tech: Battery costs at $115/kWh, avg range 320 miles
- Major Policy: EU 2035 ICE ban, US $7,500 tax credit, China 38% NEV mandate

REPORT STRUCTURE REQUIRED:
1. Executive Summary
2. Market Overview
3. Competitive Landscape
4. Regional Analysis
5. Key Trends & Technology
6. Outlook & Recommendations
"""
                writer_output = run_agent_llm_step(
                    tracer,
                    llm=llm,
                    agent_name="Writer",
                    task="Generate a comprehensive EV Market Research Report following the structure above. Include specific data points, percentages, and actionable insights. This is for executive stakeholders.",
                    conversation_id=conversation_id,
                    context=writer_context,
                    max_tokens=1200,
                )
                print(f"\n  Writer: {writer_output}")

                if capture_content:
                    writer_span.set_attribute(
                        "gen_ai.input.messages",
                        json.dumps(
                            [{"role": "user", "parts": [{"type": "text", "content": "Task: generate final report"}]}],
                            ensure_ascii=False,
                        ),
                    )
                    writer_span.set_attribute(
                        "gen_ai.output.messages",
                        json.dumps(
                            [{"role": "assistant", "parts": [{"type": "text", "content": writer_output}]}],
                            ensure_ascii=False,
                        ),
                    )

                writer_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 1800)
                writer_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 1100)

            if capture_content:
                crew_span.set_attribute(
                    "gen_ai.output.messages",
                    json.dumps(
                        [
                            {
                                "role": "assistant",
                                "parts": [{"type": "text", "content": writer_output}],
                            }
                        ],
                        ensure_ascii=False,
                    ),
                )
            crew_span.set_attribute(GenAIAttributes.USAGE_INPUT_TOKENS, 2770)
            crew_span.set_attribute(GenAIAttributes.USAGE_OUTPUT_TOKENS, 1900)

    # Summary
    print_section("Scenario Complete!")
    print(
        """
Trace Summary:
  - 2x create_memory_store (team + analyst agent)
  - 4x update_memory (2 findings + 1 procedure + 1 analysis with append)
  - 1x search_memory (writer retrieves all)
  - 3x invoke_agent (researcher, analyst, writer)
  - 3x chat (agent LLM calls)

Key Observability Insights:
  - Team-scoped memory enables collaboration between agents
  - Agent-scoped memory keeps procedural knowledge private
  - gen_ai.agent.id provides attribution for each contribution
  - Append strategy adds to existing knowledge without overwriting
  - Namespace isolates project-specific knowledge
"""
    )

    if use_otlp:
        print("Traces exported to OTLP collector.")
    else:
        print("Tip: Set GENAI_MEMORY_USE_OTLP=true to export to a collector.")


if __name__ == "__main__":
    run_multi_agent_research_scenario()
