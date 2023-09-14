# Semantic Conventions for LLM requests in Chains or Agents

**Status**: [Experimental][DocumentStatus]

<!-- Re-generate TOC with `markdown-toc --no-first-h1 -i` -->

<!-- toc -->

- [LLM Request attributes](#llm-request-attributes)
- [Semantic Conventions for specific LLM technologies](#semantic-conventions-for-specific-llm-technologies)

<!-- tocstop -->

A chain is defined as a sequence of requests to an LLM controlled by a program. Some requests are made in parallel, following a map-reduce pattern, and some are sequential. Crucially, requests to an LLM are initiated programmatically.

An agent is defined as an executable that, given instructions, performs any number of requests to an LLM until certain criteria is satisfied. Although similar to a chain, and agent is distinguished by the ability to make a request to an LLM on behalf of a program.

In both cases, traces model the behavior of a chain or an agent. As such, spans in a chain or agent should follow the guidance in [llm-spans](llm-spans.md).

However, a key conceptual difference between traces used to model LLM behavior and distributed traces is that a group of one or more spans may represent a *step* of a chain or an agent. In simpler applications, such as directly chaining a fixed number of LLM requets together, a single span can adequately represent each step in the chain. However, more complex applications often require a group of spans.

For example, consider an agent that continuously reads data from a knowledge base, makes a request to an LLM to summarize the data, and evaluates the effectiveness of that summarization, repeating the process until success criteria is met:

- One or more spans that tracks retrieving a subset of the knowledge base
- One or more spans that tracks one or more requests to an LLM (perhaps in parallel)
- One or more spans that tracks parsing, validation, and/or merging of results from LLM requests
- One or more spans that tracks an evaluation of the final result

Each of the above groups of spans may represent a single *step* of a chain or agent, indicating a need to distinguish each *step*.

## LLM Chain attributes

todo -- why would we name? I think we should to distinguish different chains that may be grouped together.

<!-- semconv ai(tag=llm-chain-step) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.chain.name`|string|The name of the chain.|Required|
| `llm.chain.step`|int|Denotes the current step or iteration of an LLM chain.|Required|

## LLM Agent Step attributes

todo -- why would we name? I think we should to distinguish different agents, esp. when composed together.

<!-- semconv ai(tag=llm-agent-step) -->
| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `llm.agent.name`|int|The name of the agent.|Required|
| `llm.agent.step`|int|Indicates the current step or iteration an agent is performing one or more tasks.|Required|