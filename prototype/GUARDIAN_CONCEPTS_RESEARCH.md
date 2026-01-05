# Guardian/Guardrail Concepts Research

This document summarizes guardian and guardrail concepts across major AI frameworks
to inform the OpenTelemetry GenAI Security Guardian semantic conventions.

## Reviewer Notes

> [!NOTE]
> - Treat this as a living research doc; add explicit version/links for each framework section as it evolves.
> - Add cloud-provider guardrails coverage (AWS Bedrock Guardrails, OpenAI moderation, Anthropic safety) to complement agent-framework coverage.
> - Add primary citations (or remove) for the "2025 Statistics" bullets before using them as spec rationale.
> - If proposing `agent_state` as a `gen_ai.security.target.type`, define privacy/PII guidance and how it differs from `memory_*`.
> - Keep `gen_ai.guardian.provider.name` values stable and low-cardinality (prefer reverse-DNS-style identifiers).

## Executive Summary

| Framework | Guardrail Concept | Execution Model | Observability |
|-----------|-------------------|-----------------|---------------|
| LangChain | Middleware system | Before/after hooks | Custom callbacks |
| LangGraph | Node-level guards | State-aware validation | Traces/spans |
| Google ADK | Callbacks + Plugins | before_model/before_tool | Built-in tracing |
| Semantic Kernel | Filter interfaces | IPromptFilter/IFunctionFilter | Native OTel support |
| OpenAI Agents | Guard classes | Pre/post chat, function calls | Custom instrumentation |
| Azure AI | Content Safety API | Pre/post filtering | Azure Monitor |

---

## LangChain Guardrails

### Architecture
LangChain implements guardrails through a **middleware system** that intercepts
execution at strategic points in the agent lifecycle.

> [!NOTE]
> "Middleware" is used here as a conceptual shorthand; LangChain has multiple extension points (callbacks, runnables, tool wrappers). Verify terminology against the linked docs/version.

### Key Concepts

1. **Deterministic Guardrails**
   - Rule-based logic (regex, keyword matching)
   - Fast, predictable, cost-effective
   - Examples: PII patterns, blocklists

2. **Model-based Guardrails**
   - LLM/classifier evaluation for semantic understanding
   - Catches subtle issues (toxicity, context)
   - Slower, more expensive

3. **Built-in Guardrails**
   - **PII Detection**: Emails, credit cards, IP addresses, URLs
   - **Human-in-the-Loop**: Pause for approval on sensitive operations
   - **Content Filtering**: Block harmful content

### Execution Points (Maps to our `gen_ai.security.target.type`)
| LangChain Point | Our Target Type |
|-----------------|-----------------|
| Before model call | `llm_input` |
| After model response | `llm_output` |
| Before tool execution | `tool_call` |
| Tool definition check | `tool_definition` |

### Middleware Pattern
```python
class PiiGuardrail(Middleware):
    async def before_agent(self, request, session):
        # Validate input - maps to target_type: llm_input
        pass

    async def after_agent(self, response, session):
        # Validate output - maps to target_type: llm_output
        pass
```

### Sources
- [LangChain Guardrails Docs](https://docs.langchain.com/oss/python/langchain/guardrails)
- [Guardrails AI Integration](https://guardrailsai.com/docs/integrations/langchain)
- [NVIDIA NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/user-guides/langchain/langchain-integration.html)

---

## LangGraph Guardrails

### Architecture
LangGraph enables sophisticated agent architectures with **state management**,
**conditional routing**, and **tool calling**. Guardrails are implemented at
node boundaries in the graph.

### Key Concepts

1. **Graph Node Guards**
   - Validation at each node transition
   - Access to full agent state
   - Conditional routing based on safety

2. **Tool Calling Guards**
   - Pre-execution validation of tool parameters
   - Post-execution validation of results
   - Permission checking

3. **State-Aware Security**
   - AgentState: Shared across nodes (logged)
   - Configuration: Never logged (for secrets)

### Enterprise Security Framework
From the LangGraph security framework research:
- **Least Privilege**: Avoid direct database access
- **Token Handling**: Secure credential management
- **Guardrail Plane**: Validators, schema checks, content policy, code sandbox

### 2025 Statistics
> [!WARNING]
> The statistics below need a primary source link (or should be removed) before being used in a spec rationale.
- 39% of companies reported AI agents accessing unintended systems
- 32% saw agents allowing inappropriate data downloads
- 87% of enterprises lack comprehensive AI security frameworks (Gartner)

### Sources
- [LangGraph + NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/user-guides/langchain/langgraph-integration.html)
- [Enterprise Security Framework](https://medium.com/@samuel.grummons/building-enterprise-ai-agents-with-least-privilege-a-langgraph-security-framework-ea1cbfebcc1d)

---

## Google Agent Development Kit (ADK)

### Architecture
ADK implements a **multi-layered security model** with safety controls distributed
across different components of the agent execution pipeline.

### Key Concepts

1. **Callbacks (Primary Mechanism)**
   - `before_model_callback`: Inspect/modify/block LLM requests
   - `before_tool_callback`: Validate tool parameters before execution
   - `after_tool_callback`: Validate tool results
   - `after_model_callback`: Filter model outputs

2. **In-Tool Guardrails**
   - Developer-set tool context
   - Policy enforcement within tool definitions
   - Example: Allow queries only on specific tables

3. **Plugins (Global Policies)**
   - Self-contained, modular security policies
   - Apply globally at runner level
   - Examples: Gemini-as-Judge, PII Redaction

4. **Gemini Safety Features**
   - Content filters (configurable/non-configurable)
   - System instructions for behavior guidelines
   - Harm category thresholds

### Callback Pattern (Maps to our spec)
```python
def before_tool_callback(
    tool: BaseTool,
    args: dict,
    tool_context: ToolContext
) -> Optional[dict]:
    # Maps to target_type: tool_call
    # Can return modified args or raise to block
    pass
```

### Observability
ADK provides **evaluation and tracing** to:
- Analyze agent steps
- Track tool choices and strategies
- Measure efficiency

### Sources
- [ADK Safety Docs](https://google.github.io/adk-docs/safety/)
- [ADK Callbacks Tutorial](https://raphaelmansuy.github.io/adk_training/docs/callbacks_guardrails/)
- [Guardrails with ADK](https://medium.com/google-cloud/guardrails-with-agent-development-kit-featuring-safeguard-llm-models-6d696198a063)

---

## Microsoft Semantic Kernel Guardrails

### Architecture
Semantic Kernel implements guardrails through a **filter-based system** using
strongly-typed interfaces that integrate with the kernel's execution pipeline.

### Key Concepts

1. **IPromptFilter Interface**
   - `on_prompt_rendering`: Before template expansion
   - `on_prompt_rendered`: After rendering, before AI call
   - Access to function name, plugin name, arguments
   - Can modify or block prompts

2. **IFunctionFilter Interface**
   - `on_function_invoking`: Before plugin function execution
   - `on_function_invoked`: After function returns
   - Access to function context and results
   - Enables permission checking and result sanitization

3. **Plugin Architecture**
   - Plugins expose functions (tools) to the AI
   - Each function can have security policies
   - Path restrictions, confirmation requirements
   - Per-plugin, per-function granularity

4. **Azure AI Content Safety Integration**
   - Native integration with Azure Content Safety API
   - Category-based thresholds (Hate, SelfHarm, Sexual, Violence)
   - Severity scoring (0-6 scale)

### Filter Pattern
```python
class IPromptFilter(ABC):
    async def on_prompt_rendering(self, context: PromptRenderContext):
        pass  # Template expansion stage

    async def on_prompt_rendered(self, context: PromptRenderContext):
        pass  # Post-render, pre-AI call

class IFunctionFilter(ABC):
    async def on_function_invoking(self, context: FunctionInvocationContext):
        pass  # Before tool execution

    async def on_function_invoked(self, context: FunctionInvocationContext):
        pass  # After tool execution
```

### Execution Points (Maps to our `gen_ai.security.target.type`)
| SK Point | Our Target Type |
|----------|-----------------|
| `on_prompt_rendered` | `llm_input` |
| `on_function_invoking` | `tool_call` |
| `on_function_invoked` | `tool_call` (result validation) |
| Azure Content Safety | `llm_input`, `llm_output`, `message` |

### Security Patterns Demonstrated

1. **Template Injection Prevention**
   - Detect `{{...}}` SK template syntax in user input
   - Detect `${...}` variable injection
   - Block special token markers `<|...|>`

2. **Plugin Permission Policies**
   ```python
   function_policies = {
       "EmailPlugin": {
           "SendEmail": {"require_confirmation": True, "max_recipients": 5},
           "ReadEmail": {"allowed": True},
       },
       "FilePlugin": {
           "WriteFile": {"allowed_paths": ["/tmp/", "/data/output/"]},
           "DeleteFile": {"require_confirmation": True},
       },
   }
   ```

3. **Result Sanitization**
   - Credit card number detection and redaction
   - SSN pattern detection
   - API key leak prevention

### Sources
- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/)
- [SK Filters](https://learn.microsoft.com/semantic-kernel/concepts/ai-services/chat-completion/chat-completion-filters)
- [SK Security Best Practices](https://learn.microsoft.com/semantic-kernel/concepts/enterprise-readiness/)

---

## OpenAI Agents SDK Guardrails

### Architecture
OpenAI Agents SDK implements guardrails through **guard classes** that wrap
API interactions, supporting both Chat Completions and the newer Responses API.

### Key Concepts

1. **Input/Output Guards**
   - Pre-chat validation for injection/jailbreak
   - Post-chat validation for PII/secrets
   - Message-level inspection

2. **Function Call Guards**
   - Permission checking for custom functions
   - Audit logging for built-in tools
   - Argument validation

3. **Responses API Support**
   - Server-side tool execution monitoring
   - Multi-output type handling
   - Streaming response inspection

4. **Built-in Tool Awareness**
   - `web_search`: Server-side web search
   - `code_interpreter`: Sandboxed code execution
   - `file_search`: File retrieval in threads

### Guard Pattern
```python
class OpenAIInputGuard:
    def evaluate(self, messages: List[Message]) -> GuardianResult:
        # Check all messages for injection patterns
        pass

class OpenAIOutputGuard:
    def evaluate(self, response_content: str) -> GuardianResult:
        # Check output for PII, API keys
        pass

class OpenAIToolCallGuard:
    def evaluate_tool_call(self, tool_type, tool_name, arguments) -> GuardianResult:
        # Check permissions, audit built-in tools
        pass

class ResponsesAPIGuard:
    def evaluate_responses_output(self, outputs: List[ResponsesAPIOutput]) -> GuardianResult:
        # Handle multiple output types
        pass
```

### Execution Points (Maps to our `gen_ai.security.target.type`)
| OpenAI Point | Our Target Type |
|--------------|-----------------|
| Pre-chat validation | `llm_input` |
| Post-chat validation | `llm_output` |
| Function call check | `tool_call` |
| Responses API output | `llm_output` (multi-item) |

### OpenAI-Specific Patterns

1. **Token Injection Detection**
   - Special tokens: `<|endoftext|>`, `<|im_start|>`, `<|im_end|>`
   - Instruction markers: `[INST]...[/INST]`
   - Code block overrides: ` ```system `

2. **Jailbreak Pattern Detection**
   - DAN (Do Anything Now) mode requests
   - STAN, KEVIN, and other persona jailbreaks
   - "Pretend you are/can/have" patterns
   - "Bypass your guidelines" requests

3. **API Key Leak Prevention (Critical)**
   ```python
   # OpenAI API keys follow pattern: sk-[A-Za-z0-9]{20,}
   if re.search(r"sk-[A-Za-z0-9]{20,}", response_content):
       # CRITICAL severity - always redact
       findings.append(SecurityFinding(
           risk_severity=RiskSeverity.CRITICAL,
           risk_score=0.99
       ))
   ```

4. **Responses API Output Types**
   ```python
   @dataclass
   class ResponsesAPIOutput:
       type: str  # "message", "function_call", "function_call_output", "web_search_call"
       content: Optional[str]
       call_id: Optional[str]
       name: Optional[str]
       arguments: Optional[str]
       output: Optional[str]
   ```

5. **Built-in Tool Auditing**
   - `web_search`: Log queries for compliance
   - `code_interpreter`: Monitor code execution
   - `file_search`: Track file access patterns

### Sources
- [OpenAI Agents SDK](https://platform.openai.com/docs/agents)
- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

---

## Mapping to OpenTelemetry GenAI Security Guardian Spec

### Decision Types Across Frameworks

| Our Decision Type | LangChain | LangGraph | ADK | Semantic Kernel | OpenAI |
|-------------------|-----------|-----------|-----|-----------------|--------|
| `allow` | Pass through | Continue routing | Return None | Continue | Continue |
| `deny` | Raise exception | Error node | Raise exception | Block prompt | Block request |
| `modify` | Transform response | State mutation | Return modified | Modify context | Redact output |
| `warn` | Log + continue | Flag in state | Log + continue | Log + continue | Log + continue |
| `audit` | Log only | Trace only | Trace only | Trace only | Trace only |

### Target Types Across Frameworks

| Our Target Type | Where It's Used |
|-----------------|-----------------|
| `llm_input` | LangChain `before_agent`, ADK `before_model_callback`, SK `on_prompt_rendered`, OpenAI pre-chat |
| `llm_output` | LangChain `after_agent`, ADK `after_model_callback`, OpenAI post-chat |
| `tool_call` | All frameworks support before-tool validation |
| `tool_definition` | ADK in-tool guardrails, LangChain tool validation, LangGraph tool definitions |
| `memory_store` | LangGraph state management, ADK session context |
| `memory_retrieve` | LangGraph state access |
| `message` | ADK Gemini-as-Judge, Azure Content Safety |

### Risk Categories Mapping

| OWASP LLM Top 10 | LangChain | ADK | Semantic Kernel | OpenAI |
|------------------|-----------|-----|-----------------|--------|
| Prompt Injection | Custom middleware | Gemini-as-Judge | IPromptFilter | Input guard |
| Sensitive Info | PII Detection | PII Redaction plugin | Result sanitization | API key detection |
| Excessive Agency | Human-in-the-loop | before_tool_callback | IFunctionFilter | Function policies |
| Jailbreak | Guardrails AI | Safety filters | Template injection | DAN mode detection |
| System Prompt Leakage | Pattern matching | Safety filters | Pattern matching | Pattern matching |

---

## Recommendations for Spec

1. **Callback/Hook Pattern is Universal**
   - All frameworks use before/after hooks
   - Our `apply_guardrail` span naturally fits this model

2. **Multiple Findings Pattern is Needed**
   - Frameworks often detect multiple issues
   - Our event-based findings model (multiple `gen_ai.security.finding` events) supports this

3. **Target Type is Well-Aligned**
   - Our target types match the execution points in all frameworks
   - Consider adding `agent_state` for LangGraph compatibility

4. **Decision Types Cover All Cases**
   - `modify` is especially important for PII redaction workflows
   - `audit` supports compliance-only scenarios

5. **Provider Name Examples**
   - Consider adding `langchain.guardrails`, `langgraph`, `google.adk`, `microsoft.semantic_kernel`, `openai`
   - These would complement `azure.ai.content_safety`
   - Prefer stable reverse-DNS-style identifiers (e.g., `aws.bedrock.guardrails`) and avoid per-deployment IDs
   - Examples validated in prototypes:
     - `langchain.guardrails` - LangChain middleware
     - `langgraph` - LangGraph node guards
     - `google.adk` - Google ADK callbacks
     - `microsoft.semantic_kernel` - Semantic Kernel filters
     - `openai` - OpenAI Agents SDK guards
     - `azure.ai.content_safety` - Azure Content Safety API

---

## References

### Official Documentation
- [LangChain Guardrails](https://docs.langchain.com/oss/python/langchain/guardrails)
- [Google ADK Safety](https://google.github.io/adk-docs/safety/)
- [NVIDIA NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/)

### Security Standards
- [OWASP LLM Top 10 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### Articles
- [Building Safer LLM Apps with LangChain + NeMo](https://developer.nvidia.com/blog/building-safer-llm-apps-with-langchain-templates-and-nvidia-nemo-guardrails/)
- [Guardrails with ADK](https://medium.com/google-cloud/guardrails-with-agent-development-kit-featuring-safeguard-llm-models-6d696198a063)
