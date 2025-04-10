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

test_does_not_fail_on_deprecated_namespace_collision if {
    collision := {"groups": [
        {"id": "test1", "attributes": [{"name": "test.namespace.id"}]},
        {"id": "test2", "attributes": [{"name": "test.namespace", "deprecated": {"reason" : "obsoleted"}}]},

        {"id": "test3", "attributes": [{"name": "another_test.namespace.id", "deprecated": {"reason" : "renamed", "renamed_to": "another_test.namespace"}}]},
        {"id": "test4", "attributes": [{"name": "another_test.namespace"}]},
    ]}
    count(deny) == 0 with input as collision
}

