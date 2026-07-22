package after_resolution

import rego.v1

# This policy is not provided by opentelemetry-weaver-packages.
#
# It requires a non-empty `brief` on attributes and on every signal
# (metrics, spans, events, entities).

# brief is required on attributes
deny contains finding if {
    some attr in input.registry.attributes
    brief := object.get(attr, "brief", null)
    # missing, null, or empty
    {brief == null, brief == ""}[_]

    finding := {
        "id": "brief_required",
        "message": sprintf("Attribute '%s' is invalid. Attributes must have a brief.", [attr.key]),
        "level": "violation",
        "context": {
            "attribute_key": attr.key,
        },
    }
}

# brief is required on signals
deny contains finding if {
    some entry in signals_with_brief
    brief := object.get(entry.signal, "brief", null)
    # missing, null, or empty
    {brief == null, brief == ""}[_]

    finding := {
        "id": "brief_required",
        "message": sprintf("%s '%s' is invalid. Signals must have a brief.", [entry.signal_type, entry.signal_name]),
        "level": "violation",
        "context": {},
        "signal_type": entry.signal_type,
        "signal_name": entry.signal_name,
    }
}

signals_with_brief contains entry if {
    some metric in input.registry.metrics
    entry := {"signal_type": "metric", "signal_name": metric.name, "signal": metric}
}

signals_with_brief contains entry if {
    some span in input.registry.spans
    entry := {"signal_type": "span", "signal_name": span.type, "signal": span}
}

signals_with_brief contains entry if {
    some event in input.registry.events
    entry := {"signal_type": "event", "signal_name": event.name, "signal": event}
}

signals_with_brief contains entry if {
    some entity in input.registry.entities
    entry := {"signal_type": "entity", "signal_name": entity.type, "signal": entity}
}
