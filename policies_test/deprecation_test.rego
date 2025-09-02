package after_resolution
import future.keywords

test_fails_on_attribute_renamed_to_not_existing_attribute if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "some.other.name"}}
            ]
        },
        {
            "id": "metric.some.other.name", "type": "metric", "metric_name": "some.other.name", "stability": "rc"
        }
    ]}
}

test_fails_on_attribute_renamed_to_attribute_of_different_type if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "test.me2"}, "type": "string"},
                {"name": "test.me2", "stability": "development", "type": "int"}                
            ]
        }
    ]}
}

test_fails_on_enum_attribute_renamed_to_attribute_of_different_type if {
    # string enum to int fails
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me.enum.str", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "test.me.int"}, "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.int", "stability": "development", "type": "int"}
            ]
        }
    ]}
    # int enum to string fails
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me.enum.int", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "test.me.str"}, "type": {
                        "members": [{
                            "id": "test",
                            "value": 42,
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.str", "stability": "development", "type": "string"},
            ]
        }
    ]}   
    # string enum to int enum fails 
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me.enum.int", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "test.me.enum.str"}, "type": {
                        "members": [{
                            "id": "test",
                            "value": 42,
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.enum.str", "stability": "development", "type": {
                        "members": [{
                            "id": "test",
                            "value": "value",
                            "stability": "development",
                        }]
                    }},
            ]
        }
    ]}    
    # string/int enum to string/int ok
    count(deny) == 0 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me.enum.str", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "test.me.str"}, "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.enum.int", "stability": "development", "deprecated": {"reason": "renamed", "renamed_to": "test.me.int"}, "type": {
                        "members": [{
                            "id": "test",
                            "value": 42,
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.str", "stability": "development", "type": "string"},
                {"name": "test.me.int", "stability": "development", "type": "int"}
            ]
        }
    ]}    
}


test_fails_on_attribute_renamed_to_enum_attribute_of_different_type if {
    # int to string enum fails
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me.enum.str", "stability": "development", "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.int", "stability": "development", "type": "int", "deprecated": {"reason": "renamed", "renamed_to": "test.me.enum.str"}}
            ]
        }
    ]}
    # string to int enum fails
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me.enum.int", "stability": "development", "type": {
                        "members": [{
                            "id": "test",
                            "value": 42,
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.str", "stability": "development", "type": "string", "deprecated": {"reason": "renamed", "renamed_to": "test.me.enum.int"}},
            ]
        }
    ]}   
    # string/int to string/int enum ok
    count(deny) == 0 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me.enum.str", "stability": "development", "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.enum.int", "stability": "development", "type": {
                        "members": [{
                            "id": "test",
                            "value": 42,
                            "stability": "development",
                        }]
                    }},
                {"name": "test.me.str", "stability": "development", "type": "string", "deprecated": {"reason": "renamed", "renamed_to": "test.me.enum.str"}},
                {"name": "test.me.int", "stability": "development", "type": "int", "deprecated": {"reason": "renamed", "renamed_to": "test.me.enum.int"}}
            ]
        }
    ]}    
}

test_fails_on_enum_attribute_member_renamed_to_not_existing_member if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me", "stability": "development", "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "development",
                        },{

                            "id": "test2",
                            "value": "test",
                            "stability": "development",
                            "deprecated": {
                                "reason": "renamed",
                                "renamed_to": "foo"
                            }
                        }]
                    }}
            ]
        }
    ]}
}

test_fails_on_enum_attribute_member_renamed_to_deprecated_member if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
            "attributes": [
                {"name": "test.me", "stability": "development", "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "development",
                            "deprecated": {
                                "reason": "obsolete",
                                "note": ""
                            }
                        },{

                            "id": "test2",
                            "value": "test",
                            "stability": "development",
                            "deprecated": {
                                "reason": "renamed",
                                "renamed_to": "test"
                            }
                        }]
                    }}
            ]
        }
    ]}
}

test_fails_on_attribute_renamed_to_deprecated_attribute if {
    count(deny) >= 1 with input as {"groups": [
        {
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
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
            "id": "registry.deprecation.test", "stability": "development", "type": "attribute_group",
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
