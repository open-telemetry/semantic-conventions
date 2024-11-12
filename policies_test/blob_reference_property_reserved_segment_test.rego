package after_resolution

import rego.v1

test_group_with_blob_ref_exact if {
    count(deny) > 0 with input as {
        "groups": [
            {
              "id": "registry.test",
              "type": "attribute_group",
              "prefix": "blob_ref",
              "attributes": [{
                 "name": "somekey"
               },
              ]
            }
        ]
    }
}

test_group_with_blob_ref_prefix if {
    count(deny) > 0 with input as {
        "groups": [
            {
              "id": "registry.test",
              "type": "attribute_group",
              "prefix": "blob_ref.foo",
              "attributes": [{
                 "name": "somekey"
               },
              ]
            }
        ]
    }
}

test_group_with_blob_ref_internal_segment if {
count(deny) > 0 with input as {
        "groups": [
            {
              "id": "registry.test",
              "type": "attribute_group",
              "prefix": "foo.blob_ref.bar",
              "attributes": [{
                 "name": "somekey"
               },
              ]
            }
        ]
    }
}

test_attr_with_blob_ref_exact if {
    count(deny) > 0 with input as {
        "groups": [
            {
              "id": "registry.test",
              "type": "attribute_group",
              "prefix": "some.group.prefix",
              "attributes": [{
                 "name": "blob_ref"
               },
              ]
            }
        ]
    }
}

test_attr_with_blob_ref_prefix if {
    count(deny) > 0 with input as {
        "groups": [
            {
              "id": "registry.test",
              "type": "attribute_group",
              "prefix": "some.group.prefix",
              "attributes": [{
                 "name": "blob_ref.foo"
               },
              ]
            }
        ]
    }
}

test_attr_with_blob_ref_internal_segment if {
    count(deny) > 0 with input as {
        "groups": [
            {
              "id": "registry.test",
              "type": "attribute_group",
              "prefix": "some.group.prefix",
              "attributes": [{
                 "name": "foo.blob_ref.bar"
               },
              ]
            }
        ]
    }
}
