package after_resolution

# Data structures to make checking things faster.
attribute_names := { data |
  group := input.groups[_]
  attr := group.attributes[_]
  data := { "name": attr.name, "const_name": to_const_name(attr.name), "namespace_prefix": to_namespace_prefix(attr.name) }
}


deny[attr_registry_collision(description, name)] {
    some i
    name := attribute_names[i].name
    const_name := attribute_names[i].const_name
    not excluded_const_collisions[name]
    collisions := [other.name |
        other := attribute_names[_]
        other.name != name
        other.const_name == const_name
        not excluded_const_collisions[other.name]
    ]
    count(collisions) > 0
    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Attribute '%s' has the same constant name '%s' as '%s'.", [name, const_name, collisions])
}

deny[attr_registry_collision(description, name)] {
    some i
    name := attribute_names[i].name
    prefix := attribute_names[i].namespace_prefix
    not excluded_namespace_collisions[name]
    collisions := [other.name |
        other := attribute_names[_]
        other.name != name
        startswith(other.name, prefix)
    ]
    count(collisions) > 0
    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Attribute '%s' is used as a namespace in '%s'.", [name, collisions])
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
