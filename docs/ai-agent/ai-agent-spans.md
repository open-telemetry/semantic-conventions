<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Generative AI traces
--->

# Semantic Conventions for AI Agent Spans

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

## SPAN KIND

Each step in an AI Agent workflow is treated as a span.

**Span kind:** SHOULD be `CLIENT`. It MAY be set to `INTERNAL` on spans representing call in an AI Agent workflow.

## Name

AI Agent spans MUST follow the overall [guidelines for span names](https://github.com/open-telemetry/opentelemetry-specification/tree/v1.39.0/specification/trace/api.md#span). The **span name** SHOULD be `{ai_agent.operation.name} {ai_agent.workflow.system}`.
Semantic conventions for individual AI Agent systems and frameworks MAY specify different span name format.

- ai_agent.operation.name: The operation being performed (e.g., `workflow.kickoff`,`agent.execution`, `task.execution`, `agent.interaction`).
- ai_agent.workflow.system: The type of agent performing the operation (e.g., `CrewAI`, `LangGraph`, `AutoGen`).

## AI Agent attributes

### Workflow Attributes

| Attribute                      | Type   | Description                                               | Example                           | Requirement Level | Stability    |
| ------------------------------ | ------ | --------------------------------------------------------- | --------------------------------- | ----------------- | --- |
| `ai_agent.workflow.name`       | string | Name of the workflow.                                     | `Data Processing Pipeline`        | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.workflow.tasks`      | array  | List of tasks included in the workflow.                   | `["Data Collection", "Analysis"]` | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.workflow.agents`     | array  | List of agents participating in the workflow.             | `["Agent A", "Agent B"]`          | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.workflow.config`     | object | Configuration settings for the workflow.                  | `{"setting1": "value1"}`          | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.workflow.start_time` | string | Timestamp when the workflow started.                      | `2024-12-06T10:00:00Z`            | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.workflow.end_time`   | string | Timestamp when the workflow ended.                        | `2024-12-06T11:00:00Z`            | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.workflow.end_state`  | string | Final state of the workflow (e.g., `success`, `failure`). | `success`                         | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.workflow.end_reason` | string | Reason for the workflow's end, if applicable.             | `Completed all tasks`             | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.workflow.system`     | string | System or environment where the workflow is executed.     | `CrewAI`, `LangGraph`, `AutoGen`  | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |

### Agent Attributes

| Attribute                      | Type   | Description                                | Example                          | Requirement Level | Stability    |
| ------------------------------ | ------ | ------------------------------------------ | -------------------------------- | ----------------- | --- |
| `ai_agent.agent.name`          | string | Name of the agent.                         | `Researcher Bot`                 | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.agent.role`          | string | Role assigned to the agent.                | `Data Collector`                 | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.agent.backstory`     | string | Background story or context for the agent. | `Specializes in web data mining` | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.agent.workflow_name` | string | Name of the workflow the agent is part of. | `Data Processing Pipeline`       | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.agent.model`         | string | Underlying model powering the agent.       | `gpt-4`                          | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.agent.tools`         | array  | List of tools available to the agent.      | `["Web Scraper", "Analyzer"]`    | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |

### Tools Attributes

| Attribute                | Type   | Description                                  | Example           | Requirement Level | Stability    |
| ------------------------ | ------ | -------------------------------------------- | ----------------- | ----------------- | --- |
| `ai_agent.tool.name`     | string | Name of the tool utilized by the agent.      | `Web Scraper`     | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.tool.function` | string | Specific function or capability of the tool. | `Data Extraction` | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.tool.output`   | object | Output produced by the tool.                 | `{"data": [...]}` | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |

### Task Attributes

| Attribute                   | Type    | Description                                                              | Example                            | Requirement Level | Stability    |
| --------------------------- | ------- | ------------------------------------------------------------------------ | ---------------------------------- | ----------------- | --- |
| `ai_agent.task.name`        | string  | Name of the task.                                                        | `Data Collection`                  | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.task.agent_name`  | string  | Name of the agent responsible for the task.                              | `Agent A`                          | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.task.description` | string  | Detailed description of the task.                                        | `Collect data from specified URLs` | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.task.output`      | object  | Output generated from the task.                                          | `{"collected_data": [...]}`        | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.task.priority`    | string  | Priority level of the task (e.g., `low`, `medium`, `high`).              | `high`                             | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.task.state`       | string  | Current state of the task (e.g., `pending`, `in_progress`, `completed`). | `in_progress`                      | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.task.duration`    | integer | Duration taken to complete the task in milliseconds.                     | `120000`                           | Recommended       | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |

### Interaction Attributes

| Attribute                     | Type   | Description                                                        | Example            | Requirement Level | Stability    |
| ----------------------------- | ------ | ------------------------------------------------------------------ | ------------------ | ----------------- | --- |
| `ai_agent.interaction.type`   | string | Type of interaction (e.g., `message_exchange`, `task_delegation`). | `message_exchange` | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.interaction.source` | string | Identifier of the source agent initiating the interaction.         | `Agent A`          | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.interaction.target` | string | Identifier of the target agent receiving the interaction.          | `Agent B`          | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |
| `ai_agent.interaction.status` | string | Outcome of the interaction (e.g., `success`, `failure`).           | `success`          | Required          | ![Experimental](https://img.shields.io/badge/-experimental-blue)    |

## Examples

### Workflow: Market Analysis Pipeline

Description: This workflow aims to analyze market trends by collecting and analyzing data from various sources.

- Attributes:
  - ai_agent.workflow.name: Market Analysis Pipeline
  - ai_agent.workflow.tasks: ["Data Collection", "Data Analysis"]
  - ai_agent.workflow.agents: ["DataCollectorAgent", "DataAnalystAgent"]
  - ai_agent.workflow.config: {"schedule": "weekly", "priority": "high"}
  - ai_agent.workflow.start_time: 2024-12-06T08:00:00Z
  - ai_agent.workflow.end_time: 2024-12-06T10:00:00Z
  - ai_agent.workflow.end_state: success
  - ai_agent.workflow.end_reason: All tasks completed successfully
  - ai_agent.workflow.tags: ["Market Analysis", "Automation"]
  - ai_agent.workflow.system: Production

### Agents Involved

#### DataCollectorAgent

- Attributes:
  - ai_agent.agent.name: DataCollectorAgent
  - ai_agent.agent.role: Data Collection
  - ai_agent.agent.backstory: Specializes in gathering data from diverse online sources.
  - ai_agent.agent.workflow_name: Market Analysis Pipeline
  - ai_agent.agent.model: gpt-4
  - ai_agent.agent.tools: ["WebScraperTool"]

#### DataAnalystAgent

- Attributes:
  - ai_agent.agent.name: DataAnalystAgent
  - ai_agent.agent.role: Data Analysis
  - ai_agent.agent.backstory: Proficient in interpreting data to extract meaningful insights.
  - ai_agent.agent.workflow_name: Market Analysis Pipeline
  - ai_agent.agent.model: gpt-4
  - ai_agent.agent.tools: ["DataAnalyzerTool"]

### Tasks and Tools

#### Task: Data Collection

- Assigned Agent: DataCollectorAgent

- Attributes:
  - ai_agent.task.name: Data Collection
  - ai_agent.task.agent_name: DataCollectorAgent
  - ai_agent.task.description: Gather market data from specified online sources.
  - ai_agent.task.output: {"data_size": "500MB", "records": 10000}
  - ai_agent.task.priority: high
  - ai_agent.task.state: completed
  - ai_agent.task.duration: 3600000

#### Tool Utilized: WebScraperTool

- Attributes:
  - ai_agent.tool.name: WebScraperTool
  - ai_agent.tool.function: Data Extraction
  - ai_agent.tool.output: {"records_extracted": 10000, "duration": "1h"}

#### Task: Data Analysis

- Assigned Agent: DataAnalystAgent
- Attributes:
  - ai_agent.task.name: Data Analysis
  - ai_agent.task.agent_name: DataAnalystAgent
  - ai_agent.task.description: Analyze the collected data to identify market trends.
  - ai_agent.task.output: {"insights": ["Trend A", "Trend B"]}
  - ai_agent.task.priority: high
  - ai_agent.task.state: completed
  - ai_agent.task.duration: 5400000

#### Tool Utilized: DataAnalyzerTool

- Attributes:
  - ai_agent.tool.name: DataAnalyzerTool
  - ai_agent.tool.function: Data Analysis
  - ai_agent.tool.output: {"identified_trends": 2, "duration": "1.5h"}

This simplified workflow demonstrates how two agents collaborate to perform data collection and analysis tasks, utilizing specific tools to achieve the objectives of the Market Analysis Pipeline.
