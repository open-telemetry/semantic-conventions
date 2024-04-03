{% import 'stability.j2' as stability %}
{%- set ns = namespace(notes=[]) -%}
{%- set my_file_name = ctx.prefix | file_name | lower -%}
{%- set name = ctx.prefix | file_name | upper -%}
{{- template.set_file_name(my_file_name ~ ".md") -}}

{%- macro add_note(note) %}
{%- if note %}
{%- set ns.notes = [[note], ns.notes] | flatten -%}
[{{ ns.notes | length }}]
{%- endif %}
{%- endmacro %}
<!--- Hugo front matter used to generate the website version of this page:
--->

# {{ name }}

## {{ name }} Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
{%- for attribute in ctx.attributes %}
| `{{ attribute.name }}` | {%- include "attribute_type.j2" | trim %} | {{ attribute.brief | trim }} {{ add_note(attribute.note) }} | {%- include "examples.j2" | trim %} | {{ stability.badge(attribute.stability) | trim }} |
{%- endfor %}
|---|---|---|---|---|

{% for note in ns.notes %}
[{{loop.index}}]: {{note}}
{%- endfor -%}

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