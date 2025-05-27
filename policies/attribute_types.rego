package after_resolution
import rego.v1

# checks that complex attributes are not used in any groups except events
deny contains group_stability_violation(description, group.id, attr.name) if {
    group := input.groups[_]
    group.type != "event"
    group.type != "attribute_group"

    attr := group.attributes[_]
    attr.type in ["any", "template[any]"]

    description := sprintf("Attribute '%s' has type '%s' and is referenced on group '%s' of type '%s'. Complex attributes are only allowed on events.", [attr.name, attr.type, group.id, group.type])
}

attribute_type_violation(description, group, attr) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "attribute_type_violation",
        "attr": attr,
        "group": group,
    }
}
