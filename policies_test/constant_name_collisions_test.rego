package after_resolution
import future.keywords

test_fails_on_const_name_collision if {
    collision := {"groups": [
        {"id": "test1", "attributes": [{"name": "foo.bar.baz", "stability": "development", "brief": "brief."}]},
        {"id": "test2", "attributes": [{"name": "foo.bar_baz", "stability": "development", "brief": "brief."}]}
    ]}
    # each attribute counts as a collision, so there are 2 collisions
    count(deny) == 2 with input as collision
}

test_does_not_fail_on_excluded_name_collision if {
    collision := {"groups": [
        {"id": "test1", "attributes": [{"name": "test1.namespace.id", "stability": "development", "brief": "brief."}, {"name": "test1.namespace_id", "stability": "development", "brief": "brief.", "annotations": {"code_generation": {"exclude": true}}}]},

        {"id": "test2", "attributes": [{"name": "test2.namespace_id", "stability": "development", "brief": "brief."}, {"name": "test2.namespace.id", "stability": "development", "brief": "brief.", "annotations": {"code_generation": {"exclude": true}}}]},
    ]}
    count(deny) == 0 with input as collision
}

test_fails_on_metric_const_name_collision if {
    collision := {"groups": [
        {"id": "metric.foo.bar.baz", "type": "metric", "metric_name": "foo.bar.baz", "stability": "development", "brief": "brief.", "attributes": []},
        {"id": "metric.foo.bar_baz", "type": "metric", "metric_name": "foo.bar_baz", "stability": "development", "brief": "brief.", "attributes": []},
    ]}
    count(deny) == 2 with input as collision
}

test_fails_on_event_const_name_collision if {
    collision := {"groups": [
        {"id": "event.foo.bar.baz", "type": "event", "name": "foo.bar.baz", "stability": "development", "brief": "brief.", "attributes": []},
        {"id": "event.foo.bar_baz", "type": "event", "name": "foo.bar_baz", "stability": "development", "brief": "brief.", "attributes": []},
    ]}
    count(deny) == 2 with input as collision
}

test_fails_on_entity_const_name_collision if {
    collision := {"groups": [
        {"id": "entity.foo.bar.baz", "type": "entity", "name": "foo.bar.baz", "stability": "development", "brief": "brief.", "attributes": []},
        {"id": "entity.foo.bar_baz", "type": "entity", "name": "foo.bar_baz", "stability": "development", "brief": "brief.", "attributes": []},
    ]}
    count(deny) == 2 with input as collision
}

# Same constant name across different kinds is fine — each kind lives in its
# own generated-code namespace.
test_does_not_fail_on_cross_kind_const_name_collision if {
    collision := {"groups": [
        {"id": "test", "attributes": [{"name": "foo.bar", "stability": "development", "brief": "brief."}]},
        {"id": "metric.foo.bar", "type": "metric", "metric_name": "foo.bar", "stability": "development", "brief": "brief.", "attributes": []},
        {"id": "event.foo.bar", "type": "event", "name": "foo.bar", "stability": "development", "brief": "brief.", "attributes": []},
        {"id": "entity.foo.bar", "type": "entity", "name": "foo.bar", "stability": "development", "brief": "brief.", "attributes": []},
    ]}
    count(deny) == 0 with input as collision
}
