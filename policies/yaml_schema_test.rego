package yaml_schema_test

import data.yaml_schema
import future.keywords

test_fails_on_invalid_attribute_name if {
    every name in invalid_names {
        count(yaml_schema.deny) == 1 with input as {"groups": create_attribute_group(name)}
    }
}

test_fails_on_invalid_metric_name if {
    every name in invalid_names {
        count(yaml_schema.deny) == 1 with input as {"groups": create_metric(name)}
    }
}

test_fails_on_invalid_event_name if {
    every name in invalid_names {
        count(yaml_schema.deny) == 1 with input as {"groups": create_event(name)}
    }
}

test_passes_on_valid_names if {
    every name in valid_names {
        count(yaml_schema.deny) == 0 with input as {"groups": create_attribute_group(name)}
        count(yaml_schema.deny) == 0 with input as {"groups": create_metric(name)}
        count(yaml_schema.deny) == 0 with input as {"groups": create_event(name)}
    }
}

test_fails_if_prefix_is_present if {
    count(yaml_schema.deny) == 1 with input as {"groups": [{"id": "test", "prefix": "foo"}]}
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

invalid_names := [
    "1foo.bar",
    "_foo.bar",
    ".foo.bar",
    "foo.bar_",
    "foo.bar.",
    "foo..bar",
    "foo._bar",
    "foo__bar",
    "foo_.bar",
    "foo,bar",
    "fü.bär",
]

valid_names := [
    "foo.bar",
    "foo.1bar",
    "foo_1.bar",
    "foo.bar.baz",
    "foo.bar_baz",
]
