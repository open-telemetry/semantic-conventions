package after_resolution

import rego.v1

# Data structures to make checking things faster.
metric_names := { obj |
    group := input.groups[_];
    obj := { "name": group.metric_name, "namespace_prefix": extract_metric_namespace_prefix(group.metric_name)}
}

# check that matric names do not collide with namespaces
deny contains metrics_registry_collision(description, name) if {
    some i

    name := metric_names[i].name
    prefix := metric_names[i].namespace_prefix

    collisions := [other.name |
        other := metric_names[_]

        other.name != name
        startswith(other.name, prefix)
    ]
    count(collisions) > 0
    description := sprintf("Metric name '%s' is used as a namespace in the following metrics '%s'.", [name, collisions])
}


metrics_registry_collision(description, metric_name) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "namespace_collision",
        "attr": metric_name,
        "group": "",
    }
}

extract_metric_namespace_prefix(name) = namespace if {
    namespace := concat("", [name, "."])
}

