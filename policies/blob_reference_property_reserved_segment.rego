package after_resolution

import rego.v1

reserved_segment_name = "blob_ref"

deny contains violation if {
	group := input.groups[_]
	group.prefix != null
	contains_segment(group.prefix, reserved_segment_name)
	description := sprintf("Registry group '%s' with prefix '%s' contains illegal segment '%s'; reserved for Blob Reference Properties.", [group.id, group.prefix, reserved_segment_name])
	violation := group_level_refattr_violation(description, group.id)
}

deny contains violation if {
	some group in input.groups
	some attr in group.attributes
	attr.name != null
	contains_segment(attr.name, reserved_segment_name)
	description := sprintf("Attribute '%s' contains illegal segment '%s'; reserved for Blob Reference Properties.", [attr.name, reserved_segment_name])
	violation := attr_level_refattr_violation(description, group.id, attr.name)
}

contains_segment(name, target_segment) if {
	name_segments := split(name, ".")
    some name_segment in name_segments
    name_segment == target_segment
}

group_level_refattr_violation(description, group_id) = violation if {
	violation := {
		"id": description,
		"type": "semconv_attribute",
		"category": "reserved_name_for_blob_reference_properties",
		"attr": "",
		"group": group_id,
	}
}

attr_level_refattr_violation(description, group_id, attr_name) = violation if {
	violation := {
		"id": description,
		"type": "semconv_attribute",
		"category": "reserved_name_for_blob_reference_properties",
		"attr": attr_name,
		"group": group_id,
	}
}
