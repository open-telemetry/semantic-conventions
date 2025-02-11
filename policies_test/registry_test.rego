package before_resolution_test

import data.before_resolution

import future.keywords.if

test_registry_attribute_groups if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "registry.test", "type": "foo"}]}
	count(before_resolution.deny) == 0 with input as {"groups": [{"id": "registry.test", "type": "attribute_group"}]}
}

test_attribute_ids if {
	# This requires a prefix for use with opa, but weaver will fill in.
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "not_registry", "prefix": "", "attributes": [{"id": "foo.bar", "stability": "rc"}]}]}
	count(before_resolution.deny) == 0 with input as {"groups": [
		{"id": "registry.test", "prefix": "", "attributes": [{"id": "foo.bar", "stability": "rc"}]},
		{"id": "not_registry", "prefix": "", "attributes": [{"ref": "foo.bar", "stability": "rc"}]},
	]}
}

test_attribute_without_stability if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "registry.text", "attributes": [{"id": "foo.bar"}]}]}
	count(before_resolution.deny) == 0 with input as {"groups": [
		{"id": "registry.test", "attributes": [{"id": "foo.bar", "stability": "alpha"}]},
	]}
}

test_span_without_stability if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "span.group", "type": "span"}]}
	count(before_resolution.deny) == 0 with input as {"groups": [
		{"id": "span.group", "type": "span", "stability": "alpha"}]
    }
}

test_event_without_stability if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "event.foo", "type": "event", "name": "foo"}]}
	count(before_resolution.deny) == 0 with input as {"groups": [
		{"id": "event.foo", "name": "foo", "type": "event", "stability": "alpha"}]
    }
}

test_metric_without_stability if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "metric.foo", "type": "metric", "name": "foo"}]}
	count(before_resolution.deny) == 0 with input as {"groups": [
		{"id": "metric.foo", "name": "foo", "type": "metric", "stability": "development"}]
    }
}

test_resource_without_stability if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "resource.foo", "type": "resource", "name": "foo"}]}
	count(before_resolution.deny) == 0 with input as {"groups": [
		{"id": "resource.foo", "name": "foo", "type": "resource", "stability": "stable"}]
    }
}

test_attribute_refs if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "registry.foo", "attributes": [{"ref": "foo"}]}]}
	count(before_resolution.deny) == 0 with input as {"groups": [{"id": "not_registry", "attributes": [{"ref": "foo"}]}]}
}

test_attribute_requirement_levels if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "registry.foo", "attributes": [{"id": "foo", "requirement_level": "required", "stability": "rc"}]}]}
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "registry.foo", "attributes": [{"id": "foo", "requirement_level": {"recommended": "if available"}, "stability": "rc"}]}]}
	count(before_resolution.deny) == 0 with input as {"groups": [{"id": "not_registry", "attributes": [{"ref": "foo", "requirement_level": "required"}]}]}
}
