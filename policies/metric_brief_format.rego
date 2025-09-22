package before_resolution
import rego.v1

# This file enforces formatting policy for metric briefs.
# Non-empty metric briefs should end with a period (.).

metric_brief_violation(description, group_id) = violation if {
    violation := {
        "id": description,
        "type": "semconv_attribute",
        "category": "metric_brief_formatting",
        "group": group_id,
        "attr": "",
    }
}

# Check that metric briefs end with a period
deny contains metric_brief_violation(description, group.id) if {
    group := input.groups[_]
    group.type == "metric"
    brief := group.brief
    brief != null

    # Remove trailing whitespace and check if it ends with period
    trimmed_brief := trim(brief, " \n")

    # Allow empty briefs - only check non-empty ones
    trimmed_brief != ""
    not endswith(trimmed_brief, ".")
    
    description := sprintf("Non-empty metric brief '%s' must end with a period (.).", [trimmed_brief])
}