package after_resolution

deny[attr_registry_collision(description, name)] {
    names := attr_names_except(excluded_const_collisions)
    name := names[_]
    const_name := to_const_name(name)
    collisions:= { n | n := attr_names_except(excluded_const_collisions)[_]; n != name; to_const_name(n) == const_name }
    count(collisions) > 0

    description := sprintf("Attribute '%s' has the same constant name '%s' as '%s'.", [name, const_name, collisions])
}

deny[attr_registry_collision(description, name)] {
    names := attr_names_except(excluded_namespace_collisions)
    name := names[_]

    collisions:= { n | n := input.groups[_].attributes[_].name; startswith(n, to_namespace_prefix(name)) }
    count(collisions) > 0

    description := sprintf("Attribute '%s' name is used as a namespace in the following attributes '%s'.", [name, collisions])
}

attr_registry_collision(description, attr_name) = violation {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "naming_collision",
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
    names := { n | n := input.groups[_].attributes[_].name } - excluded
}

# These lists contain exceptions for existing collisions that were introduced unintentionally.
# We'll have a way to specify how collision resolution happens in the schema -
# see phase 2 in https://github.com/open-telemetry/semantic-conventions/issues/1118#issuecomment-2173803006
# For now we'll exclude existing collisions from the checks.
# ADDING NEW EXCEPTIONS IS NOT ALLOWED.

# DO NOT ADD ATTRIBUTES TO THIS LIST
excluded_const_collisions := {"messaging.client_id"}
# DO NOT ADD ATTRIBUTES TO THIS LIST
excluded_namespace_collisions := {"messaging.operation", "db.operation", "deployment.environment"}
