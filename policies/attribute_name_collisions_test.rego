package after_resolution
import future.keywords

test_fails_on_const_name_collision if {
    collision := {"groups": [
        {"id": "test1", "attributes": [{"name": "foo.bar.baz"}]},
        {"id": "test2", "attributes": [{"name": "foo.bar_baz"}]}
    ]}
    # each attribute counts as a collision, so there are 2 collisions
    count(deny) == 2 with input as collision
}

test_fails_on_namespace_collision if {
    collision := {"groups": [
        {"id": "test1", "attributes": [{"name": "foo.bar.baz"}]},
        {"id": "test2", "attributes": [{"name": "foo.bar"}]}
    ]}
    count(deny) == 1 with input as collision
}
