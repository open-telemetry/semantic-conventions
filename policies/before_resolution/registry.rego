package otel

# A registry `attribute_group` containing at least one `ref` attribute is
# considered invalid if it's not in the registry group.
deny[attr_registry_violation("registry_with_ref_attr", group.id, attr.ref)] {
	group := input.groups[_]
	startswith(group.id, "registry.")
	attr := group.attributes[_]
	attr.ref != null
}

# We only allow attribute groups in the attribute registry.
deny[attr_registry_violation("registry_must_be_attribute_group", group.id, "")] {
	group := input.groups[_]
	startswith(group.id, "registry.")
	group.type != "attribute_group"
}

# Any group that is NOT in the attribute registry that has an attribute id is
# in violation of not using the attribute registry.
deny[attr_registry_violation("nonregistry_with_id_attr", group.id, attr.id)] {
	group := input.groups[_]
	not startswith(group.id, "registry.")
	attr := group.attributes[_]
	attr.id != null
}

# Build an attribute registry violation
attr_registry_violation(violation_id, group_id, attr_id) = violation {
	violation := {
		"id": violation_id,
		"type": "semconv_attribute",
		"category": "attribute_registry",
		"group": group_id,
		"attr": attr_id,
	}
}
