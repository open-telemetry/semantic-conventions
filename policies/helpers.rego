package after_resolution

import rego.v1

to_const_name(name) = const_name if {
    const_name := replace(name, ".", "_")
}

is_property_set(obj, property) = true if {
    obj[property] != null
} else = false

property_or_null(obj, property) := obj[property] if {
    obj[property]
} else = null
