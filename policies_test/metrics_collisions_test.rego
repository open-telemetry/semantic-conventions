package after_resolution
import future.keywords

test_fails_on_namespace_collision if {
    collision := {"groups": [
        {"id": "metric.foo.bar", "type": "metric", "metric_name": "foo.bar", "stability": "development", "brief": "brief."},
        {"id": "metric.foo.bar.baz", "type": "metric", "metric_name": "foo.bar.baz", "stability": "development", "brief": "brief."}
    ]}
    # foo.bar is used as namespace in foo.bar.baz, so 1 collision
    count(deny) == 1 with input as collision
}

test_does_not_fail_when_no_collision if {
    no_collision := {"groups": [
        {"id": "metric.foo.bar", "type": "metric", "metric_name": "foo.bar", "stability": "development", "brief": "brief."},
        {"id": "metric.foo.baz", "type": "metric", "metric_name": "foo.baz", "stability": "development", "brief": "brief."},
    ]}

    # No metric name is used as namespace prefix, so no collisions
    count(deny) == 0 with input as no_collision
}

test_does_not_fail_on_deprecated_namespace_metric if {
    deprecated := {"groups": [
        {"id": "metric.foo.bar", "type": "metric", "metric_name": "foo.bar", "stability": "development", "brief": "brief.", "deprecated": {"reason": "obsoleted"}},
        {"id": "metric.foo.bar.baz", "type": "metric", "metric_name": "foo.bar.baz", "stability": "development", "brief": "brief."}
    ]}
    # Deprecated metric foo.bar should not cause collision, so no collisions
    count(deny) == 0 with input as deprecated
}

test_does_not_fail_on_deprecated_colliding_metric if {
    deprecated := {"groups": [
        {"id": "metric.foo.bar", "type": "metric", "metric_name": "foo.bar", "stability": "development", "brief": "brief."},
        {"id": "metric.foo.bar.baz", "type": "metric", "metric_name": "foo.bar.baz", "stability": "development", "brief": "brief.", "deprecated": {"reason": "obsoleted"}}
    ]}
    # Deprecated metric foo.bar.baz should not count as collision, so no collisions
    count(deny) == 0 with input as deprecated
}

test_does_not_fail_on_both_deprecated if {
    deprecated := {"groups": [
        {"id": "metric.foo.bar", "type": "metric", "metric_name": "foo.bar", "stability": "development", "brief": "brief.", "deprecated": {"reason": "obsoleted"}},
        {"id": "metric.foo.bar.baz", "type": "metric", "metric_name": "foo.bar.baz", "stability": "development", "brief": "brief.", "deprecated": {"reason": "obsoleted"}}
    ]}
    # Both deprecated, so no collisions
    count(deny) == 0 with input as deprecated
}
