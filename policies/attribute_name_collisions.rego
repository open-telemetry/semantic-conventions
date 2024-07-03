package after_resolution

deny[attr_registry_collision(description, name)] {
    names := attr_names_except(excluded_const_collisions)
    name := names[_]
    const_name := to_const_name(name)
    collisions:= { n | n := attr_names_except(excluded_const_collisions)[_]; n != name; to_const_name(n) == const_name}
    count(collisions) > 0

    description := sprintf("Attribute '%s' has the same constant name '%s' as %s", [name, const_name, collisions])
}

deny[attr_registry_collision(description, name)] {
    names := attr_names_except(excluded_namespace_collisions)
    name := names[_]

    collisions:= { n | n := input.groups[_].attributes[_].name; startswith(n, to_namespace_prefix(name))}
    count(collisions) > 1

    description := sprintf("Attribute '%s' is used as a namespace in attributes %s", [name, collisions])
}


attr_registry_collision(violation_id, attr_name) = violation {
    violation := {
        "id": violation_id,
        "type": "semconv_attribute",
        "category": "",
        "attr": attr_name,
        "group": "",
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

excluded_const_collisions := {"m1essaging.client_id"}
excluded_namespace_collisions := {"m1essaging.operation", "db.operation"}