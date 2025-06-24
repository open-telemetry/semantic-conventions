package after_resolution
import future.keywords

test_fails_on_stable_entity_with_attributes_having_no_role if {
    count(deny) >= 1 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "stable",
        "attributes": [{
            "name": "test.experimental",
            "stability": "stable",
        }, {
            "name": "test.id",
            "stability": "stable",
            "role": "identifying",
        }]}]}
}

test_fails_on_stable_entity_with_attributes_having_no_id if {
    count(deny) >= 1 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "stable",
        "attributes": [{
            "name": "test.experimental",
            "stability": "stable",
            "role": "descriptive",
        }]}]}
}

test_passes_on_stable_entity_with_id if {
    count(deny) == 0 with input as {"groups": [{
        "id": "entity.foo",
        "type": "entity",
        "name": "foo",
        "stability": "stable",
        "attributes": [{
            "name": "test.experimental",
            "stability": "stable",
            "role": "descriptive",
        },{
            "name": "test.id",
            "stability": "stable",
            "role": "identifying",
        }]}]}
}
