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

test_fails_on_invalid_attribute_member_id if {
    every name in invalid_names {
        count(deny) >= 1 with input as {"groups": [{"id": "yaml_schema.test", "attributes": [{"id": "foo.bar", "stability": "rc", "type": {
                        "members": [{
                            "id": name,
                            "value": "test",
                            "stability": "stable",
                        }]
                    }}]}]}
    }
}

test_fails_on_invalid_metric_name if {
    every name in invalid_names {
        count(deny) >= 1 with input as {"groups": create_metric(name)}
    }
}

test_fails_on_invalid_metric_id if {
    invalid_ids := [
        "foo.bar",
        "metric..foo.bar",
        "metric.123",
        "metric.foo.bar.deprecated",
    ]
    every id in invalid_ids {
        count(deny) >= 1 with input as {"groups": [{"id": id, "type": "metric", "metric_name": "foo.bar"}]}
    }
}

test_fails_on_invalid_event_name if {
    every name in invalid_names {
        count(deny) >= 1 with input as {"groups": create_event(name)}
    }
}

test_fails_on_invalid_event_id if {
    invalid_ids := [
        "foo.bar",
        "event..foo.bar",
        "event.123",
        "evnt.foo.bar.deprecated",
    ]
    every id in invalid_ids {
        count(deny) >= 1 with input as {"groups": [{"id": id, "type": "event", "name": "foo.bar"}]}
    }
}

test_fails_on_referenced_event_name_on_event if {
    event := [{ "id": "event.foo",
                "type": "event",
                "name": "foo",
                "stability": "rc",
                "attributes": [{"ref": "event.name"}]}]
    count(deny) == 1 with input as {"groups": event}
}

test_fails_on_invalid_resource_name if {
    every name in invalid_names {
        count(deny) >= 1 with input as {"groups": create_resource(name)}
    }
}

test_fails_on_missing_resource_name if {
    count(deny) >= 1 with input as {"groups": [{"id": "resource.", "type": "resource", "name": null}]}
}

test_passes_on_valid_names if {
    every name in valid_names {
        count(deny) == 0 with input as {"groups": create_attribute_group(name)}
        count(deny) == 0 with input as {"groups": create_metric(name)}
        count(deny) == 0 with input as {"groups": create_event(name)}
    }
}

test_passes_on_valid_attribute_member_id if {
    every name in valid_names {
        count(deny) == 0 with input as {"groups": [{"id": "yaml_schema.test", "attributes": [{"id": "foo.bar", "stability": "rc", "type": {
                        "members": [{
                            "id": name,
                            "value": "test",
                            "stability": "stable",
                        }]
                    }}]}]}
    }
}

test_fails_if_prefix_is_present if {
    count(deny) == 1 with input as {"groups": [{"id": "test", "prefix": "foo"}]}
}

test_fails_on_invalid_span_id if {
    invalid_ids := [
        "foo.bar",
        "span.foo.bar",
        "span.foo.bar.client.deprecated",
    ]
    every id in invalid_ids {
        count(deny) >= 1 with input as {"groups": [{"id": id, "type": "span", "span_kind": "client"}]}
    }
}

test_fails_on_invalid_resource_id if {
    invalid_ids := [
        "foo.bar",
        "resource..foo.bar",
        "resource.foo.bar.deprecated",
    ]
    every id in invalid_ids {
        count(deny) >= 1 with input as {"groups": [{"id": id, "type": "resource", "name": "foo.bar"}]}
    }
}

create_attribute_group(attr) = json if {
    json := [{"id": "yaml_schema.test", "attributes": [{"id": attr, "stability": "rc"}]}]
}

create_metric(name) = json if {
    id := sprintf("metric.%s", [name])
    json := [{"id": id, "type": "metric", "metric_name": name, "stability": "rc"}]
}

create_event(name) = json if {
    id := sprintf("event.%s", [name])
    json := [{"id": id, "type": "event", "name": name, "stability": "rc"}]
}

create_resource(name) = json if {
    id := sprintf("resource.%s", [name])
    json := [{"id": id, "type": "resource", "name": name, "stability": "rc"}]
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
    "Foo.bar",
    "foo.bAR",
]

valid_names := [
    "foo.bar",
    "foo.1bar",
    "foo_1.bar",
    "foo.bar.baz",
    "foo.bar_baz",
]
