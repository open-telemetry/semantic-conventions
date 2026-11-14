package after_resolution

import rego.v1

# This policy is not provided by opentelemetry-weaver-packages and MUST NOT be
# moved there: it is specific to the core semantic conventions registry.
#
# Some namespaces are owned by another registry (for example, a federated
# OpenTelemetry semantic conventions repository). Core MUST NOT define new
# attributes or signals in those namespaces. Deprecated definitions are allowed
# so that core can keep the entries that point users to the new owner.

# Namespace -> owning registry.
owned_namespaces := {
    "gen_ai": "https://github.com/open-telemetry/semantic-conventions-genai",
    "mcp": "https://github.com/open-telemetry/semantic-conventions-genai",
    "openai": "https://github.com/open-telemetry/semantic-conventions-genai",
    "focus": "https://github.com/FinOps-Open-Cost-and-Usage-Spec/focus-otel-semconv",
}

# attributes
deny contains finding if {
    some attr in input.registry.attributes
    not is_deprecated(attr)
    some ns, owner in owned_namespaces
    in_namespace(attr.key, ns)

    finding := {
        "id": "namespace_owned_by_other_registry",
        "message": sprintf("Attribute '%s' is in the '%s' namespace, which is owned by %s. Define it there instead.", [attr.key, ns, owner]),
        "level": "violation",
        "context": {
            "attribute_key": attr.key,
            "namespace": ns,
            "owner": owner,
        },
    }
}

# signals
deny contains finding if {
    some entry in named_signals
    not is_deprecated(entry.signal)
    some ns, owner in owned_namespaces
    in_namespace(entry.signal_name, ns)

    finding := {
        "id": "namespace_owned_by_other_registry",
        "message": sprintf("%s '%s' is in the '%s' namespace, which is owned by %s. Define it there instead.", [entry.signal_type, entry.signal_name, ns, owner]),
        "level": "violation",
        "context": {
            "namespace": ns,
            "owner": owner,
        },
        "signal_type": entry.signal_type,
        "signal_name": entry.signal_name,
    }
}

in_namespace(name, ns) if name == ns

in_namespace(name, ns) if startswith(name, concat("", [ns, "."]))

is_deprecated(obj) if object.get(obj, "deprecated", null) != null

named_signals contains entry if {
    some metric in input.registry.metrics
    entry := {"signal_type": "metric", "signal_name": metric.name, "signal": metric}
}

named_signals contains entry if {
    some span in input.registry.spans
    entry := {"signal_type": "span", "signal_name": span.type, "signal": span}
}

named_signals contains entry if {
    some event in input.registry.events
    entry := {"signal_type": "event", "signal_name": event.name, "signal": event}
}

named_signals contains entry if {
    some entity in input.registry.entities
    entry := {"signal_type": "entity", "signal_name": entity.type, "signal": entity}
}
