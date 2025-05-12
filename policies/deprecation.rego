package after_resolution

import rego.v1

registry_attribute_names := {attr.name |
    some g in input.groups
    some attr in g.attributes
    not attr.deprecated
}

registry_metric_names := {group.metric_name |
    some group in input.groups
    group.type == "metric"
    not group.deprecated
}

registry_event_names := {group.name |
    some group in input.groups
    group.type == "event"
    not group.deprecated
}

# attribute.deprecated.renamed_to must be another attribute
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    attr := group.attributes[_]
    attr.deprecated != null
    attr.deprecated.renamed_to != null

    not attr.deprecated.renamed_to in registry_attribute_names
    description := sprintf("Attribute '%s' was renamed to '%s', but the new attribute does not exist or is deprecated.", [attr.name, attr.deprecated.renamed_to])
}

# metric.deprecated.renamed_to must be another metric
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    group.type == "metric"
    group.deprecated != null
    group.deprecated.renamed_to != null

    not group.deprecated.renamed_to in registry_metric_names
    description := sprintf("Metric '%s' was renamed to '%s', but the new metric does not exist or is deprecated.", [group.metric_name, group.deprecated.renamed_to])
}

# event.deprecated.renamed_to must be another event
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    group.type == "event"
    group.deprecated != null
    group.deprecated.renamed_to != null

    not group.deprecated.renamed_to in registry_event_names
    description := sprintf("Event '%s' was renamed to '%s', but the new event does not exist or is deprecated.", [group.name, group.deprecated.renamed_to])
}

deprecation_violation(description, group, attr) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "deprecation_violation",
        "attr": attr,
        "group": group,
    }
}
