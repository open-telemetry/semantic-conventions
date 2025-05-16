package after_resolution
import future.keywords

test_fails_on_attribute_renamed_to_not_existing_attribute if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "some.other.name"}}
            ]
        },
        {
            "id": "metric.some.other.name", "type": "metric", "metric_name": "some.other.name", "stability": "rc"
        }
    ]}
}


test_fails_on_attribute_renamed_to_deprecated_attribute if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "some.other.name"}},
                {"name": "some.other.name", "stability": "development", "deprecated": {"reason": "obsoleted"}}

            ]
        },
    ]}
}


test_fails_on_metric_renamed_to_not_existing_metric if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "metric.test.me", "type": "metric", "metric_name": "test.me", "stability": "rc", "deprecated": {"reason": "renamed", "renamed_to": "some.other.name"}
        },
        {
            "id": "deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [ {"id": "some.other.name", "stability": "development"}]
        }
    ]}
}

test_fails_on_metric_renamed_to_deprecated_metric if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "metric.test.me", "type": "metric", "metric_name": "test.me", "stability": "rc", "deprecated": {"reason": "renamed", "renamed_to": "some.other.name"}
        },
        {
            "id": "metric.some.other.name", "type": "metric", "metric_name": "some.other.name", "stability": "rc", "deprecated": {"reason": "obsoleted"}
        }
    ]}
}
