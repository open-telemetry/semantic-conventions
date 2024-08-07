package comparison_after_resolution

import rego.v1

# Semantic Convention Registry Compatibility Checker
#
# This file contains rules for checking backward compatibility
# between different versions of semantic convention registries.
# It builds upon the data structures and rules defined in the
# semconv package.

# Import the set of baseline attributes from the semconv package
baseline_attributes := data.semconv.registry_baseline_attributes

# Rule: Detect Removed Attributes
#
# This rule checks for attributes that existed in the baseline registry
# but are no longer present in the current registry. Removing attributes
# is considered a backward compatibility violation.
#
# In other words, we do not allow the removal of an attribute once added
# to the registry. It must exist SOMEWHERE in a group.
#
# The rule populates the 'deny' set with compatibility violations.
deny contains back_comp_violation(description, group_id, attr_name) if {
    # Check if an attribute from the baseline is missing in the current registry
    some attr_name in baseline_attributes
    not data.semconv.registry_attributes[attr_name]

    # Retrieve the group ID of the attribute from the baseline registry
    group_id := data.semconv.baseline_group_ids_by_attribute[attr_name]

    # Generate a description of the violation
    description := sprintf("Attribute '%s' no longer exists in the attribute registry", [attr_name])
}

# Helper Function: Create Backward Compatibility Violation Object
#
# This function generates a structured violation object for each
# detected backward compatibility issue.
back_comp_violation(description, group_id, attr_id) := violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "backward_compatibility",
        "group": group_id,
        "attr": attr_id,
    }
}