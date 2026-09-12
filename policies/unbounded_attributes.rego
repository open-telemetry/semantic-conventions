package after_resolution

import rego.v1

# An attribute marked with unbounded value size must not be required.
deny contains finding if {
    some entry in signals_with_attributes
    attr := entry.attr
    is_unbounded(attr)
    attr.requirement_level == "required"

    finding := {
        "id": "unbounded_attribute_required",
        "message": sprintf("Attribute '%s' on %s '%s' is marked as unbounded and cannot be required.", [attr.key, entry.signal_type, entry.signal_name]),
        "level": "violation",
        "context": {
            "attribute_key": attr.key,
            "signal_type": entry.signal_type,
            "signal_name": entry.signal_name,
        },
    }
}

deny contains finding if {
    some attr in input.registry.attributes
    is_unbounded(attr)
    attr.requirement_level == "required"

    finding := {
        "id": "unbounded_attribute_required",
        "message": sprintf("Attribute '%s' is marked as unbounded and cannot be required.", [attr.key]),
        "level": "violation",
        "context": {
            "attribute_key": attr.key,
        },
    }
}

is_unbounded(attr) if {
    attr.annotations.value.unbounded_size == true
}

is_unbounded(attr) if {
    some reg_attr in input.registry.attributes
    reg_attr.key == attr.key
    reg_attr.annotations.value.unbounded_size == true
}

signals_with_attributes contains entry if {
    some span in input.registry.spans
    some attr in span.attributes
    entry := {"signal_type": "span", "signal_name": span.type, "attr": attr}
}

signals_with_attributes contains entry if {
    some event in input.registry.events
    some attr in event.attributes
    entry := {"signal_type": "event", "signal_name": event.name, "attr": attr}
}

signals_with_attributes contains entry if {
    some metric in input.registry.metrics
    some attr in metric.attributes
    entry := {"signal_type": "metric", "signal_name": metric.name, "attr": attr}
}

signals_with_attributes contains entry if {
    some entity in input.registry.entities
    some attr in entity.attributes
    entry := {"signal_type": "entity", "signal_name": entity.type, "attr": attr}
}

signals_with_attributes contains entry if {
    some group in input.registry.attribute_groups
    some attr in group.attributes
    entry := {"signal_type": "attribute_group", "signal_name": group.id, "attr": attr}
}
