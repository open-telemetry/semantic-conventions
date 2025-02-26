package after_resolution
import future.keywords

test_fails_on_experimental_not_opt_in_attribute_in_stable_group if {
    experimental_stabilities := ["experimental", "development", "alpha", "beta", "release_candidate"]
    every stability in experimental_stabilities {
        count(deny) == 1 with input as {"groups": [{ "id": "span.foo",
                                            "type": "span",
                                            "stability": "stable",
                                            "attributes": [{
                                                "name": "test.experimental",
                                                "stability": stability,
                                                "requirement_level": "required"
                                            }]}]}
    }
}

test_passes_on_experimental_opt_in_attribute_in_stable_group if {
    experimental_stabilities := ["experimental", "development", "alpha", "beta", "release_candidate"]
    every stability in experimental_stabilities {
        count(deny) == 0 with input as {"groups": [{ "id": "span.foo",
                                        "type": "span",
                                        "stability": "stable",
                                        "attributes": [{
                                            "name": "test.experimental",
                                            "stability": stability,
                                            "requirement_level": "opt_in"
                                        }]}]}
    }
}
