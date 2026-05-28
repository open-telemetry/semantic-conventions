package after_resolution
import future.keywords

gs_group_types := ["span", "metric", "event", "entity"]

gs_lower_stabilities := ["experimental", "development", "alpha", "beta", "release_candidate"]

# Builds an input with a single group of the given type referencing a single attribute.
gs_input(group_type, group_stability, attr_stability, requirement_level) := {"groups": [{
    "id": sprintf("%s.foo", [group_type]),
    "type": group_type,
    "stability": group_stability,
    "brief": "brief.",
    "attributes": [{
        "name": "test.attr",
        "stability": attr_stability,
        "requirement_level": requirement_level,
        "brief": "brief.",
    }],
}]}

# A group must not reference a lower-maturity attribute unless it's opt_in.
test_fails_on_lower_maturity_not_opt_in_attribute if {
    every group_type in gs_group_types {
        every stability in gs_lower_stabilities {
            count(deny) == 1 with input as gs_input(group_type, "stable", stability, "required")
        }
    }
}

test_passes_on_lower_maturity_opt_in_attribute if {
    every group_type in gs_group_types {
        every stability in gs_lower_stabilities {
            count(deny) == 0 with input as gs_input(group_type, "stable", stability, "opt_in")
        }
    }
}

# Group stability higher than the attribute's (non-stable group) still fails.
test_fails_when_group_stability_higher_than_attribute if {
    every group_type in gs_group_types {
        count(deny) == 1 with input as gs_input(group_type, "release_candidate", "development", "required")
    }
}

# A lower-stability group referencing a higher-stability attribute is fine.
test_passes_when_group_stability_lower_than_attribute if {
    every group_type in gs_group_types {
        count(deny) == 0 with input as gs_input(group_type, "development", "stable", "required")
    }
}

test_passes_when_group_and_attribute_have_equal_stability if {
    every group_type in gs_group_types {
        count(deny) == 0 with input as gs_input(group_type, "release_candidate", "release_candidate", "required")
    }
}

# A lower-stability attribute is allowed at opt_in in a more stable group.
test_passes_on_lower_stability_opt_in_attribute if {
    every group_type in gs_group_types {
        count(deny) == 0 with input as gs_input(group_type, "release_candidate", "development", "opt_in")
    }
}

# attribute_group is exempt from the check regardless of stability.
test_passes_on_attribute_group if {
    count(deny) == 0 with input as gs_input("attribute_group", "stable", "development", "required")
}
