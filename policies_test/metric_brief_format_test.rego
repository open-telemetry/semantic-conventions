package after_resolution
import future.keywords.if

test_metric_brief_ends_with_period if {
    # Should pass: metric brief ends with period
    count(deny) == 0 with input as {"groups": [
        {"id": "metric.test", "type": "metric", "brief": "This is a valid metric brief.", "stability": "development"}
    ]}

    # Should pass: metric brief ends with period after trimming whitespace
    count(deny) == 0 with input as {"groups": [
        {"id": "metric.test2", "type": "metric", "brief": "This is a valid metric brief.   ", "stability": "development"}
    ]}
}

test_metric_brief_without_period if {
    # Should fail: metric brief doesn't end with period
    count(deny) > 0 with input as {"groups": [
        {"id": "metric.test", "type": "metric", "brief": "This metric brief is missing a period", "stability": "development"}
    ]}

    # Should fail: metric brief doesn't end with period (with whitespace)
    count(deny) > 0 with input as {"groups": [
        {"id": "metric.test2", "type": "metric", "brief": "This metric brief is missing a period   ", "stability": "development"}
    ]}
}

test_non_metric_groups_ignored if {
    # Should pass: non-metric groups are ignored
    count(deny) == 0 with input as {"groups": [
        {"id": "span.test", "type": "span", "brief": "This span brief doesn't end with period", "stability": "development"},
        {"id": "event.test", "type": "event", "brief": "This event brief doesn't end with period", "stability": "development"},
        {"id": "registry.attribute_test", "type": "attribute_group", "brief": "This attribute brief doesn't end with period"}
    ]}
}
