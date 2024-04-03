{%- set my_file_name = ctx.prefix | arg_name -%}
{%- set name = ctx.prefix | file_name -%}
{{- template.set_file_name(my_file_name ~ ".md") -}}

# `{{ name }}`

## {{ name }} Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
{%- for attribute in ctx.attributes %}
| `{{ attribute.name }}` | {%- include "attribute_type.j2" | trim %} | {{ attribute.brief | trim }} | {%- include "examples.j2" | trim %} | {%- include "stability.j2" | trim %} |
{%- endfor %}
|---|---|---|---|---|

<!-- TODO notes -->