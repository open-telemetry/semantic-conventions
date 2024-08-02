package before_resolution

yaml_schema_violation(description, group, attr) = violation {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "yaml_schema_violation",
        "attr": attr,
        "group": group,
    }
}

deny[yaml_schema_violation(description, group.id, "")] {
    group := input.groups[_]

    group.prefix != null
    group.prefix != ""

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("Group '%s' uses prefix '%s'. All attribute should be fully qualified with their id, prefix is no longer supported.", [group.id, group.prefix])
}
