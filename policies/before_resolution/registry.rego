package otel

to_const_name(prefix, id) = const_name {
    const_name := replace(trim(concat(".", [prefix, id]), "."), ".", "_")
}

deny[schema_evolution_violation("foobar", group.id, attr.id)] {
  	group := input.groups[_]
    attr := group.attributes[_]

    group.type == "attribute_group"
    not attr.ref

	const_names := [n | g := input.groups[_]; a := g.attributes[_]; n := to_const_name(g.prefix, a.id)]

    const_name := to_const_name(group.prefix, attr.id)
    count({i | const_names[i] == const_name}) > 1
}

attr_registry_violation(violation_id, group_id, attr_id) = violation {
	violation := {
		"id": violation_id,
		"type": "semconv_attribute",
		"category": "attribute_registry",
		"group": group_id,
		"attr": attr_id,
	}
}

