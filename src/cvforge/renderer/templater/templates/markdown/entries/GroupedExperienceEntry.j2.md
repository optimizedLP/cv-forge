{% if entry._rendered_positions|length == 1 %}
{# Single position: render like a regular ExperienceEntry with company+position on same line #}
{% set pos = entry._rendered_positions[0] %}
## {{ entry.company_column.splitlines()[0] }}, {{ pos.main_column.splitlines()[0] }}

{% for line in pos.date_and_location_column.splitlines() %}
{{ line }}

{% endfor %}
{% for line in pos.main_column.splitlines()[1:] %}
{%- if line != "!!!" -%}{{ line|replace("    ", "") }}
{% endif -%}
{% endfor %}
{% else %}
{# Multiple positions: show company header + sub-entries #}
## {{ entry.company_column.splitlines()[0] }}

{% for pos in entry._rendered_positions %}
### {{ pos.main_column.splitlines()[0] }}

{% for line in pos.date_and_location_column.splitlines() %}
{{ line }}

{% endfor %}
{% for line in pos.main_column.splitlines()[1:] %}
{%- if line != "!!!" -%}{{ line|replace("    ", "") }}
{% endif -%}
{% endfor %}

{% endfor %}
{% endif %}
