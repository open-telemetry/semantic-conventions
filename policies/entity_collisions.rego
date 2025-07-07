package after_resolution

import rego.v1

# Data structures to make checking things faster.
entities_names := { obj |
    group := input.groups[_]
    group.type = "entity"
    obj := { "name": group.name, "namespace_prefix": to_namespace_prefix(group.name)}
}

# check that matric names do not collide with namespaces
deny contains entities_registry_collision(description, name) if {
    some i

    name := entities_names[i].name
    prefix := entities_names[i].namespace_prefix

    collisions := [other.name |
        other := entities_names[_]

        other.name != name
        startswith(other.name, prefix)
    ]
    count(collisions) > 0
    description := sprintf("Entity name '%s' is used as a namespace in the following entities '%s'.", [name, collisions])
}


entities_registry_collision(description, entity_name) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "namespace_collision",
        "attr": entity_name,
        "group": "",
    }
}

to_namespace_prefix(name) = namespace if {
    namespace := concat("", [name, "."])
}
