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

# checks that metric id matches metric.{metric_name}
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    name := group.metric_name
    name != null

    expected_id := sprintf("metric.%s", [name])
    expected_id != group.id

    description := sprintf("Metric id '%s' is invalid. Metric id must follow 'metric.{metric_name}' pattern and match '%s'", [group.id, expected_id])
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

# checks that event id matches event.{name}
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    group.type == "event"
    name := group.name

    expected_id := sprintf("event.%s", [name])
    expected_id != group.id

    description := sprintf("Event id '%s' is invalid. Event id must follow 'event.{name}' pattern and match '%s'", [group.id, expected_id])
}

# checks event.name is not referenced in event attributes
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    group.type == "event"
    name := group.name

    attr := group.attributes[_]
    attr.ref == "event.name"

    description := sprintf("Attribute 'event.name' is referenced on event group '%s'. Event name must be provided in 'name' property on the group", [name])
}

# require resources have names
deny[yaml_schema_violation(description, group.id, "")] {
    group := input.groups[_]
    group.type == "resource"
    group.name == null
    description := sprintf("Resource id '%s' is invalid. Resource must have name.", [group.id])
}

# checks resource name format
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    group.type == "resource"
    name := group.name

    name != null
    not regex.match(name_regex, name)

    description := sprintf("Resource name '%s' is invalid. Resource name %s'", [name, invalid_name_helper])
}

# checks that resource group id matches resource.{name}
deny[yaml_schema_violation(description, group.id, name)] {
    group := input.groups[_]
    group.type == "resource"

    # TODO: remove once https://github.com/open-telemetry/semantic-conventions/pull/1423 is merged
    exclusions := {"resource.telemetry.sdk_experimental", "resource.service_experimental"}
    not exclusions[group.id]

    name := group.name

    expected_id := sprintf("resource.%s", [name])
    expected_id != group.id

    description := sprintf("Resource id '%s' is invalid. Resource id must follow 'resource.{name}' pattern and match '%s'", [group.id, expected_id])
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

# TODO: remove after span_kind is required https://github.com/open-telemetry/semantic-conventions/issues/1513
# checks that span id matches span.*. pattern if span_kind is not provided
deny[yaml_schema_violation(description, group.id, "")] {
    group := input.groups[_]
    group.type == "span"
    kind := group.span_kind

    kind == null
    not regex.match("^span\\.[a-z0-9_.]+$", group.id)
    description := sprintf("Group id '%s' is invalid. Span group 'id' must follow 'span.*' pattern", [group.id])
}

# checks that span id matches span.*.{kind} pattern if span_kind is not provided
deny[yaml_schema_violation(description, group.id, "")] {
    group := input.groups[_]
    group.type == "span"
    kind := group.span_kind

    kind != null
    pattern := sprintf("^span\\.[a-z0-9_.]+\\.%s$", [kind])
    not regex.match(pattern, group.id)
    description := sprintf("Group id '%s' is invalid. Span group 'id' must follow 'span.*.%s' pattern", [group.id, kind])
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
