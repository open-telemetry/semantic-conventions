package before_resolution

# checks attribute name format
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    attr := group.attributes[_]
    name := attr.id

    not regex.match(name_regex, name)

    description := sprintf("Attribute name '%s' is invalid. Attribute name %s", [name, invalid_name_helper])
}

# checks attribute name has a namespace
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    attr := group.attributes[_]
    name := attr.id

    # some deprecated attributes have no namespace and need to be ignored
    not attr.deprecated
    not regex.match(has_namespace_regex, name)

    description := sprintf("Attribute name '%s' should have a namespace. Attribute name %s", [name, invalid_name_helper])
}


# checks metric name format
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    name := group.metric_name

    name != null
    not regex.match(name_regex, name)

    description := sprintf("Metric name '%s' is invalid. Metric name %s'", [name, invalid_name_helper])
}

# checks event name format
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    group.type == "event"
    name := group.name

    name != null
    not regex.match(name_regex, name)

    description := sprintf("Event name '%s' is invalid. Event name %s'", [name, invalid_name_helper])
}

# checks attribute member id format
deny[yaml_schema_violation(description, group.id, attr_name)] {
    group := input.groups[_]
    attr := group.attributes[_]
    attr_name := attr.id
    name := attr.type.members[_].id

    not regex.match(name_regex, name)

    description := sprintf("Member id '%s' on attribute '%s' is invalid. Member id %s'", [name, attr_name, invalid_name_helper])
}

# check that attribute is fully qualified with their id, prefix is no longer supported
deny[yaml_schema_violation(description, group.id, "")] {
    group := input.groups[_]

    group.prefix != null
    group.prefix != ""

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Group '%s' uses prefix '%s'. All attribute should be fully qualified with their id, prefix is no longer supported.", [group.id, group.prefix])
}

yaml_schema_violation(description, group, attr) = violation {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "yaml_schema_violation",
        "attr": attr,
        "group": group,
    }
}

# not valid: '1foo.bar', 'foo.bar.', 'foo.bar_', 'foo..bar', 'foo._bar' ...
# valid: 'foo.bar', 'foo.1bar', 'foo.1_bar'
name_regex := "^[a-z][a-z0-9]*([._][a-z0-9]+)*$"

has_namespace_regex := "^[a-z0-9_]+\\.([a-z0-9._]+)+$"

invalid_name_helper := "must consist of lowercase alphanumeric characters separated by '_' and '.'"
