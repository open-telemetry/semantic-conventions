{% import 'stability.j2' as stability %}
{% import 'notes.j2' as notes %}
{%- set my_file_name = ctx.id | split_id | list | reject("eq", "registry") | join("/") | file_name | lower -%}
{%- set name = ctx.id | split_id | list | reject("eq", "registry") | join(" ") | upper -%}
{{- template.set_file_name(my_file_name ~ ".md") -}}

<!--- Hugo front matter used to generate the website version of this page:
--->

# {{ name }}

## {{ name }} Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
{%- for attribute in ctx.attributes %}
| `{{ attribute.name }}` | {%- include "attribute_type.j2" | trim %} | {{ attribute.brief | trim }} {{ notes.add(attribute.note) }} | {%- include "examples.j2" | trim %} | {{ stability.badge(attribute.stability) | trim }} |
{%- endfor %}
|---|---|---|---|---|

{{ notes.render() }}

{%- for enum in ctx.attributes %}
{%- if enum.type is mapping %}{# We should use a filter for enums vs. this if. #}

`{{enum.name}}` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
{%- for espec in enum.type.members %}
| `{{espec.value}}` | {{espec.brief}} | {{ stability.badge(espec.stability) }} |
{%- endfor %}
{%- endif %}
{%- endfor %}