package after_resolution
import future.keywords

test_fails_on_stable_entity_with_attributes_having_no_role if {
    count(deny) >= 1 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "stable",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "stable",
            "brief": "brief."
        }, {
            "name": "test.id",
            "stability": "stable",
            "role": "identifying",
            "brief": "brief."
        }]}]}
}

test_fails_on_stable_entity_with_attributes_having_no_id if {
    count(deny) >= 1 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "stable",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "stable",
            "role": "descriptive",
            "brief": "brief."
        }]}]}
}

test_fails_on_rc_entity_with_attributes_having_no_role if {
    count(deny) >= 1 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "release_candidate",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "release_candidate",
            "brief": "brief."
        }, {
            "name": "test.id",
            "stability": "release_candidate",
            "role": "identifying",
            "brief": "brief."
        }]}]}
}

test_fails_on_rc_entity_with_attributes_having_no_id if {
    count(deny) >= 1 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "release_candidate",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "release_candidate",
            "role": "descriptive",
            "brief": "brief."
        }]}]}
}

test_fails_on_beta_entity_with_attributes_having_no_role if {
    count(deny) >= 1 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "beta",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "beta",
            "brief": "brief."
        }, {
            "name": "test.id",
            "stability": "beta",
            "role": "identifying",
            "brief": "brief."
        }]}]}
}

test_fails_on_beta_entity_with_attributes_having_no_id if {
    count(deny) >= 1 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "beta",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "beta",
            "role": "descriptive",
            "brief": "brief."
        }]}]}
}

test_passes_on_stable_entity_with_id if {
    count(deny) == 0 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "stable",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "stable",
            "role": "descriptive",
            "brief": "brief."
        },{
            "name": "test.id",
            "stability": "stable",
            "role": "identifying",
            "brief": "brief."
        }]}]}
}

test_passes_on_rc_entity_with_id if {
    count(deny) == 0 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "release_candidate",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "release_candidate",
            "role": "descriptive",
            "brief": "brief."
        },{
            "name": "test.id",
            "stability": "release_candidate",
            "role": "identifying",
            "brief": "brief."
        }]}]}
}

test_passes_on_beta_entity_with_id if {
    count(deny) == 0 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "beta",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "beta",
            "role": "descriptive",
            "brief": "brief."
        },{
            "name": "test.id",
            "stability": "beta",
            "role": "identifying",
            "brief": "brief."
        }]}]}
}

test_passes_on_development_entity_having_no_role if {
    count(deny) == 0 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "development",
        "brief": "brief.",
        "attributes": [{
            "name": "test.experimental",
            "stability": "development",
            "brief": "brief."
        },{
            "name": "test.id",
            "stability": "beta",
            "brief": "brief."
        }]}]}
}
