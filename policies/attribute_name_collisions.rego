package after_resolution

import rego.v1

# Data structures to make checking things faster.
attribute_names := { obj |
    group := input.groups[_];
    attr := group.attributes[_];
    obj := { "name": attr.name, "const_name": to_const_name(attr.name), "namespace_prefix": to_namespace_prefix(attr.name), "deprecated": is_property_set(attr, "deprecated"), "annotations": property_or_null(attr, "annotations") }
}

# check that attribute constant names do not collide
deny contains attr_registry_collision(description, name) if {
    some i
    name := attribute_names[i].name
    const_name := attribute_names[i].const_name
    annotations := attribute_names[i].annotations

    not annotations["code_generation"]["exclude"]

    collisions := [other.name |
        other := attribute_names[_]
        other.name != name
        other.const_name == const_name

        not other.annotations["code_generation"]["exclude"]
    ]
    count(collisions) > 0

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Attribute '%s' has the same constant name '%s' as '%s'.", [name, const_name, collisions])
}

# check that attribute names do not collide with namespaces
deny contains attr_registry_collision(description, name) if {
    some i

    # ignore deprecated attributes
    not attribute_names[i].deprecated

    name := attribute_names[i].name
    prefix := attribute_names[i].namespace_prefix

    collisions := [other.name |
        other := attribute_names[_]
        not other.deprecated

        other.name != name
        startswith(other.name, prefix)
    ]
    count(collisions) > 0
    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Attribute '%s' name is used as a namespace in the following attributes '%s'.", [name, collisions])
}

# check that attribute is not defined or referenced more than once within the same group
deny contains attr_registry_collision(description, name) if {
    group := input.groups[_]
    attr := group.attributes[_]
    name := attr.name

    collisions := [n | n := group.attributes[_].name; n == name ]
    count(collisions) > 1

    description := sprintf("Attribute '%s' is already defined in the group '%s'. Attributes must be unique.", [name, group.id])
}

attr_registry_collision(description, attr_name) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "naming_collision",
        "attr": attr_name,
        "group": "",
    }
}

to_namespace_prefix(name) = namespace if {
    namespace := concat("", [name, "."])
}

to_const_name(name) = const_name if {
    const_name := replace(name, ".", "_")
}

is_property_set(obj, property) = true if {
    obj[property] != null
} else = false

property_or_null(obj, property) := obj[property] if {
    obj[property]
} else = null
