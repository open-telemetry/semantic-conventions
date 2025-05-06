package after_resolution
import future.keywords

test_fails_on_invalid_entity_association if {
    count(deny) >= 1 with input as {"groups": [
        create_metric("test", "my_wrong_entity"), 
        create_entity("my_entity")] }
}

test_succeed_on_valid_entity_association if {
    count(deny) == 0 with input as {"groups": [
        create_metric("test", "my_entity"), 
        create_entity("my_entity")] }
}

create_metric(name, association) = json if {
    id := sprintf("metric.%s", [name])
    json := {"id": id, "type": "metric", "metric_name": name, "stability": "rc", "entity_associations": [association]}
}

create_entity(name) = json if {
    id := sprintf("resource.%s", [name])
    json := {"id": id, "type": "entity", "name": name, "stability": "rc"}
}