package before_resolution
import rego.v1

# This file enforces policies requiring all attributes to be defined within
# a semantic convention "registry".  This is a naming/structure convention
# used by semantic conventions.

# Helper to create attribute registry violations.
attr_registry_violation(description, group_id, attr_id) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "attribute_registry_checks",
        "group": group_id,
        "attr": attr_id,
    }
}

# We only allow attribute groups in the attribute registry.
deny contains attr_registry_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")
    group.type != "attribute_group"

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    # violation_id := "attribute_registry_can_only_contain_attribute_groups"
    description := sprintf("Registry group '%s' has invalid type '%s'. Groups in attribute registry must have `attribute_group` type.", [group.id, group.type])
}

# Any group that is NOT in the attribute registry that has an attribute id is
# in violation of not using the attribute registry.
deny contains attr_registry_violation(description, group.id, attr.id) if {
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
deny contains attr_registry_violation(description, group.id, attr.ref) if {
    # TODO - this will need to be updated to support `embed` in the future.
    group := input.groups[_]
    startswith(group.id, "registry.")
    attr := group.attributes[_]
    attr.ref != null

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    # violation_id := "attributes_in_registry_cannot_reference_each_other"
    description := sprintf("Registry group '%s' references attribute '%s'. Registry groups can only define new attributes.", [group.id, attr.ref])
}

# We don't allow attribute definitions to have requirement_level
deny contains attr_registry_violation(description, group.id, attr.id) if {
    group := input.groups[_]
    startswith(group.id, "registry.")

    attr := group.attributes[_]

    # TODO: requirement_level defaults to recommended - no way to check if it's not set.
    attr.requirement_level != "recommended"

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Attribute definition '%s' has requirement_level set to %s. Only attribute references can set requirement_level.", [attr.id, attr.requirement_level])
}

# We require attribute definitions to have stability
deny contains attr_registry_violation(description, group.id, attr.id) if {
    group := input.groups[_]
    attr := group.attributes[_]
    not attr.stability
    description := sprintf("Attribute definition '%s' does not contain stability field. All attribute definitions must include stability level.", [attr.id])
}

# We require span, metrics, events, resources definitions to have stability
deny contains attr_registry_violation(description, group.id, "") if {
    semconv_types := {"span", "metric", "event", "resource"}
    group := input.groups[_]

    semconv_types[group.type] != null

    not group.stability
    description := sprintf("Semconv group '%s' does not contain stability field. All semconv definitions must include stability level.", [group.id])
}

get_attribute_name(attr, group) := name if {
    full_name := concat(".", [group.prefix, attr.id])

    # if there was no prefix, we have a leading dot
    name := trim(full_name, ".")
}

