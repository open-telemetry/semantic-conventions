package after_resolution
import rego.v1

# Collection of all entity names from the registry.
known_entities := { g.name |
    some g in input.groups
    g.type == "entity"
}

# checks that all entity associations have valid groups.
deny contains entity_association_violation(description, group.id) if {
    group := input.groups[_]
    some entity in group.entity_associations
    not known_entities[entity]
    description := sprintf("Unknown entity '%s' associated in group '%s'", [entity, group.id])
}

entity_association_violation(description, group) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "entity_association_violation",
        "attr": "",
        "group": group,
    }
}