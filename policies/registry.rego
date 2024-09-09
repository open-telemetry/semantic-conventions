package before_resolution

# This file enforces policies requiring all attributes to be defined within
# a semantic convention "registry".  This is a naming/structure convention
# used by semantic conventions.

# Helper to create attribute registry violations.
attr_registry_violation(description, group_id, attr_id) = violation {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "attribute_registry_checks",
        "group": group_id,
        "attr": attr_id,
    }
}

# We only allow attribute groups in the attribute registry.
deny[attr_registry_violation(description, group.id, "")] {
    group := input.groups[_]
    startswith(group.id, "registry.")
    group.type != "attribute_group"

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    # violation_id := "attribute_registry_can_only_contain_attribute_groups"
    description := sprintf("Registry group '%s' has invalid type '%s'. Groups in attribute registry must have `attribute_group` type.", [group.id, group.type])
}

# Any group that is NOT in the attribute registry that has an attribute id is
# in violation of not using the attribute registry.
deny[attr_registry_violation(description, group.id, attr.id)] {
    group := input.groups[_]
    not startswith(group.id, "registry.")
    attr := group.attributes[_]
    attr.id != null

    attr_name := get_attribute_name(attr, group)

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    # violation_id := "attributes_must_be_defined_in_attribute_registry"
    description := sprintf("Attribute '%s' is defined in the group '%s' which is not part of the attribute registry. Attributes can be defined in the registry group only.", [attr_name, group.id])
}

# A registry `attribute_group` containing at least one `ref` attribute is
# considered invalid if it's not in the registry group.
deny[attr_registry_violation(description, group.id, attr.ref)] {
    # TODO - this will need to be updated to support `embed` in the future.
    group := input.groups[_]
    startswith(group.id, "registry.")
    attr := group.attributes[_]
    attr.ref != null

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    # violation_id := "attributes_in_registry_cannot_reference_each_other"
    description := sprintf("Registry group '%s' references attribute '%s'. Registry groups can only define new attributes.", [group.id, attr.ref])
}

get_attribute_name(attr, group) = name {
    full_name = concat(".", [group.prefix, attr.id])

    # if there was no prefix, we have a leading dot
    name := trim(full_name, ".")
}
