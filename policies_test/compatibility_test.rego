package comparison_after_resolution

import future.keywords.if

# Check that attributes cannot be removed.
test_removed_attributes if {
	count(deny) > 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing"
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
    count(deny) == 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing"
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing"
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
}

# Check that attributes cannot change stability
test_attribute_stability_change if {
	count(deny) > 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "experimental",
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
    count(deny) == 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
}

# Check stable attribute changing type
test_attribute_type_change if {
	count(deny) > 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": "int",
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": "string",
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
    count(deny) == 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": "string",
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": "string",
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
}
# Check stable attribute enum type
test_attribute_enum_type_change if {
	count(deny) > 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": "string",
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
    count(deny) == 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
}

# Check stable attribute enum members changing to nonstable
test_attribute_enum_member_stability_change if {
	count(deny) > 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "experimental",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
    count(deny) == 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
}

# Check stable attribute enum member values changing
test_attribute_enum_member_value_change if {
	count(deny) > 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "changed",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
    count(deny) == 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
}

# Check enum member missing for attributes of any stability level
test_attribute_enum_member_missing if {
	count(deny) > 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }, {
                            "id": "missing",
                            "value": "missing",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "changed",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
    count(deny) == 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }, {
                            "id": "missing",
                            "value": "missing",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "stable",
                        }, {
                            "id": "missing",
                            "value": "missing",
                            "stability": "stable",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
	count(deny) > 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "experimental",
                        }, {
                            "id": "missing",
                            "value": "missing",
                            "stability": "experimental",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "experimental",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
    count(deny) == 0 with data.semconv as {
            "registry_baseline_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "experimental",
                        }, {
                            "id": "missing",
                            "value": "missing",
                            "stability": "experimental",
                        }]
                    },
                }]
            }],
            "registry_groups": [{
                "id": "registry.test",
                "type": "attribute_group",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "type": {
                        "members": [{
                            "id": "test",
                            "value": "test",
                            "stability": "experimental",
                        }, {
                            "id": "missing",
                            "value": "missing",
                            "stability": "experimental",
                        }]
                    },
                }]
            }],
            "baseline_group_ids_by_attribute": {
                "test.missing": "registry.test"
            }
    }
}

# Check that metrics cannot be removed.
test_removed_metrics if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
            }],
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
            }]
    }
}

# Check that Stable metrics cannot become unstable
test_metric_stability_change if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "experimental",
            }]
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
            }]
    }
}

# Check that Stable metrics cannot change unit
test_metric_unit_change if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "ms",
            }]
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
            }]
    }
}

# Check that Stable metrics cannot change unit
test_metric_instrument_change if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "histogram",
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "gauge",
            }]
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "histogram",
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "histogram",
            }]
    }
}

# Check that Stable metrics cannot change required/recommended attributes
test_metric_attribute_missing if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "histogram",
                "attributes": [{
                    "name": "test.missing",
                    "requirement_level": "required"
                }],
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "gauge",
            }]
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "histogram",
                "attributes": [{
                    "name": "test.missing",
                    "requirement_level": "required"
                },{
                    "name": "test.ignored",
                    "requirement_level": "opt_in"
                }],
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "histogram",
                "attributes": [{
                    "name": "test.missing",
                    "requirement_level": "required"
                }],
            }]
    }
}

# Check that Stable metrics cannot change required/recommended attributes
test_metric_attribute_added if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "histogram",
                "attributes": [{
                    "name": "test.missing",
                    "requirement_level": "required"
                }],
            }],
            "groups": [{
                "id": "metric.test",
                "type": "metric",
                "metric_name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "gauge",
                "attributes": [{
                    "name": "test.missing",
                    "requirement_level": "required"
                }, {
                    "name": "test.added",
                    "requirement_level": "required"
                }],
            }]
    }
}

# Check that resources cannot be removed.
test_removed_resources if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
            }],
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
            }],
            "groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
            }]
    }
}

# Check that events cannot be removed.
test_removed_events if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "event.test.missing",
                "type": "event",
                "name": "test.missing"
            }],
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "event.test.deprecated",
                "type": "event",
                "name": "test.deprecated",
            }],
            "groups": [{
                "id": "event.test.deprecated",
                "type": "event",
                "name": "test.deprecated",
                "deprecated": "use `test` instead",
            }]
    }
}

# Check that Stable resources cannot become unstable
test_resource_stability_change if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
            }],
            "groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "experimental",
            }]
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
            }],
            "groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
            }]
    }
}


# Check that Stable attributes on stable resources cannot be removed
test_resource_attribute_missing if {
	count(deny) > 0 with data.semconv as {
            "baseline_groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "requirement_level": "required"
                }],
            }],
            "groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
            }]
    }
    count(deny) == 0 with data.semconv as {
            "baseline_groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "requirement_level": "required"
                },{
                    "name": "test.ignored",
                    "requirement_level": "opt_in"
                }],
            }],
            "groups": [{
                "id": "resource.test",
                "type": "resource",
                "name": "test.missing",
                "stability": "stable",
                "unit": "s",
                "instrument": "histogram",
                "attributes": [{
                    "name": "test.missing",
                    "stability": "stable",
                    "requirement_level": "required"
                }],
            }]
    }
}
