package after_resolution

# checks that stable group does not have experimental attributes with requirement levels other than opt_in
deny[group_stability_violation(description, group.id, name)] {
    group := input.groups[_]
    # ignore attribute_groups
    group.type != "attribute_group"
    group.stability == "stable"

    exceptions = {
        # TODO: https://github.com/open-telemetry/semantic-conventions/issues/1514
        "metric.kestrel.connection.duration", "metric.kestrel.tls_handshake.duration",
        # TODO: https://github.com/open-telemetry/semantic-conventions/issues/1519
        "resource.service",
    }
    not exceptions[group.id]

    attr := group.attributes[_]

    attr.stability != "stable"
    attr.requirement_level != "opt_in"

    name := attr.name

    description := sprintf("Stable group '%s' references experimental attribute with requirement level '%s', only 'opt_in' level is allowed", [group.id, name])
}

group_stability_violation(description, group, attr) = violation {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "group_stability_violation",
        "attr": attr,
        "group": group,
    }
}
