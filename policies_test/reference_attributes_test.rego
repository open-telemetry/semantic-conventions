package after_resolution

import future.keywords

test_fails_when_reference_attribute_counterpart_missing if {
    count(deny) == 1 with input as {"registry": {"attributes": [
        {"key": "test.payload_ref", "type": "string", "brief": "Ref."},
    ]}}
}

test_fails_when_reference_attribute_type_not_string if {
    count(deny) == 1 with input as {"registry": {"attributes": [
        {"key": "test.payload", "type": "any", "brief": "Base payload."},
        {"key": "test.payload_ref", "type": "int", "brief": "Ref."},
    ]}}
}

test_passes_when_reference_attribute_valid if {
    count(deny) == 0 with input as {"registry": {"attributes": [
        {"key": "test.payload", "type": "any", "brief": "Base payload."},
        {"key": "test.payload_ref", "type": "string", "brief": "Ref."},
    ]}}
}
