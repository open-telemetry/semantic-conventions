package after_resolution
import rego.v1

# Maturity ranking of stability levels. Higher number == more mature/stable.
stability_rank := {
    "development": 1,
    "experimental": 1,
    "alpha": 2,
    "beta": 3,
    "release_candidate": 4,
    "stable": 5,
}

# checks that a group's stability is not higher than the stability of any of its
# attributes, unless that attribute is opt_in
deny contains group_stability_violation(description, group.id, name) if {
    group := input.groups[_]
    # ignore attribute_groups
    group.type != "attribute_group"

    exceptions = {
        # TODO: https://github.com/open-telemetry/semantic-conventions/issues/1514
        "metric.kestrel.connection.duration", "metric.kestrel.tls_handshake.duration",
        # TODO: https://github.com/open-telemetry/semantic-conventions/issues/1519
        "entity.service",
        # TODO: https://github.com/open-telemetry/semantic-conventions/issues/1616
        "metric.dotnet.process.cpu.time",
    }
    not exceptions[group.id]

    group_rank := stability_rank[group.stability]

    attr := group.attributes[_]
    not attr.requirement_level == "opt_in"

    attr_rank := stability_rank[attr.stability]

    # group claims a higher maturity than the attribute it references
    group_rank > attr_rank

    name := attr.name

    description := sprintf("Group '%s' has stability '%s' which is higher than the stability '%s' of attribute '%s'; lower-stability attributes are only allowed at 'opt_in' requirement level", [group.id, group.stability, attr.stability, name])
}

group_stability_violation(description, group, attr) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "group_stability_violation",
        "attr": attr,
        "group": group,
    }
}
