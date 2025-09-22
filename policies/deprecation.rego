package after_resolution

import rego.v1

registry_attribute_names := {attr.name |
    some g in input.groups
    some attr in g.attributes
    not attr.deprecated
}


registry_attribute_type_map := { attr.name: attr.type |
    some g in input.groups
    some attr in g.attributes
    not attr.deprecated
}

registry_metric_names := {group.metric_name |
    some group in input.groups
    group.type == "metric"
    not group.deprecated
}

registry_event_names := {group.name |
    some group in input.groups
    group.type == "event"
    not group.deprecated
}

# attribute.deprecated.renamed_to must be another attribute
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")    
    attr := group.attributes[_]
    attr.deprecated != null
    attr.deprecated.renamed_to != null

    not attr.deprecated.renamed_to in registry_attribute_names
    description := sprintf("Attribute '%s' was renamed to '%s', but the new attribute does not exist or is deprecated.", [attr.name, attr.deprecated.renamed_to])
}

# attribute.deprecated.renamed_to attribute must be of the same type
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")    
    attr := group.attributes[_]
    attr.deprecated != null
    attr.deprecated.renamed_to != null
    # enums are checked separately
    not attr.type.members

    new_type = registry_attribute_type_map[attr.deprecated.renamed_to]
    # enums are checked separately    
    not new_type.members
    attr.type != new_type
    description := sprintf("Attribute '%s' was renamed to '%s', but the new attribute type '%s' is not the same as the old attribute type '%s'.", [attr.name, attr.deprecated.renamed_to, new_type, attr.type])
}

# attribute.deprecated.renamed_to: string to enum of strings is ok
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")    
    attr := group.attributes[_]
    attr.deprecated != null
    attr.deprecated.renamed_to != null
    new_type = registry_attribute_type_map[attr.deprecated.renamed_to]

    attr.type == "string"
    new_type.members != null
    not is_string(new_type.members[0].value)

    description := sprintf("String attribute '%s' was renamed to enum attribute '%s', but the new attribute member type '%s' is not a string type", [attr.name, attr.deprecated.renamed_to, new_type.members[0].value])
}

# attribute.deprecated.renamed_to: int to enum of ints is ok
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")    
    attr := group.attributes[_]
    attr.deprecated != null
    attr.deprecated.renamed_to != null
    new_type = registry_attribute_type_map[attr.deprecated.renamed_to]

    attr.type == "int"
    new_type.members != null
    not is_number(new_type.members[0].value)

    description := sprintf("Int attribute '%s' was renamed to enum attribute '%s', but the new attribute member type '%s' is not a number", [attr.name, attr.deprecated.renamed_to, new_type.members[0].value])
}

# enum attribute.deprecated.renamed_to: enum of the same value types is ok
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")    
    attr := group.attributes[_]
    attr.deprecated != null
    attr.deprecated.renamed_to != null
    attr.type.members != null
    new_type = registry_attribute_type_map[attr.deprecated.renamed_to]
    new_type.members != null

    not same_type(attr.type.members[0].value, new_type.members[0].value)
    description := sprintf("Enum attribute '%s' was renamed to '%s', but the value types are not the same: old - '%s', new - '%s'.", 
        [attr.name, attr.deprecated.renamed_to, attr.type.members[0].value, new_type.members[0].value])
}

# enum attribute.deprecated.renamed_to: enum of strings to string is ok
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")    
    attr := group.attributes[_]
    attr.deprecated != null
    attr.deprecated.renamed_to != null

    attr.type.members != null

    is_string(attr.type.members[0].value)

    new_type = registry_attribute_type_map[attr.deprecated.renamed_to]
    not new_type.members
    new_type != "string"
    description := sprintf("Enum attribute '%s' with string values was renamed to '%s', but the new attribute type is '%s'.", [attr.name, attr.deprecated.renamed_to, new_type])
}

# enum attribute.deprecated.renamed_to: enum of ints to int is ok
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")    
    attr := group.attributes[_]
    attr.deprecated != null
    attr.deprecated.renamed_to != null
    attr.type.members != null
    is_number(attr.type.members[0].value)

    new_type = registry_attribute_type_map[attr.deprecated.renamed_to]
    not new_type.members
    new_type != "int"
    description := sprintf("Enum attribute '%s' with int values was renamed to '%s', but the new attribute type is '%s'.", [attr.name, attr.deprecated.renamed_to, new_type])
}

# attribute.members.deprecated.renamed_to member must be a member of the same enum
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    startswith(group.id, "registry.")    
    attr := group.attributes[_]
    attr.type.members != null
    member := attr.type.members[_]
    member.deprecated.renamed_to != null

    matches := [m.id |
        m := attr.type.members[_]
        m.id == member.deprecated.renamed_to
        object.get(m, "deprecated", null) == null
    ]
    count(matches) == 0
    
    description := sprintf("Member '%s' of the attribute '%s' was renamed to '%s', but the new member does not exist or is deprecated.", [member.id, 
        attr.name, member.deprecated.renamed_to])
}

# metric.deprecated.renamed_to must be another metric
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    group.type == "metric"
    group.deprecated != null
    group.deprecated.renamed_to != null

    not group.deprecated.renamed_to in registry_metric_names
    description := sprintf("Metric '%s' was renamed to '%s', but the new metric does not exist or is deprecated.", [group.metric_name, group.deprecated.renamed_to])
}

# event.deprecated.renamed_to must be another event
deny contains deprecation_violation(description, group.id, "") if {
    group := input.groups[_]
    group.type == "event"
    group.deprecated != null
    group.deprecated.renamed_to != null

    not group.deprecated.renamed_to in registry_event_names
    description := sprintf("Event '%s' was renamed to '%s', but the new event does not exist or is deprecated.", [group.name, group.deprecated.renamed_to])
}

deprecation_violation(description, group, attr) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "deprecation_violation",
        "attr": attr,
        "group": group,
    }
}

same_type(a, b) if {
  is_string(a)
  is_string(b)
}

same_type(a, b) if {
  is_number(a)
  is_number(b)
}

same_type(a, b) if {
  is_boolean(a)
  is_boolean(b)
}

same_type(a, b) if {
  is_array(a)
  is_array(b)
}

same_type(a, b) if {
  is_set(a)
  is_set(b)
}

same_type(a, b) if {
  is_object(a)
  is_object(b)
}
