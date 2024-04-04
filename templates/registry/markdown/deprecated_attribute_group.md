{% import 'stability.j2' as stability %}
{% import 'notes.j2' as notes %}
{%- set my_file_name = "deprecated_" ~ ctx.prefix -%}
{%- set name = ctx.prefix | upper -%}
{{- template.set_file_name(my_file_name ~ ".md") -}}

# Deprecated {{ name }}

## Deprecated {{ name }} Attributes

| Attribute  | Type | Description  | Examples  | Stability |
{%- for attribute in ctx.attributes %}
| `{{ attribute.name }}` | {%- include "attribute_type.j2" | trim %} | {{ attribute.brief | trim }} {{ notes.add(attribute.note) }} | {%- include "examples.j2" | trim %} | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br/>{{ attribute.deprecated | trim }} |
{%- endfor %}

{{ notes.render() }}