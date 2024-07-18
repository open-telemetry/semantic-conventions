package before_resolution

# This file enforces policies requiring all attributes to be defined within
# a semantic convention "registry".  This is a naming/structure convention
# used by semantic conventions.

# Helper to create attribute registry violations.
attr_registry_violation(violation_id, group_id, attr_id) = violation {
	violation := {
		"id": violation_id,
		"type": "semantic_convention_policies",
		"category": "attribute_registry_checks",
		"group": group_id,
		"attr": attr_id,
	}
}

# We only allow attribute groups in the attribute registry.
deny[attr_registry_violation("attribute_registry_can_only_contain_attribute_groups", group.id, "")] {
	group := input.groups[_]
	startswith(group.id, "registry.")
	group.type != "attribute_group"
}

# Any group that is NOT in the attribute registry that has an attribute id is
# in violation of not using the attribute registry.
deny[attr_registry_violation("attributes_must_be_defined_in_attribute_registry", group.id, attr.id)] {
	group := input.groups[_]
	not startswith(group.id, "registry.")
	attr := group.attributes[_]
	attr.id != null
}

# A registry `attribute_group` containing at least one `ref` attribute is
# considered invalid if it's not in the registry group.
deny[attr_registry_violation("attributes_in_registry_cannot_reference_each_other", group.id, attr.ref)] {
	# TODO - this will need to be updated to support `embed` in the future.
	group := input.groups[_]
	startswith(group.id, "registry.")
    attr := group.attributes[_]
	attr.ref != null
}

