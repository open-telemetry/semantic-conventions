package comparison_after_resolution

import rego.v1

# Semantic Convention Registry Compatibility Checker
#
# This file contains rules for checking backward compatibility
# between different versions of semantic convention registries.
# It builds upon the data structures and rules defined in the
# semconv package.

# Import the previous release (baseline) and current sets of attributes, metrics.
baseline_attributes := [attr |
    some g in data.semconv.registry_baseline_groups
    some attr in g.attributes
]
registry_attributes := [attr |
    some g in data.semconv.registry_groups
    some attr in g.attributes
]
registry_attribute_names := {attr.name |
    some g in data.semconv.registry_groups
    some attr in g.attributes
}
baseline_metrics := [ g |
    some g in data.semconv.baseline_groups
    g.type == "metric"
]
registry_metrics := [ g |
    some g in data.semconv.groups
    g.type == "metric"
]
registry_metric_names := { g.metric_name | some g in registry_metrics }


# Rules we enforce:
# - Attributes
#   - [x] Attributes cannot be removed
#   - [x] Attributes cannot "degrade" stability (stable->experimental)
#   - [x] Stable attributes cannot change type
#   - Enum members
#     - [x] Stable members cannot change stability
#     - [x] Values cannot change
#     - [x] ids cannot be removed
# - Metrics
#   - [x] metrics cannot be removed
#   - [x] Stable metrics cannot become unstable
#   - [x] Stable Metric units cannot change
#   - [x] Stable Metric instruments cannot change
#   - [ ] Set of required/recommended attributes must remain the same


# Rule: Detect Removed Attributes
#
# This rule checks for attributes that existed in the baseline registry
# but are no longer present in the current registry. Removing attributes
# is considered a backward compatibility violation.
#
# In other words, we do not allow the removal of an attribute once added
# to the registry. It must exist SOMEWHERE in a group, but may be deprecated.
deny contains back_comp_violation(description, group_id, attr.name) if {
    # Check if an attribute from the baseline is missing in the current registry
    some attr in baseline_attributes
    not registry_attribute_names[attr.name]

    # Generate human readable error.
    group_id := data.semconv.baseline_group_ids_by_attribute[attr.name]
    description := sprintf("Attribute '%s' no longer exists in the attribute registry", [attr.name])
}



# Rule: Detect Stable Attributes moving to unstable
#
# This rule checks for attributes that were stable in the baseline registry
# but are no longer stable in the current registry. Once stable, attributes
# remain forever but may be deprecated.
deny contains back_comp_violation(description, group_id, attr.name) if {
     # Find stable baseline attributes in latest registry.
     some attr in baseline_attributes
     attr.stability == "stable"
     some nattr in registry_attributes
     attr.name == nattr.name

     # Enforce the policy
     attr.stability != nattr.stability

     # Generate human readable error.
     group_id := data.semconv.baseline_group_ids_by_attribute[attr.name]
     description := sprintf("Attribute '%s' was stable, but has new stability marker", [attr.name])
}

# Rule: Detect Stable Attributes changing type
#
# This rule checks for attributes that were stable in the baseline registry
# but are no longer stable in the current registry. Once stable, attributes
# remain forever but may be deprecated.
deny contains back_comp_violation(description, group_id, attr.name) if {
     # Find stable baseline attributes in latest registry.
     some attr in baseline_attributes
     attr.stability == "stable"
     some nattr in registry_attributes
     attr.name == nattr.name

     # Enforce the policy
     # TODO - deal with enum type changes, probably in enum sections
     not is_enum(attr)
     attr.type != nattr.type

     # Generate human readable error.
     group_id := data.semconv.baseline_group_ids_by_attribute[attr.name]
     attr_type_string := type_string(attr)
     nattr_type_string := type_string(nattr)
     description := sprintf("Attribute '%s' was '%s', but has new type '%s'", [attr.name, attr_type_string, nattr_type_string])
}

# Rule: Detect Stable enum Attributes changing type
#
# This rule checks for attributes that were stable in the baseline registry
# but are no longer stable in the current registry. Once stable, attributes
# remain forever but may be deprecated.
deny contains back_comp_violation(description, group_id, attr.name) if {
     # Find stable baseline attributes in latest registry.
     some attr in baseline_attributes
     attr.stability == "stable"
     some nattr in registry_attributes
     attr.name == nattr.name
     # Enforce the policy
     attr.type != nattr.type
     is_enum(attr)
     not is_enum(nattr)

     # Generate human readable error.
     group_id := data.semconv.baseline_group_ids_by_attribute[attr.name]
     nattr_type_string := type_string(nattr)
     description := sprintf("Attribute '%s' was enum, but has new type '%s'", [attr.name, nattr_type_string])
}

# Rule: Detect Stable Enum members changing stability level
#
# This rule checks for enum values that were stable in the baseline registry
# but are no longer stable in the current registry.
deny contains back_comp_violation(description, group_id, attr.name) if {
     # Find data we need to enforce: Enums in baseline/current.
     some attr in baseline_attributes
     attr.stability == "stable"
     some nattr in registry_attributes
     attr.name == nattr.name
     is_enum(attr)
     some member in attr.type.members
     some nmember in nattr.type.members
     member.id == nmember.id

     # Enforce the policy    
     member.stability == "stable"
     nmember.stability != "stable"

     # Generate human readable error.
     group_id := data.semconv.baseline_group_ids_by_attribute[attr.name]
     description := sprintf("Enum '%s' had stable member '%s', but is no longer stable", [attr.name, member.id])
}

# Rule: Enum member values cannot change
#
# This rule checks for enum values that have the same id, but values
# are different.
deny contains back_comp_violation(description, group_id, attr.name) if {
     # Find data we need to enforce: Enums in baseline/current.
     some attr in baseline_attributes
     attr.stability == "stable"
     some nattr in registry_attributes
     attr.name == nattr.name
     is_enum(attr)
     some member in attr.type.members
     some nmember in nattr.type.members
     member.id == nmember.id

     # Enforce the policy    
     member.value != nmember.value

     # Generate human readable error.
     group_id := data.semconv.baseline_group_ids_by_attribute[attr.name]
     description := sprintf("Enum '%s' had stable value '%s', but is now '%s'", [attr.name, member.value, nmember.value])
}

# Rule: Detect Stable Enum members missing
#
# This rule checks for enum values that were stable in the baseline registry
# but are no longer have the same values in the current registry. Once stable,
# enum values remain forever but may be deprecated.
deny contains back_comp_violation(description, group_id, attr.name) if {
     # Find data we need to enforce: Enums in baseline/current.
     some attr in baseline_attributes
     attr.stability == "stable"
     some nattr in registry_attributes
     attr.name == nattr.name
     is_enum(attr)
     current_member_ids := {member.id | some member in nattr.type.members}
     # Enforce the policy
     some member in attr.type.members
     not current_member_ids[member.id]

     # Generate human readable error.
     group_id := data.semconv.baseline_group_ids_by_attribute[attr.name]
     description := sprintf("Enum '%s' had member '%s', but is no longer defined", [attr.name, member.id])
}

# Rule: Detect Removed Metrics
#
# This rule checks for stable metrics that existed in the baseline registry
# but are no longer present in the current registry. Removing attributes
# is considered a backward compatibility violation.
#
# In other words, we do not allow the removal of an attribute once added
# to the registry. It must exist SOMEWHERE in a group, but may be deprecated.
deny contains back_comp_violation(description, group_id, "") if {
    # Find data we need to enforce
    some metric in baseline_metrics
    metric.stability == "stable"
    # Enforce the policy
    not registry_metric_names[metric.metric_name]

    # Generate human readable error.
    group_id := metric.id
    description := sprintf("Metric '%s' no longer exists in semantic conventions", [metric.metric_name])
}

# Rule: Stable metrics cannot become unstable
#
# This rule checks that stable metrics cannot have their stability level changed.
deny contains back_comp_violation(description, group_id, "") if {
    # Find data we need to enforce
    some metric in baseline_metrics
    metric.stability == "stable"
    some nmetric in registry_metrics
    metric.metric_name = nmetric.metric_name
    # Enforce the policy
    nmetric.stability != "stable"

    # Generate human readable error.
    group_id := metric.id
    description := sprintf("Metric '%s' cannot change from stable", [metric.metric_name])
}

# Rule: Stable metrics units cannot change
#
# This rule checks that stable metrics cannot change the unit type.
deny contains back_comp_violation(description, group_id, "") if {
    # Find data we need to enforce
    some metric in baseline_metrics
    metric.stability == "stable"
    some nmetric in registry_metrics
    metric.metric_name = nmetric.metric_name
    # Enforce the policy
    nmetric.unit != metric.unit

    # Generate human readable error.
    group_id := metric.id
    description := sprintf("Metric '%s' cannot change unit (was '%s', now: '%s')", [metric.metric_name, metric.unit, nmetric.unit])
}

# Rule: Stable Metric instruments cannot change
#
# This rule checks that stable metrics cannot change the instrument type.
deny contains back_comp_violation(description, group_id, "") if {
    # Find data we need to enforce
    some metric in baseline_metrics
    metric.stability == "stable"
    some nmetric in registry_metrics
    metric.metric_name = nmetric.metric_name
    # Enforce the policy
    nmetric.instrument != metric.instrument

    # Generate human readable error.
    group_id := metric.id
    description := sprintf("Metric '%s' cannot change instrument (was '%s', now: '%s')", [metric.metric_name, metric.instrument, nmetric.instrument])
}

# Rule: Stable Metric required/recommended attributes cannot change - missing
#
# This rule checks that stable metrics have stable sets of attributes.
deny contains back_comp_violation(description, group_id, "") if {
    # Find data we need to enforce
    some metric in baseline_metrics
    metric.stability == "stable"
    some nmetric in registry_metrics
    metric.metric_name = nmetric.metric_name
    
    baseline_attributes := { attr.name |
        some attr in metric.attributes
        not is_opt_in(attr)
    }
    new_attributes := { attr.name |
        some attr in nmetric.attributes
        not is_opt_in(attr)
    }
    missing_attributes := baseline_attributes - new_attributes
    # Enforce the policy
    count(missing_attributes) > 0

    # Generate human readable error.
    group_id := metric.id
    description := sprintf("Metric '%s' cannot change required/recommended attributes (missing '%s')", [metric.metric_name, missing_attributes])
}

# Rule: Stable Metric required/recommended attributes cannot change - added
#
# This rule checks that stable metrics have stable sets of attributes.
deny contains back_comp_violation(description, group_id, "") if {
    # Find data we need to enforce
    some metric in baseline_metrics
    metric.stability == "stable"
    some nmetric in registry_metrics
    metric.metric_name = nmetric.metric_name
    
    baseline_attributes := { attr.name |
        some attr in metric.attributes
        not is_opt_in(attr)
    }
    new_attributes := { attr.name |
        some attr in nmetric.attributes
        not is_opt_in(attr)
    }
    added_attributes := new_attributes - baseline_attributes
    # Enforce the policy
    count(added_attributes) > 0

    # Generate human readable error.
    group_id := metric.id
    description := sprintf("Metric '%s' cannot change required/recommended attributes (added '%s')", [metric.metric_name, added_attributes])
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

# Helpers for enum values and type strings
is_enum(attr) := true if count(attr.type.members) > 0
type_string(attr) := attr.type if not is_enum(attr)
type_string(attr) := "enum" if is_enum(attr)
is_opt_in(attr) := true if attr.requirement_level == "opt_in"