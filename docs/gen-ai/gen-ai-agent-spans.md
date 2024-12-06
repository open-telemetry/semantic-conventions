<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Generative AI traces
--->

# Semantic Conventions for GenAI agent and framework spans

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [SPAN KIND](#span-kind)
- [Name](#name)
- [AI Agent attributes](#ai-agent-attributes)
  - [Workflow Attributes](#workflow-attributes)
  - [Agent Attributes](#agent-attributes)
  - [Tools Attributes](#tools-attributes)
  - [Task Attributes](#task-attributes)
  - [Interaction Attributes](#interaction-attributes)
- [Examples](#examples)
  - [Workflow: Market Analysis Pipeline](#workflow-market-analysis-pipeline)
  - [Agents Involved](#agents-involved)
    - [DataCollectorAgent](#datacollectoragent)
    - [DataAnalystAgent](#dataanalystagent)
  - [Tasks and Tools](#tasks-and-tools)
    - [Task: Data Collection](#task-data-collection)
    - [Tool Utilized: WebScraperTool](#tool-utilized-webscrapertool)
    - [Task: Data Analysis](#task-data-analysis)
    - [Tool Utilized: DataAnalyzerTool](#tool-utilized-dataanalyzertool)

<!-- tocstop -->

Generative AI scenarios may involve multiple steps. For example RAG pattern implementation usually involves
the following steps:

- initial request to the GenAI model to rewrite user query
- getting embeddings for the rewritten query
- searching for similar documents in the vector store using embeddings
- getting completion from the GenAI model based on the similar documents.

These steps may be done by the application itself using GenAI models and vector databases.
It's also common to leverage client framework such as [LangGraph](https://github.com/langchain-ai/langgraph)
or service offerings such as [OpenAI Assistants](https://platform.openai.com/docs/assistants),
[Azure AI Agents](TODO link), or [Amazon Bedrock Agents](https://aws.amazon.com/bedrock/agents/).

This document defines semantic conventions for GenAI agent calls that are
handled by the remote agent service.
It MAY be applicable to agent operations that are performed by the GenAI
framework locally.

The semantic conventions for GenAI agents extend and override the semantic conventions
for [Gen AI Spans](gen-ai-spans.md).

## Spans

### Create Workflow Span

### Create Agent Span

Describes GenAI agent creation and is usually applicable when working with remote agent
services.

The `gen_ai.operation.name` MUST be `create_agent`.

The **span name** SHOULD be `create_agent {gen_ai.agent.name}`.
Semantic conventions for individual GenAI systems and frameworks MAY specify different span name format.

<!-- semconv trace.gen_ai.client.create_agent -->
<!-- endsemconv -->

### Create Task Span

<!-- semconv trace.gen_ai.client.create_task -->
<!-- endsemconv -->

### Create Tool Span

<!-- semconv trace.gen_ai.client.create_tool -->
<!-- endsemconv -->

### Run Tool Span

<!-- semconv trace.gen_ai.client.run_tool -->
<!-- endsemconv -->

### Run Task Span

<!-- semconv trace.gen_ai.client.run_task -->
<!-- endsemconv -->

### Run Workflow Span

<!-- semconv trace.gen_ai.client.run_workflow -->
<!-- endsemconv -->
