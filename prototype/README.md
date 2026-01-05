# GenAI Security Guardian Prototypes

This directory documents prototype implementations demonstrating how to integrate
OpenTelemetry GenAI Security Guardian semantic conventions with major AI agent
frameworks.

> **Note**: Local credentials (`prototype/.env.local`) and virtual environments (`prototype/.venv*`) are excluded from version control (see `.gitignore` and `prototype/.gitignore`).

## Overview

These prototypes validate the `apply_guardrail` span and `gen_ai.security.finding`
event semantic conventions proposed in the [GenAI Security Guardian specification](../model/gen-ai/).

## Quickstart

```bash
cd prototype
cp .env.example .env.local  # fill in credentials (git-ignored)

python3 -m venv .venv-appinsights
source .venv-appinsights/bin/activate
pip install -r requirements-appinsights.txt
deactivate

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-traceloop.txt
deactivate

./run_demos.sh all
```

### Optional: Real Chat + Safe (“Almost Real”) Tools

By default, prototypes run in **auto** mode: if `OPENAI_API_KEY` is set they use real OpenAI chat, otherwise they run offline using a deterministic mock chat model. To make traces look more realistic, the prototypes can also:

- Perform a **real** OpenAI chat call (Chat Completions or Responses API) via `prototype/demo_chat.py`.
- Execute **safe** tools that actually do work (SQLite queries, file writes under `/tmp`, and an “email outbox”)
  via `prototype/demo_tools.py`.

**Enable real chat (OpenAI):**

```bash
export OPENAI_API_KEY=...
export DEMO_OPENAI_MODEL=gpt-4.1     # optional
export DEMO_OPENAI_API=responses     # optional: auto|responses|chat_completions
export OPENAI_BASE_URL=https://api.openai.com/v1  # optional
export DEMO_LLM_MODE=auto            # optional: auto|openai|mock
```

For local runs, prefer putting credentials in `prototype/.env.local` (git-ignored) and using `prototype/run_all_demos.py` or `prototype/run_demos.sh`, which load it automatically.

### Core Semantic Conventions

| Convention | Type | Description |
|------------|------|-------------|
| `apply_guardrail` | Span | Security evaluation operation (SpanKind: INTERNAL) |
| `gen_ai.security.finding` | Event | Individual security finding attached to span |
| `gen_ai.security.decision.type` | Attribute | `allow`, `deny`, `modify`, `warn`, `audit` |
| `gen_ai.security.target.type` | Attribute | `llm_input`, `llm_output`, `tool_call`, `memory_store`, etc. |
| `gen_ai.security.risk.category` | Attribute | OWASP LLM Top 10 aligned categories |

---

## Shared Utilities (`otel_guardian_utils.py`)

The shared utilities module provides the foundation for all framework prototypes.

### Core Classes

#### GuardianTracer

```python
class GuardianTracer:
    """Utility class for creating guardian spans and events."""

    def __init__(
        self,
        service_name: str = "genai-security-guardian",
        service_version: str = "0.1.0",
        enable_console_export: bool = True
    ):
        """Initialize the guardian tracer with OpenTelemetry SDK."""

    def create_guardian_span(
        self,
        guardian_config: GuardianConfig,
        target_type: str,
        target_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        conversation_id: Optional[str] = None
    ) -> _GuardianSpanContext:
        """Create an apply_guardrail span as a context manager."""

    @staticmethod
    def hash_content(content: str, algorithm: str = "sha256") -> str:
        """Hash content for forensic correlation without storing raw content."""
```

#### Data Classes

```python
@dataclass
class GuardianConfig:
    """Configuration for a guardian/guardrail."""
    id: str               # Unique identifier (e.g., "langchain-input-guard-v1")
    name: str             # Human-readable name
    version: str          # Version string (default: "1.0.0")
    provider_name: str    # Provider namespace (e.g., "langchain.guardrails")

@dataclass
class GuardianResult:
    """Result of a guardian evaluation."""
    decision_type: str              # From DecisionType enum
    decision_reason: Optional[str]  # Human-readable explanation
    decision_code: Optional[int]    # HTTP-style status code
    findings: Optional[List[SecurityFinding]]
    modified_content: Optional[str] # For decision_type=modify
    content_redacted: bool          # True if PII/secrets removed

@dataclass
class SecurityFinding:
    """Represents a security finding to be recorded as an event."""
    risk_category: str      # OWASP category or custom
    risk_severity: str      # From RiskSeverity enum
    risk_score: float       # 0.0-1.0 confidence score
    policy_id: Optional[str]
    policy_name: Optional[str]
    policy_version: Optional[str]
    metadata: Optional[List[str]]  # Low-cardinality descriptors
```

### Enum Classes

```python
class DecisionType:
    ALLOW = "allow"   # Clean pass, no issues
    DENY = "deny"     # Block entirely
    MODIFY = "modify" # Sanitize and allow modified
    WARN = "warn"     # Allow but flag for review
    AUDIT = "audit"   # Log only, no enforcement

class TargetType:
    LLM_INPUT = "llm_input"
    LLM_OUTPUT = "llm_output"
    TOOL_CALL = "tool_call"
    TOOL_DEFINITION = "tool_definition"
    MEMORY_STORE = "memory_store"
    MEMORY_RETRIEVE = "memory_retrieve"
    KNOWLEDGE_QUERY = "knowledge_query"
    KNOWLEDGE_RESULT = "knowledge_result"
    MESSAGE = "message"

class RiskSeverity:
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskCategory:
    # OWASP LLM Top 10 2025
    PROMPT_INJECTION = "prompt_injection"           # LLM01
    SENSITIVE_INFO_DISCLOSURE = "sensitive_info_disclosure"  # LLM02
    SUPPLY_CHAIN = "supply_chain"                   # LLM03
    DATA_AND_MODEL_POISONING = "data_and_model_poisoning"    # LLM04
    IMPROPER_OUTPUT_HANDLING = "improper_output_handling"    # LLM05
    EXCESSIVE_AGENCY = "excessive_agency"           # LLM06
    SYSTEM_PROMPT_LEAKAGE = "system_prompt_leakage" # LLM07
    VECTOR_AND_EMBEDDING_WEAKNESSES = "vector_and_embedding_weaknesses"  # LLM08
    MISINFORMATION = "misinformation"               # LLM09
    UNBOUNDED_CONSUMPTION = "unbounded_consumption" # LLM10
    # Additional common categories
    JAILBREAK = "jailbreak"
    TOXICITY = "toxicity"
    PII = "pii"
```

### Semantic Convention Constants

```python
# Operation name
GEN_AI_OPERATION_NAME = "gen_ai.operation.name"

# Guardian identity
GEN_AI_GUARDIAN_ID = "gen_ai.guardian.id"
GEN_AI_GUARDIAN_NAME = "gen_ai.guardian.name"
GEN_AI_GUARDIAN_VERSION = "gen_ai.guardian.version"
GEN_AI_GUARDIAN_PROVIDER_NAME = "gen_ai.guardian.provider.name"

# Security decision
GEN_AI_SECURITY_DECISION_TYPE = "gen_ai.security.decision.type"
GEN_AI_SECURITY_DECISION_REASON = "gen_ai.security.decision.reason"
GEN_AI_SECURITY_DECISION_CODE = "gen_ai.security.decision.code"

# Security target
GEN_AI_SECURITY_TARGET_TYPE = "gen_ai.security.target.type"
GEN_AI_SECURITY_TARGET_ID = "gen_ai.security.target.id"

# Risk attributes (for events)
GEN_AI_SECURITY_RISK_CATEGORY = "gen_ai.security.risk.category"
GEN_AI_SECURITY_RISK_SEVERITY = "gen_ai.security.risk.severity"
GEN_AI_SECURITY_RISK_SCORE = "gen_ai.security.risk.score"
GEN_AI_SECURITY_RISK_METADATA = "gen_ai.security.risk.metadata"

# Policy attributes
GEN_AI_SECURITY_POLICY_ID = "gen_ai.security.policy.id"
GEN_AI_SECURITY_POLICY_NAME = "gen_ai.security.policy.name"
GEN_AI_SECURITY_POLICY_VERSION = "gen_ai.security.policy.version"

# Content attributes (opt-in only)
GEN_AI_SECURITY_CONTENT_INPUT_HASH = "gen_ai.security.content.input.hash"
GEN_AI_SECURITY_CONTENT_REDACTED = "gen_ai.security.content.redacted"

# Event name
GEN_AI_SECURITY_FINDING_EVENT = "gen_ai.security.finding"
```

---

## Framework Prototypes

### 1. LangChain (`langchain/`)

Demonstrates **middleware-style guardrails** using before/after hooks.

#### Guard Classes

| Class | Target Type | Purpose |
|-------|-------------|---------|
| `LangChainInputGuard` | `llm_input` | Prompt injection and jailbreak detection |
| `LangChainOutputGuard` | `llm_output` | PII detection and redaction |
| `LangChainToolGuard` | `tool_call` | Tool permission checking |

#### Key Patterns

**Input Guard - Prompt Injection Detection**
```python
class LangChainInputGuard:
    """Maps to: gen_ai.security.target.type = llm_input"""

    injection_patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"reveal\s+(your\s+)?(system\s+)?prompt",
        r"DAN\s+mode",
    ]

    def evaluate(self, input_text, conversation_id=None) -> GuardianResult:
        with tracer.create_guardian_span(config, TargetType.LLM_INPUT) as ctx:
            ctx.record_content_hash(input_text)  # Hash, not raw content

            for pattern in self.injection_patterns:
                if re.search(pattern, input_text, re.IGNORECASE):
                    findings.append(SecurityFinding(
                        risk_category=RiskCategory.PROMPT_INJECTION,
                        risk_severity=RiskSeverity.HIGH,
                        risk_score=0.95,
                        policy_id="policy_prompt_shield",
                        metadata=["pattern:...", "position:user_input"]
                    ))

            ctx.record_result(GuardianResult(
                decision_type=DecisionType.DENY if findings else DecisionType.ALLOW,
                findings=findings
            ))
```

**Output Guard - PII Redaction**
```python
class LangChainOutputGuard:
    """Maps to: gen_ai.security.target.type = llm_output"""

    pii_patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    }

    def evaluate(self, output_text) -> GuardianResult:
        # Returns decision_type=MODIFY with redacted content
        # Sets content_redacted=True
```

**Tool Guard - Permission Checking**
```python
class LangChainToolGuard:
    """Maps to: gen_ai.security.target.type = tool_call"""

    blocked_tools = ["execute_shell", "system_command"]
    sensitive_tools = {"send_email": "external_communication"}

    # Returns DENY for blocked, WARN for sensitive, ALLOW for safe
```

#### Demo Scenarios

| Scenario | Input | Expected Decision |
|----------|-------|-------------------|
| Normal request | "What's the weather?" | `allow` |
| PII in response | Response contains email | `modify` (redacted) |
| Prompt injection | "Ignore all previous..." | `deny` |
| Safe tool | `calculator` | `allow` |
| Sensitive tool | `send_email` | `warn` |
| Blocked tool | `execute_shell` | `deny` |

---

### 2. LangGraph (`langgraph/`)

Demonstrates **state-aware, graph-based guardrails** with access to full conversation history.

#### Guard Classes

| Class | Target Type | Purpose |
|-------|-------------|---------|
| `StateAwareInputGuard` | `llm_input` | Progressive jailbreak detection across conversation |
| `MemoryStoreGuard` | `memory_store` | Prevents storing secrets in agent memory |
| `MemoryRetrieveGuard` | `memory_retrieve` | Blocks bulk data retrieval attempts |
| `ToolDefinitionGuard` | `tool_definition` | Audits dangerous tool capabilities |

#### Key Patterns

**State-Aware Input Guard**
```python
class StateAwareInputGuard:
    """Evaluates input considering full agent state and history."""

    def evaluate(self, state: AgentState) -> GuardianResult:
        # Access full conversation history
        messages = state.get("messages", [])
        current_input = state.get("current_input", "")

        # Count jailbreak indicators across ALL messages
        jailbreak_indicators = 0
        for msg in messages:
            for pattern in suspicious_patterns:
                if re.search(pattern, msg.get("content", "")):
                    jailbreak_indicators += 1

        # Progressive escalation: WARN at 1, DENY at 3+
        if jailbreak_indicators >= 3:
            return GuardianResult(decision_type=DecisionType.DENY)
```

**Memory Store Guard**
```python
class MemoryStoreGuard:
    """Prevents storing sensitive data in agent memory."""

    sensitive_patterns = {
        "api_key": r"(api[_-]?key|secret[_-]?key)[:\s=]+[\w-]{20,}",
        "password": r"(password|passwd)[:\s=]+\S+",
        "private_key": r"-----BEGIN\s+PRIVATE\s+KEY-----",
    }

    # Returns DENY if secrets detected, blocks memory write
```

**Memory Retrieve Guard**
```python
class MemoryRetrieveGuard:
    """Blocks bulk data exfiltration attempts."""

    bulk_patterns = [
        r"all\s+(user|customer)\s+data",
        r"dump\s+(database|memory)",
    ]
```

**Tool Definition Guard**
```python
class ToolDefinitionGuard:
    """Audits tool definitions for dangerous capabilities."""

    dangerous_capabilities = [
        "execute_code", "shell_command", "file_system_write"
    ]

    # Returns AUDIT for dangerous capabilities (logged but allowed)
```

#### AgentState Structure

```python
class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    current_input: str
    tool_calls: List[Dict[str, Any]]
    security_flags: List[str]      # Security events accumulated
    is_blocked: bool               # Workflow halted
    final_response: Optional[str]
```

---

### 3. Google ADK (`google_adk/`)

Demonstrates **callback-based guardrails** using ADK's callback pattern.

#### Callback Classes

| Class | Target Type | ADK Hook |
|-------|-------------|----------|
| `BeforeModelCallback` | `llm_input` | `before_model_callback` |
| `AfterModelCallback` | `llm_output` | `after_model_callback` |
| `BeforeToolCallback` | `tool_call` | `before_tool_callback` |
| `AfterToolCallback` | `tool_call` | `after_tool_callback` |
| `GeminiAsJudgePlugin` | `message` | Plugin pattern |

#### Key Patterns

**Before Model Callback - Gemini Safety**
```python
class BeforeModelCallback:
    """ADK before_model_callback with Gemini safety categories."""

    harm_patterns = {
        "dangerous_content": [r"how\s+to\s+(make|create)\s+(bomb|weapon)"],
        "harassment": [r"(attack|insult)\s+(this\s+)?(person)"],
    }

    def __call__(self, request: ModelRequest, agent_context) -> Optional[ModelRequest]:
        # Returns None to block, or modified request
        # Uses risk_category="google:{category}" for Gemini-specific categories
```

**Before Tool Callback - Policy-Based Access Control**
```python
class BeforeToolCallback:
    """ADK before_tool_callback with tool-specific policies."""

    tool_policies = {
        "database_query": {
            "allowed_tables": ["products", "categories"],
            "blocked_tables": ["users", "credentials"],
        },
        "file_read": {
            "blocked_paths": ["/etc/", "/var/secrets/"],
        },
    }

    # Checks query/path against policy, returns None to block
```

**Gemini-as-Judge Plugin**
```python
class GeminiAsJudgePlugin:
    """LLM-based content evaluation plugin."""

    def evaluate_content(self, content: str, criteria: List[str]) -> GuardianResult:
        # Uses Gemini to evaluate against criteria like:
        # ["toxicity", "bias", "factuality", "relevance"]
```

#### ADK Context Types

```python
@dataclass
class ToolContext:
    tool_name: str
    agent_id: str
    session_id: str

@dataclass
class ModelRequest:
    messages: List[Dict[str, str]]
    model: str = "gemini-1.5-pro"
    system_instruction: Optional[str] = None

@dataclass
class ModelResponse:
    content: str
    safety_ratings: Optional[Dict[str, float]]  # Gemini safety scores
```

---

### 4. Semantic Kernel (`semantic_kernel/`)

Demonstrates **filter-based guardrails** using SK's filter interfaces.

#### Filter Classes

| Class | Interface | Target Type |
|-------|-----------|-------------|
| `PromptSecurityFilter` | `IPromptFilter` | `llm_input` |
| `FunctionSecurityFilter` | `IFunctionFilter` | `tool_call` |
| `AzureContentSafetyGuard` | Custom | Azure integration |

#### Key Patterns

**IPromptFilter Implementation**
```python
class PromptSecurityFilter(IPromptFilter):
    """Semantic Kernel prompt filter with security guardian."""

    async def on_prompt_rendered(self, context: PromptRenderContext):
        # Check for template injection
        injection_patterns = [
            (r"{{.*}}", "template_injection"),      # SK template syntax
            (r"\$\{.*\}", "variable_injection"),    # Variable injection
            (r"<\|.*\|>", "special_token_injection"),
        ]

        # Check for system prompt extraction
        system_prompt_patterns = [
            r"(print|show)\s+(your\s+)?(system|initial)\s+prompt",
        ]
```

**IFunctionFilter Implementation**
```python
class FunctionSecurityFilter(IFunctionFilter):
    """Semantic Kernel function filter for plugin security."""

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

    async def on_function_invoking(self, context: FunctionInvocationContext):
        # Check path restrictions
        if "allowed_paths" in policy:
            path = context.arguments.get("path", "")
            allowed = any(path.startswith(p) for p in policy["allowed_paths"])
            # Return DENY if not allowed

    async def on_function_invoked(self, context: FunctionInvocationContext):
        # Check for sensitive data in results (credit cards, SSNs, API keys)
        # Return MODIFY with redacted content if found
```

**Azure AI Content Safety Integration**
```python
class AzureContentSafetyGuard:
    """Integration with Azure AI Content Safety API."""

    config = GuardianConfig(
        provider_name="azure.ai.content_safety"
    )

    thresholds = {
        "Hate": 2,
        "SelfHarm": 2,
        "Sexual": 2,
        "Violence": 2,
    }

    def analyze(self, content: str, target_type: str) -> GuardianResult:
        # In production: call Azure Content Safety API
        # Returns findings with risk_category="azure:{category}"
```

#### SK Context Types

```python
@dataclass
class PromptRenderContext:
    rendered_prompt: str
    function_name: str
    plugin_name: Optional[str]
    arguments: Optional[Dict[str, Any]]

@dataclass
class FunctionInvocationContext:
    function_name: str
    plugin_name: Optional[str]
    arguments: Optional[Dict[str, Any]]
    result: Optional[Any]
```

---

### 5. OpenAI Agents SDK (`openai_agents/`)

Demonstrates guardrails for **OpenAI's agent patterns** including Responses API.

#### Guard Classes

| Class | Target Type | Purpose |
|-------|-------------|---------|
| `OpenAIInputGuard` | `llm_input` | Token injection, jailbreak detection |
| `OpenAIOutputGuard` | `llm_output` | API key leak prevention, PII redaction |
| `OpenAIToolCallGuard` | `tool_call` | Function permission, built-in tool audit |
| `ResponsesAPIGuard` | `llm_output` | Server-side tool execution monitoring |

#### Key Patterns

**Input Guard - OpenAI-Specific Patterns**
```python
class OpenAIInputGuard:
    """Guard for OpenAI agent input with token injection detection."""

    injection_patterns = [
        r"<\|.*\|>",              # Special tokens (<|endoftext|>)
        r"\[INST\].*\[/INST\]",   # Instruction markers
        r"```system",             # Code block system override
    ]

    jailbreak_patterns = [
        r"(DAN|STAN|KEVIN)\s+(mode|prompt)",
        r"pretend\s+(you\s+)?(are|can|have)",
        r"bypass\s+(your\s+)?guidelines",
    ]
```

**Output Guard - API Key Leak Prevention**
```python
class OpenAIOutputGuard:
    """Critical: Detect API keys in outputs."""

    def evaluate(self, response_content: str) -> GuardianResult:
        # Check for OpenAI API keys (sk-...)
        if re.search(r"sk-[A-Za-z0-9]{20,}", response_content):
            findings.append(SecurityFinding(
                risk_category=RiskCategory.SENSITIVE_INFO_DISCLOSURE,
                risk_severity=RiskSeverity.CRITICAL,  # Critical!
                risk_score=0.99,
                policy_id="policy_api_key_leak"
            ))
            # Redact the key
            modified = re.sub(r"sk-[A-Za-z0-9]{20,}", "[REDACTED_API_KEY]", content)
```

**Tool Call Guard - Built-in Tool Auditing**
```python
class OpenAIToolCallGuard:
    """Handle both client-side and server-side tools."""

    # Built-in tools require monitoring (AUDIT)
    builtin_tools = ["web_search", "code_interpreter", "file_search"]

    # Custom function policies (DENY/WARN)
    function_policies = {
        "execute_command": {"blocked": True},
        "send_email": {"requires_review": True},
    }
```

**Responses API Guard**
```python
class ResponsesAPIGuard:
    """Handle Responses API output format with server-side execution."""

    def evaluate_responses_output(self, outputs: List[ResponsesAPIOutput]):
        for output in outputs:
            if output.type == "function_call":
                # Log server-side function calls
                findings.append(SecurityFinding(
                    risk_category=RiskCategory.EXCESSIVE_AGENCY,
                    metadata=[f"function:{output.name}", "type:server_side"]
                ))

            elif output.type == "function_call_output":
                # Check for error/exception leakage
                if "stack trace" in output.output:
                    findings.append(SecurityFinding(
                        risk_category=RiskCategory.IMPROPER_OUTPUT_HANDLING
                    ))

            elif output.type == "web_search_call":
                # Audit web search usage
```

#### OpenAI-Specific Types

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

---

## Cross-Framework Mapping

### Target Types by Framework

| Target Type | LangChain | LangGraph | Google ADK | Semantic Kernel | OpenAI |
|-------------|-----------|-----------|------------|-----------------|--------|
| `llm_input` | `before_agent` | `input_node` | `before_model_callback` | `IPromptFilter.on_prompt_rendered` | pre-chat |
| `llm_output` | `after_agent` | `output_node` | `after_model_callback` | (post-invoke) | post-chat |
| `tool_call` | tool middleware | `execute_tool_node` | `before/after_tool_callback` | `IFunctionFilter` | function call |
| `tool_definition` | tool validation | `validate_tools_node` | in-tool guardrails | plugin validation | N/A |
| `memory_store` | N/A | state mutation | session context | N/A | N/A |
| `memory_retrieve` | N/A | state access | session context | N/A | N/A |

### Decision Types Usage

| Decision | When to Use | Example |
|----------|-------------|---------|
| `allow` | Clean pass, no issues detected | Normal user query |
| `deny` | Block request/response entirely | Prompt injection, blocked tool |
| `modify` | Sanitize content, allow modified | PII redaction, secret removal |
| `warn` | Allow but flag for review | Sensitive tool, borderline content |
| `audit` | Log only, no enforcement | Built-in tool usage, compliance tracking |

### Provider Name Examples

| Framework | Provider Name |
|-----------|---------------|
| LangChain | `langchain.guardrails` |
| LangGraph | `langgraph` |
| Google ADK | `google.adk` |
| Semantic Kernel | `microsoft.semantic_kernel` |
| OpenAI | `openai` |
| Azure Content Safety | `azure.ai.content_safety` |

---

## Example Trace Output

```
invoke_agent LangChainSecureAgent (SpanKind.INTERNAL)
├── gen_ai.operation.name: invoke_agent
├── gen_ai.agent.name: LangChainSecureAgent
├── gen_ai.conversation.id: conv_001
│
├── apply_guardrail LangChain Input Guard (SpanKind.INTERNAL)
│   ├── gen_ai.operation.name: apply_guardrail
│   ├── gen_ai.guardian.id: langchain-input-guard-v1
│   ├── gen_ai.guardian.name: LangChain Input Guard
│   ├── gen_ai.guardian.provider.name: langchain.guardrails
│   ├── gen_ai.security.target.type: llm_input
│   ├── gen_ai.security.decision.type: allow
│   └── gen_ai.security.content.input.hash: sha256:a1b2c3d4...
│
├── chat mock-llm (SpanKind.CLIENT)
│   └── ...
│
└── apply_guardrail LangChain Output Guard (SpanKind.INTERNAL)
    ├── gen_ai.operation.name: apply_guardrail
    ├── gen_ai.guardian.id: langchain-output-guard-v1
    ├── gen_ai.guardian.name: LangChain Output Guard
    ├── gen_ai.security.target.type: llm_output
    ├── gen_ai.security.decision.type: modify
    ├── gen_ai.security.decision.reason: PII detected and redacted
    ├── gen_ai.security.content.redacted: true
    └── Events:
        └── gen_ai.security.finding
            ├── gen_ai.security.risk.category: sensitive_info_disclosure
            ├── gen_ai.security.risk.severity: medium
            ├── gen_ai.security.risk.score: 0.85
            ├── gen_ai.security.policy.id: policy_pii_protection
            └── gen_ai.security.risk.metadata: ["pattern:email", "count:2"]
```

---

## Risk Categories (OWASP LLM Top 10 2025)

| Category | OWASP ID | Description | Example Detection |
|----------|----------|-------------|-------------------|
| `prompt_injection` | LLM01 | Malicious prompt manipulation | "Ignore previous instructions" |
| `sensitive_info_disclosure` | LLM02 | PII/secrets in output | Email, phone, API keys |
| `supply_chain` | LLM03 | Compromised dependencies | Malicious plugins |
| `data_and_model_poisoning` | LLM04 | Training data manipulation | N/A (model-level) |
| `improper_output_handling` | LLM05 | XSS, code injection in output | Stack traces, error details |
| `excessive_agency` | LLM06 | Unauthorized tool access | Shell execution, file writes |
| `system_prompt_leakage` | LLM07 | System prompt extraction | "Show your instructions" |
| `vector_and_embedding_weaknesses` | LLM08 | RAG vulnerabilities | Poisoned embeddings |
| `misinformation` | LLM09 | False claims, hallucinations | "Scientific consensus proves..." |
| `unbounded_consumption` | LLM10 | DoS via resource exhaustion | Token limits |

Additional common categories: `jailbreak`, `toxicity`, `pii`

---

## Running Locally

If you want to run the prototypes locally, the code is available in this directory
but excluded from git. To set up:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install opentelemetry-api opentelemetry-sdk azure-monitor-opentelemetry-exporter

# For Azure Application Insights export
export APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=..."

# Run all demos
python run_all_demos.py
```

---

## References

- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai)
- [OWASP LLM Top 10 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Guardian Concepts Research](./GUARDIAN_CONCEPTS_RESEARCH.md)
