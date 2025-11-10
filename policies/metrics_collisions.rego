package after_resolution

import rego.v1

# Data structures to make checking things faster.
metric_names := { obj |
    group := input.groups[_];
    group.type = "metric"
    obj := {
    "name": group.metric_name,
    "namespace_prefix": extract_metric_namespace_prefix(group.metric_name),
    "deprecated": is_property_set(group, "deprecated")
    }
}

# check that metric names do not collide with namespaces
deny contains metrics_registry_collision(description, name) if {
    some i

    name := metric_names[i].name
    prefix := metric_names[i].namespace_prefix
    not metric_names[i].deprecated


    exceptions = {
        # TODO: https://github.com/open-telemetry/semantic-conventions/issues/3058
        # legacy hardware metrics that are known to cause collisions
        "hw.battery.charge", "hw.cpu.speed", "hw.fan.speed", "hw.temperature", "hw.voltage"
    }
    not exceptions[name]

    collisions := [other.name |
        other := metric_names[_]
        not other.deprecated

        other.name != name
        startswith(other.name, prefix)
    ]
    count(collisions) > 0
    description := sprintf("Metric with name '%s' is used as a namespace in the following metrics '%s'.", [name, collisions])
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

is_property_set(obj, property) = true if {
    obj[property] != null
} else = false
