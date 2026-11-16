package after_resolution

import future.keywords

test_fails_on_attribute_in_owned_namespace if {
    findings := deny with input as {"registry": {"attributes": [
        {"key": "gen_ai.request.model", "type": "string", "brief": "Model."},
    ]}}
    count(findings) == 1
    some f in findings
    f.id == "namespace_owned_by_other_registry"
    f.context.namespace == "gen_ai"
}

test_fails_on_attribute_equal_to_owned_namespace if {
    count(deny) == 1 with input as {"registry": {"attributes": [
        {"key": "openai", "type": "string", "brief": "OpenAI."},
    ]}}
}

test_fails_on_each_signal_type if {
    count(deny) == 4 with input as {"registry": {
        "metrics": [{"name": "mcp.client.operation.duration", "brief": "Duration."}],
        "spans": [{"type": "gen_ai.client.inference", "brief": "Inference."}],
        "events": [{"name": "gen_ai.client.inference.operation.details", "brief": "Details."}],
        "entities": [{"type": "gen_ai.agent", "brief": "Agent."}],
    }}
}

test_fails_on_each_federated_owner if {
    findings := deny with input as {"registry": {
        "attributes": [
            {"key": "zos.sysplex.name", "type": "string", "brief": "Sysplex."},
            {"key": "enduser.id", "type": "string", "brief": "End user."},
            {"key": "a2a.task.id", "type": "string", "brief": "Task."},
        ],
        "spans": [{"type": "a2a.client", "brief": "Client."}],
        "entities": [{"type": "zos.software", "brief": "Software."}],
    }}
    count(findings) == 5
    owners := {f.context.owner | some f in findings}
    owners == {
        "https://github.com/open-telemetry/semantic-conventions-mainframe",
        "https://github.com/open-telemetry/semantic-conventions-client-side",
        "https://github.com/open-telemetry/semantic-conventions-genai",
    }
}

test_passes_on_deprecated_definitions if {
    count(deny) == 0 with input as {"registry": {
        "attributes": [
            {"key": "gen_ai.system", "type": "string", "brief": "System.", "deprecated": {"reason": "uncategorized", "note": "Moved."}},
        ],
        "metrics": [
            {"name": "gen_ai.client.token.usage", "brief": "Tokens.", "deprecated": {"reason": "uncategorized", "note": "Moved."}},
        ],
        "spans": [
            {"type": "openai.client", "brief": "Client.", "deprecated": {"reason": "uncategorized", "note": "Moved."}},
        ],
    }}
}

test_passes_on_similar_prefix_outside_namespace if {
    count(deny) == 0 with input as {"registry": {
        "attributes": [
            {"key": "gen_ai_like.attr", "type": "string", "brief": "Not gen_ai."},
            {"key": "mcpx.id", "type": "string", "brief": "Not mcp."},
            {"key": "aws.bedrock.guardrail.id", "type": "string", "brief": "Not owned."},
        ],
        "metrics": [{"name": "endusers.metric", "brief": "Not enduser."}],
    }}
}

test_fails_on_focus_namespace if {
    findings := deny with input as {"registry": {
        "attributes": [{"key": "focus.workload.id", "type": "string", "brief": "Workload."}],
        "metrics": [{"name": "focused.metric", "brief": "Not focus."}],
    }}
    count(findings) == 1
    some f in findings
    f.context.owner == "https://github.com/FinOps-Open-Cost-and-Usage-Spec/focus-otel-semconv"
}
