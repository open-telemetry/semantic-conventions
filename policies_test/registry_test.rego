package before_resolution_test

import data.before_resolution

import future.keywords.if

test_registry_attribute_groups if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "registry.test", "type": "foo"}]}
	count(before_resolution.deny) == 0 with input as {"groups": [{"id": "registry.test", "type": "attribute_group"}]}
}

test_attribute_ids if {
	# This requires a prefix for use with opa, but weaver will fill in.
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "not_registry", "prefix": "", "attributes": [{"id": "foo.bar"}]}]}
	count(before_resolution.deny) == 0 with input as {"groups": [
		{"id": "registry.test", "prefix": "", "attributes": [{"id": "foo.bar"}]},
		{"id": "not_registry", "prefix": "", "attributes": [{"ref": "foo.bar"}]},
	]}
}

test_attribute_refs if {
	count(before_resolution.deny) > 0 with input as {"groups": [{"id": "registry.foo", "attributes": [{"ref": "foo"}]}]}
	count(before_resolution.deny) == 0 with input as {"groups": [{"id": "not_registry", "attributes": [{"ref": "foo"}]}]}
}
