package after_resolution
import future.keywords

test_fails_on_complex_attribute if {
    attribute_types := ["any", "template[any]"]
    group_types = ["span", "entity", "resource", "metric"]
    every attribute_type in attribute_types {
        every group_type in group_types {
            count(deny) == 1 with input as {"groups": [{ "id": concat(".", [group_type, "attr"]),
                                                "type": group_type,
                                                "stability": "development",
                                                "attributes": [{
                                                    "name": "test.any",
                                                    "stability": "development",
                                                    "type": attribute_type
                                                }]}]}
        }
    }
}


test_pass_on_complex_attribute if {
    attribute_types := ["any", "template[any]"]
    group_types = ["attribute_group", "event"]
    every attribute_type in attribute_types {
        every group_type in group_types {
            count(deny) == 0 with input as {"groups": [{ "id": concat(".", [group_type, "attr"]),
                                                "type": group_type,
                                                "stability": "development",
                                                "attributes": [{
                                                    "name": "test.any",
                                                    "stability": "development",
                                                    "type": attribute_type
                                                }]}]}
        }
    }
}
