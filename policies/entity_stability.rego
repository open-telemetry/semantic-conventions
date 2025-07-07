package after_resolution
import rego.v1

# checks for stable entity groups that have no identifying attributes
deny contains entity_stability_violation(description, group.id, "") if {
    group := input.groups[_]
    # ignore attribute_groups
    group.type == "entity"
    group.stability == "stable"

    exceptions = {}
    not exceptions[group.id]

    ids := [attr |
        some attr in group.attributes
        attr.role == "identifying"
    ]
    count(ids) < 1

    description := sprintf("Stable entity '%s' has no identifying attributes", [group.name])
}


# checks for stable entity groups that have attributes with no role
deny contains entity_stability_violation(description, group.id, attr.name) if {
    group := input.groups[_]
    # ignore attribute_groups
    group.type == "entity"
    group.stability == "stable"

    exceptions = {}
    not exceptions[group.id]

    attr := group.attributes[_]
    not attr.role

    description := sprintf("Stable entity '%s' has attribute without role: '%s'", [group.name, attr.name])
}

entity_stability_violation(description, group, attr) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "group_stability_violation",
        "attr": attr,
        "group": group,
    }
}