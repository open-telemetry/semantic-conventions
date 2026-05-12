package after_resolution
import future.keywords

test_fails_on_namespace_collision if {
    collision := {"groups": [
        {"id": "test1", "attributes": [{"name": "foo.bar.baz", "stability": "development", "brief": "brief."}]},
        {"id": "test2", "attributes": [{"name": "foo.bar", "stability": "development", "brief": "brief."}]}
    ]}
    count(deny) == 1 with input as collision
}

test_does_not_fail_on_deprecated_namespace_collision if {
    collision := {"groups": [
        {"id": "test1", "attributes": [{"name": "test.namespace.id", "stability": "development", "brief": "brief."}]},
        {"id": "test2", "attributes": [{"name": "test.namespace", "stability": "development", "brief": "brief.", "deprecated": {"reason" : "obsoleted"}}]},

        {"id": "test3", "attributes": [{"name": "another_test.namespace.id", "stability": "development", "brief": "brief.", "deprecated": {"reason" : "renamed", "renamed_to": "another_test.namespace"}}]},
        {"id": "test4", "attributes": [{"name": "another_test.namespace", "stability": "development", "brief": "brief."}]},
    ]}
    count(deny) == 0 with input as collision
}
