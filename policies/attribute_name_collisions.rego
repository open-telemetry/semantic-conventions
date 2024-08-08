package after_resolution

# Data structures to make checking things faster.
attribute_names := [ data |
  attr := input.groups[_].attributes[_].name
  data := { "name": attr.name, "const_name": to_const_name(attr.name), "namespace_prefix": to_namespace_prefix(attr.name) }
]


deny[attr_registry_collision(description, name)] {
    name := attribute_names
    name2 := attribute_names
    name.name != name2.name
    name.const_name == name2.const_name
    not excluded_const_collisions[name.name]
    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Attribute '%s' has the same constant name '%s' as '%s'.", [name.name, name.const_name, name2.name])
}

deny[attr_registry_collision(description, name)] {
    name := attribute_names
    name2 := attribute_names
    name.name != name2.name
    name.namespace_prefix == name2.namespace_prefix
    not excluded_namespace_collisions[name.namespace_prefix]

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Attribute '%s' name is used as a namespace in the following attributes '%s'.", [name.name, name2.name])
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

# These lists contain exceptions for existing collisions that were introduced unintentionally.
# We'll have a way to specify how collision resolution happens in the schema -
# see phase 2 in https://github.com/open-telemetry/semantic-conventions/issues/1118#issuecomment-2173803006
# For now we'll exclude existing collisions from the checks.
# ADDING NEW EXCEPTIONS IS NOT ALLOWED.

# DO NOT ADD ATTRIBUTES TO THIS LIST
excluded_const_collisions := {"messaging.client_id"}
# DO NOT ADD ATTRIBUTES TO THIS LIST
excluded_namespace_collisions := {"messaging.operation", "db.operation", "deployment.environment"}
