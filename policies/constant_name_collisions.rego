package after_resolution

import rego.v1

# Data structures to make checking things faster.
# constant_names collects everything that produces a generated-code constant:
# attributes, metrics, events, and entities. The collision check below
# matches within the same type, since each type lives in its own namespace
# in generated code.
constant_names contains obj if {
    group := input.groups[_]
    attr := group.attributes[_]
    obj := to_constant_entry(attr.name, "attribute", group.id, attr.name, attr)
}

constant_names contains obj if {
    group := input.groups[_]
    group.type == "metric"
    obj := to_constant_entry(group.metric_name, "metric", group.id, "", group)
}

constant_names contains obj if {
    group := input.groups[_]
    group.type == "event"
    obj := to_constant_entry(group.name, "event", group.id, "", group)
}

constant_names contains obj if {
    group := input.groups[_]
    group.type == "entity"
    obj := to_constant_entry(group.name, "entity", group.id, "", group)
}

to_constant_entry(name, type, group_id, attr_name, source) = obj if {
    obj := {
        "name": name,
        "const_name": to_const_name(name),
        "type": type,
        "group_id": group_id,
        "attr_name": attr_name,
        "annotations": property_or_null(source, "annotations"),
    }
}

# check that constant names do not collide within the same type
deny contains constant_name_collision(description, group_id, attr_name) if {
    some i
    name := constant_names[i].name
    const_name := constant_names[i].const_name
    type := constant_names[i].type
    group_id := constant_names[i].group_id
    attr_name := constant_names[i].attr_name
    annotations := constant_names[i].annotations

    not annotations["code_generation"]["exclude"]

    collisions := [other.name |
        other := constant_names[_]
        other.type == type
        other.name != name
        other.const_name == const_name

        not other.annotations["code_generation"]["exclude"]
    ]
    count(collisions) > 0

    # TODO (https://github.com/open-telemetry/weaver/issues/279): provide other violation properties once weaver supports it.
    description := sprintf("%s '%s' has the same constant name '%s' as '%s'.", [type, name, const_name, collisions])
}

# attr_name is empty for metric/event/entity, since
# those collisions are reported on the group itself.
constant_name_collision(description, group_id, attr_name) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "naming_collision",
        "attr": attr_name,
        "group": group_id,
    }
}
