package after_resolution
import future.keywords

test_fails_on_experimental_not_opt_in_attribute_in_stable_group if {
    experimental_stabilities := ["experimental", "development", "alpha", "beta", "release_candidate"]
    every stability in experimental_stabilities {
        count(deny) == 1 with input as {"groups": [{ "id": "span.foo",
                                            "type": "span",
                                            "stability": "stable",
                                            "brief": "brief.",
                                            "attributes": [{
                                                "name": "test.experimental",
                                                "stability": stability,
                                                "requirement_level": "required",
                                                "brief": "brief.",
                                            }]}]}
    }
}

test_passes_on_experimental_opt_in_attribute_in_stable_group if {
    experimental_stabilities := ["experimental", "development", "alpha", "beta", "release_candidate"]
    every stability in experimental_stabilities {
        count(deny) == 0 with input as {"groups": [{ "id": "span.foo",
                                        "type": "span",
                                        "stability": "stable",
                                        "brief": "brief.",
                                        "attributes": [{
                                            "name": "test.experimental",
                                            "stability": stability,
                                            "requirement_level": "opt_in",
                                            "brief": "brief.",
                                        }]}]}
    }
}

# A group's stability must not be higher than its attributes', regardless of
# whether the group is stable.
test_fails_when_group_stability_higher_than_attribute if {
    count(deny) == 1 with input as {"groups": [{ "id": "span.foo",
                                        "type": "span",
                                        "stability": "release_candidate",
                                        "brief": "brief.",
                                        "attributes": [{
                                            "name": "test.experimental",
                                            "stability": "development",
                                            "requirement_level": "required",
                                            "brief": "brief.",
                                        }]}]}
}

test_fails_when_beta_group_has_development_attribute if {
    count(deny) == 1 with input as {"groups": [{ "id": "span.foo",
                                        "type": "span",
                                        "stability": "beta",
                                        "brief": "brief.",
                                        "attributes": [{
                                            "name": "test.experimental",
                                            "stability": "development",
                                            "requirement_level": "required",
                                            "brief": "brief.",
                                        }]}]}
}

# A lower-stability group referencing a higher-stability attribute is fine.
test_passes_when_group_stability_lower_than_attribute if {
    count(deny) == 0 with input as {"groups": [{ "id": "span.foo",
                                        "type": "span",
                                        "stability": "development",
                                        "brief": "brief.",
                                        "attributes": [{
                                            "name": "test.stable",
                                            "stability": "stable",
                                            "requirement_level": "required",
                                            "brief": "brief.",
                                        }]}]}
}

test_passes_when_group_and_attribute_have_equal_stability if {
    count(deny) == 0 with input as {"groups": [{ "id": "span.foo",
                                        "type": "span",
                                        "stability": "release_candidate",
                                        "brief": "brief.",
                                        "attributes": [{
                                            "name": "test.rc",
                                            "stability": "release_candidate",
                                            "requirement_level": "required",
                                            "brief": "brief.",
                                        }]}]}
}

# A lower-stability attribute is allowed at opt_in in a more stable group.
test_passes_on_lower_stability_opt_in_attribute_in_rc_group if {
    count(deny) == 0 with input as {"groups": [{ "id": "span.foo",
                                        "type": "span",
                                        "stability": "release_candidate",
                                        "brief": "brief.",
                                        "attributes": [{
                                            "name": "test.experimental",
                                            "stability": "development",
                                            "requirement_level": "opt_in",
                                            "brief": "brief.",
                                        }]}]}
}
