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

# Check stable attribute enum member values changing
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
}

## TODO - Metrics