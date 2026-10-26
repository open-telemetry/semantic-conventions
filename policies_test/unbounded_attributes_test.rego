package after_resolution

import future.keywords

test_fails_when_unbounded_attribute_required_on_span if {
    count(deny) == 1 with input as {"registry": {
        "attributes": [
            {
                "key": "test.body",
                "type": "string",
                "brief": "Body.",
                "annotations": {"value": {"unbounded_size": true}},
            },
        ],
        "spans": [
            {
                "type": "test.span",
                "brief": "Test span.",
                "attributes": [
                    {
                        "key": "test.body",
                        "requirement_level": "required",
                    },
                ],
            },
        ],
    }}
}

test_passes_when_unbounded_attribute_opt_in_or_recommended if {
    count(deny) == 0 with input as {"registry": {
        "attributes": [
            {
                "key": "test.body",
                "type": "string",
                "brief": "Body.",
                "annotations": {"value": {"unbounded_size": true}},
            },
        ],
        "spans": [
            {
                "type": "test.span",
                "brief": "Test span.",
                "attributes": [
                    {
                        "key": "test.body",
                        "requirement_level": "opt_in",
                    },
                ],
            },
        ],
    }}
}
