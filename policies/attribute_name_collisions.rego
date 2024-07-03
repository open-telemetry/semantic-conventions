package after_resolution

# TODO: https://github.com/open-telemetry/semantic-conventions/issues/1118
# we need to specify exclusions in the schema
excluded_const_collisions := {"messaging.client_id"}
excluded_namespace_collisions := {"messaging.operation", "db.operation"}

deny[attr_registry_collision(description, "", attr.name)] {
    attr := attr_names_except(excluded_const_collisions)[_]
    const_name := to_const_name(attr.name)

	collisions:= [ n | n := attr_names_except(excluded_const_collisions)[_]; n != attr.name; to_const_name(n) == const_name]
	count(collisions) > 0

	description := sprintf("Attribute '%s' has the same constant name '%s' as %s", [attr.name, const_name, collisions])
}

deny[attr_registry_collision(description, "", attr.name)] {
    attr := attr_names_except(excluded_namespace_collisions)[_]

	collisions:= [ n | n := input.groups[_].attributes[_].name; startswith(n, to_namespace_prefix(attr.name))]
	count(collisions) > 1

	description := sprintf("Attribute '%s' is used as a namespace in attributes %s", [attr.name, collisions])
}

attr_registry_collision(violation_id, group_id, attr_name) = violation {
	violation := {
		"id": violation_id,
		"type": "semconv_attribute",
		"category": "",
		"attr": attr_name,
		"group": group_id,
	}
}

to_namespace_prefix(name) = namespace {
    namespace := concat("", [name, "."])
}

to_const_name(name) = const_name {
    const_name := replace(name, ".", "_")
}

attr_names_except(excluded) = names {
	names := {n | n := input.groups[_].attributes[_].name} - excluded
}
