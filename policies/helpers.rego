package after_resolution

import rego.v1

to_const_name(name) = const_name if {
    const_name := replace(name, ".", "_")
}

# Appends a trailing dot so the result can be used with `startswith` to find
# names nested under this namespace, e.g. "foo.bar" -> "foo.bar.".
to_namespace_prefix(name) = prefix if {
    prefix := concat("", [name, "."])
}

is_property_set(obj, property) = true if {
    obj[property] != null
} else = false

property_or_null(obj, property) := obj[property] if {
    obj[property]
} else = null
