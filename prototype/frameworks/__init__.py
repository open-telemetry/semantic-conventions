"""
Framework Guardian Adapters

Thin adapters for integrating the GenAI Security Guardian semantic conventions
with popular agent frameworks. Each adapter:

1. Creates `apply_guardrail` spans as children of framework operation spans
2. Records `GuardianResult` and `SecurityFinding` attributes/events
3. Honors opt-in content capture via `OTEL_DEMO_CAPTURE_GUARDIAN_CONTENT`
4. Maps framework-specific IDs to `gen_ai.agent.id` and `gen_ai.conversation.id`

Available adapters:
- langchain: LangChain callback-based integration
- langgraph: LangGraph node-based integration
- agno: Agno middleware integration
- adk: Google ADK middleware integration
- semantic_kernel: Semantic Kernel filter integration
- mcp: Model Context Protocol interception

Usage:
    from frameworks.langchain.guardian_adapter import LangChainGuardianAdapter
    from frameworks.langgraph.guardian_adapter import LangGraphGuardianAdapter
    # etc.

Author: OpenTelemetry GenAI SIG
"""
