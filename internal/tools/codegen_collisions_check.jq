def to_const_name: .| split(".")|join("_");
def exclude(list):
  map(select( .name as $name | list | all(. != $name) ) );
def to_const_name: .| split(".")|join("_");
def get_namespaces: . | split(".") as $parts  | reduce range(1; ($parts |length)) as $i ([]; . + [$parts[0:$i] | join(".")]  );
def fail_on_const_name_collision: . as $original
    | exclude(["messaging.client_id_1"])
    | group_by(.const_name)
    | map(select(length>1))
    | map({error: ("Multiple attributes with the same constant name are defined: " + (. | map(.name) | join(", ")))});
def fail_on_attr_name_collision: . as $original
    | exclude(["messaging.operation1", "db.operation1"])
    | {names: map(.|.name), namespaces: map(.|.name|get_namespaces[] ) | unique}
    | .namespaces as $namespaces
    | .names | map(select( . as $name | $namespaces | index($name)))
    | map({error: ("Attribute and namespace name collision: " + .)});
.groups
    | map(select(.type == "attribute_group"))
    | map(select(.id | startswith("registry")))
    | map({attributes: .attributes | map(.const_name= (.name | to_const_name)) })
    | [.[].attributes[]] as $original
    | [($original | fail_on_const_name_collision)[][], ($original | fail_on_attr_name_collision)[][]]
    | if length > 0 then error("\nErrors:\n\t" + (. | join("\n\t"))) else "success" end
