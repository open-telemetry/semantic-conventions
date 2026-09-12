package after_resolution

import rego.v1

# An attribute ending with `_ref` must have a counterpart attribute without `_ref`.
deny contains finding if {
    some attr in input.registry.attributes
    endswith(attr.key, "_ref")
    base_key := substring(attr.key, 0, count(attr.key) - 4)

    not attribute_exists(base_key)

    finding := {
        "id": "reference_attribute_counterpart_missing",
        "message": sprintf("Attribute '%s' ends with '_ref' but counterpart attribute '%s' does not exist.", [attr.key, base_key]),
        "level": "violation",
        "context": {
            "attribute_key": attr.key,
            "base_key": base_key,
        },
    }
}

# An attribute ending with `_ref` must have value type 'string'.
deny contains finding if {
    some attr in input.registry.attributes
    endswith(attr.key, "_ref")
    attr.type != "string"

    finding := {
        "id": "reference_attribute_type_invalid",
        "message": sprintf("Attribute '%s' ends with '_ref' and must have type 'string', but got '%v'.", [attr.key, attr.type]),
        "level": "violation",
        "context": {
            "attribute_key": attr.key,
            "type": attr.type,
        },
    }
}

attribute_exists(key) if {
    some a in input.registry.attributes
    a.key == key
}
