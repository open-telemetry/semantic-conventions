package after_resolution

import future.keywords

test_fails_on_attribute_without_brief if {
    every brief in [null, ""] {
        count(deny) == 1 with input as {"registry": {"attributes": [{"key": "foo.bar", "stability": "rc", "brief": brief}]}}
    }
    # missing brief entirely
    count(deny) == 1 with input as {"registry": {"attributes": [{"key": "foo.bar", "stability": "rc"}]}}
}

test_passes_on_attribute_with_brief if {
    count(deny) == 0 with input as {"registry": {"attributes": [{"key": "foo.bar", "stability": "rc", "brief": "brief."}]}}
}

test_fails_on_signal_without_brief if {
    count(deny) == 1 with input as {"registry": {"metrics": [{"name": "foo.bar", "stability": "rc"}]}}
    count(deny) == 1 with input as {"registry": {"spans": [{"type": "foo.bar", "stability": "rc"}]}}
    count(deny) == 1 with input as {"registry": {"events": [{"name": "foo.bar", "stability": "rc"}]}}
    count(deny) == 1 with input as {"registry": {"entities": [{"type": "foo.bar", "stability": "rc"}]}}
}

test_passes_on_signal_with_brief if {
    count(deny) == 0 with input as {"registry": {"metrics": [{"name": "foo.bar", "stability": "rc", "brief": "brief."}]}}
    count(deny) == 0 with input as {"registry": {"entities": [{"type": "foo.bar", "stability": "rc", "brief": "brief."}]}}
}
