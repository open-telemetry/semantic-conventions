package before_resolution

import future.keywords

test_fails_on_invalid_attribute_name if {
    every name in invalid_names {
        count(deny) >= 1 with input as {"groups": create_attribute_group(name)}
    }
}

test_fails_on_attribute_name_without_namespace if {
    count(deny) >= 1 with input as {"groups": create_attribute_group("foo")}
}

test_fails_on_invalid_metric_name if {
    every name in invalid_names {
        count(deny) >= 1 with input as {"groups": create_metric(name)}
    }
}

test_fails_on_invalid_event_name if {
    every name in invalid_names {
        count(deny) >= 1 with input as {"groups": create_event(name)}
    }
}

test_fails_on_invalid_resource_name if {
    every name in invalid_names {
        count(deny) >= 1 with input as {"groups": create_resource(name)}
    }
}

test_fails_on_missing_resource_name if {
    count(deny) >= 1 with input as {"groups": [{"id": "yaml_schema.test", "type": "resource"}]}
}

test_passes_on_valid_names if {
    every name in valid_names {
        count(deny) == 0 with input as {"groups": create_attribute_group(name)}
        count(deny) == 0 with input as {"groups": create_metric(name)}
        count(deny) == 0 with input as {"groups": create_event(name)}
    }
}

test_fails_if_prefix_is_present if {
    count(deny) == 1 with input as {"groups": [{"id": "test", "prefix": "foo"}]}
}

create_attribute_group(attr) = json {
    json := [{"id": "yaml_schema.test", "attributes": [{"id": attr}]}]
}

create_metric(name) = json {
    json := [{"id": "yaml_schema.test", "type": "metric", "metric_name": name}]
}

create_event(name) = json {
    json := [{"id": "yaml_schema.test", "type": "event", "name": name}]
}

create_resource(name) = json {
    json := [{"id": "yaml_schema.test", "type": "resource", "name": name}]
}

invalid_names := [
    "1foo.bar",
    "_foo.bar",
    ".foo.bar",
    "foo.bar_",
    "foo.bar.",
    "foo..bar",
    "foo._bar",
    "foo.bar__baz",
    "foo_.bar",
    "foo.bar,baz",
    "fü.bär",
]

valid_names := [
    "foo.bar",
    "foo.1bar",
    "foo_1.bar",
    "foo.bar.baz",
    "foo.bar_baz",
]
